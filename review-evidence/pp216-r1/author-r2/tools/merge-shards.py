#!/usr/bin/env python3
"""merge-shards.py <out> <clone>: join the N shard sweeps of proc-shards.py into one sweep record.

Reads each <out>/shard-k/spec/01.log (the shard's run_suites.sh output) and results.json (its exit status), and
requires: every shard exited 0 and printed its closing `suites: ... 0 failing` line; every suite the full sweep
would run (each tb/*/ of <clone> holding a Makefile, the glob scripts/run_suites.sh reads) is PASS in exactly one
shard; no FAIL or UNREADABLE line. Writes <out>/sweep.log (the shards' lines in suite order and the full sweep's
closing tally, in run_suites.sh's words) and <out>/req-tags.txt (the shards' evidence, concatenated) for
scripts/check-req-tags.py. Exit 0 only when every requirement holds.
"""
import json
import re
import sys
from pathlib import Path

out, clone = Path(sys.argv[1]), Path(sys.argv[2])
suites = sorted(p.parent.name for p in clone.glob('tb/*/Makefile'))
shards = sorted(out.glob('shard-*'), key=lambda p: int(p.name.split('-')[1]))
ok = True
seen: dict[str, str] = {}
evidence = []
for s in shards:
    res = json.loads((s / 'spec' / 'results.json').read_text())
    rc = res['results'][0]['exit_code']
    log = (s / 'spec' / '01.log').read_text()
    closing = re.findall(r'^suites: (\d+) checks total, (\d+) failing$', log, re.M)
    print(f'{s.name}: rc={rc} {res["results"][0]["seconds"]} s closing={closing}')
    ok &= rc == 0 and len(closing) == 1 and closing[0][1] == '0'
    for line in log.splitlines():
        m = re.match(r'^(PASS|FAIL|UNREADABLE) (\S+)', line)
        if not m:
            continue
        if m.group(1) != 'PASS' or m.group(2) in seen:
            ok = False
            print('BAD', s.name, line)
        seen[m.group(2)] = line
    tags = s / 'logs' / 'req-tags.txt'
    if tags.exists():
        evidence.append(tags.read_text())
missing = [x for x in suites if x not in seen]
extra = [x for x in seen if x not in suites]
total = 0
for x in suites:
    if x in seen:
        total += int(re.search(r'\((\d+) checks:', seen[x]).group(1))
ok &= not missing and not extra
print(f'suites at the head: {len(suites)}; PASS: {len(seen)}; missing: {missing}; extra: {extra}')
lines = [seen[x] for x in suites if x in seen]
lines.append(f'suites: {total} checks total, {len(suites) - len(seen)} failing')
(out / 'sweep.log').write_text('\n'.join(lines) + '\n')
(out / 'req-tags.txt').write_text(''.join(evidence))
print(lines[-1])
print('MERGE OK' if ok else 'MERGE FAIL')
raise SystemExit(0 if ok else 1)
