#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: first-party HDL uses the SystemVerilog construct that says what it means.

Why this exists. Rule 10 of the maintainability guide
(docs/development/CODE_QUALITY.md) says new and touched synthesizable HDL uses
the strongest appropriate SystemVerilog construct. `CONTRIBUTING.md` already
requires SystemVerilog for new HDL - but a `.sv` file can still be written as
Verilog-2001, and the compile-time checks that make ownership and intent
reviewable are exactly what is lost when it is.

Three things are checked, at two different strengths.

  1. A GENERIC `always @` in synthesizable first-party HDL is REFUSED. It is
     the one construct here that discards a real check: `always_ff` asks every
     tool to enforce a single driver and to reject a procedural block that is
     not sequential, and `always @` asks for neither. The tree has none, and
     the arm below proves the check bites.

  2. `reg` DECLARATIONS are RATCHETED. A `reg` in a `.sv` file is legal and
     usually harmless, and 48 of them across twelve modules cannot be rewritten
     in one change without exactly the churn the governing rule forbids.
     `logic` is the SystemVerilog spelling and new code uses it.

  3. UNTYPED `parameter` declarations are RATCHETED. `parameter W = 8` takes an
     implementation-defined type; `parameter int W = 8` does not.

WHAT IS NOT CHECKED, deliberately. A `wire` is NOT a finding. A net type is the
correct model for module, primitive, continuous-assignment and multiple-driver
connectivity, and mechanically rewriting `wire` to `logic` would be a
repository-wide edit that changes nothing a reader or a tool can use. The
issue that asked for this rule says so in as many words.

Vendored, generated and archived sources are excluded through
`scripts/lint_rtl.py`'s `LINT_EXCLUDE`, the same list Rules 5, 6 and this rule
share - `hdl/milan/milan_dma_wrapper.v` is a Vivado-generated IP wrapper and
keeps the representation its tool requires.

Usage:
    python3 scripts/check_sv_idiom.py            # gate
    python3 scripts/check_sv_idiom.py --list     # per-file counts
    python3 scripts/check_sv_idiom.py --selftest # fixture arms

Exit 0 = no generic `always`, and the ratchets in scripts/sv_idiom.budget hold.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "sv_idiom.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_rtl import LINT_EXCLUDE

COMMENT = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)
#: `always @` that is NOT always_ff/always_comb/always_latch. The suffixed forms
#: are separate keywords, so a plain `always` followed by `@` is unambiguous.
GENERIC_ALWAYS = re.compile(r"(?<![\w_])always\s*@")
REG_DECL = re.compile(r"^\s*reg\s+", re.M)
UNTYPED_PARAM = re.compile(
    r"\bparameter\s+(?!int\b|logic\b|bit\b|integer\b|byte\b|real\b|shortreal\b"
    r"|string\b|type\b|signed\b|unsigned\b)(\w+)\s*=")


def blank_comments(text):
    return COMMENT.sub(lambda m: "".join(c if c == "\n" else " " for c in m.group(0)),
                       text)


def sources():
    out = subprocess.run(["git", "ls-files", "hdl"], cwd=REPO,
                         capture_output=True, text=True, check=True).stdout.split()
    return [p for p in out
            if p.endswith((".sv", ".svh", ".v")) and p not in LINT_EXCLUDE]


def scan(text):
    """{finding: count} for one HDL source, comments removed first."""
    code = blank_comments(text)
    return {
        "generic always": len(GENERIC_ALWAYS.findall(code)),
        "reg declaration": len(REG_DECL.findall(code)),
        "untyped parameter": len(UNTYPED_PARAM.findall(code)),
    }


