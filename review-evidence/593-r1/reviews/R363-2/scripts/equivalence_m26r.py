#!/usr/bin/env python3
"""Verdict-equivalence grid for R1-M26r. Usage: equivalence_m26r.py <head planner> <R1-M26r planner copy>"""
import importlib.util, itertools, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

head, mutant = load(sys.argv[1], "head"), load(sys.argv[2], "mutant")
diff = n = 0
for clear in (0.2, 0.25, 0.3, 0.6):
    for gms in itertools.product([-0.002, -0.001, 0, 0.1, 0.2, 0.25, 0.3, 0.6, 1.0], repeat=2):
        for disc in ([], [0], [0.1]):
            args = dict(intervals_s=[(0, clear), (1.0, 1.3)], discontinuities_s=disc, gm_changes_s=list(gms),
                        observation_resolution_s=0.001, capture_complete=True)
            n += 1
            diff += head.check_release_tu_history(**args)[0] != mutant.check_release_tu_history(**args)[0]
print(f"R1-M26r verdict-equivalence grid: {n} inputs, {diff} verdict differences")
