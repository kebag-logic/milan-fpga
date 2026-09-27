#!/usr/bin/env python3
"""Show R3-21 (history positive-duration guard removed) is verdict-equivalent.
usage: r3_21_witness.py <planner.py>"""
import importlib.util, sys, tempfile
from pathlib import Path
text = Path(sys.argv[1]).read_text(encoding="utf-8")
old = "if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):"
new = "if (intervals and start_s <= intervals[-1][1]):"
assert text.count(old) == 1
def load(src, name):
    d = tempfile.mkdtemp(); p = Path(d) / f"{name}.py"; p.write_text(src, encoding="utf-8")
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); sys.modules[name] = m; s.loader.exec_module(m); return m
a, b = load(text, "pristine"), load(text.replace(old, new), "mutant")
cases = [([(0, 0)], [0], [0]), ([(0.3, 0.1)], [0.3], []), ([(0, 0.3), (0.4, 0.4)], [0, 0.4], [0]),
         ([(0, 0.3), (0.5, 0.45)], [0], []), ([(-1, -1)], [], [])]
diff = 0
for iv, ev, gm in cases:
    for r in (0, 0.001, 0.1):
        va = a.check_release_tu_history(iv, ev, gm_changes_s=gm, observation_resolution_s=r, capture_complete=True)[0]
        vb = b.check_release_tu_history(iv, ev, gm_changes_s=gm, observation_resolution_s=r, capture_complete=True)[0]
        print(f"{iv} R={r}: pristine={va} mutant={vb}"); diff += va != vb
print("verdict differences:", diff)
