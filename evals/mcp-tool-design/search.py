"""Point 4 in search mode: the host shows tool names only, and the agent loads definitions by search.

Run:
  python3 search.py stage1 results/<dir>   # surfaces, stage-1 inputs, manifest
  python3 search.py stage2 results/<dir>   # rank each stage-1 search, write stage-2 inputs
  python3 search.py grade  results/<dir>   # graded.json and summary.md

Stage 1 sees only names, so it does not depend on the description variant: one stage-1 run per
size, model, and repeat feeds both variants' stage 2. The variants differ in how the search ranks
the helpdesk tools and in what the agent reads once they are loaded.
"""

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

from build_fixtures import helpdesk
from grade import grade_helpdesk

HERE = Path(__file__).resolve().parent
PREFIX = "mcp__helpdesk__"
SIZES = {
    "S": ["Gmail", "Google_Calendar"],
    "M": ["Gmail", "Google_Calendar", "Langmail", "Slack", "Google_Drive", "Granola", "Claude_Docs"],
    "L": ["Gmail", "Google_Calendar", "Langmail", "Slack", "Google_Drive", "Granola", "Claude_Docs", "Cal_com", "betterstack"],
}
VARIANTS = ["short", "long"]
MODELS = ["haiku", "sonnet", "opus"]
REPEATS = [1, 2]
TOP_K = 5
HOST = ("You are the assistant in a chat app with many connected tools. The user is Sam Ortiz, a support "
        "agent on the Billing team, timezone Europe/Berlin. Right now it is Thursday 2026-10-29, 14:00 in Berlin.")


def real_tools():
    tools = []
    for f in sorted((HERE / "fixtures" / "real_tools").glob("*.json")):
        tools += json.loads(f.read_text())
    return tools


def helpdesk_tools(variant):
    out = []
    for t in helpdesk(variant, "minimal", 12)["tools"]:
        out.append({"name": PREFIX + t["name"], "server": "helpdesk", "description": t["description"],
                    "input_schema": t["input_schema"], "annotations": t["annotations"]})
    return out


def surface(size, variant):
    servers = set(SIZES[size])
    return helpdesk_tools(variant) + [t for t in real_tools() if t["server"] in servers]


def cases():
    hd = json.loads((HERE / "cases" / "helpdesk.json").read_text())
    ov = json.loads((HERE / "cases" / "helpdesk_overlap.json").read_text())
    return [c for c in hd if c["set"] in ("B", "C")] + ov


def render_case(c):
    lines = [f"### Case {c['id']}", ""]
    if c.get("context"):
        lines += ["Earlier in this conversation:", "", "```", c["context"], "```", ""]
    lines += [f"User: {c['request']}", ""]
    return "\n".join(lines)


# --- search -----------------------------------------------------------------

TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text):
    return TOKEN.findall(text.lower().replace("_", " "))


def doc_text(t):
    short_name = t["name"].replace("mcp__claude_ai_", "").replace("mcp__", "")
    return f"{short_name} {t['description']}"


def bm25(query, tools, k1=1.2, b=0.75):
    """Keyword search over name and description, top TOP_K. A '+term' must appear in the name."""
    required = [w[1:].lower() for w in query.split() if w.startswith("+")]
    q = tokens(" ".join(w.lstrip("+") for w in query.split()))
    pool = [t for t in tools if all(r in t["name"].lower() for r in required)]
    docs = [tokens(doc_text(t)) for t in pool]
    if not docs:
        return []
    avg = sum(map(len, docs)) / len(docs)
    df = Counter(w for d in docs for w in set(d))
    n = len(docs)
    scored = []
    for t, d in zip(pool, docs):
        tf = Counter(d)
        s = 0.0
        for w in q:
            if w not in tf:
                continue
            idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
            s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(d) / avg))
        if s > 0:
            scored.append((s, t["name"], t))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [t for _, _, t in scored[:TOP_K]]


def load(stage1_move, tools):
    by_name = {t["name"]: t for t in tools}
    sel = stage1_move.get("select") or []
    if sel:
        return [by_name[n] for n in sel[:TOP_K] if n in by_name]
    if stage1_move.get("query"):
        return bm25(stage1_move["query"], tools)
    return []


