#!/usr/bin/env python3
"""Build an extra public-API probe against exact-head sources in a disposable directory."""
import argparse
from pathlib import Path
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
args = ap.parse_args()
repo, packet = args.repo.resolve(), args.packet.resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
from ctrl_build import Tree, PORTABLE, HOST, compile_c, sources, link, execute
tree = Tree(repo / 'sw/firmware/ctrl', packet / 'scratch/restart', packet / 'scratch/restart/reuse')
objs = compile_c(tree, sources(tree, PORTABLE + HOST) + [packet / 'scripts/restart_probe.c'], 'objects')
result = execute('restart', link(tree, 'restart_probe', objs))
print(result.log, end='')
raise SystemExit(result.rc)
