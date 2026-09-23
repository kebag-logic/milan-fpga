#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the engine suite's own mutation arm, and reviewer-owned mutants, with
the arm's own stage/build/generate/run/verdict functions imported from the
exported tree, capped at 8 concurrent jobs (RTL builds run one at a time
with 8 build jobs; ROM-only mutants reuse the control build and run up to 8
harness processes at once).

Usage: mutation_arm.py <exported-tree> <work-dir> <selection>
  selection: author[:i-j] | reviewer | control
Prints one line per mutant and a tally; exit 0 when the control passes and
every selected mutant is caught.
"""

from __future__ import annotations

import concurrent.futures as cf
import importlib.util
import sys
from pathlib import Path

GEN = "ucode/gen_gptp_ucode.py"

#: reviewer-owned mutants on the #68 arms: (name, pattern, replacement,
#: property). Each must match exactly once in the generator at the head.
REVIEWER = [
    ("R1 a repeat asCapable verdict also unlocks the servo",
     '    p.emit("BRS", cnd=BRS_Z, label="done")           # already capable\n',
     "",
     "only an asCapable RISE re-arms the link-up"),
    ("R2 the clamp picks its bound with a logical shift",
     '    p.emit("ALU", rd=RU, ra=RW, rb=0, cnd=ALU_SAR, imm=63)\n',
     '    p.emit("ALU", rd=RU, ra=RW, rb=0, cnd=ALU_SHR, imm=63)\n',
     "a negative overflow clamps to -envelope"),
    ("R3 the trim clamp is one unit narrower than the envelope",
     '    e_sat(p, RT, RUNTIME["ilim"], "sv_a")',
     '    e_sat(p, RT, RUNTIME["ilim"] - 1, "sv_a")',
     "the trim reaches the envelope exactly"),
    ("R4 the integrator clamp is one unit wider",
     '    e_sat(p, RC, RUNTIME["ilim"], "sv_i")',
     '    e_sat(p, RC, RUNTIME["ilim"] + 1, "sv_i")',
     "the integrator is clamped to the envelope"),
    ("R5 the locked threshold is 1 ns wider",
     '    p.emit("MOVE", rd=RT, ra=0, imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)\n',
     '    p.emit("MOVE", rd=RT, ra=0, imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C + 1)\n',
     "a locked pair steps above exactly 100 us"),
    ("R6 the positive boundary is 1 ns wider",
     '    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=1)\n'
     '    p.emit("MD", rd=RU, ra=RW, rb=RB, cnd=MD_DIVU)\n',
     '    p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=2)\n'
     '    p.emit("MD", rd=RU, ra=RW, rb=RB, cnd=MD_DIVU)\n',
     "+(T + 1 ns) steps"),
    ("R7 the step writes a zero addend, not the integrator",
     '    p.emit("RDST", rd=RT, imm=RG_SCR | S_INTG, fmt=FMT_Q)\n'
     '    p.emit("BR", label="sv_rate")\n',
     '    p.emit("MOVE", rd=RT, ra=0, imm=0)\n'
     '    p.emit("BR", label="sv_rate")\n',
     "a step keeps the rate estimate as the whole addend"),
    ("R8 the threshold reads the wrong scratch cell",
     '    p.emit("RDST", rd=RB, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n',
     '    p.emit("RDST", rd=RB, imm=RG_SCR | S_T3, fmt=FMT_Q)\n',
     "the threshold follows the lock cell"),
    ("R9 the step carries +offset",
     '    p.emit("WRST", ra=RB, imm=RG_PHC | 1, fmt=FMT_Q)         # adjtime\n',
     '    p.emit("WRST", ra=RA, imm=RG_PHC | 1, fmt=FMT_Q)         # adjtime\n',
     "a step carries -offset"),
]


def load(tree: Path):
    here = tree / "tb/verilator/engine"
    sys.path.insert(0, str(tree / "tb"))
    spec = importlib.util.spec_from_file_location("mutants", here / "mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.VFLAGS = [("8" if v == "4" else v) for v in mod.VFLAGS]
    return mod


def main() -> int:
    tree, work, sel = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
    work.mkdir(parents=True, exist_ok=True)
    m = load(tree)
    hdl = tree / "hdl"
    if sel.startswith("author"):
        muts = [(n, f, p, r, b) for n, f, p, r, b in m.MUTATIONS]
        if ":" in sel:
            lo, hi = (int(x) for x in sel.split(":")[1].split("-"))
            muts = muts[lo:hi + 1]
    elif sel == "reviewer":
        muts = [(n, GEN, p, r, b) for n, p, r, b in REVIEWER]
    else:
        muts = []
    fails = passes = 0
    clean_src = m.stage(work, "clean")
    clean_run = work / "run_clean"
    clean_exe = m.build(clean_src, work, "clean")
    if clean_exe is None or not m.generate_image(clean_src, clean_run):
        print("[FAIL] control did not build")
        return 1
    ans = m.verdict(*m.run_harness(clean_exe, clean_run))
    print(f"[{'PASS' if ans == 'pass' else 'FAIL'}] control: {ans}")
    passes, fails = (1, 0) if ans == "pass" else (0, 1)
    jobs = []
    for name, fname, pat, rep, breaks in muts:
        src = (hdl / fname).read_text(encoding="utf-8")
        if src.count(pat) != 1:
            print(f"[FAIL] {name}: pattern count {src.count(pat)}")
            fails += 1
            continue
        tag = "".join(c if c.isalnum() else "_" for c in name)[:60]
        srcdir = m.stage(work, tag, (fname, pat, rep))
        rundir = work / f"run_{tag}"
        if not m.generate_image(srcdir, rundir):
            print(f"[FAIL] {name}: generator refused the image")
            fails += 1
            continue
        exe = clean_exe if fname == GEN else m.build(srcdir, work, tag)
        if exe is None:
            print(f"[FAIL] {name}: did not build")
            fails += 1
            continue
        jobs.append((name, breaks, exe, rundir))

    def one(job):
        name, breaks, exe, rundir = job
        rc, out = m.run_harness(exe, rundir)
        tally = [ln for ln in out.splitlines() if " checks: " in ln]
        failed = [ln.strip() for ln in out.splitlines() if "FAIL" in ln
                  and " checks: " not in ln][:6]
        return name, breaks, m.verdict(rc, out), tally, failed

    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for name, breaks, ans, tally, failed in ex.map(one, jobs):
            ok = ans == "caught"
            passes += ok
            fails += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {ans}: {name} - defends "
                  f"\"{breaks}\"; {tally[-1] if tally else 'no tally'}")
            for ln in failed:
                print(f"        {ln[:150]}")
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