def render_definition(t):
    if "input_schema" in t:
        body = {"name": t["name"], "description": t["description"], "input_schema": t["input_schema"],
                "annotations": t["annotations"]}
    else:
        body = {"name": t["name"], "description": t["description"], "params": t.get("params", []),
                "required": t.get("required", [])}
    return json.dumps(body, ensure_ascii=False)


# --- stages ---------------------------------------------------------------------

STAGE1_HEAD = """# Stage 1: find the tool

Host context: {host}

Your host shows you the names of {n} connected tools below, but not their descriptions or inputs. Before you can call a
tool you must load it with one search, in one of two forms:

- `select`: up to 5 exact tool names to load.
- `query`: keywords; the search matches them against tool names and descriptions and loads the 5 best matches. A word
  starting with `+` must appear in the tool name (for example `+helpdesk reply`).

## Connected tool names

{names}

## Cases

Every case below is a separate conversation. For each, decide the one search you would run first. If you would not need
any tool (for example you would ask the user something first), give neither.
"""

STAGE2_HEAD = """# Stage 2: act

Host context: {host}

Every case below is a separate conversation. For each, you already ran one search; the tool definitions it loaded are
listed. Decide your single next move: one call to a loaded tool, or a message to the user with no tool call. If none of
the loaded tools fits and you would search again, set `tool` to `"search_again"`.
"""


def stage1(rd):
    rd = Path(rd)
    (rd / "inputs").mkdir(parents=True, exist_ok=True)
    (rd / "raw").mkdir(parents=True, exist_ok=True)
    cs = cases()
    runs = []
    for size in SIZES:
        names = sorted(t["name"] for t in surface(size, "long"))
        text = STAGE1_HEAD.format(host=HOST, n=len(names), names="\n".join(f"- {n}" for n in names))
        text += "\n" + "\n".join(render_case(c) for c in cs)
        inp = rd / "inputs" / f"s1_{size}.md"
        inp.write_text(text)
        for m in MODELS:
            for r in REPEATS:
                runs.append({"stage": 1, "run": f"s1_{size}_{m}_r{r}", "size": size, "model": m, "repeat": r,
                             "input": str(inp), "output": str(rd / "raw" / f"s1_{size}_{m}_r{r}.json")})
    (rd / "manifest_stage1.json").write_text(json.dumps(runs, indent=1) + "\n")
    sizes = {s: len(surface(s, "long")) for s in SIZES}
    print(f"{len(runs)} stage-1 runs; surface sizes {sizes}")


def stage2(rd):
    rd = Path(rd)
    cs = {c["id"]: c for c in cases()}
    runs, loaded_log = [], {}
    for r1 in json.loads((rd / "manifest_stage1.json").read_text()):
        moves = {m["id"]: m for m in json.loads(Path(r1["output"]).read_text())}
        for v in VARIANTS:
            tools = surface(r1["size"], v)
            parts = [STAGE2_HEAD.format(host=HOST)]
            name = f"s2_{r1['size']}_{v}_{r1['model']}_r{r1['repeat']}"
            loaded_log[name] = {}
            for cid, c in cs.items():
                mv = moves.get(cid, {})
                got = load(mv, tools)
                loaded_log[name][cid] = [t["name"] for t in got]
                search = f"select {mv['select']}" if mv.get("select") else (f"query \"{mv.get('query')}\"" if mv.get("query") else "no search")
                parts.append(render_case(c) + f"You ran: {search}\n\nLoaded definitions:\n\n```\n"
                             + ("\n".join(render_definition(t) for t in got) or "(none)") + "\n```\n")
            inp = rd / "inputs" / f"{name}.md"
            inp.write_text("\n".join(parts))
            runs.append({"stage": 2, "run": name, "size": r1["size"], "variant": v, "model": r1["model"],
                         "repeat": r1["repeat"], "input": str(inp), "output": str(rd / "raw" / f"{name}.json")})
    (rd / "manifest_stage2.json").write_text(json.dumps(runs, indent=1) + "\n")
    (rd / "loaded.json").write_text(json.dumps(loaded_log, indent=1) + "\n")
    print(f"{len(runs)} stage-2 runs")


