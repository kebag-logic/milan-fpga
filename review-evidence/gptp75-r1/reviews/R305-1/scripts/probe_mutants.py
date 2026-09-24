#!/usr/bin/env python3
"""Reviewer mutation probes for FPGA-gPTP #75 / PR #76.

Runs either the PR's own engine mutants (--set pr) or the reviewer's
additional mutants (--set reviewer) against an extracted, unmodified tree,
using the tree's own mutants.py helpers (stage/generate_image/build/
run_harness) and tb/mutation_verdict.py. Nothing is written into the tree:
every mutant is staged under --work.

Usage:
  PATH=<dir holding verilator>:$PATH \
  python3 probe_mutants.py --tree <extracted head> --work <scratch dir> \
      --set pr|reviewer [--slice A:B] [--jobs N]
"""
from __future__ import annotations

import argparse
import importlib.util
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ENG = "top/KL_gptp_engine.sv"
GEN = "ucode/gen_gptp_ucode.py"

# (name, file, pattern, replacement, expectation)
REVIEWER = [
    ("R01 lapse hook fires while inactive", ENG,
     "                if (phc_slew_active_o &&\n"
     "                    (!st_wdata_w[2] || !st_wdata_w[3]))",
     "                if ((!st_wdata_w[2] || !st_wdata_w[3]))",
     "a lapse while inactive must not arm a later in-band pair"),
    ("R02 lapse hook ignores asCapable (bit 2)", ENG,
     "(!st_wdata_w[2] || !st_wdata_w[3])", "(!st_wdata_w[3])",
     "asCapable loss restarts qualification"),
    ("R03 lapse hook ignores sync-ok (bit 3)", ENG,
     "(!st_wdata_w[2] || !st_wdata_w[3])", "(!st_wdata_w[2])",
     "missing Sync restarts qualification"),
    ("R04 lapse hook removed", ENG,
     "                  phc_slew_left_r <= 2'd2;",
     "                  phc_slew_left_r <= phc_slew_left_r;",
     "lapse restarts qualification"),
    ("R05 lapse hook reloads only one pair", ENG,
     "                  phc_slew_left_r <= 2'd2;",
     "                  phc_slew_left_r <= 2'd1;",
     "lapse needs two fresh pairs"),
    ("R06 mastership leaves the qualifier armed", ENG,
     "                phc_slew_left_r   <= 2'd0;\n"
     "                phc_slew_active_o <= 1'b0;",
     "                phc_slew_active_o <= 1'b0;",
     "return to slave: next pair decides afresh"),
    ("R07 mastership writes a rate even when inactive", ENG,
     "                if (phc_slew_active_o) begin\n"
     "                  phc_addend_we_o <= 1'b1;",
     "                if (1'b1) begin\n"
     "                  phc_addend_we_o <= 1'b1;",
     "mastership without a correction leaves the PHC rate alone"),
    ("R08 mastership never writes the rate", ENG,
     "                if (phc_slew_active_o) begin\n"
     "                  phc_addend_we_o <= 1'b1;",
     "                if (1'b0) begin\n"
     "                  phc_addend_we_o <= 1'b1;",
     "mastership replaces the active correction's rate"),
    ("R09 step keeps the qualifier", ENG,
     "                //! Keep an existing level until the step's rate tail.\n"
     "                phc_slew_left_r <= 2'd0;",
     "                //! Keep an existing level until the step's rate tail.",
     "replacement step clears at its rate"),
    ("R10 step clears the level before its rate", ENG,
     "                //! Keep an existing level until the step's rate tail.\n"
     "                phc_slew_left_r <= 2'd0;",
     "                phc_slew_left_r <= 2'd0;\n"
     "                phc_slew_active_o <= 1'b0;",
     "level held through the step until its rate"),
    ("R11 level rises only at the rate write", ENG,
     "                if (st_wdata_w[1:0] != 2'd0)\n"
     "                  phc_slew_active_o <= 1'b1;",
     "",
     "level rises on the decision, before the affected rate"),
    ("R12 rate write never clears", ENG,
     "                phc_slew_active_o <= (phc_slew_left_r != 2'd0);",
     "                phc_slew_active_o <= phc_slew_active_o;",
     "completion clears"),
    ("R13 qualifier reads back as zero", ENG,
     "      4'd4: st_rd_mux_w = {62'd0, phc_slew_left_r};",
     "      4'd4: st_rd_mux_w = 64'd0;",
     "microcode sees the remaining pairs"),
    ("R14 reset leaves the level high", ENG,
     "      phc_slew_active_o <= 1'b0;\n      phc_slew_left_r   <= 2'd0;",
     "      phc_slew_active_o <= 1'b1;\n      phc_slew_left_r   <= 2'd0;",
     "reset clears the level"),
    ("R15 band excludes +100 ns", GEN,
     "imm=2 * SLEW_SETTLED_NS_C + 1)", "imm=2 * SLEW_SETTLED_NS_C)",
     "band is inclusive at +100 ns"),
    ("R16 band 101 ns wide", GEN,
     "SLEW_SETTLED_NS_C = 100", "SLEW_SETTLED_NS_C = 101",
     "+-101 ns starts a correction"),
    ("R17 three settled pairs required", GEN,
     "    p.emit(\"MOVE\", rd=RB, ra=0, imm=3)                       # reload, then -1",
     "    p.emit(\"MOVE\", rd=RB, ra=0, imm=4)                       # reload, then -1",
     "second in-band pair completes"),
    ("R18 mastership skips the retire write", GEN,
     "    p.emit(\"WRST\", ra=RT, imm=RG_PHC | 3, fmt=FMT_Q)",
     "",
     "mastership retires the correction"),
    ("R19 mastership retires with the wrong sign", GEN,
     "    p.emit(\"RDST\", rd=RT, imm=RG_SCR | S_INTG, fmt=FMT_Q)\n"
     "    p.emit(\"ALU\", rd=RT, ra=R0, rb=RT, cnd=ALU_SUB)\n"
     "    p.emit(\"WRST\", ra=RT, imm=RG_PHC | 3, fmt=FMT_Q)",
     "    p.emit(\"RDST\", rd=RT, imm=RG_SCR | S_INTG, fmt=FMT_Q)\n"
     "    p.emit(\"WRST\", ra=RT, imm=RG_PHC | 3, fmt=FMT_Q)",
     "mastership keeps the integral-only rate"),
    ("R20 verdict written after the rate", GEN,
     "    p.emit(\"WRST\", ra=RB, imm=RG_PHC | 2, fmt=FMT_Q)\n",
     "",
     "verdict published at all"),
]


