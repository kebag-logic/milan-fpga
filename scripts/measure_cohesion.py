#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure module cohesion: how many DISJOINT state groups does one module own?

Why this exists. "That module is too big" is not a reviewable claim, and line
count cannot make it one - a generated table or an explicit state machine may
be long and perfectly cohesive, while a short block can still own two
unrelated pieces of state. Rule 1 of the maintainability guide
(docs/development/CODE_QUALITY.md) asks for a split when a unit's
responsibilities have independently named state, so the measurement has to be
about STATE OWNERSHIP, not size.

What it measures. Every `always_ff` block in a first-party `.sv` file is a
state owner. Two blocks are COUPLED when they share a written signal, or when
one reads a signal the other writes. Coupling is transitive, so the blocks of
a module partition into groups; a module with one group is cohesive by this
measure whatever its length, and a module with twenty is twenty state machines
sharing a file and a reset.

What it does NOT measure. Combinational glue, structural instantiation and
port-level fan-out are invisible here: two groups may still be one
responsibility joined by an `assign`, and the tool says so rather than
pretending otherwise. The number is a CANDIDATE list for review, never an
automatic verdict, and nothing in CI fails on it. The guide's exception list
(a cohesive generated table, descriptor image or explicit state machine may
stay large) is applied by a reader, not here.

Usage:
    python3 scripts/measure_cohesion.py              # ranked candidate table
    python3 scripts/measure_cohesion.py --list       # every module, with groups
    python3 scripts/measure_cohesion.py --module P   # one file, group detail
    python3 scripts/measure_cohesion.py --json       # machine-readable
    python3 scripts/measure_cohesion.py --selftest   # fixture arms

Exit 0 unless --selftest fails.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from code_quality_scope import tracked

#: `always_ff @(...) begin : name` - the name is optional
_BLOCK_RE = re.compile(r"always_ff\s*@\s*\(([^)]*)\)\s*begin(?:\s*:\s*(\w+))?")
#: A non-blocking assignment target, with or without bit/part selects.
#: The leading separator class is load-bearing: `<=` is also the SystemVerilog
#: less-than-or-equal operator, and a target only ever follows a point where a
#: statement can START. `if (count_r <= LIMIT)` puts count_r after `(`, which
#: is deliberately NOT in the set, so a comparison is not read as a write.
_WRITE_RE = re.compile(
    r"(?:^|[\n;:)]|\bbegin\b|\bend\b|\belse\b)\s*(\w+)\s*(?:\[[^\]]*\])*\s*<=", re.M)
#: clock edges inside the sensitivity list
_EDGE_RE = re.compile(r"(?:pos|neg)edge\s+(\w+)")
#: line comments and block comments, stripped before any body analysis so a
#: signal named only inside a comment cannot couple two independent groups
_COMMENT_RE = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
_MODULE_RE = re.compile(r"^\s*module\s+([A-Za-z_]\w*)\b", re.M)
_ENDMODULE_RE = re.compile(r"\bendmodule\b")


def strip_comments(text: str) -> str:
    """Blank out comments, preserving newlines so line numbers survive."""
    def blank(m: re.Match[str]) -> str:
        """One comment as spaces, keeping its newlines so later lines still align."""
        return "".join(ch if ch == "\n" else " " for ch in m.group(0))
    return _COMMENT_RE.sub(blank, text)


def find_blocks(text: str) -> list[tuple[str, str, int]]:
    """Return [(name, body, line)] for every always_ff block in `text`.

    The body runs to the `end` that closes the block's own `begin`, found by
    counting begin/end tokens rather than by matching indentation.
    """
    blocks = []
    for m in _BLOCK_RE.finditer(text):
        start = m.end()
        depth = 1
        for tok in re.finditer(r"\b(begin|end)\b", text[start:]):
            depth += 1 if tok.group(1) == "begin" else -1
            if depth == 0:
                line = text[: m.start()].count("\n") + 1
                blocks.append((m.group(2) or f"line{line}", text[start:start + tok.start()], line))
                break
    return blocks


