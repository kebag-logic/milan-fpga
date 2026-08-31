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

Five things are checked, at two different strengths.

  1. A first-party HDL file that is NOT SystemVerilog is REFUSED. The accepted
     spellings are a lower-case `.sv` or `.svh`. Every other tracked file under
     `hdl/` whose extension names an HDL source - `.v`, `.vh`, `.vhd`, an
     upper-case `.V` or `.SV`, the rest of `HDL_SUFFIXES`, compared
     case-insensitively - is refused, because each of them is invisible to the
     `*.sv` globs every other tool in this repository matches. The one
     checked-in Verilog wrapper is a documented Vivado boundary in
     `LINT_EXCLUDE`; a new file may not quietly bypass the repository's
     SystemVerilog-only rule.

  2. A GENERIC `always` in synthesizable first-party HDL is REFUSED: the bare
     keyword, whatever follows it (`always @(posedge c)`, `always begin @(..)`,
     `always #5`). It is the one construct here that discards a real check:
     `always_ff` asks every tool to enforce a single driver and to reject a
     procedural block that is not sequential, and `always` asks for neither.
     The tree has none, and the arms below prove the check bites.

  3. `reg` DECLARATIONS are RATCHETED. A `reg` in a `.sv` file is legal and
     usually harmless, and the remaining population cannot be rewritten in
     one change without exactly the churn the governing rule forbids.
     `logic` is the SystemVerilog spelling and new code uses it.

  4. UNTYPED `parameter` declarations are RATCHETED, at zero. `parameter W = 8`
     takes an implementation-defined type; `parameter int W = 8` does not. A
     declaration with no default (`parameter W;`, the must-override form)
     counts, and every name of a list (`parameter A = 1, B = 2;`) counts once.
     A packed range (`parameter [3:0] W = 4`) is an explicit width and is not
     counted; a user-defined type ahead of the name is a type.

  5. UNTYPED `localparam` declarations are RATCHETED separately, by the same
     matcher. A localparam crosses no boundary, so the two that remain are a
     smaller debt than an untyped port parameter would be, but the rule the
     issue wrote names both and a separate entry keeps the two populations
     from being traded against each other.

WHAT IS NOT CHECKED, deliberately. A `wire` is NOT a finding. A net type is the
correct model for module, primitive, continuous-assignment and multiple-driver
connectivity, and mechanically rewriting `wire` to `logic` would be a
repository-wide edit that changes nothing a reader or a tool can use. The
issue that asked for this rule says so in as many words.

WHAT THE POPULATION IS. Every tracked HDL file under `hdl/` in this repository
and under the two pinned project processors, through the shared scope helper
(`code_quality_scope.py`, which refuses an absent or off-pin processor), minus
the whole-file exceptions `scripts/lint_rtl.py` records in `LINT_EXCLUDE` with a
reason each: the Vivado-generated `hdl/milan/milan_dma_wrapper.v` and the
archived Zynq top `hdl/milan/milan_top.sv`. Nothing else is excluded. The
generated headers under `hdl/common/gen/` and `hdl/common/csr/gen/` are
INSIDE the gated set on
purpose - a finding there is fixed in `sw/builder/endstation_builder.py`, which
writes them, and the gate reading them is how a generator regression would be
seen - and the vendored trees (`third_party/`, `external/`) are outside the
scope helper altogether. An empty population, or one that reaches no file under
`hdl/` or under either processor's `hdl/`, is REFUSED (exit 2) before the budget
is read: a gate over a missing tree would otherwise read as a clean ratchet.
Only tracked files are seen (`git ls-files`), so a new file is invisible to the
gate until it is `git add`ed.

Usage:
    python3 scripts/check_sv_idiom.py            # gate
    python3 scripts/check_sv_idiom.py --list     # per-file counts
    python3 scripts/check_sv_idiom.py --selftest # fixture arms

Exit 0 = every file is SystemVerilog, no generic `always`, and the ratchets in
scripts/sv_idiom.budget hold; 1 = a finding, or a missing/malformed ratchet;
2 = the population was refused.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUDGET = Path(__file__).resolve().parent / "sv_idiom.budget"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lint_rtl import LINT_EXCLUDE
from code_quality_scope import PROJECT_SUBMODULES, tracked

