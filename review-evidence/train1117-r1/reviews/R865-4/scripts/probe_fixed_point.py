#!/usr/bin/env python3
"""Reviewer probe: the slice rule and the queued rule at 1x1/1if as a pair. For each (slice, queued) the tree could
state, the slice the slice rule chooses, the last row there and the bound the queued rule then rules. Usage:
probe_fixed_point.py <tree>  (edits that tree's ctrl_loop.h and restores its exact bytes)"""
import sys, re
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "tb/verilator/ctrl_service_budget"))
import rows_tiers as rt, queued_bound as qb
h = root / "sw/firmware/ctrl/loop/ctrl_loop.h"
orig = h.read_text()
blk = orig[orig.index("CTRL_LOOP_SHAPE(1u, 2u, 2u)"):]
def state(slice_us, queued):
    t = orig
    i = t.index("CTRL_LOOP_SHAPE(1u, 2u, 2u)")
    j = t.index("#elif", i)
    seg = t[i:j]
    seg = re.sub(r"#define CTRL_LOOP_SLICE_US \d+u", f"#define CTRL_LOOP_SLICE_US {slice_us}u", seg)
    seg = re.sub(r"#define CTRL_LOOP_QUEUED_MS \d+u", f"#define CTRL_LOOP_QUEUED_MS {queued}u", seg)
    h.write_text(t[:i] + seg + t[j:])
PAIRS = tuple(tuple(int(v) for v in a.split(",")) for a in sys.argv[2:]) or ((950, 130), (900, 140), (950, 140), (900, 130))
try:
  for s, q in PAIRS:
      state(s, q); us, m = rt.slice_choice(root)
      w_here = rt.solve('last', rt.point_inputs(root, '1x1/1if'), rt.BUILT)[0]
      state(us, q)
      w_chosen = rt.solve('last', rt.point_inputs(root, '1x1/1if'), rt.BUILT)[0]
      print(f"stated slice {s} queued {q}: last at stated {w_here:.2f} -> rules {qb.ruled(w_here)}; slice rule chooses {us} "
            f"(margin {m:.4f}); last there {w_chosen:.2f} -> rules {qb.ruled(w_chosen)}; ruled() {rt.ruled(root)}")
finally:
  h.write_text(orig)
