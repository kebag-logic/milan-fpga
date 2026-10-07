#!/usr/bin/env python3
"""Independent setup-boundary, invalid-count and test-failure probes."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'sw/litex'))
import milan_soc as soc
from litex.soc.cores.cpu.naxriscv import NaxRiscv
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv

class Boundary(Exception):
    pass

count = 0
with patch.object(NaxRiscv, 'args_fill', side_effect=Boundary), \
     patch.object(VexiiRiscv, 'args_fill', side_effect=Boundary), \
     patch.object(soc.alinx_ax7101, 'Platform', side_effect=Boundary), \
     patch.object(soc.board_audio_routing, 'assert_front_end_routed', side_effect=Boundary):
    for cpu in ('vexiiriscv', 'naxriscv'):
        for xlen in (32, 64):
            cases = [(v, 'whole number') for v in (-float('inf'), -0.5, 1e-12, 8192.5)]
            cases += [(1, 'without a data cache')] if cpu == 'vexiiriscv' else [(-0.0, 'keeps its nonzero default')]
            for value, reason in cases:
                try:
                    soc.MilanSoC(None, 50000000, cpu=cpu, xlen=xlen, with_milan=False, l2_bytes=value)
                except ValueError as exc:
                    assert reason in str(exc), str(exc)
                else:
                    raise AssertionError('invalid count accepted')
                print(json.dumps({'case': f'{cpu}-RV{xlen}-{value}', 'reason': reason, 'before_cpu_args_fill': True}))
                count += 1
    for argv, reason in ((['--l2-bytes=-inf'], 'whole number'),
                         (['--l2-bytes=1e309'], 'whole number'),
                         (['--l2-bytes=1e-12'], 'whole number'),
                         (['--l2-bytes=bad'], 'invalid float value'),
                         (['--with-fpu', '--board=arty'], 'floating-point hardware')):
        output = io.StringIO()
        with contextlib.redirect_stderr(output), patch.object(sys, 'argv', ['milan_soc.py', *argv]):
            try:
                soc.main()
            except SystemExit as exc:
                assert exc.code == 2, exc
            else:
                raise AssertionError('CLI accepted')
        assert reason in output.getvalue(), output.getvalue()
        assert 'Traceback' not in output.getvalue()
        print(json.dumps({'case': argv, 'reason': reason, 'before_platform': True, 'rc': 2}))
        count += 1

spec = importlib.util.spec_from_file_location('tested_bank', root / 'sw/builder/test_soc_options.py')
bank = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bank)
with tempfile.TemporaryDirectory() as tmp:
    try:
        bank._killed(lambda: bank._probe(Path(tmp), mutations=[
            ('\nimport math\n', '\nraise RuntimeError("planted probe transport failure")\nimport math\n')]), 'must not be killed')
    except RuntimeError as exc:
        assert 'planted probe transport failure' in str(exc)
        print('PASS: probe execution failure propagates; it cannot count as a killed control')
    else:
        raise AssertionError('probe failure masked')

print(f'PASS: {count} independent early-boundary cases')
