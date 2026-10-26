"""Compare the README mutant table rows with the self-test's 'MUTANT caught' lines.
Usage: python3 -I table_vs_selftest.py README.md selftest.log"""
import re, sys
readme, log = (open(p).read() for p in sys.argv[1:3])
rows = {}
for line in readme.splitlines():
    m = re.match(r'^\| (.+?) \| (.+?) \|$', line)
    if m and ':' in m.group(1) and not m.group(1).startswith('---'):
        rows[m.group(1)] = m.group(2)
caught = {}
for line in log.splitlines():
    m = re.match(r'^MUTANT caught: (.+?): (.*)$', line)
    if m:
        # mutant names contain ': ' once (family: text); split after the second colon-space
        parts = line[len('MUTANT caught: '):].split(': ')
        name = ': '.join(parts[:2]); rest = ': '.join(parts[2:])
        caught[name] = rest
bad = 0
for name, rest in caught.items():
    want = rows.get(name)
    if want is None:
        print('NO ROW', name); bad += 1
    elif not rest.startswith(want.replace('`', '')) and not rest.replace('`', '').startswith(want.replace('`', '')):
        print('MISMATCH', name, '| table:', want, '| log:', rest[:200]); bad += 1
print(f'{len(caught)} caught lines, {len(rows)} candidate table rows, {bad} mismatches')
sys.exit(1 if bad else 0)
