"""Render one case file per run and the run manifest.

Run: python3 prepare.py <results-dir>
Writes <results-dir>/inputs/<run>.md and <results-dir>/manifest.json.
"""

import copy
import json
import sys
from pathlib import Path

from build_fixtures import RULE_HINT, RULE_RATING
from savecheck import STRICT, REPAIR, server_response

HERE = Path(__file__).resolve().parent
HELPDESK = json.loads((HERE / "cases" / "helpdesk.json").read_text())
PRACTICE = json.loads((HERE / "cases" / "practice.json").read_text())

HELPDESK_HOST = ("You are the assistant in a helpdesk app. The user is Sam Ortiz, Billing team, timezone Europe/Berlin. "
                 "Right now it is Thursday 2026-10-29, 14:00 in Berlin.")
PRACTICE_HOST = "You are the assistant in a practice app. The user is a learner."

TOOL_OF = {"start": "start_practice", "next_drill": "next_drill", "submit": "submit_answer", "hint": "get_hint",
           "resume": "resume_practice", "topics": "list_topics", "finish": "finish_practice"}

MODELS = ["haiku", "sonnet", "opus"]

# Flawed save calls for point 6b, one per E session. Each mirrors the mess in that session.
FLAWS = {
    "E01": ("rating 6 of 5", lambda p: p.update(self_rating=6)),
    "E02": ("rating as a string", lambda p: p.update(self_rating=str(p["self_rating"]))),
    "E03": ("extra field, rating missing", lambda p: (p["results"][1].update(skipped=True), p.pop("self_rating"))),
    "E04": ("duration as text", lambda p: p.update(duration_seconds="unknown")),
    "E05": ("rating 3.5", lambda p: p.update(self_rating=3.5)),
}


def helpdesk_cases(sets):
    out = []
    for c in HELPDESK:
        if c["set"] not in sets:
            continue
        lines = [f"### Case {c['id']}", ""]
        if c["context"]:
            lines += ["Earlier in this conversation:", "", "```", c["context"], "```", ""]
        lines += [f"User: {c['request']}", ""]
        out.append("\n".join(lines))
    return out


def render_turns(turns):
    lines = []
    for t in turns:
        if t["role"] == "learner":
            lines.append(f"Learner: {t['text']}")
        elif t["role"] == "assistant":
            lines.append(f"Assistant: {t['text']}")
        elif t["role"] == "call":
            lines.append(f"Assistant called {TOOL_OF[t['intent']]} {json.dumps(t['data'], ensure_ascii=False)}")
        elif t["role"] == "result":
            lines.append(f"Result: {json.dumps(t['data'], ensure_ascii=False)}")
    return "\n".join(lines)


def inject_jit(turns):
    """The gist's placement: each rule rides on the result just before it is needed."""
    turns = copy.deepcopy(turns)
    for i, t in enumerate(turns):
        if t["role"] != "result" or i == 0 or turns[i - 1].get("intent") != "submit":
            continue
        notes = []
        if t["data"].get("correct") is False:
            notes.append(RULE_HINT)
        if t["data"].get("drill_id") == "d3":
            notes.append(RULE_RATING)
        if notes:
            t["data"]["instructions"] = " ".join(notes)
    return turns


def practice_d_cases(placement):
    out = []
    for d in PRACTICE["D"]:
        turns = inject_jit(d["transcript"]) if placement in ("jit", "both") else d["transcript"]
        out.append(f"### Case {d['id']}\n\n```\n{render_turns(turns)}\n```\n")
    return out


def practice_e_cases():
    return [f"### Case {e['id']}\n\n```\n{render_turns(e['transcript'])}\n```\n" for e in PRACTICE["E"]]


def truth_payload(e):
    t = e["truth"]
    return {
        "run_id": e["run_id"],
        "results": [{"drill_id": r["drill_id"], "answer": r["answer"], "correct": r["correct"]} for r in t["results"]],
        "self_rating": t["rating_truth"] if t["rating_truth"] is not None else 3,
        "duration_seconds": t["duration_seconds_truth"],
    }


def flawed_payload(e):
    p = truth_payload(e)
    FLAWS[e["id"]][1](p)
    return p


def practice_f_cases(mode):
    out = []
    for e in PRACTICE["E"]:
        p = flawed_payload(e)
        turns = render_turns(e["transcript"])
        turns += f"\nAssistant called finish_practice {json.dumps(p, ensure_ascii=False)}"
        turns += f"\nResult: {json.dumps(server_response(p, mode), ensure_ascii=False)}"
        out.append(f"### Case {e['id']}\n\n```\n{turns}\n```\n")
    return out


def write_input(path, fixture, host, cases):
    head = [
        f"# Fixture: {fixture}",
        "",
        f"Host context: {host}",
        "",
        "Every case below is a separate conversation. Decide your single next move in each.",
        "",
    ]
    path.write_text("\n".join(head) + "\n".join(cases))


def main(results_dir):
    rd = Path(results_dir)
    (rd / "inputs").mkdir(parents=True, exist_ok=True)
    (rd / "raw").mkdir(parents=True, exist_ok=True)
    runs = []

    def add(point, fixture, host, cases, variant):
        name = f"{point}_{variant}"
        inp = rd / "inputs" / f"{name}.md"
        write_input(inp, fixture, host, cases)
        for m in MODELS:
            runs.append({"run": f"{name}_{m}", "point": point, "variant": variant, "model": m,
                         "fixture": f"fixtures/{fixture}.json", "input": str(inp),
                         "output": str(rd / "raw" / f"{name}_{m}.json")})

    for v in ["all", "none", "minimal"]:
        add("p1", f"p1_args_{v}", HELPDESK_HOST, helpdesk_cases({"A", "C"}), v)
    # p4 long_12 doubles as p2 split: same fixture, same cases.
    for v in ["short_12", "long_12", "short_35", "long_35"]:
        add("p4", f"p4_{v}", HELPDESK_HOST, helpdesk_cases({"B", "C"}), v)
    add("p2", "p2_merged", HELPDESK_HOST, helpdesk_cases({"B", "C"}), "merged")
    for v in ["control", "server", "jit", "both"]:
        add("p3", f"p3_{v}", PRACTICE_HOST, practice_d_cases(v), v)
    add("p6a", "p6_practice", PRACTICE_HOST, practice_e_cases(), "write")
    for mode in [STRICT, REPAIR]:
        add("p6b", "p6_practice", PRACTICE_HOST, practice_f_cases(mode), mode)

    (rd / "manifest.json").write_text(json.dumps(runs, indent=1) + "\n")
    print(f"{len(runs)} runs")


if __name__ == "__main__":
    main(sys.argv[1])
