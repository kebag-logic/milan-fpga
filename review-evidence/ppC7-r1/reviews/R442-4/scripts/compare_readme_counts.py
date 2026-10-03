#!/usr/bin/env python3
"""Compare a campaign log's per-arm failure counts with a README record table.

Usage: compare_readme_counts.py README SECTION_HEADING_PREFIX LOG
The README table rows look like "| `arm` | ... | N: ..." (the last cell starts
with the count); the log lines look like "arm: rc=R failures=N ... KILLED".
Prints one line per arm and exits 1 on any mismatch or missing arm.
"""
import re
import sys

readme, heading, logpath = sys.argv[1:4]
text = open(readme).read()
log = open(logpath).read()
logarms = set(re.findall(r'^([A-Za-z0-9_.-]+): rc=', log, re.M))


def suffixed(base, suffix):
    """`a-b`, `-c`: the shortest dash-prefix of base that the log knows, plus suffix."""
    cuts = [i for i, ch in enumerate(base) if ch == '-'] + [len(base)]
    for i in cuts:
        if base[:i] + suffix in logarms:
            return base[:i] + suffix
    return base + suffix


start = text.index(heading)
nxt = re.search(r'^#{2,3} ', text[start + len(heading):], re.M)
section = text[start:start + len(heading) + (nxt.start() if nxt else len(text))]
expected = {}
for line in section.splitlines():
    if not line.startswith('| `'):
        continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    names = re.findall(r'`([A-Za-z0-9_.-]+)`', cells[0])
    m = re.match(r'^(?:the same )?(\d+)\b', cells[-1])
    if not names or not m:
        continue
    base = names[0]
    for name in names:
        # "`arm`, `-talker`": a leading dash names base + suffix
        expected[suffixed(base, name) if name.startswith('-') else name] = int(m.group(1))
got = {}
for m in re.finditer(r'^([A-Za-z0-9_.-]+): rc=-?\d+ failures=(\d+)\b.*?\b(KILLED|UNPROVEN|SURVIVED)\b',
                     log, re.M):
    got[m.group(1)] = (int(m.group(2)), m.group(3))
bad = 0
for arm, count in expected.items():
    g = got.get(arm)
    ok = g is not None and g[0] == count and g[1] == 'KILLED'
    bad += not ok
    print(f"{'OK' if ok else 'MISMATCH'} {arm} readme={count} log={g}")
extra = sorted(set(got) - set(expected))
print(f"README arms {len(expected)}, log arms {len(got)}, mismatches {bad}, "
      f"log arms not in README {extra}")
sys.exit(1 if bad or extra or not expected else 0)
