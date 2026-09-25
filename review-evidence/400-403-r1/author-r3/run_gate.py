from pathlib import Path
import json, os, subprocess, sys, time
OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/400-403-declaration-truth')
bank = json.loads(Path('$VALIDATION_STORAGE/400-403-manager-r1/manager-builder.json').read_text())
env = os.environ.copy()
for value in bank['commands'][0][1:3]:
    key, value = value.split('=', 1)
    env[key] = value
env['VERILATOR_JOBS'] = '8'
env['MAKEFLAGS'] = '-j8'
env['PYTHONUNBUFFERED'] = '1'
label, *cmd = sys.argv[1:]
if label.startswith('bank-'):
    number = int(label.split('-')[1])
    cmd = bank['commands'][number-1]
    if number == 48:
        cmd = [*cmd[:-1], str(OUT / 'full-builder-sdk.py')]
logfile = OUT / (label + '.log')
start = time.time()
print('START', label, ' '.join(cmd), flush=True)
with logfile.open('w') as log:
    try:
        result = subprocess.run(cmd, cwd=ROOT, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=43200)
        rc = result.returncode
    except subprocess.TimeoutExpired:
        rc = 124
row = dict(label=label, command=cmd, cwd=str(ROOT), exit=rc,
           seconds=round(time.time()-start,2), log=logfile.name)
with (OUT/'gates.jsonl').open('a') as ledger:
    ledger.write(json.dumps(row)+'\n')
with (OUT/'HANDOFF.md').open('a') as handoff:
    handoff.write(f"\n- `{label}`: rc {rc}; {row['seconds']} s; `{logfile.name}`.\n")
print('DONE', json.dumps(row), flush=True)
print(logfile.read_text(errors='replace')[-(3000 if rc else 500):], flush=True)
sys.exit(rc)