#: The accepted spellings, lower-case only: `*.sv` is what every glob in this
#: repository's tooling matches, so a `.SV` would be linted, synthesized and
#: simulated by nobody.
SYSTEMVERILOG = (".sv", ".svh")
#: Extensions that name an HDL source, compared case-insensitively. Anything
#: else tracked under hdl/ (.md, .py, .svg, .json, .drawio) is not HDL.
HDL_SUFFIXES = ("v", "vh", "vl", "vlg", "vlog", "verilog", "sv", "svh", "svi",
                "svp", "vhd", "vhdl")
#: The three trees a complete population reaches.
POPULATION_ROOTS = ("hdl/",) + tuple(f"{sub}/hdl/" for sub in PROJECT_SUBMODULES)
RATCHETED = ("reg declaration", "untyped parameter", "untyped localparam")

NON_CODE = re.compile(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"', re.S)
#: The bare keyword `always`. `always_ff`, `always_comb` and `always_latch` are
#: separate keywords and `_` is a word character, so the lookahead excludes
#: them. Nothing is required AFTER the keyword: requiring an `@` is what let
#: `always begin @(posedge c) ... end` through.
GENERIC_ALWAYS = re.compile(r"(?<![\w$])always(?![\w$])")
#: `reg` is a reserved keyword and therefore unambiguously denotes a legacy
#: variable declaration once comments and string literals have been blanked.
#: Looking only at the start of a line misses ANSI declarations such as
#: ``output reg ready_o`` and declarations preceded by synthesis attributes.
REG_DECL = re.compile(r"\breg\b")
#: A parameter or localparam keyword, and what a TYPED declaration puts right
#: after it: a type keyword, a signing, or a packed range (an explicit width).
PARAM_KW = re.compile(r"\b(parameter|localparam)\b")
TYPED_HEAD = re.compile(
    r"\s*(?:(?:int|integer|shortint|longint|byte|bit|logic|reg|real|shortreal|"
    r"realtime|time|string|type|signed|unsigned)\b|\[)")
#: An untyped item: the identifier right after the keyword or after a
#: top-level comma, optionally dimensioned, then `=` or the end of the item.
#: Anything else in that position is a user-defined type name ahead of the
#: identifier, or the keyword of the next declaration in a port list.
UNTYPED_NAME = re.compile(r"\s*([A-Za-z_]\w*)\s*(?:\[[^\]]*\]\s*)*(?:=|$)")


def blank_non_code(text):
    return NON_CODE.sub(
        lambda m: "".join(c if c == "\n" else " " for c in m.group(0)), text)


def hdl_suffix(path):
    name = path.rsplit("/", 1)[-1]
    return name.rsplit(".", 1)[-1].lower() if "." in name else ""


def is_hdl(path):
    return hdl_suffix(path) in HDL_SUFFIXES


def not_systemverilog(path):
    """True for an HDL file whose spelling is not a lower-case .sv/.svh."""
    return is_hdl(path) and not path.endswith(SYSTEMVERILOG)


def sources():
    return [p for p in tracked("hdl") if is_hdl(p) and p not in LINT_EXCLUDE]


def population_problem(paths):
    """Why this population may not be judged, or None when it is complete."""
    if not paths:
        return "the scan found no tracked HDL at all"
    missing = [root for root in POPULATION_ROOTS
               if not any(p.startswith(root) for p in paths)]
    if missing:
        return "no tracked HDL under " + ", ".join(missing)
    return None


def declaration_items(rest):
    """Top-level comma-separated items of the declaration that starts at rest.

    The declaration ends at a top-level `;`, or at the `)` that closes the
    parameter port list it sits in. Parentheses, brackets and braces inside a
    default expression are tracked, so `f(a, b)` and `{1, 2}` split nothing.
    """
    items, depth, start = [], 0, 0
    for i, ch in enumerate(rest):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            if depth == 0:
                items.append(rest[start:i])
                return items
            depth -= 1
        elif ch == ";" and depth == 0:
            items.append(rest[start:i])
            return items
        elif ch == "," and depth == 0:
            items.append(rest[start:i])
            start = i + 1
    items.append(rest[start:])
    return items


def untyped_names(code):
    """{keyword: [names]} for the parameter/localparam declarations with no type."""
    out = {"parameter": [], "localparam": []}
    for m in PARAM_KW.finditer(code):
        rest = code[m.end():]
        if TYPED_HEAD.match(rest):
            continue
        for item in declaration_items(rest):
            name = UNTYPED_NAME.match(item)
            if not name:
                break  # a user-defined type ahead of the name, or a keyword
            out[m.group(1)].append(name.group(1))
    return out


def scan(text, path="x.sv"):
    """{finding: count} for one HDL source, non-code text removed first."""
    code = blank_non_code(text)
    names = untyped_names(code)
    return {
        "not SystemVerilog": int(not_systemverilog(path)),
        "generic always": len(GENERIC_ALWAYS.findall(code)),
        "reg declaration": len(REG_DECL.findall(code)),
        "untyped parameter": len(names["parameter"]),
        "untyped localparam": len(names["localparam"]),
    }


def audit(paths=None):
    paths = sources() if paths is None else paths
    totals = {"not SystemVerilog": 0, "generic always": 0,
              "reg declaration": 0, "untyped parameter": 0,
              "untyped localparam": 0}
    per_file, sites, foreign = {}, [], []
    for rel in paths:
        text = (REPO / rel).read_text(errors="replace")
        found = scan(text, rel)
        if any(found.values()):
            per_file[rel] = found
        for k, v in found.items():
            totals[k] += v
        if found["not SystemVerilog"]:
            foreign.append(rel)
        if found["generic always"]:
            code = blank_non_code(text)
            for m in GENERIC_ALWAYS.finditer(code):
                sites.append((rel, code[:m.start()].count("\n") + 1))
    return totals, per_file, sites, foreign


def undocumented_hdl_exceptions():
    """Excluded non-SystemVerilog files whose required local rationale is absent."""
    bad = []
    for rel, rationale in LINT_EXCLUDE.items():
        if not not_systemverilog(rel):
            continue
        if (not isinstance(rationale, tuple) or len(rationale) < 2
                or not all(isinstance(item, str) and item.strip()
                           for item in rationale)):
            bad.append(rel)
    return bad


def parse_budget(text):
    """{key: int} from budget text; a malformed value simply has no entry."""
    out = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0].strip()
        if "=" in line:
            k, v = line.split("=", 1)
            if v.strip().isdigit():
                out[k.strip()] = int(v.strip())
    return out