def audit():
    totals = {"generic always": 0, "reg declaration": 0, "untyped parameter": 0}
    per_file, sites = {}, []
    for rel in sources():
        text = (REPO / rel).read_text(errors="replace")
        found = scan(text)
        if any(found.values()):
            per_file[rel] = found
        for k, v in found.items():
            totals[k] += v
        if found["generic always"]:
            code = blank_comments(text)
            for m in GENERIC_ALWAYS.finditer(code):
                sites.append((rel, code[:m.start()].count("\n") + 1))
    return totals, per_file, sites


def read_budget():
    if not BUDGET.is_file():
        return {}
    out = {}
    for line in BUDGET.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            if v.strip().isdigit():
                out[k.strip()] = int(v.strip())
    return out


def selftest():
    failures = 0

    def ck(name, ok, detail=""):
        nonlocal failures
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    ck("a generic always is caught",
       scan("always @(posedge c) x <= 1;")["generic always"] == 1)
    ck("always_ff is not a generic always",
       scan("always_ff @(posedge c) x <= 1;")["generic always"] == 0)
    ck("always_comb is not a generic always",
       scan("always_comb begin x = 1; end")["generic always"] == 0)
    ck("always_latch is not a generic always",
       scan("always_latch @(*) x = 1;")["generic always"] == 0)
    ck("a generic always inside a COMMENT is not counted",
       scan("// always @(posedge c) x <= 1;")["generic always"] == 0,
       "comments are blanked before the search")

    ck("a reg declaration is caught", scan("  reg [7:0] x_r;")["reg declaration"] == 1)
    ck("a wire declaration is NOT a finding",
       scan("  wire [7:0] x_w;")["reg declaration"] == 0,
       "a net type is the right model for connectivity")
    ck("a logic declaration is not a finding",
       scan("  logic [7:0] x_r;")["reg declaration"] == 0)
    ck("a bare reg declaration with no width is caught",
       scan("  reg x_r;")["reg declaration"] == 1)

    ck("an untyped parameter is caught",
       scan("parameter W = 8;")["untyped parameter"] == 1)
    ck("a typed parameter is not", scan("parameter int W = 8;")["untyped parameter"] == 0)
    ck("a logic-typed parameter is not",
       scan("parameter logic [7:0] M = 8'hFF;")["untyped parameter"] == 0)

    totals, per_file, sites = audit()
    ck("the live scan reads the tree", len(sources()) > 40, f"{len(sources())} files")
    ck("the excluded list is shared with lint_rtl",
       "hdl/milan/milan_dma_wrapper.v" in LINT_EXCLUDE)
    ck("the ratcheted populations are non-empty",
       totals["reg declaration"] > 0,
       "an inert scan would report zero everywhere and ratchet to nothing")

    n = 15
    print(f"\n{n} checks: {n - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="per-file counts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    totals, per_file, sites = audit()
    bad = False

    for rel, line in sites:
        bad = True
        print(f"GENERIC ALWAYS: {rel}:{line} — use always_ff or always_comb. "
              f"`always @` asks no tool to enforce a single driver, and it does "
              f"not say whether the block is sequential or combinational.")

    if args.list:
        for rel in sorted(per_file, key=lambda r: -sum(per_file[r].values())):
            bits = ", ".join(f"{k} x{v}" for k, v in per_file[rel].items() if v)
            print(f"  {rel}: {bits}")
        print()

    budget = read_budget()
    for key in ("reg declaration", "untyped parameter"):
        limit = budget.get(key)
        if limit is None:
            print(f"NO RATCHET for {key!r} in {BUDGET.relative_to(REPO)}")
            bad = True
        elif totals[key] > limit:
            print(f"FAIL: {key} {totals[key]} > ratchet {limit}. New HDL uses "
                  f"`logic` and typed parameters.")
            bad = True
    if bad:
        return 1

    print(f"SystemVerilog idiom gate: OK ({len(sources())} first-party HDL file(s); "
          f"0 generic `always`; {totals['reg declaration']} reg <= "
          f"{budget['reg declaration']}; {totals['untyped parameter']} untyped "
          f"parameter <= {budget['untyped parameter']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
