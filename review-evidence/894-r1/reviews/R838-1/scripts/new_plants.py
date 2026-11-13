"""Reviewer helper: the plants of the lane's plant tables that are new or changed between the base and the head.
usage: python3 -I new_plants.py <repo-root> <base-copies-dir>"""
import importlib.util, sys
from pathlib import Path
root, base = Path(sys.argv[1]), Path(sys.argv[2])
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m); return m
rec = lambda *a, **k: (a, tuple(sorted(k.items())))
out = {}
for mod, fn in (('loop_step_mutants', 'mutants'), ('srp_transmit_mutants', 'defects'), ('aecp_fan_mutants', None)):
    h = load(root / f'sw/firmware/ctrl/test/{mod}.py', 'h_' + mod); b = load(base / f'{mod}.py', 'b_' + mod)
    hs = getattr(h, fn)(rec) if fn else h.ROWS; bs = getattr(b, fn)(rec) if fn else b.ROWS
    key = (lambda t: t[0][0]) if fn else (lambda t: t[0])
    bmap = {key(t): t for t in bs}
    new = [key(t) for t in hs if key(t) not in bmap]
    changed = [key(t) for t in hs if key(t) in bmap and bmap[key(t)] != t]
    gone = [k for k in bmap if k not in {key(t) for t in hs}]
    print(f'{mod}: head {len(hs)} base {len(bs)} new {len(new)} changed {len(changed)} removed {len(gone)}')
    print('  new:', ' '.join(new)); print('  changed:', ' '.join(changed)); print('  removed:', ' '.join(gone))
