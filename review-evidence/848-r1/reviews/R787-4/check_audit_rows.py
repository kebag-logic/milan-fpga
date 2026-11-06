#!/usr/bin/env python3
"""Independent read of the audit at the head: population, table arithmetic, and column shape."""
import re, subprocess, sys, collections
H = sys.argv[1]
text = subprocess.check_output(['git', 'show', H + ':docs/DOCUMENTATION_AUDIT.md']).decode()
names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', H]).decode().split('\n')
pop = {n for n in names if n and (n.endswith('.md') or re.search(r'(^|/)README[^/]*$', n))}
rows = []
for line in text.splitlines():
    m = re.match(r'\| \[([^\]]+)\]\(([^)]+)\) \| (.*)$', line)
    if m:
        cells = [c.strip() for c in re.split(r'(?<!\\)\|', m.group(3))]
        if len(cells) >= 8 and cells[0] and not cells[0].startswith(('on page', 're-verify')):
            rows.append((m.group(1).replace(' (historical)', ''), cells))
print('rows', len(rows), 'population', len(pop))
seen = {r[0] for r in rows}
print('in tree not on page', sorted(pop - seen)); print('on page not in tree', sorted(seen - pop))
print('duplicates', [k for k, v in collections.Counter(r[0] for r in rows).items() if v > 1])
print('cell counts', collections.Counter(len(r[1]) for r in rows))
print('status', dict(collections.Counter(r[1][3] for r in rows)))
lanes = collections.defaultdict(lambda: collections.Counter())
for p, c in rows:
    lanes[c[6]][c[3]] += 1; lanes[c[6]]['D0'] += c[5] == 'D0'; lanes[c[6]]['n'] += 1
for k in sorted(lanes):
    print(k, dict(lanes[k]))
print(re.findall(r'^\| (?:current|stale|superseded|obsolete|\*\*total\*\*) \|.*$', text, re.M))
print([l for l in text.splitlines() if re.match(r'\| (archive|design|findings|module READMEs|overview and guides|reference|repository contract|testing and CI) \|', l)])
print('findings rows', len(re.findall(r'^\| D0-\d+ \|', text, re.M)))
print('numeric-only inventory cells', sum(1 for _, c in rows if any(re.fullmatch(r'[\d,]+', x) for x in c)))
print('summary header Lines', bool(re.search(r'^\|.*\bLines\b.*\|$', text, re.M)))