def group_blocks(blocks: list[tuple[str, str, int]]) -> list[list[int]]:
    """Partition blocks into coupled groups. Returns a list of lists of indices.

    Coupling is symmetric and transitive:
      * two blocks that assign the same signal are the same state owner;
      * a block that READS what another writes consumes that owner's state.
    """
    writes = [set(_WRITE_RE.findall(body)) for _, body, _ in blocks]
    parent = list(range(len(blocks)))

    def find(a: int) -> int:
        """The group `a` currently belongs to, path-compressed on the way up."""
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: int, b: int) -> None:
        """Declare two blocks one state owner; coupling is symmetric, so either
        direction gives the same partition."""
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    def reads(body: str, signals: set[str]) -> bool:
        """Whether `body` consumes any of `signals`, which is what makes reading
        another block's state a coupling rather than an independent group."""
        return any(re.search(r"\b" + re.escape(s) + r"\b", body) for s in signals)

    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            if writes[i] & writes[j]:
                union(i, j)
            elif reads(blocks[j][1], writes[i]) or reads(blocks[i][1], writes[j]):
                union(i, j)

    groups = {}
    for i in range(len(blocks)):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def measure_text(text: str) -> dict[str, object]:
    """Measure one already-read SystemVerilog source."""
    stripped = strip_comments(text)
    blocks = find_blocks(stripped)
    groups = group_blocks(blocks)
    clocks = set()
    for m in _BLOCK_RE.finditer(stripped):
        clocks.update(_EDGE_RE.findall(m.group(1)))
    return {
        "loc": len(text.splitlines()),
        "blocks": len(blocks),
        "groups": len(groups),
        "clocks": sorted(clocks),
        "writes": sorted({w for _, body, _ in blocks for w in _WRITE_RE.findall(body)}),
        "detail": [[(blocks[i][0], blocks[i][2]) for i in g] for g in groups],
    }


def first_party_sources() -> list[str]:
    """The population: tracked first-party SystemVerilog, vendor RTL excluded."""
    return [p for p in tracked("hdl") if p.endswith(".sv")]


def measure_source(text: str) -> list[dict[str, object]]:
    """Return one measurement per module declaration in a source file."""
    code = strip_comments(text)
    rows = []
    for match in _MODULE_RE.finditer(code):
        end = _ENDMODULE_RE.search(code, match.end())
        if end is None:
            continue
        first_line = code[:match.start()].count("\n")
        row = measure_text(code[match.start():end.end()])
        row["module"] = match.group(1)
        row["line"] = first_line + 1
        row["detail"] = [
            [(name, line + first_line) for name, line in group]
            for group in row["detail"]
        ]
        rows.append(row)
    return rows


def measure_repo(paths: list[str] | None = None) -> list[dict[str, object]]:
    """Every module in `paths` (default: the whole population), worst first -
    most disjoint state groups, then longest, which is the review order."""
    rows = []
    for rel in (paths if paths is not None else first_party_sources()):
        for row in measure_source((REPO / rel).read_text(errors="replace")):
            row["path"] = rel
            rows.append(row)
    rows.sort(key=lambda r: (-r["groups"], -r["loc"]))
    return rows


# ---------------------------------------------------------------------------
# self-test - fixtures whose answer is known by construction
# ---------------------------------------------------------------------------
FIXTURES = [
    # (name, source, expected groups, what a wrong answer would mean)
    ("shared write is one owner", """
     module f; always_ff @(posedge c) begin : a  x_r <= 1; end
               always_ff @(posedge c) begin : b  x_r <= 2; end endmodule
     """, 1, "two blocks assigning the same signal must not split"),
    ("independent state is two owners", """
     module f; always_ff @(posedge c) begin : a  x_r <= 1; end
               always_ff @(posedge c) begin : b  y_r <= 2; end endmodule
     """, 2, "unrelated state must be visible as separate owners"),
    ("read of another owner's state couples", """
     module f; always_ff @(posedge c) begin : a  x_r <= 1; end
               always_ff @(posedge c) begin : b  y_r <= x_r; end endmodule
     """, 1, "dropping the read edge would report 2 and hide a real coupling"),
    ("transitive coupling closes the chain", """
     module f; always_ff @(posedge c) begin : a  x_r <= 1; end
               always_ff @(posedge c) begin : b  y_r <= x_r; end
               always_ff @(posedge c) begin : d  z_r <= y_r; end endmodule
     """, 1, "coupling must be transitive, not pairwise"),
    ("a comment cannot couple two owners", """
     module f; always_ff @(posedge c) begin : a  x_r <= 1; end
               always_ff @(posedge c) begin : b  // mirrors x_r
                                                 y_r <= 2; end endmodule
     """, 2, "a signal named only in a comment must not create coupling"),
    ("nested begin/end does not end the block early", """
     module f; always_ff @(posedge c) begin : a
                 if (q) begin x_r <= 1; end else begin x_r <= 2; end
               end
               always_ff @(posedge c) begin : b  y_r <= x_r; end endmodule
     """, 1, "the body must run to the block's own end, not the first one"),
    ("a bit-select write is still a write", """
     module f; always_ff @(posedge c) begin : a  x_r[3] <= 1; end
               always_ff @(posedge c) begin : b  y_r <= x_r; end endmodule
     """, 1, "a part-select assignment is an assignment"),
]


