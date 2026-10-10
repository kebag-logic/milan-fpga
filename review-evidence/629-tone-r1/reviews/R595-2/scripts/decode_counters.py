#!/usr/bin/env python3
"""Decode STREAM_INPUT GET_COUNTERS payloads from a lane events.jsonl (1722.1-2021 Table 7-157 bit order).
usage: decode_counters.py <events.jsonl> ..."""
import json, struct, sys
NAMES = {0: 'MEDIA_LOCKED', 1: 'MEDIA_UNLOCKED', 2: 'STREAM_INTERRUPTED', 3: 'SEQ_NUM_MISMATCH', 4: 'MEDIA_RESET',
         5: 'TIMESTAMP_UNCERTAIN', 6: 'TIMESTAMP_VALID', 7: 'TIMESTAMP_NOT_VALID', 8: 'UNSUPPORTED_FORMAT',
         9: 'LATE_TIMESTAMP', 10: 'EARLY_TIMESTAMP', 11: 'FRAMES_RX'}
for path in sys.argv[1:]:
    rows = {}
    for line in open(path):
        e = json.loads(line)
        if e.get('kind') == 'counters' and e.get('who') == 'dut':
            p = bytes.fromhex(e['payload'])
            dt, idx, valid = struct.unpack('>HHI', p[:8])
            c = struct.unpack('>32I', p[8:8 + 128])
            rows[e['tag']] = {NAMES[i]: c[i] for i in NAMES if valid >> i & 1}
            print(path, e['tag'], hex(valid), rows[e['tag']])
    if 'before' in rows and 'after' in rows:
        print(path, 'delta', {k: rows['after'][k] - rows['before'][k] for k in rows['after']})
