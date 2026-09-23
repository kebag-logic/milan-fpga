#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R259-3 mutation and probe runner for FPGA-gPTP PR #74 (disposable).

    mutation_probe.py EXE TREE [--set SET]

EXE   a built engine harness (the suite's own, or the probe build)
TREE  an export of the reviewed head (its generator is copied, never edited)

Each run writes a ROM image with the suite's arguments from a generator
copy carrying at most one mutation (or from another revision's generator),
runs EXE from that image's directory, and reports the harness tally and the
names of the checks that failed. At most 8 runs execute at once. The verdict
per mutant is the suite's own rule (tb/mutation_verdict.py): caught only when
the harness tally reports a failed check.
"""

from __future__ import annotations

import concurrent.futures as cf
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

GENARGS = ["--clk-hz", "2000000", "--cease-ms", "3000"]
GEN_REL = "hdl/ucode/gen_gptp_ucode.py"
TALLY = re.compile(r"^(\d+) checks: (\d+) PASS, (\d+) FAIL$", re.M)
FAIL_LINE = re.compile(r"^FAIL (.*?)\s+got [0-9a-f]+ exp [0-9a-f]+$", re.M)

S = "    "
RISE_WRITE = (f'{S}p.emit("WRST", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)'
              "  # rose: link-up\n")
LOCK_TAIL = (f'{S}p.emit("MOVE", rd=RT, ra=0, imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)\n'
             f'{S}p.emit("WRST", ra=RT, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n')
STEP_ARM = (f'{S}p.emit("WRST", ra=RB, imm=RG_PHC | 1, fmt=FMT_Q)         # adjtime\n')
SLEW_ARM = (f'{S}p.emit("WRST", ra=RC, imm=RG_SCR | S_INTG, fmt=FMT_Q)\n')
LOCK_VIA_RB = (f'{S}p.emit("MOVE", rd=RB, ra=0, imm=STEP_LOCKED_NS_C - STEP_LINKUP_NS_C)\n'
               f'{S}p.emit("WRST", ra=RB, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n')
BAD_ARM = (f'{S}p.label("bad")\n'
           f'{S}p.emit("WRST", ra=0, imm=RG_SCR | S_PDOK, fmt=FMT_Q)\n')
FUTO_BODY = (f'{S}p.emit("WRST", ra=0, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)\n'
             f'{S}p.emit("END")\n    return p\n\n\ndef prog_leg_rfu')

#: reviewer mutants: (name, [(pattern, replacement), ...], property)
REVIEWER = [
    ("RV1 every good Pdelay verdict re-arms the link-up",
     [(f'{S}p.emit("BRS", cnd=BRS_Z, label="done")           # already capable\n', "")],
     "a good exchange while already capable leaves the lock alone"),
    ("RV2 the delay-threshold fall re-arms, the rise does not",
     [(RISE_WRITE, ""),
      (BAD_ARM, BAD_ARM + f'{S}p.emit("WRST", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n')],
     "every asCapable rise, whatever made it fall, re-arms the link-up"),
    ("RV3 only a step locks the servo",
     [(LOCK_TAIL, ""), (STEP_ARM, STEP_ARM + LOCK_VIA_RB)],
     "a link-up pair that slews also locks the servo"),
    ("RV4 only a slew locks the servo",
     [(LOCK_TAIL, ""), (SLEW_ARM, SLEW_ARM + LOCK_VIA_RB)],
     "a link-up pair that steps also locks the servo"),
    ("RV5 the Follow_Up receipt timeout unlocks the servo",
     [(FUTO_BODY, f'{S}p.emit("WRST", ra=0, imm=RG_SCR | S_SYNCTS, fmt=FMT_Q)\n'
                  f'{S}p.emit("WRST", ra=0, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n'
                  f'{S}p.emit("END")\n    return p\n\n\ndef prog_leg_rfu')],
     "only an asCapable rise unlocks"),
    ("RV6 the link-up threshold is 25 us",
     [(f'{S}p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=STEP_LINKUP_NS_C)\n',
       f'{S}p.emit("ALU", rd=RB, ra=RB, rb=0, cnd=ALU_ADD, imm=25000)\n'),
      (LOCK_TAIL, f'{S}p.emit("MOVE", rd=RT, ra=0, imm=75000)\n'
                  f'{S}p.emit("WRST", ra=RT, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n')],
     "a link-up pair steps over 20 us, locked still over 100 us"),
    ("RV7 the locked threshold is 99 us",
     [(LOCK_TAIL, f'{S}p.emit("MOVE", rd=RT, ra=0, imm=79000)\n'
                  f'{S}p.emit("WRST", ra=RT, imm=RG_SCR | S_LOCK, fmt=FMT_Q)\n')],
     "a locked pair of exactly 100 us slews"),
]


def load_author_mutants(tree: Path):
    """The suite's own #68 generator mutants, read from the head's list."""
    spec = importlib.util.spec_from_file_location(
        "mut", tree / "tb/verilator/engine/mutants.py")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(tree / "tb"))
    spec.loader.exec_module(mod)
    names = mod.MUTATIONS
    start = next(i for i, m in enumerate(names)
                 if m[0] == "every pair uses the locked threshold")
    return [(f"A {n}", [(p, r)], b) for n, f, p, r, b in names[start:]
            if f == mod.GENERATOR]


def run_one(exe: Path, work: Path, tag: str, gen_text: str) -> dict:
    rundir = work / tag
    rundir.mkdir(parents=True, exist_ok=True)
    gen = rundir / "gen_gptp_ucode.py"
    gen.write_text(gen_text, encoding="utf-8")
    g = subprocess.run([sys.executable, str(gen), *GENARGS, "-o",
                        str(rundir / "gptp_ucode.hex")],
                       capture_output=True, text=True)
    if g.returncode != 0:
        return {"tag": tag, "verdict": "generator refused",
                "detail": g.stderr.strip().splitlines()[-1:]}
    r = subprocess.run([str(exe)], cwd=str(rundir), capture_output=True, text=True)
    out = r.stdout + r.stderr
    t = TALLY.search(out)
    failed = [m.group(1).strip() for m in FAIL_LINE.finditer(out)]
    other = [ln for ln in out.splitlines() if ln.startswith("FAIL") and not FAIL_LINE.match(ln)]
    if t is None:
        verdict = f"no tally (rc {r.returncode})"
    elif int(t.group(3)) == 0 and r.returncode == 0:
        verdict = "pass"
    elif int(t.group(3)) > 0 and r.returncode != 0:
        verdict = "caught"
    else:
        verdict = f"masked (rc {r.returncode}, {t.group(0)})"
    return {"tag": tag, "verdict": verdict, "tally": t.group(0) if t else "-",
            "failed": failed + other}


def main() -> int:
    exe = Path(sys.argv[1]).resolve()
    tree = Path(sys.argv[2]).resolve()
    which = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--set" else "all"
    work = Path(os.environ.get("MP_WORK", str(tree.parent / "mp-work"))) / exe.parent.name / which
    head_gen = (tree / GEN_REL).read_text(encoding="utf-8")
    jobs = [("control (head generator)", head_gen, "must pass")]
    muts = []
    if which in ("all", "author"):
        muts += load_author_mutants(tree)
    if which in ("all", "reviewer", "probe"):
        muts += REVIEWER
    if which == "probe":
        muts = [m for m in load_author_mutants(tree) + REVIEWER
                if m[0] in ("A asCapable's rise keeps the lock",
                            "RV2 the delay-threshold fall re-arms, the rise does not",
                            "A becoming grandmaster unlocks the servo",
                            "RV5 the Follow_Up receipt timeout unlocks the servo",
                            "A a receipt timeout unlocks the servo",
                            "A the locked threshold is 200 us")]
    bad = 0
    for name, reps, prop in muts:
        text = head_gen
        for p, r in reps:
            if text.count(p) != 1:
                print(f"PATTERN {name!r}: appears {text.count(p)} times, expected 1")
                bad += 1
                break
            text = text.replace(p, r)
        else:
            jobs.append((name, text, prop))
    for extra in os.environ.get("MP_OTHER_GENS", "").split(":"):
        if extra:
            label, path = extra.split("=", 1)
            jobs.append((f"generator of {label}", Path(path).read_text(encoding="utf-8"),
                         "retired behaviour"))
    tags = {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {}
        for i, (name, text, prop) in enumerate(jobs):
            tag = f"m{i:02d}"
            tags[tag] = (name, prop)
            futs[ex.submit(run_one, exe, work, tag, text)] = tag
        results = {futs[f]: f.result() for f in cf.as_completed(futs)}
    for tag in sorted(results):
        res = results[tag]
        name, prop = tags[tag]
        print(f"[{res['verdict']}] {name}  ({res.get('tally', '-')})")
        print(f"    property: {prop}")
        for f in res.get("failed", []):
            print(f"    FAIL {f}")
        for d in res.get("detail", []):
            print(f"    {d}")
        want = "pass" if tag == "m00" else ("pass" if name.startswith("generator of") and False else None)
        if tag == "m00" and res["verdict"] != "pass":
            bad += 1
        elif tag != "m00" and not name.startswith("generator of") and res["verdict"] != "caught":
            bad += 1
    print(f"\nruns {len(jobs)}; unexpected outcomes {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
