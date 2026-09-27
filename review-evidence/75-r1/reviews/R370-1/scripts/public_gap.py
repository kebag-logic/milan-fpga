"""Infer, for each public cycle, how long the bound CRF stream was absent.

usage: public_gap.py <packet author dir>
The tap time origin is the first tapped record, so the capture span is
response_ns + observation_s. At 500 PDU/s (48 kHz, 96-sample interval, one
timestamp per PDU) a stream that never stopped would give span * 500 valid PDUs.
"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
for d in ('listener', 'talker'):
    for n in range(1, 6):
        a = json.loads((root / f'{d}-{n:03d}' / 'analysis.json').read_text())
        span = a['response_ns'] / 1e9 + a['observation_s']
        missing = span * 500 - a['valid_avtp']
        print(f'{d}-{n:03d}: span {span:.3f} s, valid PDUs {a["valid_avtp"]}, never-stopped expectation {span*500:.0f}, '
              f'absent {missing/500:.3f} s (disconnect response to reconnect response {(a["response_ns"]-a["disconnect_response_ns"])/1e9:.3f} s), '
              f'PDUs in last 0.5 s before CONNECT_RX command: {a["frames_last_half_second_disconnected"]}')
