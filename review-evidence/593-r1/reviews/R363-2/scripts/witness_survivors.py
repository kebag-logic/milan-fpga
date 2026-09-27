#!/usr/bin/env python3
"""Witness inputs whose verdict differs between the head planner and the two surviving
reviewer mutants (M01, M04). Usage: witness_survivors.py <head torture_campaign.py> <M01 copy> <M04 copy>"""
import importlib.util, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

head, m01, m04 = (load(p, f"w{i}") for i, p in enumerate(sys.argv[1:4]))
w1 = dict(intervals_s=[(0, 0.2)], discontinuities_s=[0], gm_changes_s=[-0.0005],
          observation_resolution_s=0.001, capture_complete=True)
w4 = dict(intervals_s=[(0, 0.3), (0.3, 0.6)], discontinuities_s=[0, 0.3], gm_changes_s=[0],
          observation_resolution_s=0.001, capture_complete=True)
for label, mod, args in (("M01 witness: GM 0.5 ms before rise, PHC at rise, tu held 0.2 s", m01, w1),
                         ("M04 witness: touching intervals (0,0.3),(0.3,0.6)", m04, w4)):
    h = head.check_release_tu_history(**args)[0]
    m = mod.check_release_tu_history(**args)[0]
    print(f"{label}: head={h} mutant={m} {'DIFFERS' if h != m else 'SAME'}")
