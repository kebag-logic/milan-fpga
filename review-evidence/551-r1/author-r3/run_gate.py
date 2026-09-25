import json, os, shlex, subprocess, sys, time
from pathlib import Path
out = Path(__file__).resolve().parent
name, *cmd = sys.argv[1:]
start = time.time()
with (out / (name + '.log')).open('w') as log:
    rc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=14400).returncode
record = dict(name=name, command=shlex.join(cmd), cwd=os.getcwd(), rc=rc, seconds=round(time.time()-start, 2), log=name+'.log')
with (out/'gates.jsonl').open('a') as ledger:
    ledger.write(json.dumps(record)+'\n')
print(json.dumps(record), flush=True)
lines=(out/(name+'.log')).read_text(errors='replace').splitlines()
print('\n'.join(lines[-18:]))
sys.exit(rc)
