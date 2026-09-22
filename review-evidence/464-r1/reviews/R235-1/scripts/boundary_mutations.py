#!/usr/bin/env python3
"""R235 observe-only mutants: boundary TIGHTENING and bound SCOPE.

The PR claims each retained arm detects the LOSS of its bound; these plants
ask the different question of whether a stricter or narrower-scoped bound is
visible, to characterise (not grade) the self-test's boundary coverage.
Same mechanics as mutation_matrix.py: exact single-count edits in a minimal
tree (avdecc/ + hdl/common/csr/milan_csr.sv), Python 3.14 and 3.12.
Usage: boundary_mutations.py <head-extract> <work-root> <receipt-dir>
"""
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
from pathlib import Path

HEAD, WORK, OUT = (Path(a) for a in sys.argv[1:4])
PYS = ["/usr/bin/python3.14", str(Path.home() / ".local/bin/python3.12")]
MAPS = "avdecc/aem_maps.py"
B = [
    ("B1", "Table 7-32: a 62-mapping map now refused (> -> >=)",
     [(MAPS, "if len(rows) > SMAP_MAX_ROWS:", "if len(rows) >= SMAP_MAX_ROWS:")]),
    ("B2", "cluster_offset: last in-range offset refused",
     [(MAPS, 'if co >= port["clusters"]:', 'if co >= port["clusters"] - 1:')]),
    ("B3", "stream_index: last in-range stream refused",
     [(MAPS, "if si >= side.n_streams:", "if si >= side.n_streams - 1:")]),
    ("B4", "base_map: last defined AUDIO_MAP refused",
     [(MAPS, "if not 0 <= bm < len(maps):", "if not 0 <= bm < len(maps) - 1:")]),
    ("L1", "OUTPUT rule scoped per port, not across the Configuration",
     [(MAPS, "    cfg_stream_ch = {}\n    for k, p in enumerate(side.ports):\n",
       "    for k, p in enumerate(side.ports):\n        cfg_stream_ch = {}\n")]),
    ("L2", "INPUT rule scoped across all input ports instead of per map",
     [(MAPS, "        seen = set()\n", ""),
      (MAPS, "    cfg_stream_ch = {}\n", "    cfg_stream_ch = {}\n    seen = set()\n")]),
]


def one(mid, desc, edits):
    d = WORK / mid
    if d.exists():
        shutil.rmtree(d)
    shutil.copytree(HEAD / "avdecc", d / "avdecc")
    (d / "hdl/common/csr").mkdir(parents=True)
    shutil.copy2(HEAD / "hdl/common/csr/milan_csr.sv", d / "hdl/common/csr/milan_csr.sv")
    for f, old, new in edits:
        t = (d / f).read_text()
        if t.count(old) != 1:
            return f"{mid} INVALID {desc}: {t.count(old)} x {old!r}"
        (d / f).write_text(t.replace(old, new))
    rcs, first = [], ""
    for py in PYS:
        p = subprocess.run([py, "-B", "-E", "-s", "avdecc/gen_aem_store.py", "--self-test"],
                           cwd=d, capture_output=True, text=True,
                           env={"PATH": os.environ["PATH"], "HOME": os.environ["HOME"]})
        log = p.stdout + p.stderr
        (OUT / f"{mid}-{Path(py).name}.log").write_text(log)
        rcs.append(p.returncode)
        first = first or next((l.strip()[:150] for l in log.splitlines() if "[FAIL]" in l), "")
    det = "DETECTED" if all(rcs) else ("NOT-DETECTED" if not any(rcs) else "DISAGREE")
    return f"{mid} {det:13s} {desc}  rc={rcs}" + (f"\n     first FAIL: {first}" if first else "")


OUT.mkdir(parents=True, exist_ok=True)
WORK.mkdir(parents=True, exist_ok=True)
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    rows = list(ex.map(lambda b: one(*b), B))
text = "\n".join(rows) + "\n"
(OUT / "SUMMARY.txt").write_text(text)
print(text)
