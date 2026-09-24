#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer mutation driver for FPGA-gPTP #75 / PR #76 (round R304-1).

Reuses the engine suite's own staging, image generation and verdict code from
an exported tree (never the reviewed clone), runs the author's 30 mutants and a
reviewer-owned set in a bounded thread pool (each worker drives one subprocess at a time), and records every FAIL line.

usage: probe_mutants.py TREE WORKDIR OUTDIR {author,reviewer} [--jobs N]
                        [--only I,J,...]
The pinned simulator must be first on PATH as `verilator`. Each build runs
single-threaded so N pool workers never exceed N compile jobs.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import importlib.util
import json
import sys
from pathlib import Path

RTL = "top/KL_gptp_engine.sv"
GEN = "ucode/gen_gptp_ucode.py"

# (name, file, pattern, replacement, contract clause the probe attacks)
REVIEWER = [
    ("R01 lapse hook disabled", RTL,
     "                if (phc_slew_active_o &&\n",
     "                if (1'b0 &&\n",
     "asCapable loss / missing Sync restart qualification"),
    ("R02 lapse hook ignores asCapable", RTL,
     "(!st_wdata_w[2] || !st_wdata_w[3])", "(!st_wdata_w[3])",
     "asCapable loss restarts qualification"),
    ("R03 lapse hook ignores sync-ok", RTL,
     "(!st_wdata_w[2] || !st_wdata_w[3])", "(!st_wdata_w[2])",
     "missing Sync / GM change restarts qualification"),
    ("R04 lapse restarts with one pair", RTL,
     "                  phc_slew_left_r <= 2'd2;",
     "                  phc_slew_left_r <= 2'd1;",
     "restart needs two fresh pairs"),
    ("R05 mastership keeps the level", RTL,
     "                phc_slew_left_r   <= 2'd0;\n"
     "                phc_slew_active_o <= 1'b0;\n",
     "                phc_slew_left_r   <= 2'd0;\n",
     "return to GM clears"),
    ("R06 mastership always writes a rate", RTL,
     "                if (phc_slew_active_o) begin\n",
     "                if (1'b1) begin\n",
     "mastership writes a rate only to retire an active correction"),
    ("R07 mastership keeps qualification", RTL,
     "                phc_slew_left_r   <= 2'd0;\n"
     "                phc_slew_active_o <= 1'b0;\n",
     "                phc_slew_active_o <= 1'b0;\n",
     "return to slave starts a fresh decision"),
    ("R08 step clears at the step pulse", RTL,
     "                phc_slew_left_r <= 2'd0;\n              end\n"
     "              2'd2: begin\n",
     "                phc_slew_left_r <= 2'd0;\n"
     "                phc_slew_active_o <= 1'b0;\n              end\n"
     "              2'd2: begin\n",
     "replacement step clears with its rate tail, not before"),
    ("R09 step keeps qualification", RTL,
     "                //! Keep an existing level until the step's rate tail.\n"
     "                phc_slew_left_r <= 2'd0;\n",
     "",
     "replacement step clears"),
    ("R10 reset keeps the level", RTL,
     "      phc_slew_active_o <= 1'b0;\n      phc_slew_left_r   <= 2'd0;\n",
     "      phc_slew_left_r   <= 2'd0;\n",
     "reset clears"),
    ("R11 zero verdict asserts", RTL,
     "                if (st_wdata_w[1:0] != 2'd0)\n"
     "                  phc_slew_active_o <= 1'b1;\n",
     "                phc_slew_active_o <= 1'b1;\n",
     "ordinary tracking stays inactive"),
    ("R12 level rises only with the rate", RTL,
     "                if (st_wdata_w[1:0] != 2'd0)\n"
     "                  phc_slew_active_o <= 1'b1;\n",
     "",
     "level asserts on the decision, before the affected rate"),
    ("R13 rate write never clears", RTL,
     "                phc_slew_active_o <= (phc_slew_left_r != 2'd0);",
     "                phc_slew_active_o <= phc_slew_active_o ||"
     " (phc_slew_left_r != 2'd0);",
     "completion clears"),
    ("R14 lapse hook arms while inactive", RTL,
     "                if (phc_slew_active_o &&\n",
     "                if (1'b1 &&\n",
     "an idle lapse cannot turn ordinary tracking into a slew"),
    ("R15 band excludes +100 ns", GEN,
     "imm=2 * SLEW_SETTLED_NS_C + 1)", "imm=2 * SLEW_SETTLED_NS_C)",
     "inclusive band upper edge"),
    ("R16 band admits +101 ns", GEN,
     "imm=2 * SLEW_SETTLED_NS_C + 1)", "imm=2 * SLEW_SETTLED_NS_C + 2)",
     "decision at +101 ns"),
    ("R17 band biased by 1 ns", GEN,
     "cnd=ALU_ADD, imm=SLEW_SETTLED_NS_C)",
     "cnd=ALU_ADD, imm=SLEW_SETTLED_NS_C - 1)",
     "inclusive band lower edge"),
    ("R18 in-band pair never settles", GEN,
     "    p.emit(\"BRS\", cnd=BRS_LT, label=\"sv_tracking\")\n", "",
     "completion while tracking continues"),
    ("R19 mastership skips retirement", GEN,
     "    p.emit(\"WRST\", ra=RT, imm=RG_PHC | 3, fmt=FMT_Q)\n", "",
     "return to GM clears"),
    ("R20 mastership retires with the wrong sign", GEN,
     "    p.emit(\"ALU\", rd=RT, ra=R0, rb=RT, cnd=ALU_SUB)\n"
     "    p.emit(\"WRST\", ra=RT, imm=RG_PHC | 3, fmt=FMT_Q)\n",
     "    p.emit(\"WRST\", ra=RT, imm=RG_PHC | 3, fmt=FMT_Q)\n",
     "mastership keeps the integral-only rate"),
    ("R21 verdict forgets retained count", GEN,
     "    p.emit(\"RDST\", rd=RB, imm=RG_PHC | 2, fmt=FMT_Q)\n",
     "    p.emit(\"MOVE\", rd=RB, ra=0, imm=0)\n",
     "two consecutive in-band pairs"),
    ("R22 verdict never published", GEN,
     "    p.emit(\"WRST\", ra=RB, imm=RG_PHC | 2, fmt=FMT_Q)\n", "",
     "level asserts on the policy decision"),
]


