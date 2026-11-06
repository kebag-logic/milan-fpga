#!/usr/bin/env python3
"""readme_arm_audit.py <README.md> <camp-srp.log>: compare the failing-check count the README records for each
arm with the failures= the campaign measured for that arm, summed over the suites the arm ran in. Prints every
arm the README names with a count, and exits 1 on any arm whose recorded count differs from the measured one."""
import collections
import re
import sys


def measured(log):
    arms = collections.defaultdict(list)
    for line in open(log):
        m = re.match(r'([A-Za-z0-9][A-Za-z0-9-]*): rc=\d+ failures=(\d+) KILLED', line)
        if m:
            arms[m.group(1)].append(int(m.group(2)))
    return arms


def recorded(readme):
    """Yield (arm, [counts], row): a bare integer cell, or the '(n)' figures of a per-suite cell."""
    for line in open(readme):
        if not line.startswith('| `'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        name = re.match(r'`([A-Za-z0-9][A-Za-z0-9-]*)`', cells[0])
        if not name:
            continue
        counts = [int(c) for c in cells[1:] if re.fullmatch(r'\d+', c)]
        if not counts:
            counts = [int(n) for c in cells[1:] for n in re.findall(r'\((\d+)\)', c)]
        yield name.group(1), counts, line


def main():
    arms = measured(sys.argv[2])
    seen = bad = 0
    rows = collections.defaultdict(list)
    for arm, counts, _ in recorded(sys.argv[1]):
        if arm in arms and counts:
            rows[arm].extend(counts)
    for arm, counts in sorted(rows.items()):
        seen += 1
        have, want = sorted(counts), sorted(arms[arm])
        if sum(have) != sum(want) and not set(have) <= set(want):
            bad += 1
            print(f'DIFFERS {arm}: README {have} campaign {want}')
    print(f'{seen} arms with a README count of {len(arms)} measured; {bad} differ')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
