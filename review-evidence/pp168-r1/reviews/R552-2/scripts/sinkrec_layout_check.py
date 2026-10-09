#!/usr/bin/env python3
"""Compare the F07.6 WaveDrom sink-record layout and its prose with the RTL struct.

Reads docs/architecture/07_memory_maps.md (the fig-07-sinkrec WaveDrom JSON and
the prose ranges) and hdl/acmp/pp_acmp_pkg.sv (acmp_rec_t), then checks:
  L1 total width 384 in both
  L2 every documented lane maps onto the struct field(s) occupying exactly that range
  L3 the prose ranges ([319:304] VLAN, [255:192] stream_id) match the struct
  L4 the prose flag order from bit 11 matches the struct's one-bit fields
Exit 0 only when every check holds.  usage: sinkrec_layout_check.py TREE
"""
import json
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1])
md = (tree / "docs/architecture/07_memory_maps.md").read_text()
pkg = (tree / "hdl/acmp/pp_acmp_pkg.sv").read_text()

blk = md.split('<a id="fig-07-sinkrec"></a>', 1)[1]
src = re.search(r"```wavedrom\n(.*?)```", blk, re.S).group(1)
lanes, lo = [], 0
for f in json.loads(src)["reg"]:
    lanes.append((lo + f["bits"] - 1, lo, f["name"]))
    lo += f["bits"]

body = re.search(r"typedef struct packed \{(.*?)\} acmp_rec_t;", pkg, re.S).group(1)
fields = []
for m in re.finditer(r"logic\s*(?:\[(\d+):0\])?\s+(\w+);\s*//\s*\[(\d+)(?::(\d+))?\]", body):
    w = int(m.group(1)) + 1 if m.group(1) else 1
    hi = int(m.group(3)); lo_ = int(m.group(4)) if m.group(4) else hi
    assert hi - lo_ + 1 == w, m.group(0)
    fields.append((hi, lo_, m.group(2)))
fields.sort(key=lambda t: t[1])

ok = True
def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok &= bool(cond)

check(lo == 384 and sum(h - l + 1 for h, l, _ in fields) == 384,
      f"L1 width doc={lo} rtl={sum(h - l + 1 for h, l, _ in fields)}")
for hi, l, name in lanes:
    covered = [f for f in fields if f[1] >= l and f[0] <= hi]
    exact = covered and min(c[1] for c in covered) == l and max(c[0] for c in covered) == hi \
        and sum(c[0] - c[1] + 1 for c in covered) == hi - l + 1
    check(exact, f"L2 doc [{hi}:{l}] {name!r} -> rtl {[c[2] for c in covered]}")
rng = {n: (h, l) for h, l, n in fields}
check(rng["settled_vlan"] == (319, 304) and "occupies bits [319:304]" in md,
      f"L3 settled_vlan rtl {rng['settled_vlan']} vs prose [319:304]")
check(rng["settled_stream_id"] == (255, 192) and "word at [255:192]" in md,
      f"L3 settled_stream_id rtl {rng['settled_stream_id']} vs prose [255:192]")
order = [n for h, l, n in fields if 11 <= l <= 18]
want = ["f_bound", "f_started", "f_sw", "f_retried", "f_srp_decl", "f_tk_reg", "f_tk_disc"]
check(order == want and "runs from bit 11 upward as bound, started, saved STREAMING_WAIT,\n"
      "retried, srp_decl[1:0], tk_reg and tk_disc" in md, f"L4 flag order rtl {order}")
sys.exit(0 if ok else 1)
