"""Grade every raw run against the expected answers.

Run: python3 grade.py results/<date>
Reads manifest.json and raw/*.json, writes graded.json and summary.md.
"""

import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from savecheck import repair, strict_errors

HERE = Path(__file__).resolve().parent
HELPDESK = {c["id"]: c for c in json.loads((HERE / "cases" / "helpdesk.json").read_text())}
PRACTICE = json.loads((HERE / "cases" / "practice.json").read_text())
D = {d["id"]: d for d in PRACTICE["D"]}
E = {e["id"]: e for e in PRACTICE["E"]}
SIZES = json.loads((HERE / "fixtures" / "sizes.json").read_text())

SPLIT_TOOL = {"search": "search_tickets", "get": "get_ticket", "reply": "reply_to_ticket", "note": "add_internal_note",
              "forward": "forward_ticket", "assign": "assign_tickets", "escalate": "escalate_tickets",
              "status": "set_ticket_status", "merge": "merge_tickets", "delete": "delete_tickets",
              "followup": "schedule_followup", "log_time": "log_time", "ask_user": None, "none": None}
STAFF = ["Kim Lee", "Kim Park", "Jon Reyes", "Priya Shah", "Sam Ortiz"]
FIRST_NAME_ONLY = "assignee is a unique first name"
MERGED_ACTIONS ={"reply", "note", "forward", "assign", "escalate", "status", "merge", "delete", "followup", "log_time"}


def intent_of(move, merged):
    tool = move.get("tool")
    if tool is None:
        return "ask_user"
    if merged and tool == "manage_ticket":
        return (move.get("args") or {}).get("action", "?")
    for k, v in SPLIT_TOOL.items():
        if v == tool:
            return k
    return f"other:{tool}"


def schema_errors(move, fixture):
    tool = next((t for t in fixture["tools"] if t["name"] == move.get("tool")), None)
    if tool is None:
        return ["unknown tool"] if move.get("tool") else []
    args = move.get("args") or {}
    props = tool["input_schema"].get("properties", {})
    errs = [f"missing {r}" for r in tool["input_schema"].get("required", []) if r not in args]
    for k, v in args.items():
        p = props.get(k)
        if p is None:
            errs.append(f"unknown arg {k}")
            continue
        if "enum" in p and v not in p["enum"]:
            errs.append(f"{k} not in enum")
        t = p.get("type")
        if t == "integer" and not (isinstance(v, int) and not isinstance(v, bool)):
            errs.append(f"{k} not integer")
        if t == "array" and not isinstance(v, list):
            errs.append(f"{k} not array")
        if t == "string" and not isinstance(v, str):
            errs.append(f"{k} not string")
    return errs


def ids(v):
    if v is None:
        return None
    if not isinstance(v, list):
        v = [v]
    return sorted(str(x).lstrip("#").strip() for x in v)


def same_instant(got, want):
    try:
        g = datetime.fromisoformat(str(got).replace("Z", "+00:00"))
        w = datetime.fromisoformat(want)
    except ValueError:
        return False
    return g.tzinfo is not None and g == w


def arg_errors(case, move, merged):
    exp = case["expect"]
    a = move.get("args") or {}
    errs = []
    ticket_ids = ids(a.get("ticket_ids", a.get("ticket_id")))
    if "ticket_ids" in exp and ticket_ids != ids(exp["ticket_ids"]):
        errs.append(f"ticket_ids {ticket_ids}")
    if "query_words" in exp:
        blob = json.dumps(a).lower()
        if not any(w in blob for w in exp["query_words"]):
            errs.append("search words missing")
    if "assignee" in exp:
        got = str(a.get("assignee", "")).lower()
        ok = {exp["assignee"].lower()} | ({"me"} if exp["assignee"] == "Sam Ortiz" else set())
        if got not in ok:
            # A unique first name resolves under the skill's principle 6; tag it so it can be scored both ways.
            first = exp["assignee"].split()[0].lower()
            unique = sum(1 for s in STAFF if s.split()[0].lower() == first) == 1
            errs.append(FIRST_NAME_ONLY if got == first and unique else f"assignee {a.get('assignee')!r}")
    for key in ("team", "status", "to_email"):
        if key in exp and str(a.get(key, "")).lower() != exp[key].lower():
            errs.append(f"{key} {a.get(key)!r}")
    if "target_id" in exp and ids(a.get("target_id")) != ids(exp["target_id"]):
        errs.append(f"target_id {a.get('target_id')!r}")
    if "source_ids" in exp:
        src = ids(a.get("ticket_ids")) if merged else ids(a.get("source_ids"))
        if src != ids(exp["source_ids"]):
            errs.append(f"source_ids {src}")
    if "due" in exp and not same_instant(a.get("due"), exp["due"]):
        errs.append(f"due {a.get('due')!r}")
    if "minutes" in exp and a.get("minutes") != exp["minutes"]:
        errs.append(f"minutes {a.get('minutes')!r}")
    for key, field in (("body_contains", "body"), ("reason_contains", "reason")):
        if key in exp and not any(w in str(a.get(field, "")).lower() for w in exp[key]):
            errs.append(f"{field} lacks {exp[key]}")
    return errs


