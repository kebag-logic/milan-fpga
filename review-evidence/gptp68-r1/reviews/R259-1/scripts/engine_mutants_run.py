#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run a slice of the donor engine suite's own mutation arm, or the
reviewer's extra generator mutants, with the suite's own staging, build,
run and verdict code (tb/verilator/engine/mutants.py, tb/mutation_verdict.py)
imported from the donor checkout given. Every run includes the unmutated
positive control. Nothing is written into the donor tree: staging is in a
temporary directory, exactly as the suite's arm does.

Usage: engine_mutants_run.py <donor checkout> author <first> <last>
       engine_mutants_run.py <donor checkout> reviewer
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

GEN = "ucode/gen_gptp_ucode.py"

#: reviewer mutants of the #68 SERVO leg and the verdict's clear paths:
#: (name, file under hdl/, pattern, replacement, the property it breaks)
REVIEWER = [
    ("R1 the sync receipt timeout keeps sync-ok", GEN,
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C)\n"
     "    p.emit(\"COMMIT\")\n    p.emit(\"END\")\n    return p\n\n\n"
     "def prog_leg_futo",
     "    e_flags(p, andm=FL_PRESENT_C | FL_AMGM_C | FL_ASCAP_C | FL_SYNCOK_C)\n"
     "    p.emit(\"COMMIT\")\n    p.emit(\"END\")\n    return p\n\n\n"
     "def prog_leg_futo",
     "the receipt timeout makes the next pair first"),
    ("R2 becoming grandmaster keeps sync-ok", GEN,
     "    e_flags(p, andm=FL_ASCAP_C, orm=FL_PRESENT_C | FL_AMGM_C)\n",
     "    e_flags(p, andm=FL_ASCAP_C | FL_SYNCOK_C, orm=FL_PRESENT_C | FL_AMGM_C)\n",
     "taking the grandmaster role clears the verdict"),
    ("R3 saturation always picks +lim", GEN,
     "    p.emit(\"ALU\", rd=RU, ra=RW, rb=0, cnd=ALU_SAR, imm=63)\n",
     "    p.emit(\"MOVE\", rd=RU, ra=0, imm=0)\n",
     "an out-of-band negative input saturates to -lim"),
    ("R4 saturation always picks -lim", GEN,
     "    p.emit(\"ALU\", rd=RU, ra=RW, rb=0, cnd=ALU_SAR, imm=63)\n",
     "    p.emit(\"ALU\", rd=RU, ra=R0, rb=0, cnd=ALU_SUB, imm=1)\n",
     "an out-of-band positive input saturates to +lim"),
    ("R6 the step writes +offset", GEN,
     "    p.emit(\"WRST\", ra=RB, imm=RG_PHC | 1, fmt=FMT_Q)         # adjtime\n",
     "    p.emit(\"WRST\", ra=RA, imm=RG_PHC | 1, fmt=FMT_Q)         # adjtime\n",
     "the step carries the negated offset"),
    ("R7 the step keeps the proportional term", GEN,
     "    p.emit(\"RDST\", rd=RT, imm=RG_SCR | S_INTG, fmt=FMT_Q)\n"
     "    p.emit(\"BR\", label=\"sv_rate\")\n",
     "    p.emit(\"BR\", label=\"sv_slew\")\n",
     "the step's addend is the bare integrator"),
    ("R10 every negative first offset steps", GEN,
     "    p.emit(\"ALU\", rd=RT, ra=RA, rb=RB, cnd=ALU_ADD)\n"
     "    p.emit(\"ALU\", rd=RB, ra=RB, rb=RB, cnd=ALU_ADD)\n",
     "    p.emit(\"ALU\", rd=RT, ra=RA, rb=0, cnd=ALU_ADD, imm=0)\n"
     "    p.emit(\"ALU\", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=0)\n",
     "a first offset in [-1 s, 0) slews"),
    ("R12 a same-grandmaster refresh clears sync-ok", GEN,
     "    p.emit(\"BRS\", cnd=BRS_Z, label=\"same_gm\")\n",
     "",
     "a new parent under the same grandmaster never makes a pair first"),
]


def load(path: Path, name: str):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    """Run the control and the selected mutants; 0 only if all are caught."""
    donor = Path(sys.argv[1]).resolve()
    mode = sys.argv[2]
    eng = load(donor / "tb/verilator/engine/mutants.py", "engine_mutants")
    if mode == "author":
        first, last = int(sys.argv[3]), int(sys.argv[4])
        chosen = list(enumerate(eng.MUTATIONS))[first:last + 1]
    else:
        chosen = [(f"r{i}", m) for i, m in enumerate(REVIEWER)]
    bad = 0
    with tempfile.TemporaryDirectory(prefix="r259-engine-mut-") as td:
        work = Path(td)
        clean_src = eng.stage(work, "clean")
        clean_run = work / "run_clean"
        exe = eng.build(clean_src, work, "clean")
        if exe is None or not eng.generate_image(clean_src, clean_run):
            print("[FAIL] control did not build")
            return 1
        ans = eng.verdict(*eng.run_harness(exe, clean_run))
        print(f"[{'PASS' if ans == 'pass' else 'FAIL'}] control: {ans}")
        bad += ans != "pass"
        for idx, (name, fname, pat, rep, breaks) in chosen:
            src = (eng.HDL / fname).read_text(encoding="utf-8")
            if src.count(pat) != 1:
                print(f"[FAIL] {idx} {name!r}: pattern count {src.count(pat)}")
                bad += 1
                continue
            tag = f"m{idx}"
            sdir = eng.stage(work, tag, (fname, pat, rep))
            rdir = work / f"run_{tag}"
            if not eng.generate_image(sdir, rdir):
                print(f"[CAUGHT-GEN] {idx} {name!r}: generator refused")
                continue
            mexe = exe if fname == GEN else eng.build(sdir, work, tag)
            if mexe is None:
                print(f"[FAIL] {idx} {name!r}: did not build")
                bad += 1
                continue
            rc, out = eng.run_harness(mexe, rdir)
            ans = eng.verdict(rc, out)
            nfail = sum(1 for ln in out.splitlines() if ln.startswith("FAIL"))
            first_fail = next((ln for ln in out.splitlines()
                               if ln.startswith("FAIL")), "")
            caught = ans != "pass"
            print(f"[{'CAUGHT' if caught else 'SURVIVED'}] {idx} {name!r} "
                  f"({ans}, {nfail} FAIL lines; first: {first_fail[:90]!r}) "
                  f"-- defends: {breaks}")
            bad += not caught
    print(f"slice result: {'ALL CAUGHT' if bad == 0 else f'{bad} problem(s)'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
