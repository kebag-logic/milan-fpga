#!/usr/bin/env python3
"""Reconstruct automatic merge trees and retained MAAP/counter inputs."""
from pathlib import Path
import subprocess
import sys
root = Path(sys.argv[1]).resolve()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root).decode().strip()
for merge in ('a7291311', 'b075a994', '313616d1'):
    parents = git('rev-list', '--parents', '-n', '1', merge).split()
    assert len(parents) == 3
    reconstructed = git('merge-tree', '--write-tree', parents[1], parents[2])
    expected = git('rev-parse', merge+'^{tree}')
    assert reconstructed == expected, (merge, reconstructed, expected)
    print('PASS automatic merge', parents[0], 'parents', *parents[1:], 'tree', expected)
paths = [
 'hdl/ieee1722/maap/KL_maap.sv', 'tb/verilator/maap/Makefile',
 'tb/verilator/maap/integration.mk', 'tb/verilator/maap/mutants.py',
 'tb/verilator/maap/sim_main.cpp', 'tb/verilator/maap/sim_integration.cpp',
 'docs/design/MAAP_FABRIC.md', 'hdl/ieee1722/maap/doc/KL_maap/KL_maap.md',
 'sw/firmware/ctrl/test/maap_differential.py', 'sw/firmware/ctrl/test/test_maap_differential.cpp',
 'syn/ooc/pp_resource_baseline.json',
]
for path in paths:
    old, new = [git('rev-parse', ref+':'+path) for ref in ('32582421', 'HEAD')]
    assert old == new, path
    print('PASS retained from 32582421', path, new)
path = 'hdl/milan/milan_datapath.sv'
diff = git('diff', '--unified=0', 'e81ce82f', 'HEAD', '--', path)
print('Datapath delta against imported dev:')
print(diff)
additions = [line for line in diff.splitlines() if line.startswith('+') and not line.startswith('+++')]
assert len(additions) == 4
assert any('.port_operational_i (eff_link_w)' in line for line in additions)
assert any('.realtime_ns_i     (ptp_now_w[31:0])' in line for line in additions)
print('PASS imported datapath counter wiring retained; only MAAP comment and two pins differ')
