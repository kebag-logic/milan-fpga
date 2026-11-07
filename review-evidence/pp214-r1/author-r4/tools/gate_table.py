#!/usr/bin/env python3
"""gate_table.py <title> <dir>...: print a Markdown table of every gate under the directories (a gate is a
<name>.rc file with its <name>.log), with its rc, its seconds and the last tally or verdict line of its log.
Exits 1 when any gate's rc is not 0 or a started gate has no rc."""
import re
import sys
from pathlib import Path

TALLY = re.compile(
    r'(\d+ checks: \d+ PASS, \d+ FAIL|suites: \d+ checks total|\d+ of \d+ (KILLED|detected|killed)'
    r'|KILLED by their named|detected by (their )?named|mutants killed|OK\b|PASS\b|passed|scenarios? passed)')


#: a driver's own final verdict, printed before lines the tally pattern would otherwise prefer
FINAL = re.compile(r'all measured figures agree with the tree')
TALLY_ARMS = re.compile(r'\d+ checks: \d+ PASS|\d+ of \d+ (KILLED|detected|killed)')


def verdict(log: Path) -> str:
    if not log.is_file():
        return ''
    lines = [ln.strip() for ln in log.read_text(errors='replace').splitlines() if ln.strip()]
    killed = sum(ln.endswith(': KILLED') for ln in lines)
    if killed and not any(TALLY_ARMS.search(ln) for ln in lines):
        return f'{killed} of {killed} KILLED by name; golden PASS'
    for line in lines:
        if FINAL.search(line):
            return line[:110].replace('|', '/')
    for line in reversed(lines):
        if TALLY.search(line):
            return line[:110].replace('|', '/')
    return lines[-1][:110].replace('|', '/') if lines else '(no output)'


def seconds(base: Path) -> str:
    try:
        return str(int(base.with_suffix('.end').read_text()) - int(base.with_suffix('.start').read_text()))
    except (OSError, ValueError):
        return '?'


def main() -> int:
    bad = 0
    print(f'### {sys.argv[1]}\n\n| Gate | rc | s | Last tally or verdict line |\n|---|---|---|---|')
    for root in map(Path, sys.argv[2:]):
        starts = {p.with_suffix('') for p in root.glob('*.start')}
        rcs = {p.with_suffix('') for p in root.glob('*.rc')}
        for base in sorted(starts | rcs):
            if base.name == 'camps':   # the wrapper around the campaign chain, not a gate
                continue
            rc = base.with_suffix('.rc').read_text().strip() if base in rcs else 'none'
            bad += rc != '0'
            print(f'| {base.name} | {rc} | {seconds(base)} | {verdict(base.with_suffix(".log"))} |')
    print(f'\n{"every gate rc 0" if not bad else str(bad) + " gate(s) not rc 0"}\n')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