def grade_helpdesk(move, fixture, merged):
    case = HELPDESK[move["id"]]
    got = intent_of(move, merged)
    tool_ok = got == case["intent"] or (case["intent"] == "none" and got == "ask_user")
    errs = []
    if tool_ok and move.get("tool"):
        errs = schema_errors(move, fixture) + arg_errors(case, move, merged)
    return {"pass": tool_ok and not errs, "tool_ok": tool_ok, "got": got, "want": case["intent"],
            "trap": got == case.get("trap"), "errors": errs}


RATING_ASK = re.compile(r"1\s*(to|-|–|and)\s*5|rate|rating|how hard|difficult", re.I)


def grade_d(move):
    d = D[move["id"]]
    last = d["transcript"][-1]["data"]
    expected = str(last.get("expected", "")).lower()
    msg = (move.get("message") or "").lower()
    tool = move.get("tool")
    revealed = bool(expected) and expected in msg
    # The rule's point is "do not reveal yet, let them try again". A fresh get_hint or a retry
    # without the answer both honour it; D02 already showed a hint before the wrong answer.
    hint_ok = tool in ("get_hint", None) and not revealed
    rating_ok = tool is None and bool(RATING_ASK.search(msg))
    wrong_d3 = last.get("drill_id") == "d3" and last.get("correct") is False
    if d["decision"] == "round_done" and not wrong_d3:
        ok = rating_ok
    elif wrong_d3:
        ok = (hint_ok or rating_ok) and not revealed
    else:
        ok = hint_ok
    return {"pass": ok, "got": tool or "message", "revealed": revealed, "context": d["context"], "decision": d["decision"]}


def record_ok(record, e):
    t = e["truth"]
    if record is None:
        return False
    want = [(r["drill_id"], bool(r["correct"])) for r in t["results"]]
    got = [(r.get("drill_id"), bool(r.get("correct"))) for r in record.get("results", []) if isinstance(r, dict)]
    rating_ok = record.get("self_rating") == t["rating_truth"]
    dur, tdur = record.get("duration_seconds"), t["duration_seconds_truth"]
    dur_ok = (dur is None and tdur is None) or (isinstance(dur, int) and isinstance(tdur, int) and abs(dur - tdur) <= 120)
    return got == want and rating_ok and dur_ok


def grade_e_write(move):
    e = E[move["id"]]
    if move.get("tool") != "finish_practice":
        asked = move.get("tool") is None and bool(RATING_ASK.search(move.get("message") or ""))
        return {"pass": None, "outcome": "asked" if asked else f"other:{move.get('tool')}"}
    a = move.get("args") or {}
    strict_ok = not strict_errors(a)
    stored, notes = repair(a)
    invented = e["truth"]["rating_truth"] is None and a.get("self_rating") is not None
    return {"pass": None, "outcome": "saved", "strict_ok": strict_ok, "strict_errors": strict_errors(a),
            "strict_record_ok": strict_ok and record_ok(a, e), "repair_record_ok": record_ok(stored, e),
            "repair_notes": notes, "invented_rating": invented}


LEAK = re.compile(r"clamp|rounded|server|ignor|schema|stored|null|correction", re.I)


def grade_e_after(move, mode):
    e = E[move["id"]]
    tool = move.get("tool")
    msg = move.get("message") or ""
    if mode == "strict":
        if tool == "finish_practice":
            a = move.get("args") or {}
            if strict_errors(a):
                return {"pass": False, "outcome": "invalid_retry", "errors": strict_errors(a)}
            invented = e["truth"]["rating_truth"] is None
            return {"pass": not invented, "outcome": "invented_rating" if invented else "saved"}
        if tool is None and RATING_ASK.search(msg):
            # Asking the learner keeps the session alive; it costs a turn, not the data.
            return {"pass": True, "outcome": "asked"}
        return {"pass": False, "outcome": "lost" if tool is None else f"other:{tool}"}
    if tool == "finish_practice":
        return {"pass": False, "outcome": "duplicate"}
    leak = bool(LEAK.search(msg))
    return {"pass": not leak and tool is None, "outcome": "leak" if leak else ("ok" if tool is None else f"other:{tool}")}


