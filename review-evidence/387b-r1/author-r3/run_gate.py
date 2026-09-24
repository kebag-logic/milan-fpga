import json, os, subprocess, sys, time
from pathlib import Path
out = Path(__file__).resolve().parent
name, *command = sys.argv[1:]
start = time.monotonic()
with (out / (name + '.log')).open('w') as log:
    result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, timeout=14400, check=False)
record = dict(command=command, cwd=os.getcwd(), rc=result.returncode, elapsed_s=round(time.monotonic()-start, 2))
(out / (name + '.json')).write_text(json.dumps(record, indent=2)+'\n')
print(name, json.dumps(record), flush=True)
print('\n'.join((out / (name + '.log')).read_text(errors='replace').splitlines()[-12:]), flush=True)
sys.exit(result.returncode)
