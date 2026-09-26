#!/usr/bin/env python3
"""Compare the three 04-pp_top.sh logs: (a) per-build warning sets, C++ compiler
(' warning:') separately from Verilator lint (%Warning-), Verilator entries
normalised by dropping line:col (the header grew by 3 lines at base->r2); (b) the
simulation transcripts (everything the two binaries print) r2 vs head and base vs
head, so 'no behaviour change' is shown on the full output, not only the tally."""
import re
from pathlib import Path
PK = Path(__file__).resolve().parents[1]
def split(rev):
    """(default build lines, default sim lines, fixture build lines, fixture sim lines),
    cut at the two `verilator --cc --exe --build` invocations and the two binaries;
    the scratch path of the revision is normalised so r2/head can be compared."""
    L = [l.replace(f"scratch/{rev}/", "scratch/REV/") for l in (PK / f"receipts/04-{rev}-run.log").read_text().splitlines()]
    v = [i for i, l in enumerate(L) if l.startswith("verilator --cc --exe --build")]
    assert len(v) == 2, v
    i_dr, i_fr = L.index("./obj_dir/Vpp_top_sim"), L.index("./obj_vid/Vpp_top_vid")
    return L[v[0]:i_dr], L[i_dr + 1:v[1]], L[v[1]:i_fr], L[i_fr + 1:]
norm = lambda l: re.sub(r"(\.sv|\.cpp|\.h):\d+:\d+", r"\1:L:C", l)
data = {r: split(r) for r in ("base", "r2", "head")}
for r, (db, ds, fb, fs) in data.items():
    for name, b in (("default", db), ("fixture", fb)):
        cxx = [l for l in b if " warning:" in l]; vl = sorted({norm(l) for l in b if l.startswith("%Warning")})
        print(f"[{r}] {name} build: C++ compiler warnings {len(cxx)}; Verilator lint warning kinds {len(vl)}")
        for l in cxx: print("      C++:", l.replace(str(PK), "<packet>"))
vset = lambda r, k: sorted({norm(l) for l in data[r][k] if l.startswith("%Warning")})
for k, name in ((0, "default"), (2, "fixture")):
    print(f"Verilator lint set identical base/r2/head ({name}): {vset('base', k) == vset('r2', k) == vset('head', k)}")
    print(f"   {name} set: {[l.split(':')[0] + ' ' + l.split(': ', 2)[-1][:70] for l in vset('head', k)]}")
for k, name in ((1, "default"), (3, "fixture")):
    a, b, h = data["base"][k], data["r2"][k], data["head"][k]
    print(f"simulation transcript ({name}): r2 == head byte-identical: {b == h} ({len(h)} lines)")
    extra = [l for l in h if l not in a]; missing = [l for l in a if l not in h]
    print(f"   base -> head: {len(extra)} lines only at head (NW prefix {sum(l.startswith('NW') for l in extra)}; others: {[l for l in extra if not l.startswith('NW')][:4]}), "
          f"{len(missing)} lines only at base: {missing[:4]}")
for r in ("base", "head"):
    print(f"--- {r} default simulation transcript:"); [print("   ", l) for l in data[r][1]]
    print(f"--- {r} fixture simulation transcript:"); [print("   ", l) for l in data[r][3]]
