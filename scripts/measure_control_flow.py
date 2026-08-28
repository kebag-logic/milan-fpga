#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure control-flow shape: nesting, decisions, and implicit priority.

Why this exists. Rule 2 of the maintainability guide
(docs/development/CODE_QUALITY.md) asks for the simplest control flow that
makes state, priority, timing and error paths obvious. "Simplest" cannot be
argued from taste and must not be imported as a generic complexity limit from
some other codebase, so this tool measures THIS tree first and the guide quotes
what it found.

Two languages, two different questions:

  * Host code (Python) - how deep does control flow nest inside one function,
    and how many decision points does a reader hold at once? Depth is the
    number of enclosing branch/loop/try constructs; decisions counts `if`,
    `for`, `while`, `try` handlers, boolean operators and conditional
    expressions. Neither is a defect on its own; together they say how much of
    a function a reader must simulate to know what it does with a failure.

  * SystemVerilog - is priority VISIBLE? A signal assigned more than once in
    one procedural block resolves by source order: the last assignment wins.
    That is real, legal, frequently correct - and it is invisible at the point
    of use, because nothing in the block says "this is the default and that is
    the override". The rule does not forbid it; it asks that the priority be
    visible in structure or named explicitly, so this tool lists where the
    ordering is load-bearing.

Nothing here is a gate. There is no threshold, nothing in CI fails on these
numbers, and a high count is a question for review, not a defect.

Usage:
    python3 scripts/measure_control_flow.py             # both, ranked
    python3 scripts/measure_control_flow.py --python    # host code only
    python3 scripts/measure_control_flow.py --sv        # RTL only
    python3 scripts/measure_control_flow.py --json      # machine-readable
    python3 scripts/measure_control_flow.py --selftest  # fixture arms

Exit 0 unless --selftest fails.
"""

import argparse
import ast
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from code_quality_scope import tracked

#: constructs that add a level of nesting a reader must hold
_NESTING = (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.Match,
            ast.AsyncFor, ast.AsyncWith)
#: constructs that add a decision point
_DECISION = (ast.If, ast.For, ast.While, ast.Match, ast.match_case,
             ast.ExceptHandler, ast.BoolOp, ast.IfExp, ast.Assert,
             ast.comprehension)


# ---------------------------------------------------------------------------
# host code
# ---------------------------------------------------------------------------
#: a nested definition is measured as its own unit, so the enclosing function
#: does not inherit its depth or its decisions. Without this an orchestrator
#: that defines one small helper reads as deeply nested when it is not.
_OWN_UNIT = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)


def _own_body(node):
    """Walk `node`, yielding every descendant that still belongs to it."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _OWN_UNIT):
            continue
        yield child
        yield from _own_body(child)


def _depth(node, level=0):
    deepest = level
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _OWN_UNIT):
            continue
        step = level + 1 if isinstance(child, _NESTING) else level
        deepest = max(deepest, _depth(child, step))
    return deepest


def measure_python_source(src):
    """Return one row per function defined in `src`."""
    rows = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        end = getattr(node, "end_lineno", None) or max(
            (getattr(c, "lineno", node.lineno) for c in ast.walk(node)), default=node.lineno)
        rows.append({
            "name": node.name,
            "line": node.lineno,
            "loc": end - node.lineno + 1,
            "depth": _depth(node),
            "decisions": sum(1 for c in _own_body(node) if isinstance(c, _DECISION)),
        })
    return rows


def measure_python():
    rows = []
    for rel in tracked("scripts/*.py", "sw/**/*.py", "tb/**/*.py", "harness/**/*.py"):
        try:
            found = measure_python_source((REPO / rel).read_text(errors="replace"))
        except SyntaxError:
            continue
        for row in found:
            row["path"] = rel
            rows.append(row)
    rows.sort(key=lambda r: (-r["depth"], -r["decisions"]))
    return rows


# ---------------------------------------------------------------------------
# SystemVerilog - where is priority decided by source order?
# ---------------------------------------------------------------------------
_SV_BLOCK_RE = re.compile(r"always_(ff|comb|latch)\s*(?:@\s*\([^)]*\))?\s*begin(?:\s*:\s*(\w+))?")
_SV_ASSIGN_RE = re.compile(
    r"(?:^|[\n;:)]|\bbegin\b|\bend\b|\belse\b)\s*(\w+)\s*(?:\[[^\]]*\])*\s*(?:<=|=)(?!=)", re.M)
_SV_COMMENT_RE = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)


def _sv_strip(text):
    def blank(m):
        return "".join(ch if ch == "\n" else " " for ch in m.group(0))
    return _SV_COMMENT_RE.sub(blank, text)


def _sv_blocks(text):
    blocks = []
    for m in _SV_BLOCK_RE.finditer(text):
        start, depth = m.end(), 1
        for tok in re.finditer(r"\b(begin|end)\b", text[start:]):
            depth += 1 if tok.group(1) == "begin" else -1
            if depth == 0:
                line = text[: m.start()].count("\n") + 1
                blocks.append((m.group(1), m.group(2) or f"line{line}",
                               text[start:start + tok.start()], line))
                break
    return blocks


def _sv_depth(body):
    """Deepest nesting of begin/case inside one procedural block."""
    depth = best = 0
    for tok in re.finditer(r"\b(begin|end|case|casez|casex|endcase)\b", body):
        word = tok.group(1)
        if word in ("begin", "case", "casez", "casex"):
            depth += 1
            best = max(best, depth)
        else:
            depth -= 1
    return best


def measure_sv_source(text):
    rows = []
    for kind, name, body, line in _sv_blocks(_sv_strip(text)):
        targets = _SV_ASSIGN_RE.findall(body)
        repeated = sorted({t for t in targets if targets.count(t) > 1})
        rows.append({
            "block": name,
            "kind": f"always_{kind}",
            "line": line,
            "loc": body.count("\n") + 1,
            "depth": _sv_depth(body),
            "order_dependent": repeated,
        })
    return rows