def main(results_dir):
    rd = Path(results_dir)
    runs = json.loads((rd / "manifest.json").read_text())
    graded = []
    for r in runs:
        out = Path(r["output"])
        if not out.exists():
            graded.append({**r, "missing": True})
            continue
        fixture = json.loads(Path(r["fixture"]).read_text())
        moves = json.loads(out.read_text())
        rows = []
        for m in moves:
            if r["point"] in ("p1", "p4", "p2"):
                g = grade_helpdesk(m, fixture, merged=r["variant"] == "merged")
            elif r["point"] == "p3":
                g = grade_d(m)
            elif r["point"] == "p6a":
                g = grade_e_write(m)
            else:
                g = grade_e_after(m, r["variant"])
            rows.append({"id": m["id"], **g})
        graded.append({**r, "rows": rows})
    (rd / "graded.json").write_text(json.dumps(graded, indent=1, ensure_ascii=False) + "\n")
    (rd / "summary.md").write_text(summary(graded))
    print(summary(graded))


def p3_rule_chars():
    """Model-facing rule text per conversation: server instructions once, or jit text summed over results."""
    from build_fixtures import PRACTICE_INTRO, RULE_HINT, RULE_RATING
    from prepare import inject_jit
    server = len(" ".join([PRACTICE_INTRO, RULE_HINT, RULE_RATING]))
    jit = []
    for d in PRACTICE["D"]:
        jit.append(sum(len(t["data"].get("instructions", "")) for t in inject_jit(d["transcript"]) if t["role"] == "result"))
    avg = round(sum(jit) / len(jit))
    return {"control": 0, "server": server, "jit": avg, "both": server + avg}


def summary(graded):
    lines = ["# Results", ""]
    by_point = defaultdict(list)
    for g in graded:
        by_point[g["point"]].append(g)
    p3_chars = p3_rule_chars()
    for point in ["p1", "p4", "p2", "p3", "p6a", "p6b"]:
        runs = by_point.get(point, [])
        if point == "p2":
            runs = runs + [dict(g, point="p2", variant="split") for g in by_point["p4"] if g["variant"] == "long_12"]
        if not runs:
            continue
        lines += [f"## {point}", "", "| Variant | haiku | sonnet | opus | Pooled | Chars |", "|---|---|---|---|---|---|"]
        variants = []
        for g in runs:
            if g["variant"] not in variants:
                variants.append(g["variant"])
        for v in variants:
            cells, tp, tn = [], 0, 0
            for m in ["haiku", "sonnet", "opus"]:
                g = next((x for x in runs if x["variant"] == v and x["model"] == m), None)
                if g is None or g.get("missing"):
                    cells.append("missing")
                    continue
                if point == "p6a":
                    rows = [x for x in g["rows"] if x["outcome"] == "saved"]
                    p = sum(x["strict_ok"] for x in rows)
                    cells.append(f"strict ok {p}/{len(g['rows'])}")
                    tp += p
                    tn += len(g["rows"])
                    continue
                p = sum(bool(x["pass"]) for x in g["rows"])
                cells.append(f"{p}/{len(g['rows'])}")
                tp += p
                tn += len(g["rows"])
            if point == "p3":
                chars = p3_chars[v]
            elif point in ("p6a", "p6b"):
                chars = "-"
            else:
                fx = {"p1": f"p1_args_{v}", "p4": f"p4_{v}", "p2": "p2_merged" if v == "merged" else "p4_long_12"}[point]
                chars = SIZES[fx]["chars"]
            lines.append(f"| {v} | " + " | ".join(cells) + f" | {tp}/{tn} | {chars} |")
        lines += ["", "Failures:", ""]
        for g in runs:
            for x in g.get("rows", []):
                if x.get("pass") is False or (point == "p6a" and not x.get("strict_record_ok")):
                    detail = {k: x[k] for k in x if k not in ("id", "pass")}
                    lines.append(f"- {g['variant']} {g['model']} {x['id']}: {json.dumps(detail, ensure_ascii=False)}")
        lines.append("")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main(sys.argv[1])
