#!/usr/bin/env python3
"""Focused reader, mutation and C-preprocessor checks; never edit source."""
import hashlib
import importlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
scratch = packet / 'scratch'
os.environ['TMPDIR'] = str(scratch)
tempfile.tempdir = str(scratch)
sys.path.insert(0, str(repo / 'sw/builder'))
gate = importlib.import_module('test_builder')
reader = gate._shapes_reader()
header = 'sw/firmware/ctrl/loop/ctrl_loop.h'
base, prior, head = ('854bd7236792ce1adbd10c43b13a6a5002ad3bb6',
    '66b4def34dcbc0d371ce4eb339d3d0226875befa',
    '58f7673b8c57a80230e716bc1774ff9cc2f71ddc')
def blob(rev, name):
    return subprocess.check_output(['git', '-C', str(repo), 'show', rev + ':' + name])
def chain(data):
    start = data.index(b'#if CTRL_LOOP_SHAPE(')
    end = data.index(b'\n#endif', start) + len(b'\n#endif\n')
    return data[start:end]

a, b = chain(blob(base, header)), chain(blob(head, header))
assert a == b and len(a.splitlines()) == 39
print('THE SHAPES: 39 byte-identical lines; sha256', hashlib.sha256(a).hexdigest())
assert blob(base, 'tb/verilator/ctrl_service_budget/shape_costs.py') == blob(head, 'tb/verilator/ctrl_service_budget/shape_costs.py')
for rev in (base, prior, head):
    try:
        table = reader.listed(blob(rev, header).decode())
    except ValueError as exc:
        assert rev == prior
        print(rev, 'EXPECTED REFUSAL', exc)
    else:
        assert rev != prior
        print(rev, 'READS', sorted(table), 'at(1)', reader.at(1, texts={header: blob(rev, header).decode()}))
assert reader.listed(blob(base, header).decode()) == reader.listed(blob(head, header).decode())
print('Unmutated gate reader:', sorted(gate._check_shapes_text()))

# Run the complete current gate with only the header input redirected to m1.
with tempfile.TemporaryDirectory(dir=scratch, prefix='reader-m1-') as work:
    planted = Path(work) / 'ctrl_loop.h'
    planted.write_bytes(blob(prior, header))
    original = gate.LOOP_HEADER
    gate.LOOP_HEADER = planted
    try:
        gate.test_host_profile_feeds_the_generators()
    except AssertionError as exc:
        assert 'shape_costs.py does not read THE SHAPES' in str(exc)
        print('m1 COMPLETE gate 41 KILLED:', exc)
    else:
        raise AssertionError('m1 survived gate 41')
    finally:
        gate.LOOP_HEADER = original

# Independent compiler matrix including near misses and bare header misuse.
with tempfile.TemporaryDirectory(dir=scratch, prefix='cpp-matrix-') as work:
    work = Path(work)
    contract = (repo / 'sw/firmware/ctrl/mbx/mbx_contract.h').read_text()
    count = 0
    for n_if in (1, 2):
        cp = work / 'contract.h'
        cp.write_text(contract.replace('#define MBX_N_IF 1u\n', f'#define MBX_N_IF {n_if}u\n'))
        for source, sink in ((1, 2), (2, 2), (9, 9), (1, 1), (2, 1)):
            for host in (False, True):
                cmd = ['cc', '-E', '-dM', '-x', 'c', '-include', str(cp),
                       f'-DCTRL_SRP_SOURCES={source}u', f'-DCTRL_SRP_SINKS={sink}u',
                       '-I' + str(repo / 'sw/firmware/ctrl/loop'),
                       '-I' + str(repo / 'sw/firmware/ctrl/mbx')]
                if host:
                    cmd.append('-DCTRL_HOST_PLATFORM')
                run = subprocess.run(cmd + ['-'], input=b'#include "ctrl_loop.h"\n', capture_output=True)
                shape = (n_if, source, sink)
                host_selected = host and shape == (1, 1, 2)
                accepted = host_selected or shape in table
                assert (run.returncode == 0) == accepted, (shape, host, run.stderr)
                macros = dict(re.findall(rb'^#define (CTRL_LOOP_\w+) (\d+)u$', run.stdout, re.M))
                if accepted:
                    expected = table[(1, 2, 2)] if host_selected else table[shape]
                    assert {name: int(macros[name.encode()]) for name in expected} == expected
                else:
                    assert b'THE SHAPES:' in run.stderr
                print('CPP', shape, 'host=', host, 'rc=', run.returncode, 'host_header=', b'#define CTRL_LOOP_HOST_H' in run.stdout)
                assert (b'#define CTRL_LOOP_HOST_H' in run.stdout) == host_selected
                count += 1
    direct = subprocess.run(['cc', '-E', '-x', 'c', '-'], input=('#include "' + str(repo / 'sw/firmware/ctrl/host/ctrl_loop_host.h') + '"\n').encode(), capture_output=True)
    assert direct.returncode != 0 and b'through ctrl_loop.h' in direct.stderr
    print('Direct host-header include: correctly REFUSED')
    print('Independent preprocessor points:', count)
print('RESULT: PASS')
