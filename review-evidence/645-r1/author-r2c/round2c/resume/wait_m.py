import sys, time, re
from pathlib import Path
w = Path('$VALIDATION_STORAGE/645-a531/round2c/functional')
logs = [w / 'full-gates-m.log', w / 'full-gates-a531k.log']
start = sum(p.read_text().count('DONE') for p in logs)
deadline = time.time() + float(sys.argv[1])
while time.time() < deadline and sum(p.read_text().count('DONE') for p in logs) == start:
    time.sleep(10)
for p in logs:
    print(p.name, '|', ' / '.join(p.read_text().splitlines()[-2:]))
    rc = p.with_suffix('.rc')
    if rc.exists(): print('  DRIVER RC', rc.read_text().strip())
s = w / 'merged-gates-m/sweep-0.log'
if s.exists():
    print('sweep-0 suites done', len([l for l in s.read_text().splitlines() if re.match(r'^(PASS|FAIL|TIMEOUT)\s', l)]))
