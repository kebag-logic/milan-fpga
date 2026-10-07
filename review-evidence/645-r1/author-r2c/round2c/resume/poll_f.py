import sys, time, re
from pathlib import Path
w = Path('$VALIDATION_STORAGE/645-a531/round2c')
logs = [w / 'functional/full-gates-f.log', w / 'tf/run-timing.log']
start = sum(p.read_text().count('DONE') for p in logs)
deadline = time.time() + float(sys.argv[1])
while time.time() < deadline and sum(p.read_text().count('DONE') for p in logs) == start and not (w / 'tf/run-timing.rc').exists():
    time.sleep(10)
for p in logs:
    lines = p.read_text().splitlines()
    print(p.name, '|', ' / '.join(l[11:] for l in lines[-3:]))
for rc in [w / 'functional/full-gates-f.rc', w / 'tf/run-timing.rc']:
    if rc.exists(): print(rc.name, rc.read_text().strip())
s = w / 'functional/merged-gates-f/sweep-0.log'
if s.exists(): print('sweep-0', len([l for l in s.read_text().splitlines() if re.match(r'^(PASS|FAIL|TIMEOUT)\s', l)]), 'suites')
cg = Path('/sys/fs/cgroup') / open('/proc/self/cgroup').read().strip().split('::', 1)[1].lstrip('/')
print('mem', int((cg / 'memory.current').read_text()) // 10**6, 'MB; peak', int((cg / 'memory.peak').read_text()) // 10**6, 'MB')
