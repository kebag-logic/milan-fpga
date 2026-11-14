#!/usr/bin/env python3
"""Spot-check map-table plants at exact head in disposable copies.
usage: probe_plants.py REPO SCRATCH
Each row: a name, aecp_maps.c text, its replacement. Each copy runs the core arm (work mode, ASan) at 1x1/1if with
the map tests selected; a plant is caught when the arm exits non-zero. The repository is never written."""
import shutil, sys
from pathlib import Path
repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms, fw_gtest
from ctrl_build import Tree, STACK
PLACE = "return first < MAP_FIRSTS && channel < MAP_CHANNELS ? first * MAP_CHANNELS + channel : MAP_SLOTS;"
ROWS = [
    ("author:map-index-channel-dropped", "? first * MAP_CHANNELS + channel : MAP_SLOTS;", "? first * MAP_CHANNELS : MAP_SLOTS;"),
    ("author:map-domain-a-channel-wide", "return first < MAP_FIRSTS && channel < MAP_CHANNELS ?",
     "return first < MAP_FIRSTS && channel <= MAP_CHANNELS ?"),
    ("reviewer:first-range-unchecked", PLACE, "return channel < MAP_CHANNELS ? first * MAP_CHANNELS + channel : MAP_SLOTS;"),
    ("reviewer:range-check-after-geometry-dropped",
     "size_t s = legal(a, port, &e.rows[n].r) ? place(&e, &e.rows[n]) : MAP_SLOTS;",
     "size_t s = place(&e, &e.rows[n]); if (!legal(a, port, &e.rows[n].r)) s = MAP_SLOTS;"),
]
FILTER = "Core.*Map*:Core.Every*"
for name, old, new in ROWS:
    src = scratch / name.replace(":", "-")
    if src.exists():
        shutil.rmtree(src)
    shutil.copytree(repo / "sw/firmware/ctrl", src)
    p = src / "aecp/aecp_maps.c"
    t = p.read_text()
    assert t.count(old) == 1, name
    p.write_text(t.replace(old, new))
    tree = Tree(src, scratch / f"out-{src.name}", scratch / f"out-{src.name}" / "reuse",
                fw_gtest.Build(coverage=False, address_sanitizer=True, jobs=4), STACK.resolve())
    r = aecp_arms.core_arm(tree, repo / "configs/endstation_ax7101_1x1_tdm8.yaml", 1, "work", FILTER)
    failed = sorted({l.split("]")[1].split("(")[0].strip() for l in r.log.splitlines() if l.startswith("[  FAILED  ] Core.")})
    print(f"{name}: arm rc {r.rc} -> {'CAUGHT' if r.rc else 'SURVIVED'}; failing: {', '.join(failed) or 'none'}", flush=True)
