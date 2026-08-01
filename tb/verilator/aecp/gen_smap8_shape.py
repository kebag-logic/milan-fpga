#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_smap8_shape.py - emit an 8x8 shape whose listener ports keep STATIC maps.

WHY THIS EXISTS.  sim_amap.cpp is the wire witness for defect A: the static
GET_AUDIO_MAP serving table must address each port's OWN base_map descriptor,
with that descriptor's OWN number_of_mappings and its OWN mappings_offset,
rather than a hardcoded index/length that only happened to be right at 1x1.
Proving that needs a shape with MANY statically-mapped ports of DIFFERENT
sizes - and it used to get one by compiling against
configs/generated/endstation_ax7101_8x8, the shipped config.

That coupling broke the moment roadmap 23 made every shipped listener
map_mode dynamic (Milan v1.2 5.3.3.9): a dynamic port carries no AUDIO_MAP at
all, so the shipped 8x8 stopped being able to witness static serving, and
sim_amap's assertions started describing a shape that no longer exists.

The static multi-port path is STILL LIVE RTL - `AEM_SMAP_IN_*` serves any
config that keeps static listeners, and a mixed shape can have both - so the
coverage must not go away with the config that happened to exercise it. This
generator therefore builds the SAME 8x8 shape with `map_mode: static` forced
back on every listener, through the whole software-defined path (config ->
endstation_builder -> aem_overlay -> gen_aem_store), and sim_amap compiles
against that instead. The witness now depends on the RTL it is testing, not
on a product decision.

Usage: python3 gen_smap8_shape.py <out-dir>
"""
import copy
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))
sys.path.insert(0, os.path.join(ROOT, "sw", "builder"))

import gen_aem_store as g            # noqa: E402
import endstation_builder as eb      # noqa: E402
import yaml                          # noqa: E402

out = sys.argv[1]
os.makedirs(os.path.join(out, "gen"), exist_ok=True)

SRC = os.path.join(ROOT, "configs/endstation_ax7101_8x8.yaml")
with open(SRC) as f:
    cfg = copy.deepcopy(yaml.safe_load(f))

#: the ONE mutation: put EVERY port back on static maps. Everything else -
#: stream counts, formats, cluster policy, the CRF output - stays exactly as
#: the shipped 8x8 declares it, so the shape under test is the ship shape in
#: every respect that matters to the serving table. The talkers must revert
#: WITH the listeners (USER 08-01 made the shipped talkers dynamic too):
#: a static-input/dynamic-output half-revert is exactly the nonconformant
#: combination gen_aem_store's 5.3.3.9 guard refuses to build.
for s in (cfg["streams"]["listeners"] + cfg["streams"]["talkers"]):
    s.pop("map_mode", None)
    s.pop("map_page", None)

with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "endstation_ax7101_8x8_static.yaml")
    with open(p, "w") as f:
        yaml.safe_dump(cfg, f)
    res = eb.build(p, os.path.join(td, "out"))
    M = g.build_model(g.spec_from_overlay(res["overlay"]))

dm = M["DYNMAP"]
assert not dm["EMIT"], "the static 8x8 shape must NOT emit `AEM_DYNMAP"
sm = M["SMAP"]
assert sm["IN_N"] == 8 and sm["OUT_N"] == 8, (sm["IN_N"], sm["OUT_N"])
#: what the witness needs: every input port owns a map, and the ports do NOT
#: all share one descriptor address (that is the defect being fenced)
assert all(r > 0 for r in sm["IN_ROWS"]), sm["IN_ROWS"]
assert len(set(sm["IN_ADDR"])) == 8, sm["IN_ADDR"]

g.emit_svh(M, os.path.join(out, "gen", "aecp_aem_rom.svh"))
print(f"[gen_smap8_shape] {len(M['directory'])} descriptors, "
      f"ROM {M['ROM_SIZE']} B, 8 static input ports + 8 output ports, "
      f"rows in={sm['IN_ROWS']} -> {out}")