def read_budget():
    return parse_budget(BUDGET.read_text()) if BUDGET.is_file() else {}


def ratchet(totals, budget):
    """(failures, notes): the ratchet verdict for the measured totals.

    A missing or malformed entry is a failure, because an absent budget must
    not read as an unbounded one. A count below its entry is a note that the
    entry can be lowered: a budget only moves downward, and slack in it is
    exactly where the next regression hides.
    """
    failures, notes = [], []
    for key in RATCHETED:
        limit = budget.get(key)
        if limit is None:
            failures.append(f"NO RATCHET for {key!r} in {BUDGET.relative_to(REPO)} "
                            f"(entry missing or not an integer)")
        elif totals[key] > limit:
            failures.append(f"FAIL: {key} {totals[key]} > ratchet {limit}. New HDL "
                            f"uses `logic` and typed parameters.")
        elif totals[key] < limit:
            notes.append(f"  the {key} ratchet can be lowered to {totals[key]}")
    return failures, notes


def selftest():
    failures = checks = 0

    def ck(name, ok, detail=""):
        nonlocal failures, checks
        checks += 1
        if ok:
            print(f"[PASS] {name}")
        else:
            failures += 1
            print(f"[FAIL] {name}{': ' + detail if detail else ''}")

    def n_untyped(text):
        found = scan(text)
        return found["untyped parameter"], found["untyped localparam"]

    ck("a generic always is caught",
       scan("always @(posedge c) x <= 1;")["generic always"] == 1)
    ck("a generic always with begin before the sensitivity list is caught",
       scan("always begin @(posedge c) x <= 1; end")["generic always"] == 1,
       "the keyword is the finding, not the `@` after it")
    ck("a delay-driven generic always is caught",
       scan("always #5 c = ~c;")["generic always"] == 1)
    ck("always_ff is not a generic always",
       scan("always_ff @(posedge c) x <= 1;")["generic always"] == 0)
    ck("always_comb is not a generic always",
       scan("always_comb begin x = 1; end")["generic always"] == 0)
    ck("always_latch is not a generic always",
       scan("always_latch @(*) x = 1;")["generic always"] == 0)
    ck("an identifier containing the word is not a generic always",
       scan("assign my_always_w = always_seen_r;")["generic always"] == 0)
    ck("a generic always inside a COMMENT is not counted",
       scan("// always @(posedge c) x <= 1;")["generic always"] == 0,
       "comments are blanked before the search")
    ck("a generic always inside a string is not counted",
       scan('$display("always @(posedge c)");')["generic always"] == 0,
       "string literals are blanked before the search")

    ck("a reg declaration is caught", scan("  reg [7:0] x_r;")["reg declaration"] == 1)
    ck("an ANSI output reg declaration is caught",
       scan("  output reg [7:0] x_o")["reg declaration"] == 1)
    ck("a wire declaration is NOT a finding",
       scan("  wire [7:0] x_w;")["reg declaration"] == 0,
       "a net type is the right model for connectivity")
    ck("a logic declaration is not a finding",
       scan("  logic [7:0] x_r;")["reg declaration"] == 0)
    ck("a bare reg declaration with no width is caught",
       scan("  reg x_r;")["reg declaration"] == 1)
    ck("the word reg inside a string is not counted",
       scan('$display("reg declaration");')["reg declaration"] == 0)

    for path in ("hdl/x.v", "hdl/x.vh", "hdl/x.V", "hdl/x.SV", "hdl/x.vhd",
                 "protocol-processor/hdl/x.vh"):
        ck(f"a non-SystemVerilog HDL file is refused: {path}",
           scan("module x; endmodule", path)["not SystemVerilog"] == 1)
    for path in ("hdl/x.sv", "hdl/common/x.svh"):
        ck(f"a SystemVerilog file is not refused by extension: {path}",
           scan("module x; endmodule", path)["not SystemVerilog"] == 0)
    ck("a non-HDL file under hdl/ is not in the population",
       not is_hdl("hdl/README.md") and not is_hdl("hdl/x.py"))

    ck("an untyped parameter is caught", n_untyped("parameter W = 8;") == (1, 0))
    ck("an untyped parameter with no default is caught",
       n_untyped("parameter X;") == (1, 0), "the must-override form")
    ck("every name of an untyped parameter list is counted",
       n_untyped("parameter A = 1, B = 2;") == (2, 0))
    ck("a default expression with its own commas splits nothing",
       n_untyped("parameter A = f(1, 2), B = {3, 4};") == (2, 0))
    ck("untyped parameters without defaults in a port list are caught",
       n_untyped("module zz #(parameter X, parameter Y) (input a);") == (2, 0))
    ck("a typed parameter list types every name after it",
       n_untyped("module zz #(parameter int A = 1, B = 2) (input a);") == (0, 0),
       "`B` belongs to the same list_of_param_assignments as the typed `A`")
    ck("a typed parameter is not", n_untyped("parameter int W = 8;") == (0, 0))
    ck("a logic-typed parameter is not",
       n_untyped("parameter logic [7:0] M = 8'hFF;") == (0, 0))
    ck("a user-defined type ahead of the name is a type",
       n_untyped("parameter my_t X = 1;") == (0, 0))
    ck("a packed range is an explicit width, not an untyped parameter",
       n_untyped("parameter [3:0] X = 4;") == (0, 0))
    ck("an untyped localparam is counted in its own population",
       n_untyped("localparam X = $clog2(N);") == (0, 1))
    ck("a typed localparam is not", n_untyped("localparam int X = 4;") == (0, 0))

    ck("an empty population is refused",
       population_problem([]) is not None)
    ck("a population without the processors names both",
       (population_problem(["hdl/a.sv"]) or "").count("/hdl/") == 2)
    ck("a population without one processor names it",
       "gptp-processor/hdl/" in (population_problem(
           ["hdl/a.sv", "protocol-processor/hdl/b.sv"]) or ""))
    ck("a population without the superproject tree is refused",
       "hdl/" in (population_problem(
           ["protocol-processor/hdl/b.sv", "gptp-processor/hdl/c.sv"]) or ""))
    ck("a complete population is not refused",
       population_problem(["hdl/a.sv", "protocol-processor/hdl/b.sv",
                           "gptp-processor/hdl/c.sv"]) is None)

    measured = {"reg declaration": 2, "untyped parameter": 0, "untyped localparam": 0}
    full = {"reg declaration": 2, "untyped parameter": 0, "untyped localparam": 0}
    below = dict(full, **{"reg declaration": 1})
    slack = dict(full, **{"reg declaration": 3})
    ck("a count above its budget fails the ratchet",
       ratchet(measured, below)[0] and "2 > ratchet 1" in ratchet(measured, below)[0][0])
    ck("a count equal to its budget passes with no note",
       ratchet(measured, full) == ([], []))
    ck("a count below its budget passes and names the lowerable value",
       not ratchet(measured, slack)[0]
       and ratchet(measured, slack)[1] == ["  the reg declaration ratchet can be lowered to 2"])
    ck("a missing budget entry fails the ratchet",
       any("NO RATCHET for 'untyped localparam'" in f
           for f in ratchet(measured, dict(full, **{"untyped localparam": None}))[0]))
    ck("a malformed budget value is no entry",
       parse_budget("reg declaration = lots\nuntyped parameter = 0") == {"untyped parameter": 0})
    ck("an absent budget file is an empty budget",
       all(k in ratchet(measured, {})[0][i] for i, k in enumerate(RATCHETED)))

    paths = sources()
    totals, per_file, sites, foreign = audit(paths)
    ck("the live scan reads the tree", len(paths) > 100, f"{len(paths)} files")
    ck("the live scan reaches both project processor submodules",
       any(p.startswith("protocol-processor/") for p in paths)
       and any(p.startswith("gptp-processor/") for p in paths))
    ck("the live population is complete", population_problem(paths) is None,
       str(population_problem(paths)))
    ck("the excluded list is shared with lint_rtl",
       "hdl/milan/milan_dma_wrapper.v" in LINT_EXCLUDE)
    ck("the checked-in Verilog exception has a reason and evidence",
       not undocumented_hdl_exceptions())
    ck("the ratcheted populations are non-empty",
       totals["reg declaration"] > 0,
       "an inert scan would report zero everywhere and ratchet to nothing")
    ck("the checked-in budget carries every ratcheted key",
       all(k in read_budget() for k in RATCHETED), str(read_budget()))

    print(f"\n{checks} checks: {checks - failures} PASS, {failures} FAIL")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="per-file counts")
    ap.add_argument("--selftest", action="store_true", help="run the fixture arms")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    try:
        paths = sources()
    except RuntimeError as exc:
        print(f"POPULATION: REFUSED - {exc}")
        return 2
    problem = population_problem(paths)
    if problem:
        print(f"POPULATION: REFUSED - {problem}. The gate reads the tracked files "
              f"(`git ls-files --recurse-submodules`) under hdl/ in this repository "
              f"and in both pinned processors, and a missing tree would otherwise "
              f"read as a clean ratchet. Refused rather than counted, before the "
              f"budget is read.")
        return 2

    totals, per_file, sites, foreign = audit(paths)
    bad = False

    for rel in foreign:
        bad = True
        print(f"NOT SYSTEMVERILOG: {rel} — first-party HDL carries a lower-case .sv "
              "or .svh extension; an ordinary Verilog file, an include header or "
              "an upper-case extension is seen by no tool here. Rename it, or "
              "record the generated/tool boundary with its rationale in "
              "scripts/lint_rtl.py:LINT_EXCLUDE.")

    for rel in undocumented_hdl_exceptions():
        bad = True
        print(f"UNDOCUMENTED VERILOG EXCEPTION: {rel} — record both the owner/tool "
              "reason and repository evidence in scripts/lint_rtl.py:LINT_EXCLUDE.")

    for rel, line in sites:
        bad = True
        print(f"GENERIC ALWAYS: {rel}:{line} — use always_ff or always_comb. "
              f"A bare `always` asks no tool to enforce a single driver, and it "
              f"does not say whether the block is sequential or combinational.")

    if args.list:
        for rel in sorted(per_file, key=lambda r: -sum(per_file[r].values())):
            bits = ", ".join(f"{k} x{v}" for k, v in per_file[rel].items() if v)
            print(f"  {rel}: {bits}")
        print()

    budget = read_budget()
    failures, notes = ratchet(totals, budget)
    for line in failures:
        print(line)
    if bad or failures:
        return 1

    print(f"SystemVerilog idiom gate: OK ({len(paths)} first-party HDL file(s) across "
          f"the superproject and both processor submodules, every one .sv/.svh; "
          f"0 generic `always`; {totals['reg declaration']} reg <= "
          f"{budget['reg declaration']}; {totals['untyped parameter']} untyped "
          f"parameter <= {budget['untyped parameter']}; "
          f"{totals['untyped localparam']} untyped localparam <= "
          f"{budget['untyped localparam']})")
    for line in notes:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
