#!/usr/bin/env python3
"""Run one named command plan on a built head native driver in its own directory.

Usage: plan_run.py <repo> <build-dir> <shape> <plan> <erase-us> <program-us> <run-dir> [commands-file]
Copies the build's populated slots.bin, writes the plan's commands (or copies the
given file), runs <build>/native/Vsim from <build>/gateware in the foreground,
then grades the raw log with the head's grade() and writes <run-dir>/result.json.
"""
import hashlib, json, shutil, subprocess, sys, time
from pathlib import Path
repo, build, shape, plan = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
erase, program, rundir = int(sys.argv[5]), int(sys.argv[6]), Path(sys.argv[7])
sys.path.insert(0, str(repo / 'tb/verilator/fw_service_budget'))
import run
rundir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(build / 'slots.bin', rundir / 'slots.bin')
if len(sys.argv) > 8:
    shutil.copyfile(sys.argv[8], rundir / 'commands.txt')
else:
    (rundir / 'commands.txt').write_text('\n'.join(run.command_plan(plan, shape)) + '\n')
run.validate_waits(erase, program)
media = json.loads((build / 'media_all.json').read_text())
media['plan'] = plan
argv = [str(build / 'native/Vsim'), str(build / 'aem_desc.bin'), str(rundir / 'slots.bin'),
        str(rundir / 'commands.txt'), str(erase), str(program), str(int(plan == 'uart-paced'))]
t0 = time.time()
with (rundir / 'raw.log').open('w') as log:
    rc = subprocess.run(argv, cwd=build / 'gateware', stdout=log, stderr=subprocess.STDOUT).returncode
raw = (rundir / 'raw.log').read_bytes().decode()
out = dict(shape=shape, plan=plan, erase_us=erase, program_us=program, native_rc=rc,
           elapsed_s=round(time.time() - t0), log_sha256=hashlib.sha256(raw.encode()).hexdigest(), media=media)
try:
    g = run.grade(raw, media)
    out.update(rows=g['rows'], heartbeat=g['heartbeat'], liveness=g['liveness'], budget_findings=g['budget_findings'])
except Exception as exc:
    out['grade_error'] = f'{type(exc).__name__}: {exc}'
(rundir / 'result.json').write_text(json.dumps(out, indent=2) + '\n')
print(shape, plan, 'native_rc', rc, 'grade_error' in out and out['grade_error'] or 'graded', out['log_sha256'])