def load(tree: Path):
    eng = tree / "tb/verilator/engine"
    sys.path.insert(0, str(eng))
    spec = importlib.util.spec_from_file_location("mutants", eng / "mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # single-threaded builds: pool size bounds the compile jobs
    vf = list(mod.VFLAGS)
    i = vf.index("-j")
    vf[i + 1] = "1"
    mod.VFLAGS = vf
    return mod


def run_one(mod, work: Path, clean_exe: Path, entry) -> dict:
    name, fname, pattern, repl, breaks = entry
    src = (mod.HDL / fname).read_text(encoding="utf-8")
    rec = {"name": name, "file": fname, "breaks": breaks,
           "pattern_count": src.count(pattern)}
    if src.count(pattern) != 1:
        rec["answer"] = "pattern not unique"
        return rec
    tag = "".join(c if c.isalnum() else "_" for c in name)
    srcdir = mod.stage(work, tag, (fname, pattern, repl))
    rundir = work / f"run_{tag}"
    if not mod.generate_image(srcdir, rundir):
        rec["answer"] = "generator refused"
        return rec
    exe = clean_exe if fname == mod.GENERATOR else mod.build(srcdir, work, tag)
    if exe is None:
        rec["answer"] = "build failed"
        return rec
    rc, out = mod.run_harness(exe, rundir)
    rec["rc"] = rc
    rec["answer"] = mod.verdict(rc, out)
    rec["fail_lines"] = [l for l in out.splitlines() if l.startswith("FAIL ")]
    rec["tally"] = [l for l in out.splitlines() if " checks: " in l]
    if breaks.startswith("slew:"):
        rec["named_check_failed"] = any(breaks in l for l in rec["fail_lines"])
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("set", choices=["author", "reviewer"])
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    assert 1 <= a.jobs <= 8
    mod = load(a.tree.resolve())
    work = a.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    a.out.mkdir(parents=True, exist_ok=True)
    clean_exe = work / "obj_clean" / "Vengine_clean"
    ctl = a.out / "control.json"
    if not clean_exe.is_file() or not ctl.is_file():
        src = mod.stage(work, "clean")
        exe = mod.build(src, work, "clean")
        ok = exe is not None and mod.generate_image(src, work / "run_clean")
        rc, out = mod.run_harness(exe, work / "run_clean") if ok else (-1, "")
        c = {"answer": mod.verdict(rc, out) if ok else "build failed",
             "tally": [l for l in out.splitlines() if " checks: " in l]}
        ctl.write_text(json.dumps(c, indent=1) + "\n")
        print("control:", c)
        if c["answer"] != "pass":
            return 1
    entries = list(mod.MUTATIONS) if a.set == "author" else REVIEWER
    idx = range(len(entries))
    if a.only:
        idx = [int(x) for x in a.only.split(",")]
    todo = [(i, entries[i]) for i in idx]
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(run_one, mod, work, clean_exe, e): i for i, e in todo}
        for f in cf.as_completed(futs):
            i = futs[f]
            r = f.result()
            r["index"] = i
            (a.out / f"{a.set}_{i:02d}.json").write_text(
                json.dumps(r, indent=1) + "\n")
            print(f"{a.set}[{i:02d}] {r['name']}: {r['answer']}"
                  + (f" named={r.get('named_check_failed')}"
                     if 'named_check_failed' in r else "")
                  + (f" first={r['fail_lines'][:1]}" if r.get('fail_lines') else ""),
                  flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
