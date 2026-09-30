#!/usr/bin/env python3
"""Compare tb/adp_engine/README.md ledger failure counts ('| `arm` | suite | defect | N: ...')
with a campaign log's 'arm: rc=.. failures=N' lines.
usage: adp_ledger_vs_campaign.py <README.md> <campaign-log>"""
import re, sys
readme, log = open(sys.argv[1]).read(), open(sys.argv[2]).read()
ledger = {m.group(1): int(m.group(2)) for m in
          re.finditer(r"^\| `([a-z0-9-]+)` \|[^|]*\|[^|]*\| (\d+):", readme, re.M)}
bad = 0
for arm, n in re.findall(r"^([a-z0-9-]+): rc=\d+ failures=(\d+)", log, re.M):
    ok = ledger.get(arm) == int(n)
    bad |= not ok
    print(f"{'EQUAL ' if ok else 'DIFFER'} {arm} campaign={n} ledger={ledger.get(arm)}")
print("RESULT", "PASS" if not bad else "FAIL")
sys.exit(bad)
