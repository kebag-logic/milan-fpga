#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Reviewer probe: does the queued-builtins per-line oracle fire, and only there?

Usage: builtin_oracle_probe.py <repo-root>
Imports the committed tb/verilator/fw_service_budget/run.py and feeds its
service_findings() one serviced and one unserviced console-line row.
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/fw_service_budget"))
import run  # noqa: E402

raw = ('BACKING armed=1 unbacked_cycles=0\n'
       'PHY_TIMING transactions=8 publications=1 max_transaction_cycles=10 '
       'max_poll_cycles=90 down_edges=1 up_edges=1\n')
for plan in ("queued-builtins", "queued-short"):
    for ticks in (1, 0):
        row = dict(run.interval('', 1, 100_001, 500), period_bound_ms=260,
                   command_index=0, tick_calls=ticks)
        result = dict(rows=[row], media=dict(plan=plan), liveness=[dict(backed=1)])
        print(f"plan={plan} tick_calls={ticks} findings={run.service_findings(result, raw)}")
print("remove-dispatch verdict requires only:",
      "'continuous backing lost'" if "'continuous backing lost' in findings"
      in Path(run.__file__).read_text() else "UNKNOWN")
