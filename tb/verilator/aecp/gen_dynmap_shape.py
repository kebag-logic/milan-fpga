#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_dynmap_shape.py - emit the dynamic-audio-map TB shape svh (gaps item 8).

Builds the builtin (deployed) spec with STREAM_PORT_INPUT[0] switched to
map_mode "dynamic" (its AUDIO_MAP descriptor dropped, number_of_maps=0 per
1722.1-2021 7.2.13) while STREAM_PORT_OUTPUT[0] keeps its static map (the
Milan 5.4.2.27/28 NOT_SUPPORTED regression stays testable in the SAME
shape). map_page=4 over 8 cluster keys makes number_of_maps=2, so the
GET_AUDIO_MAP paging path is exercised for real. The svh crosses the
`AEM_DYNMAP gate the sim_dynmap harness exercises; the Makefile puts
<out-dir> FIRST on the Verilator include path so it shadows the tracked
deployed svh.

Usage: python3 gen_dynmap_shape.py <out-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))

import gen_aem_store as g  # noqa: E402

out = sys.argv[1]
spec = g.builtin_spec()
spec["ports_in"][0] = dict(clusters=8, base_cluster=0, maps=0, base_map=0,
                           map_mode="dynamic", map_page=4)
# output map is now AUDIO_MAP[0] (the input port's map no longer exists)
spec["ports_out"][0] = dict(clusters=8, base_cluster=8, maps=1, base_map=0)
spec["audio_maps"] = [[[0, ch, ch, 0] for ch in range(8)]]

M = g.build_model(spec)
dm = M["DYNMAP"]
assert dm["EMIT"], "dynamic input port must emit the AEM_DYNMAP block"
assert (dm["KEYS"], dm["PAGE"], dm["NMAPS"], dm["OUTROWS"]) == (8, 4, 2, 8)

os.makedirs(os.path.join(out, "gen"), exist_ok=True)
g.emit_svh(M, os.path.join(out, "gen", "aecp_aem_rom.svh"))
print(f"[gen_dynmap_shape] {len(M['directory'])} descriptors, "
      f"ROM {M['ROM_SIZE']} B, AEM_DYNMAP keys={dm['KEYS']} "
      f"page={dm['PAGE']} nmaps={dm['NMAPS']} -> {out}")