def measure_sv():
    rows = []
    for rel in [p for p in tracked("hdl") if p.endswith(".sv")]:
        for row in measure_sv_source((REPO / rel).read_text(errors="replace")):
            row["path"] = rel
            rows.append(row)
    rows.sort(key=lambda r: (-len(r["order_dependent"]), -r["depth"], -r["loc"]))
    return rows


# ---------------------------------------------------------------------------
# self-test
# ---------------------------------------------------------------------------
PY_FIXTURES = [
    ("flat function is depth 0", "def f():\n    return 1\n", 0, 0),
    ("one if is depth 1", "def f(a):\n    if a:\n        return 1\n    return 0\n", 1, 1),
    ("sibling ifs do not stack", "def f(a):\n    if a:\n        pass\n    if a:\n        pass\n", 1, 2),
    ("nested if/for stacks", "def f(a):\n    if a:\n        for i in a:\n            if i:\n                pass\n", 3, 3),
    ("try/except counts the handler",
     "def f():\n    try:\n        pass\n    except ValueError:\n        pass\n", 1, 1),
    ("boolean operators are decisions", "def f(a, b):\n    return a and b\n", 0, 1),
    ("a nested def is measured on its own",
     "def outer():\n    def inner(a):\n        if a:\n            pass\n    return inner\n", 0, 0),
    ("match cases are visible control flow",
     "def f(x):\n    match x:\n        case 0: return 0\n        case _: return 1\n", 1, 3),
]

SV_FIXTURES = [
    ("single assignment has no implicit priority",
     "always_comb begin : b  x_w = 1; end", []),
    ("a re-assigned signal is order dependent",
     "always_comb begin : b  x_w = 1; if (q) x_w = 2; end", ["x_w"]),
    ("default-then-override in a case is order dependent",
     "always_comb begin : b  y_w = 0; case (s) 2'd1: y_w = 1; endcase end", ["y_w"]),
    ("two different signals are not order dependent",
     "always_comb begin : b  x_w = 1; y_w = 2; end", []),
    ("a comparison is not an assignment",
     "always_comb begin : b  x_w = (a == b); end", []),
]


def selftest():
    failures = 0
    for name, src, want_depth, want_dec in PY_FIXTURES:
        rows = measure_python_source(src)
        row = next(r for r in rows if r["name"] in ("f", "outer"))
        if row["depth"] == want_depth and row["decisions"] == want_dec:
            print(f"[PASS] python: {name}")
        else:
            failures += 1
            print(f"[FAIL] python: {name}: got depth {row['depth']} decisions "
                  f"{row['decisions']}, want {want_depth}/{want_dec}")

    # the nested-def arm also proves the inner function is reported separately
    rows = measure_python_source(PY_FIXTURES[-2][1])
    inner = [r for r in rows if r["name"] == "inner"]
    if len(inner) == 1 and inner[0]["depth"] == 1:
        print("[PASS] python: inner function reported with its own depth")
    else:
        failures += 1
        print(f"[FAIL] python: inner function reported with its own depth: {inner}")

    for name, src, want in SV_FIXTURES:
        row = measure_sv_source(src)[0]
        if row["order_dependent"] == want:
            print(f"[PASS] sv: {name}")
        else:
            failures += 1
            print(f"[FAIL] sv: {name}: got {row['order_dependent']}, want {want}")

    # nesting inside a procedural block, including case
    # depth is measured INSIDE the block: the block's own `begin` is the block,
    # so `if (q) begin case (...) ... endcase end` nests two levels, not three.
    depth = measure_sv_source(
        "always_ff @(posedge c) begin : b if (q) begin case (s) 2'd0: x_r <= 1; endcase end end"
    )[0]["depth"]
    if depth == 2:
        print("[PASS] sv: begin/case nesting is counted inside the block")
    else:
        failures += 1
        print(f"[FAIL] sv: begin/case nesting is counted inside the block: got {depth}, want 2")

    total = len(PY_FIXTURES) + len(SV_FIXTURES) + 2
    print(f"\n{total} checks: {total - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--python", action="store_true", help="host code only")
    ap.add_argument("--sv", action="store_true", help="RTL only")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    ap.add_argument("--top", type=int, default=15, help="rows per table (default 15)")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    want_py = args.python or not args.sv
    want_sv = args.sv or not args.python
    out = {}

    if want_py:
        rows = measure_python()
        out["python"] = rows
        if not args.json:
            print(f"{'path:line':<58}{'function':<34}{'loc':>6}{'depth':>7}{'decisions':>11}")
            for r in rows[: args.top]:
                where = f"{r['path']}:{r['line']}"
                print(f"{where:<58}{r['name'][:33]:<34}{r['loc']:>6}{r['depth']:>7}{r['decisions']:>11}")
            deep = sum(1 for r in rows if r["depth"] >= 5)
            print(f"\n{len(rows)} first-party function(s); {deep} nest five levels or deeper\n")

    if want_sv:
        rows = measure_sv()
        out["sv"] = rows
        if not args.json:
            print(f"{'path:line':<58}{'block':<28}{'depth':>7}{'order-dependent signals':>26}")
            for r in rows[: args.top]:
                where = f"{r['path']}:{r['line']}"
                print(f"{where:<58}{r['block'][:27]:<28}{r['depth']:>7}{len(r['order_dependent']):>26}")
            ordered = sum(1 for r in rows if r["order_dependent"])
            print(f"\n{len(rows)} procedural block(s); {ordered} resolve at least one signal "
                  f"by source order")

    if args.json:
        print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
