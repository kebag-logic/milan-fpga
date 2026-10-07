from pathlib import Path
import re, sys, time
w = Path(__file__).resolve().parents[1]
if len(sys.argv) > 1:
    time.sleep(float(sys.argv[1]))
cg = Path('/sys/fs/cgroup') / open('/proc/self/cgroup').read().strip().split('::', 1)[1].lstrip('/')
stat = dict(l.split() for l in (cg / 'memory.stat').read_text().splitlines())
print(time.strftime('%H:%M:%S'), 'memory.current', int((cg / 'memory.current').read_text()), 'anon', stat['anon'],
      'peak', (cg / 'memory.peak').read_text().strip() if (cg / 'memory.peak').exists() else '?')
for name, root in [('baseline', w / 'baseline'), ('candidate', w / 'candidate/campaigns')]:
    good = bad = 0
    for p in root.glob('*/b8_*_p*.rc'):
        log = p.with_suffix('.log')
        if log.exists() and p.read_text().strip() == '0' and 'RESULT: PASS' in log.read_text():
            good += 1
        else:
            bad += 1
    print(name, good, '/128', 'nonpass rc files', bad)
for f in ['resume/baseline-a531k.rc', 'resume/candidate-slow-a531k.rc', 'resume/candidate-fast-a531k.rc', 'functional/full-gates-a531k.rc']:
    p = w / f
    if p.exists():
        print(f, p.read_text().strip())
print((w / 'functional/full-gates-a531k.log').read_text()[-700:])
for n in ['sweep-0', 'physical']:
    p = w / 'functional/merged-gates-k' / (n + '.log')
    if p.exists():
        lines = p.read_text(errors='replace').splitlines()
        print(n, len([l for l in lines if re.match(r'^(PASS|FAIL|TIMEOUT)\s', l)]), 'suites done;', lines[-1][:150] if lines else '')
