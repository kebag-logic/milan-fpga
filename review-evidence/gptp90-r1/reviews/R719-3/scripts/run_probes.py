#!/usr/bin/env python3
"""Generator-mutant probes against a prebuilt engine harness.
usage: run_probes.py <head-src> <workdir> <jobs>
Each probe copies the head generator, applies one exact text substitution
(which must match once), regenerates the image and runs the named pass of
the unmodified harness, recording the tally and every failing check."""
import concurrent.futures as cf, shutil, subprocess, sys
from pathlib import Path
src, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
GEN = "hdl/ucode/gen_gptp_ucode.py"
ARGS = ["--clk-hz", "2000000", "--cease-ms", "3000"]
E = '    p.emit("MASK", rd=RT, ra=R0, rb=RV)               # RT & ~RV\n'
PROBES = [
  ("ctl-clean", None, None),
  ("a sync receipt timeout that ages nothing keeps sync-ok", E, '    p.emit("NOP")\n'),
  ("a consumed pair leaves sync-ok down", "    e_flags(p, orm=FL_SYNCOK_C)\n", "    e_flags(p)\n"),
  ("an expiry takes a master's own vector for a peer's",
   '    p.emit("ALU", rd=RV, ra=RT, rb=0, cnd=ALU_AND, imm=FL_PRESENT_C)\n',
   '    p.emit("MOVE", rd=RV, ra=0, imm=FL_PRESENT_C)\n'),
  ("own: the expiry writes the flags but never commits",
   E + '    p.emit("BR", label=LB["PUBFLAGS"])\n',
   E + '    p.emit("WRST", ra=RT, imm=RG_PUB | 2, fmt=FMT_Q)\n    p.emit("END")\n'),
  ("own: the unaged expiry commits but publishes the flags unmasked",
   E + '    p.emit("BR", label=LB["PUBFLAGS"])\n',
   '    p.emit("NOP")\n    p.emit("BR", label=LB["PUBFLAGS"])\n'),
]
PASSES = [("shipping", [], []), ("p1-255", ["--p1", "255"], ["+not-gm-capable"])]
exe = (src / "tb/verilator/engine/obj_dir/Vengine_sim").resolve()

def one(idx, name, old, new, pname, gargs, pargs):
    d = work / f"{idx:02d}-{pname}"
    if d.exists(): shutil.rmtree(d)
    (d / "hdl/ucode").mkdir(parents=True)
    text = (src / GEN).read_text()
    if old is not None:
        assert text.count(old) == 1, (name, text.count(old))
        text = text.replace(old, new)
    (d / GEN).write_text(text)
    run = d / "run"; run.mkdir()
    g = subprocess.run([sys.executable, "-I", str(d / GEN), *ARGS, *gargs, "-o", str(run / "gptp_ucode.hex")],
                       capture_output=True, text=True)
    if g.returncode:
        return name, pname, f"GENERATOR REJECTED rc={g.returncode}: {g.stderr.strip().splitlines()[-1] if g.stderr.strip() else ''}", [], g.stdout.splitlines()[:1]
    r = subprocess.run([str(exe), *pargs], cwd=run, capture_output=True, text=True, timeout=1500)
    out = r.stdout + r.stderr
    (d / "harness.log").write_text(out)
    tally = [l for l in out.splitlines() if " checks: " in l]
    fails = [l for l in out.splitlines() if l.startswith("FAIL ")]
    return name, pname, f"rc={r.returncode} {tally[-1] if tally else 'NO TALLY'}", fails, g.stdout.splitlines()[:1]

jobsl = [(i, n, o, w, pn, ga, pa) for i, (n, o, w) in enumerate(PROBES) for (pn, ga, pa) in PASSES]
with cf.ThreadPoolExecutor(jobs) as ex:
    res = list(ex.map(lambda a: one(*a), jobsl))
for name, pname, tally, fails, gen in res:
    print(f"== {name} [{pname}] {gen[0] if gen else ''}\n   {tally}")
    for f in fails[:12]: print("   ", f[:220])
    if len(fails) > 12: print(f"    ... {len(fails)-12} more FAIL lines")
