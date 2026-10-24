#!/usr/bin/env python3
"""Run the committed campaign while recording the actual source build inputs."""
import hashlib, importlib.util, json, sys
from pathlib import Path
repo, out = map(Path, sys.argv[1:3])
spec = importlib.util.spec_from_file_location('format_mutants', repo / 'tb/verilator/avtp_rxmon/format_mutants.py')
fm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fm)
out.mkdir(parents=True, exist_ok=True)
records = []
original_build, original_ls = fm.build, fm.build_lockstep
def describe(path):
    text = path.read_text()
    return {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'reject_writes': [l.strip() for l in text.splitlines() if 'monst_r <=' in l and 'seq}' in l]}
def build(src, dest):
    records.append({'leg':'NX', 'inputs':[describe(src)]})
    exe = original_build(src, dest)
    return exe
def lockstep(src, dest, ref):
    records.append({'leg':'lockstep N=1,N=8', 'inputs':[describe(src), describe(ref)]})
    return original_ls(src, dest, ref)
fm.build, fm.build_lockstep = build, lockstep
orig_run = fm.run_harness
def run(exe):
    rc, output = orig_run(exe)
    (out / (exe.parent.name + '.log')).write_text(output)
    return rc, output
fm.run_harness = run
orig_ls_run = fm.run_lockstep
counter = 0
def ls_run(exes):
    global counter
    rc, output = orig_ls_run(exes)
    (out / ('pair-' + str(counter) + '.log')).write_text(output)
    counter += 1
    return rc, output
fm.run_lockstep = ls_run
try:
    rc = fm.main()
finally:
    (out / 'build-inputs.json').write_text(json.dumps(records, indent=2) + '\n')
sys.exit(rc)
