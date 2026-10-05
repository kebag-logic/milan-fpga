#!/usr/bin/env python3
"""Build and execute the reviewer's queue probe without editing the checkout."""
import argparse
from pathlib import Path
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
a = ap.parse_args()
sys.path.insert(0, str(a.repo.resolve() / 'sw/firmware/ctrl/test'))
import ctrl_build as b
tree = b.Tree(b.CTRL, a.packet.resolve() / 'scratch/queue-probe', a.packet.resolve() / 'scratch/reuse')
sources = b.sources(tree, b.PORTABLE + b.HOST) + [a.packet.resolve() / 'scripts/queue_probe.c']
objects = b.compile_c(tree, sources, 'objects')
exe = b.link(tree, 'probe', objects)
outcome = b.execute('queue', exe)
print(outcome.log, end='')
raise SystemExit(outcome.rc)
