#!/usr/bin/env python3
"""Reviewer driver: run the checkout's nvm_split_target/run.py main with the
native model's make parallelism capped (build.JOBS), so concurrent campaigns
stay within the reviewer's job cap. Nothing else is changed.
Usage: run_point_jobs.py CLONE MAKE_JOBS -- run.py arguments..."""
import os
import sys
from pathlib import Path

clone, jobs = Path(sys.argv[1]).resolve(), int(sys.argv[2])
args = sys.argv[sys.argv.index('--') + 1:]
sys.path.insert(0, str(clone / 'tb/verilator/nvm_split_target'))
os.environ.setdefault('PYTHONHASHSEED', '0')
import run  # noqa: E402
run.build.JOBS = jobs
sys.exit(run.main(args))