def load_mutants(tree: Path):
    path = tree / "tb/verilator/engine/mutants.py"
    spec = importlib.util.spec_from_file_location("tree_mutants", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True, type=Path)
    ap.add_argument("--work", required=True, type=Path)
    ap.add_argument("--set", choices=("pr", "reviewer", "control"),
                    required=True)
    ap.add_argument("--slice", default=":")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="",
                    help="comma-separated name prefixes, e.g. R01,R06")
    a = ap.parse_args()
    m = load_mutants(a.tree.resolve())
    # two build threads per job keeps jobs * 2 within the reviewer's budget
    m.VFLAGS[m.VFLAGS.index("-j") + 1] = "2"
    lo, hi = (int(x) if x else None for x in a.slice.split(":"))
    work = a.work.resolve()
    work.mkdir(parents=True, exist_ok=True)

    clean_src = m.stage(work, "clean")
    clean_exe = m.build(clean_src, work, "clean")
    if clean_exe is None:
        print("[FAIL] unmutated build failed")
        return 1
    if a.set == "control":
        run = work / "run_clean"
        m.generate_image(clean_src, run)
        rc, out = m.run_harness(clean_exe, run)
        for ln in out.splitlines():
            if ln.startswith("FAIL ") or " checks: " in ln or "r305" in ln:
                print(ln)
        print(f"[CONTROL] unmutated: {m.verdict(rc, out)}")
        return 0

    if a.set == "pr":
        muts = [(n, f, p, r, b) for n, f, p, r, b in m.MUTATIONS]
    else:
        muts = REVIEWER
    muts = muts[lo:hi]
    if a.only:
        keys = tuple(a.only.split(","))
        muts = [e for e in muts if e[0].startswith(keys)]

    def one(entry):
        name, fname, pat, rep, breaks = entry
        src = (m.HDL / fname).read_text(encoding="utf-8")
        if src.count(pat) != 1:
            return name, f"pattern count {src.count(pat)}", ""
        tag = "".join(c if c.isalnum() else "_" for c in name)
        srcdir = m.stage(work, tag, (fname, pat, rep))
        rundir = work / f"run_{tag}"
        if not m.generate_image(srcdir, rundir):
            return name, "generator refused image", ""
        exe = clean_exe if fname == m.GENERATOR else m.build(srcdir, work, tag)
        if exe is None:
            return name, "build failed", ""
        rc, out = m.run_harness(exe, rundir)
        ans = m.verdict(rc, out)
        first = " || ".join(ln for ln in out.splitlines()
                            if ln.startswith("FAIL "))[:600]
        if a.set == "pr" and breaks.startswith("slew:") and ans == "caught":
            if not any(ln.startswith("FAIL ") and breaks in ln
                       for ln in out.splitlines()):
                ans = "missed its named check"
        return name, ans, first

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        results = list(ex.map(one, muts))
    for name, ans, first in results:
        print(f"[{ans.upper() if ans in ('caught', 'pass') else ans}] {name}"
              + (f"  | first: {first}" if first else ""))
    survived = [r for r in results if r[1] != "caught"]
    print(f"\n{len(results)} probes: {len(results) - len(survived)} caught, "
          f"{len(survived)} not caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())