def grade(rd):
    rd = Path(rd)
    loaded = json.loads((rd / "loaded.json").read_text())
    cs = {c["id"]: c for c in cases()}
    graded, missing = [], []
    for r in json.loads((rd / "manifest_stage2.json").read_text()):
        out = Path(r["output"])
        if not out.exists():
            missing.append(r["run"])
            continue
        fixture = helpdesk(r["variant"], "minimal", 12)
        rows = []
        for m in json.loads(out.read_text()):
            m = dict(m)
            tool = m.get("tool")
            if tool == "search_again":
                m["tool"] = "search_again"
            elif tool and tool.startswith(PREFIX):
                m["tool"] = tool[len(PREFIX):]
            g = _grade_case(cs[m["id"]], m, fixture)
            want = cs[m["id"]]["intent"]
            target = None if want in ("ask_user", "none") else PREFIX + _tool_for(want)
            g["found"] = target is None or target in loaded[r["run"]][m["id"]]
            rows.append({"id": m["id"], "set": cs[m["id"]]["set"], **g})
        graded.append({**r, "rows": rows})
    (rd / "graded.json").write_text(json.dumps(graded, indent=1, ensure_ascii=False) + "\n")
    text = summary(graded, missing)
    (rd / "summary.md").write_text(text)
    print(text)


def _tool_for(intent):
    from grade import SPLIT_TOOL
    return SPLIT_TOOL[intent]


def _grade_case(case, move, fixture):
    # grade_helpdesk looks cases up by id in helpdesk.json; overlap cases live elsewhere.
    import grade as g
    g.HELPDESK.setdefault(case["id"], case)
    return grade_helpdesk(move, fixture, merged=False)


def lenient_pass(x):
    from grade import FIRST_NAME_ONLY
    return x["pass"] or (x.get("tool_ok") and x.get("errors") == [FIRST_NAME_ONLY])


def summary(graded, missing):
    lines = ["# Search-mode results", ""]
    if missing:
        lines += [f"Missing runs: {', '.join(missing)}", ""]
    lines += ["| Size | Variant | haiku | sonnet | opus | Pooled correct | First names ok | Found by search | Overlap set O |",
              "|---|---|---|---|---|---|---|---|---|"]
    for size in SIZES:
        for v in VARIANTS:
            cells, tp, tn, tf, op, on = [], 0, 0, 0, 0, 0
            lenient = sum(lenient_pass(x) for g in graded if g["size"] == size and g["variant"] == v for x in g["rows"])
            for m in MODELS:
                rs = [g for g in graded if g["size"] == size and g["variant"] == v and g["model"] == m]
                p = sum(x["pass"] for g in rs for x in g["rows"])
                n = sum(len(g["rows"]) for g in rs)
                cells.append(f"{p}/{n}")
                tp, tn = tp + p, tn + n
                tf += sum(x["found"] for g in rs for x in g["rows"])
                op += sum(x["pass"] for g in rs for x in g["rows"] if x["set"] == "O")
                on += sum(1 for g in rs for x in g["rows"] if x["set"] == "O")
            pct = f" ({100 * tp / tn:.0f}%)" if tn else ""
            lines.append(f"| {size} | {v} | " + " | ".join(cells) + f" | {tp}/{tn}{pct} | {lenient}/{tn} | {tf}/{tn} | {op}/{on} |")
    lines += ["", "Failures (size variant model repeat case: got / want):", ""]
    for g in graded:
        for x in g["rows"]:
            if not x["pass"]:
                lines.append(f"- {g['size']} {g['variant']} {g['model']} r{g['repeat']} {x['id']}: {x['got']} / {x['want']}"
                             f"{' (not found)' if not x['found'] else ''}{' ' + str(x['errors']) if x.get('errors') else ''}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    {"stage1": stage1, "stage2": stage2, "grade": grade}[sys.argv[1]](sys.argv[2])
