#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_dynmap2_shape.py - emit the MULTI-PORT dynamic-audio-map TB shape svh.

Roadmap 23: Milan v1.2 5.3.3.9 makes dynamic mappings a shall on EVERY
Stream Port Input ("The Stream Port Input of a Configuration shall not
contain any AUDIO_MAP descriptor. Note: this means that a PAAD-AE
implements dynamic mappings on all of its Stream Port Inputs"), so the
engine has to survive more than one port. This shape is the NxN listener
shape in miniature:

  STREAM_INPUT   0 = AAF "Stream 1"    STREAM_PORT_INPUT 0: 8 clusters,
  STREAM_INPUT   1 = AAF "Stream 2"      base_cluster 0, map_mode dynamic
  STREAM_INPUT   2 = CRF (unmappable)  STREAM_PORT_INPUT 1: 8 clusters,
  STREAM_OUTPUT  0 = AAF talker          base_cluster 8, map_mode dynamic
                                       STREAM_PORT_OUTPUT 0: static map

map_page 4 over 8 clusters per port makes number_of_maps=2 on both ports, so
paging is exercised on a port whose keys do NOT start at 0. 16 keys against a
render crossbar 10 deep also puts keys 10..15 out of PHYSICAL reach, which is
how this shape exercises the 7.4.45.1 vendor reachability refusal. Three AAF/CRF
stream inputs also cross the per-stream-format gate, so the shape carries
`AEM_PER_STREAM_FMT AND `AEM_DYNMAP together - the combination a real 4x4 or
8x8 build compiles.

Usage: python3 gen_dynmap2_shape.py <out-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))

import gen_aem_store as g  # noqa: E402

out = sys.argv[1]
spec = g.builtin_spec()

# second AAF listener sink, inserted BEFORE the CRF sink
second = dict(spec["stream_inputs"][0])
second["name"] = "Stream 2"
spec["stream_inputs"].insert(1, second)
spec["clock_sources"][2]["loc_index"] = 2      # CRF sink moved to input 2

# two dynamic input ports, 4 mono clusters each; the output port keeps its
# static AUDIO_MAP so the 5.4.2.26-28 NOT_SUPPORTED path stays in-shape
spec["ports_in"] = [
    dict(clusters=8, base_cluster=0, maps=0, base_map=0,
         map_mode="dynamic", map_page=4),
    dict(clusters=8, base_cluster=8, maps=0, base_map=0,
         map_mode="dynamic", map_page=4),
]
spec["ports_out"] = [dict(clusters=8, base_cluster=16, maps=1, base_map=0)]
spec["audio_maps"] = [[[0, ch, ch, 0] for ch in range(8)]]
#: D10: one name per cluster, in global descriptor-index order
spec["cluster_names_in"] = [f"Render {n}" for n in range(16)]
spec["cluster_names_out"] = [f"Capture {n}" for n in range(8)]

M = g.build_model(spec)
dm = M["DYNMAP"]
assert dm["EMIT"], "dynamic input ports must emit the AEM_DYNMAP block"
assert M["PER_STREAM"]["EMIT"], "3 stream inputs must emit per-stream tables"
assert (dm["KEYS"], dm["PAGE"], dm["NPORTS"]) == (16, 4, 2)
assert dm["PDYN"] == [True, True]
assert dm["PBASE"] == [0, 8]
assert dm["PCLS"] == [8, 8]
assert dm["PNMAPS"] == [2, 2]
#: 16 declared keys against a render crossbar 10 deep: keys 10..15 (port 1
#: offsets 2..7) are model-only, which is what makes the 7.4.45.1 vendor
#: physical-reachability refusal reachable in THIS shape.
assert dm["PHYS"] == 10 and dm["KEYS"] > dm["PHYS"]
assert (dm["NSTRIN"], dm["SAAF"], dm["SCH"]) == (3, [True, True, False],
                                                 [2, 2, 0])

os.makedirs(os.path.join(out, "gen"), exist_ok=True)
g.emit_svh(M, os.path.join(out, "gen", "aecp_aem_rom.svh"))
print(f"[gen_dynmap2_shape] {len(M['directory'])} descriptors, "
      f"ROM {M['ROM_SIZE']} B, AEM_DYNMAP keys={dm['KEYS']} "
      f"page={dm['PAGE']} ports={dm['PBASE']} -> {out}")
