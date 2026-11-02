#!/usr/bin/env python3
"""Print each mailbox channel's admission bucket (burst, refill period) from the contract the harness reads.

usage: contract_buckets.py <checkout root>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / 'tb/verilator/ctrl_service_budget'), str(root / 'sw/mailbox')]
import scenario  # noqa: E402

total = 0.0
for name, idx in scenario.CH.items():
    ch = scenario.CONTRACT.channels[idx]
    total += 1.0 / ch.refill_ms
    print(f'{name:5s} channel {idx}: burst {ch.burst}, one record per {ch.refill_ms} ms sustained, ring {ch.rx_words} words')
print(f'sustained admitted records over every channel: {total:.2f} a ms (buckets are per channel, KL_mbx_rx.sv:194-195)')
