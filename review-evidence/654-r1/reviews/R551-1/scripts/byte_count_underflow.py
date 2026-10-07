#!/usr/bin/env python3
"""Record whether nonzero fractional CLI byte counts reach setup."""
import contextlib
import io
import json
from pathlib import Path
import sys
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'sw/litex'))
import milan_soc

class SetupStarted(Exception):
    pass

rows = []
for token in ('0', '1e-12', '1e-400', '-1e-400'):
    stream = io.StringIO()
    argv = ['milan_soc.py', '--no-milan', '--sys-clk-freq=50000000', '--l2-bytes=' + token]
    with patch.object(sys, 'argv', argv), contextlib.redirect_stderr(stream), \
         patch.object(milan_soc.board_audio_routing, 'assert_front_end_routed', side_effect=SetupStarted):
        try:
            milan_soc.main()
        except SetupStarted:
            outcome = {'kind': 'setup_started'}
        except SystemExit as exc:
            outcome = {'kind': 'refused', 'rc': exc.code, 'reason': stream.getvalue().splitlines()[-1]}
        else:
            raise AssertionError('unexpected completion')
    rows.append({'token': token, 'parsed_float': repr(float(token)), **outcome})
assert rows[0]['kind'] == 'setup_started'
assert rows[1]['kind'] == 'refused'
print(json.dumps(rows, indent=2))
if any(row['kind'] != 'refused' for row in rows[2:]):
    print('FAIL: nonzero fractional byte count reached setup after float underflow')
    raise SystemExit(1)
print('PASS: underflowing byte counts refused')
