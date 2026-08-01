#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_odmap_shape.py - emit the DYNAMIC-OUTPUT audio-map TB shape svh.

USER 08-01: "enable dynamic mapping on stream_output as well". Milan v1.2
5.3.3.9 leaves Stream Port Outputs free to be dynamic (no AUDIO_MAP), and
5.4.2.26-28 then make GET/ADD/REMOVE_AUDIO_MAPPINGS a SHALL on them. This
shape is the talker-side mirror of gen_dynmap2_shape:

  STREAM_INPUT   0 = AAF "Stream 1"     STREAM_PORT_INPUT 0/1: dynamic
  STREAM_INPUT   1 = AAF "Stream 2"       (the 5.3.3.9 shall; also arms
  STREAM_INPUT   2 = CRF (unmappable)      `AEM_DYNMAP, which `AEM_ODYNMAP
  STREAM_OUTPUT  0 = AAF talker (8ch)      builds on)
  STREAM_OUTPUT  1 = AAF talker (8ch)   STREAM_PORT_OUTPUT 0: 8 clusters,
                                          default ring sources, dynamic
                                        STREAM_PORT_OUTPUT 1: 9 clusters,
                                          EXPLICIT sources - 4 loopback
                                          (rx stream 1) + 4 ring + 1 mono
                                          pilot TONE - dynamic

Port 1's explicit cluster_sources exercise every template class the
capture crossbar knows: LOOP (idxh), RING, and the mono TONE cluster whose
pair maps BOTH stream channels to the same cluster. Port 0's default-policy
sources prove the generator's ring-identity fallback.

Usage: python3 gen_odmap_shape.py <out-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))

import gen_aem_store as g  # noqa: E402

out = sys.argv[1]
spec = g.builtin_spec()

# 48 kHz 8-channel concrete AAF (channels_per_frame field = 8) + the 2ch
# family member, so a SET_STREAM_FORMAT SHRINK (the output prune) is legal
AAF8 = 0x0205022002006000
AAF2 = 0x0205022000806000

# second AAF listener sink, inserted BEFORE the CRF sink (dynmap2 shape)
second = dict(spec["stream_inputs"][0])
second["name"] = "Stream 2"
spec["stream_inputs"].insert(1, second)
spec["clock_sources"][2]["loc_index"] = 2      # CRF sink moved to input 2

# second talker, both 8ch-first so SCH=8 and SLOTB={0,4}
spec["stream_outputs"] = [
    dict(name="Stream Output 0", formats=[AAF8, AAF2]),
    dict(name="Stream Output 1", formats=[AAF8, AAF2]),
]

spec["ports_in"] = [
    dict(clusters=8, base_cluster=0, maps=0, base_map=0,
         map_mode="dynamic", map_page=4),
    dict(clusters=8, base_cluster=8, maps=0, base_map=0,
         map_mode="dynamic", map_page=4),
]


def loop(idxh, idx, half):
    return dict(src=5, idxh=idxh, idx=idx, half=half, valid=True)


def ring(idx, half):
    return dict(src=3, idxh=0, idx=idx, half=half, valid=idx < 16)


TONE = dict(src=4, idxh=0, idx=0, half=0, valid=True)

spec["ports_out"] = [
    # default policy: the talker's own ring pairs (slot base 0 + c//2)
    dict(clusters=8, base_cluster=16, maps=0, base_map=0,
         map_mode="dynamic", stream_index=0),
    # explicit: loopback from rx stream 1 (pairs 0..1), ring pairs 6..7,
    # and the mono pilot tone at cluster offset 8
    dict(clusters=9, base_cluster=24, maps=0, base_map=0,
         map_mode="dynamic", stream_index=1,
         cluster_sources=[loop(1, 0, 0), loop(1, 0, 1),
                          loop(1, 1, 0), loop(1, 1, 1),
                          ring(6, 0), ring(6, 1), ring(7, 0), ring(7, 1),
                          TONE]),
]
spec["audio_maps"] = []            # fully dynamic: no AUDIO_MAP descriptors
spec["cluster_names_in"] = [f"Render {n}" for n in range(16)]
spec["cluster_names_out"] = ([f"Cap0 Host {n}" for n in range(8)]
                             + [f"Cap1 Loop {n}" for n in range(4)]
                             + [f"Cap1 Host {n}" for n in range(4)]
                             + ["Pilot Tone"])

M = g.build_model(spec)
dm, od = M["DYNMAP"], M["ODMAP"]
assert dm["EMIT"] and od["EMIT"], "both engines must emit"
assert (od["KEYS"], od["NPORTS"]) == (16, 2)
assert od["PDYN"] == [True, True]
assert od["PCLS"] == [8, 9] and od["PCBASE"] == [0, 8]
assert od["PSTR"] == [0, 1] and od["SLOTB"] == [0, 4]
assert od["SCH"] == [8, 8]
#: identity images: port 0 full 8 (ring); port 1 full 8 (loop+ring mix);
#: the pilot cluster (offset 8) is NOT part of any identity
assert all(e["v"] for e in od["INIT"]), od["INIT"]
assert [e["co"] for e in od["INIT"]] == list(range(8)) * 2

os.makedirs(os.path.join(out, "gen"), exist_ok=True)
g.emit_svh(M, os.path.join(out, "gen", "aecp_aem_rom.svh"))
print(f"[gen_odmap_shape] {len(M['directory'])} descriptors, "
      f"ROM {M['ROM_SIZE']} B, AEM_ODYNMAP keys={od['KEYS']} "
      f"ports={od['PCLS']} -> {out}")
