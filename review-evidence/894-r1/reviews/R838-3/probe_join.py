#!/usr/bin/env python3
"""Execute the focused join-gate controls and the old-horizon mutation."""
import sys
from pathlib import Path
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import selftest
import selftest_polls
import mrpdu_grade

def checks():
    return selftest_polls.join_checks(selftest.synthetic, selftest.SYS_HZ,
                                     selftest.CPU_HZ, selftest.tx_record)

baseline = checks()
for name, ok, detail in baseline:
    print(('PASS ' if ok else 'FAIL ') + name)
    print(detail)
original = mrpdu_grade.resolve
with patch.object(mrpdu_grade, 'resolve', lambda log, entry: original(log, entry) if any(
        entry < c < entry + log.sys_hz // 10 for c, n in log.entries if n == mrpdu_grade.BUILD)
        else ('empty', [])):
    failures = [name for name, ok, _ in checks() if not ok]
print('Old-horizon mutant failures:', failures)
raise SystemExit(not all(ok for _, ok, _ in baseline) or not failures)
