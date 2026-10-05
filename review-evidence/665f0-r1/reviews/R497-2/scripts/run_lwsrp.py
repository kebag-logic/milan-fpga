#!/usr/bin/env python3
"""Run the pinned library integration and both negative pin controls."""
import argparse
from pathlib import Path
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--packet', type=Path, required=True)
ap.add_argument('--lwsrp', type=Path, required=True)
args = ap.parse_args()
repo, packet = args.repo.resolve(), args.packet.resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / 'sw/firmware/ctrl/test'))
import ctrl_arms
import ctrl_mutants
from ctrl_build import Tree
tree = Tree(repo / 'sw/firmware/ctrl', packet / 'scratch/lwsrp-build', packet / 'scratch/lwsrp-reuse')
result = ctrl_arms.arm_lwsrp(tree, args.lwsrp.resolve())
print(result.log)
bad = ctrl_mutants.lwsrp_pin_arms(packet / 'scratch/lwsrp-controls', args.lwsrp.resolve())
raise SystemExit(int(result.rc != 0 or bad != 0))
