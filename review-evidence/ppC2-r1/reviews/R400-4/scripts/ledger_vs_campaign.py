#!/usr/bin/env python3
"""Compare tb/maap/README.md ledger 'N FAIL of M' per arm row with a campaign log's tallies.
usage: ledger_vs_campaign.py <README.md> <campaign-log>"""
import re, sys
readme, log = open(sys.argv[1]).read(), open(sys.argv[2]).read()
ledger = {}
prev = None
for line in readme.splitlines():
    line = line.replace("| (same arm) |", f"| `{prev}` |") if prev else line
    m = re.match(r"\| `([a-z0-9-]+)` \|(.*)\| (maap|rx_validator|pp_top[^|]*) \|(.*)\|\s*$", line)
    if not m:
        continue
    prev = m.group(1)
    tail = re.findall(r"(\d+) FAIL of ([\d,]+)", m.group(4))
    if tail:
        n, of = tail[-1]
        suite = "pp_top" if m.group(3).startswith("pp_top") else m.group(3)
        ledger[(m.group(1), suite)] = (int(of.replace(",", "")), int(n))
bad = 0
for label, suite, checks, fails in re.findall(r"^(\S+) \[(\w+)\]: rc=\d+ tally=\((\d+), (\d+)\)", log, re.M):
    want = ledger.get((label, suite))
    got = (int(checks), int(fails))
    ok = want == got
    bad |= not ok
    print(f"{'EQUAL ' if ok else 'DIFFER'} {label} [{suite}] campaign={got} ledger={want}")
print("RESULT", "PASS" if not bad else "FAIL")
sys.exit(bad)