#: statements whose non-blocking assignment targets are known by construction.
#: These grade the write extractor directly, because a wrong write set can be
#: invisible in a group count: a block that compares a signal usually reads it
#: too, and reading couples the same blocks that a false write would.
WRITE_FIXTURES = [
    ("plain assignment", "x_r <= 1;", ["x_r"]),
    ("bit select", "x_r[3] <= 1;", ["x_r"]),
    ("nested part select", "x_r[7:0][1] <= 1;", ["x_r"]),
    ("after begin", "if (q) begin x_r <= 1; end", ["x_r"]),
    ("after a closing paren", "if (q) x_r <= 1;", ["x_r"]),
    ("after else", "if (q) a_r <= 1; else b_r <= 2;", ["a_r", "b_r"]),
    ("after a case label", "case (s) 2'd1: x_r <= 1; endcase", ["x_r"]),
    ("comparison is not a write", "if (count_r <= LIMIT) x_r <= 1;", ["x_r"]),
    ("comparison inside a wider condition", "if (a && (n_r <= 3)) x_r <= 1;", ["x_r"]),
]


def selftest() -> int:
    """Grade the extractor against fixtures whose answer is known by
    construction, so a silently wrong write set cannot pass as a group count."""
    failures = 0
    for name, stmt, want in WRITE_FIXTURES:
        got = sorted(set(_WRITE_RE.findall(stmt)))
        if got == sorted(want):
            print(f"[PASS] write: {name}")
        else:
            failures += 1
            print(f"[FAIL] write: {name}: got {got}, want {sorted(want)}")
    for name, src, want, why in FIXTURES:
        got = measure_text(src)["groups"]
        if got == want:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}: got {got} groups, want {want} - {why}")
    # the block finder must see every block it is given
    blocks = measure_text(FIXTURES[3][1])["blocks"]
    if blocks == 3:
        print("[PASS] block finder counts every always_ff")
    else:
        failures += 1
        print(f"[FAIL] block finder counts every always_ff: got {blocks}, want 3")
    split = measure_source("""
      module one; always_ff @(posedge c) begin a_r <= 1; end endmodule
      module two; always_ff @(posedge c) begin b_r <= 1; end endmodule
    """)
    if len(split) == 2 and [row["groups"] for row in split] == [1, 1]:
        print("[PASS] files with multiple modules are measured per module")
    else:
        failures += 1
        print(f"[FAIL] files with multiple modules are measured per module: {split}")
    total = len(WRITE_FIXTURES) + len(FIXTURES) + 2
    print(f"\n{total} checks: {total - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main() -> int:
    """Print the candidate table, one module's group detail, or the JSON rows.
    Nothing here fails on a measurement; only --selftest can return non-zero."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="every module, not just candidates")
    ap.add_argument("--module", metavar="PATH", help="one file, with per-group detail")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    ap.add_argument("--top", type=int, default=15, help="candidate rows to print (default 15)")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    rows = measure_repo([args.module] if args.module else None)

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    if args.module:
        for row in rows:
            print(f"{row['path']}:{row['module']}: {row['loc']} lines, "
                  f"{row['blocks']} always_ff block(s), {row['groups']} disjoint "
                  f"state group(s), clock(s): {', '.join(row['clocks']) or 'none'}")
            for group in sorted(row["detail"], key=len, reverse=True):
                names = ", ".join(f"{n}@{ln}" for n, ln in group)
                print(f"  [{len(group)} block(s)] {names}")
        return 0

    shown = rows if args.list else [r for r in rows if r["groups"] > 1][: args.top]
    print(f"{'path:module':<68}{'loc':>7}{'blocks':>8}{'groups':>8}")
    for row in shown:
        unit = f"{row['path']}:{row['module']}"
        print(f"{unit:<68}{row['loc']:>7}{row['blocks']:>8}{row['groups']:>8}")
    multi = sum(1 for r in rows if r["groups"] > 1)
    worst = rows[0]["groups"] if rows else 0
    print(f"\n{len(rows)} first-party module(s); {multi} own more than one state group; "
          f"most disjoint: {worst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
