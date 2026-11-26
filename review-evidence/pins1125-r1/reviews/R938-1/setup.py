#!/usr/bin/env python3
"""Create disposable, pinned checkouts below this packet's scratch directory."""
import pathlib
import subprocess
import sys

source = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(__file__).resolve().parent
target = packet / 'scratch' / 'probe'
def run(*args):
    subprocess.run(args, check=True)
run('git', 'clone', '--shared', '--no-checkout', str(source), str(target))
run('git', '-C', str(target), 'checkout', '--detach', 'a6864a49293ba3d0df37029abfa581468ef78dce')
paths = ['gptp-processor', 'protocol-processor', 'third_party/tsn-c-stack', 'third_party/verilog-axis', 'third_party/lwSRP']
for path in paths:
    run('git', '-C', str(target), 'config', 'submodule.' + path + '.url', str(source / path))
run('git', '-C', str(target), '-c', 'protocol.file.allow=always', 'submodule', 'update', '--init', *paths)
