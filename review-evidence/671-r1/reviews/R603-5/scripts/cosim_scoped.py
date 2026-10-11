#!/usr/bin/env python3
"""Keep the scoped co-simulation's generated outputs in packet scratch."""
import importlib.util
from pathlib import Path
import sys

root, scratch = map(Path, sys.argv[1:3])
path = root / 'tb/verilator/nvm_cosim/run_cases.py'
spec = importlib.util.spec_from_file_location('scoped_cosim', path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
module.BUILD = scratch / 'build'
module.RUNS = scratch / 'runs'
sys.argv = [str(path), '--jobs', '4', '--pool', '4']
sys.exit(module.main())
