"""Arm A's groups at a point, split into N parts by simulated time (largest first, each to the lightest part); prints
part K's names, comma-separated. Run from the harness directory. usage: partition.py BUILD_DIR POINT K N K"""
import json, sys
import os
sys.path[:0] = [os.getcwd(), os.path.join(os.getcwd(), '../../../sw/mailbox')]
import run, scenario
build, point, k, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
spec = json.load(open(f'{build}/build.json'))
groups = sorted(run.all_groups(scenario.point(point, spec), spec), key=lambda g: (-g.sim_ms, g.name))
parts = [[0, []] for _ in range(n)]
for g in groups:
    lightest = min(parts, key=lambda p: p[0])
    lightest[0] += g.sim_ms
    lightest[1].append(g.name)
print(','.join(parts[k][1]))
