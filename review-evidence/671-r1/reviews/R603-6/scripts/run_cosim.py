#!/usr/bin/env python3
"""Run the two shipping co-simulation shapes, placing products in scratch."""
import os
from pathlib import Path
import sys
root, packet, compiler = map(Path, sys.argv[1:4])
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['TMPDIR'] = str(packet / 'scratch')
os.environ['PATH'] = str(compiler.parent) + os.pathsep + os.environ['PATH']
sys.path.insert(0, str(root / 'tb/verilator/nvm_cosim'))
import run_cases as suite
suite.BUILD = packet / 'scratch/cosim-build'
suite.RUNS = packet / 'scratch/cosim-runs'
sys.argv = ['run_cases.py', '--shapes', '1x1,8x8', '--jobs', '8', '--pool', '4', '--skip-mutants']
sys.exit(suite.main())
