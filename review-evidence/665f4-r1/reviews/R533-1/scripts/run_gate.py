#!/usr/bin/env python3
"""Run a foreground validation command and retain its raw output and status."""
import os, pathlib, subprocess, sys, time, json
packet=pathlib.Path(__file__).resolve().parents[1]
(packet/'scratch').mkdir(exist_ok=True)
(packet/'receipts').mkdir(exist_ok=True)
name=sys.argv[1]; argv=sys.argv[2:]
env=os.environ.copy(); env.update(TMPDIR=str(packet/'scratch'),PYTHONDONTWRITEBYTECODE='1',PYTHON_CPU_COUNT='4',VERILATOR_JOBS='2')
start=time.monotonic()
with (packet/'receipts'/f'{name}.log').open('w') as log:
    print('COMMAND:',json.dumps(argv),file=log,flush=True)
    result=subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,env=env)
(packet/'receipts'/f'{name}.rc').write_text(str(result.returncode)+'\n')
print(name,'rc',result.returncode,'seconds',round(time.monotonic()-start,2),flush=True)
print('\n'.join((packet/'receipts'/f'{name}.log').read_text(errors='replace').splitlines()[-14:]))
sys.exit(result.returncode)
