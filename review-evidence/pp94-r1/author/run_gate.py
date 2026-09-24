#!/usr/bin/env python3
import datetime, json, pathlib, subprocess, sys, time
out = pathlib.Path(__file__).resolve().parent
name, *cmd = sys.argv[1:]
start = time.monotonic()
with (out / (name + '.log')).open('w') as log:
    proc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=7200)
record = dict(name=name, command=cmd, rc=proc.returncode,
              seconds=round(time.monotonic()-start, 2),
              finished=datetime.datetime.now(datetime.timezone.utc).isoformat())
with (out / 'gates.jsonl').open('a') as results:
    results.write(json.dumps(record)+'\n')
print(json.dumps(record))
print('\n'.join((out / (name+'.log')).read_text().splitlines()[-12:]))
sys.exit(proc.returncode)
