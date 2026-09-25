from pathlib import Path
import datetime
import json
import os
import subprocess
import sys
import time

OUT = Path(__file__).resolve().parent
ROOT = Path('$LANES/400-403-declaration-truth')
BANK = Path('$VALIDATION_STORAGE/400-403-manager-r2/manager-builder.json')

def run(label, argv, timeout=14400, cwd=ROOT):
    env = os.environ.copy()
    for value in json.loads(BANK.read_text())['commands'][0][1:]:
        if '=' not in value:
            break
        key, val = value.split('=', 1)
        env[key] = val
    start = time.monotonic()
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (OUT / (label + '.log')).open('w') as log:
        try:
            rc = subprocess.run(argv, cwd=cwd, env=env, stdout=log,
                                stderr=subprocess.STDOUT, timeout=timeout).returncode
        except subprocess.TimeoutExpired:
            rc = 124
    row = dict(label=label, argv=argv, cwd=str(cwd), start=stamp,
               seconds=round(time.monotonic()-start, 3), exit_code=rc)
    (OUT / (label + '.json')).write_text(json.dumps(row, indent=2)+'\n')
    with (OUT / 'gates.jsonl').open('a') as file:
        file.write(json.dumps(row)+'\n')
    print(f"{label}: rc={rc}, {row['seconds']} s", flush=True)
    return rc

if __name__ == '__main__':
    raise SystemExit(run(sys.argv[1], sys.argv[2:]))
