#!/usr/bin/env python3
"""Build and run the extended boundary probe after run_review.py completes."""
from pathlib import Path
import os
import subprocess
import sys

p = Path(__file__).resolve().parents[1]
src = p / 'scratch/head'
original = (src / 'tb/verilator/parser/sim_main.cpp').read_text()
assert original.count(' private:') == 1
assert original.count('int main(int argc, char **argv)') == 1
modified = original.replace(' private:', ' public:').replace('int main(int argc, char **argv)', 'int original_main(int argc, char **argv)')
probe = src / 'tb/verilator/parser/review_edges.cpp'
probe.write_text(modified + '\n' + (p / 'scripts/edge_probe.cpp').read_text())
obj = p / 'scratch/edge-obj'
env = dict(os.environ, PATH=str(p / 'scratch/bin') + ':' + os.environ['PATH'], TMPDIR=str(p / 'scratch'))
logs = p / 'receipts/local'
cmd = ['verilator', '--cc', '--exe', '--build', '-j', '4', '--top-module', 'KL_gptp_rx_parser', '-Wall', '-Wno-fatal', '-Wno-DECLFILENAME', '-Wno-UNUSEDSIGNAL', '-Wno-WIDTHEXPAND', '-Wno-WIDTHTRUNC', '-Wno-UNUSEDPARAM', '--Mdir', str(obj), '-CFLAGS', '-std=c++17 -O2', str(src / 'hdl/ucpu/gptp_ucpu_pkg.sv'), str(src / 'hdl/wire/KL_gptp_rx_parser.sv'), str(probe), '-o', 'Vedges']
for tag, args in [('edges-build', cmd), ('edges', [str(obj / 'Vedges')])]:
    with (logs / (tag + '.log')).open('w') as out:
        rc = subprocess.run(args, cwd=src, env=env, stdout=out, stderr=subprocess.STDOUT).returncode
    (logs / (tag + '.rc')).write_text(str(rc) + '\n')
    if rc:
        print((logs / (tag + '.log')).read_text())
        sys.exit(rc)
print((logs / 'edges.log').read_text())
