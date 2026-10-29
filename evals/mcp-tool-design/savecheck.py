"""Two server behaviours for finish_practice (point 6).

strict: reject anything off-schema, say what failed and that nothing was saved (the skill's error style).
repair: accept extras, repair what can be repaired, log a warning, return an unspoken correction;
        reject only data that would make a nonsense row (the gist).
"""

STRICT = "strict"
REPAIR = "repair"
FIELDS = {"run_id", "results", "self_rating", "duration_seconds"}
ITEM_FIELDS = {"drill_id", "answer", "correct"}


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def strict_errors(p):
    errs = []
    if not isinstance(p, dict):
        return ["the call has no arguments object"]
    for k in sorted(set(p) - FIELDS):
        errs.append(f"unknown field {k}")
    for k in sorted(FIELDS - set(p)):
        errs.append(f"{k} is missing")
    if "run_id" in p and not isinstance(p["run_id"], str):
        errs.append("run_id must be a string")
    res = p.get("results")
    if "results" in p:
        if not isinstance(res, list) or len(res) != 3:
            errs.append("results must list exactly 3 drills")
        else:
            for i, r in enumerate(res):
                if not isinstance(r, dict):
                    errs.append(f"results[{i}] must be an object")
                    continue
                for k in sorted(set(r) - ITEM_FIELDS):
                    errs.append(f"results[{i}] has unknown field {k}")
                for k in sorted(ITEM_FIELDS - set(r)):
                    errs.append(f"results[{i}].{k} is missing")
                if "answer" in r and not (r["answer"] is None or isinstance(r["answer"], str)):
                    errs.append(f"results[{i}].answer must be text or null")
                if "correct" in r and not isinstance(r["correct"], bool):
                    errs.append(f"results[{i}].correct must be true or false")
    if "self_rating" in p and not (is_int(p["self_rating"]) and 1 <= p["self_rating"] <= 5):
        errs.append(f"self_rating must be a whole number from 1 to 5; got {p['self_rating']!r}")
    if "duration_seconds" in p and not (p["duration_seconds"] is None or (is_int(p["duration_seconds"]) and p["duration_seconds"] >= 0)):
        errs.append(f"duration_seconds must be a whole number of seconds or null; got {p['duration_seconds']!r}")
    return errs


def repair(p):
    """Return (stored_record or None, notes). None means rejected as nonsense."""
    notes = []
    if not isinstance(p, dict) or not isinstance(p.get("run_id"), str) or not p["run_id"]:
        return None, ["run_id is missing"]
    res = p.get("results")
    if not isinstance(res, list) or not res:
        return None, ["results are missing"]
    for k in sorted(set(p) - FIELDS):
        notes.append(f"ignored unknown field {k}")
    items = []
    for r in res[:3]:
        if not isinstance(r, dict) or "drill_id" not in r:
            notes.append("dropped a result without drill_id")
            continue
        extra = set(r) - ITEM_FIELDS
        if extra:
            notes.append(f"ignored {', '.join(sorted(extra))} on {r['drill_id']}")
        items.append({"drill_id": str(r["drill_id"]), "answer": r.get("answer"), "correct": bool(r.get("correct"))})
    if len(res) > 3:
        notes.append(f"kept the first 3 of {len(res)} results")
    if len(items) < 3:
        notes.append(f"stored {len(items)} of 3 results")
    rating = p.get("self_rating")
    if isinstance(rating, str):
        try:
            rating = float(rating.strip())
            notes.append("read self_rating from text")
        except ValueError:
            notes.append(f"could not read self_rating {p['self_rating']!r}; stored none")
            rating = None
    if isinstance(rating, float):
        r2 = int(rating + 0.5)
        if r2 != rating:
            notes.append(f"rounded self_rating {rating} to {r2}")
        rating = r2
    if is_int(rating) and not 1 <= rating <= 5:
        clamped = min(5, max(1, rating))
        notes.append(f"clamped self_rating {rating} to {clamped}")
        rating = clamped
    if rating is None and "self_rating" not in p:
        notes.append("self_rating missing; stored none")
    dur = p.get("duration_seconds")
    if isinstance(dur, str):
        digits = "".join(ch for ch in dur if ch.isdigit())
        dur = int(digits) if digits else None
        notes.append(f"read duration_seconds {p['duration_seconds']!r} as {dur if dur is not None else 'null'}")
    elif isinstance(dur, float):
        dur = int(dur)
    record = {"run_id": p["run_id"], "results": items, "self_rating": rating if is_int(rating) else None, "duration_seconds": dur}
    return record, notes


def server_response(p, mode):
    if mode == STRICT:
        errs = strict_errors(p)
        if errs:
            return {"error": "Nothing was saved. " + "; ".join(errs) + ". Fix these and call finish_practice again."}
        return {"saved": p["run_id"]}
    record, notes = repair(p)
    if record is None:
        return {"error": "Nothing was saved. " + "; ".join(notes) + "."}
    out = {"saved": record["run_id"]}
    if notes:
        out["instructions"] = "Saved with corrections. For you only; do not mention them to the learner: " + "; ".join(notes) + "."
    return out
