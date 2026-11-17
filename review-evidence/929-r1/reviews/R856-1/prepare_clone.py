#!/usr/bin/env python3
"""Reproduce the disposable checkout setup from an exact-head source clone.
Usage: prepare_clone.py SOURCE DESTINATION_UNDER_PACKET_SCRATCH
"""
from pathlib import Path
import subprocess
import sys

source, dest = (Path(x).resolve() for x in sys.argv[1:])
head = '372556835d03b70134b2e76567b63b25c4cca005'
assert 'scratch' in dest.parts and not dest.exists()
subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', '--no-checkout', str(source), str(dest)], check=True)
subprocess.run(['git', '-C', str(dest), 'checkout', '--quiet', '--detach', head], check=True)
modules = ['third_party/verilog-axis', 'protocol-processor', 'gptp-processor',
           'third_party/lwSRP', 'third_party/tsn-c-stack']
cmd = ['git', '-C', str(dest)]
for name in modules:
    cmd += ['-c', f'submodule.{name}.url={source / name}']
cmd += ['-c', 'protocol.file.allow=always', 'submodule', 'update', '--init', '--jobs', '5', *modules]
subprocess.run(cmd, check=True)
