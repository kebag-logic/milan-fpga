#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_pools_shape.py - emit the D8 ROLE-POOL TB shape svh.

Unlike the other TB shape generators this one goes through the WHOLE
software-defined path - config -> endstation_builder -> aem_overlay ->
gen_aem_store -> aecp_aem_rom.svh - because that path is exactly what D8
changed and a hand-written spec would prove nothing about it.

The shape is a 2x2 end-station on a board that routes NO audio pins
(`physical_channels: {capture: 0, render: 0}` - the AX7101 truth: its
platform ships `_connectors = []`, so milan_soc.py leaves i2s_pads = None,
drives i_i2s_sdout_i = 0 and ties the TDM pins off). Every talker port
therefore carries a pool of host + PILOT + LOOPBACK clusters and NO physical
ones, and its static AUDIO_MAP falls through to the LOOPBACK segment - the
case the AX actually needs.

Small on purpose (14 AUDIO_CLUSTERs, ~2.5 kB ROM): the point is the pool
STRUCTURE and the 1722.1-2021 7.2.19 port-relative offsets, not size.

What sim_pools.cpp then proves over the wire:
  * STREAM_PORT_OUTPUT number_of_clusters/base_cluster/number_of_maps/
    base_map (7.2.13 Table 7-23) match the emitted pool;
  * every AUDIO_CLUSTER object_name says what the cluster IS (7.2.16);
  * the AUDIO_MAP rows land INSIDE the loopback segment and are
    PORT-RELATIVE (7.2.19: "the offset from the base_cluster of the
    STREAM_PORT_INPUT or STREAM_PORT_OUTPUT") - the two talker ports carry
    IDENTICAL offsets pointing at DIFFERENT global clusters;
  * Milan 5.4.2.28: a port WITH an Audio Map answers ADD_AUDIO_MAPPINGS
    NOT_SUPPORTED (conformance, not a gap);
  * negative cases: descriptors past the end answer NO_SUCH_DESCRIPTOR.

Usage: python3 gen_pools_shape.py <out-dir>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))
sys.path.insert(0, os.path.join(ROOT, "sw", "builder"))

import gen_aem_store as g            # noqa: E402
import endstation_builder as eb      # noqa: E402
import yaml                          # noqa: E402

out = sys.argv[1]
os.makedirs(os.path.join(out, "gen"), exist_ok=True)

CFG = {
    "schema": "kebag-logic/milan-endstation-config",
    "schema_version": "1.1.0",
    "entity": {
        "name": "Milan FPGA Pools TB",
        "entity_model_id": "hash-derived",
        "entity_id": "mac-derived",
        "vendor_name": "Kebag Logic",
        # NO firmware_version: it is DERIVED from milan_csr's VERSION
        # parameter, and the builder REFUSES a declared one (a second
        # copy still needs an edit per ABI bump, which is how it stops
        # agreeing). See check_entity_shape.py arm G.
        "serial_number": "AX7101-0001",
        "group_name": "",
    },
    "board": {
        "target": "ax7101",
        "constraints": {
            "sys_clk_hz": 100000000, "milan_clk_hz": 100000000,
            "l2_bytes": 16384, "phy": "gmii-1g", "gtx_tx_invert": True,
            "floorplan": True, "flashboot": "full", "uart_baudrate": 115200,
            "rx_queues": 1, "hs_page_bytes": 16384, "strip_probes": True,
            "num_queues": 5, "eth_port": "e1",
        },
    },
    "srp": {"sr_class": "A", "vid": 2,
            "stream_dmac_base": "0x91E0F000FE01", "class_queue": 4,
            "bandwidth_limit_pct": 75,
            "tspec": {"policy": "derived", "interval_frames": 1}},
    "platform": {"csr_base": 0x90000000,
                 "mac_address": "02:00:00:00:00:01", "interrupt": 3,
                 # 2 capture streams x 1 MiB stride must fit the reserved
                 # ring (the builder refuses a shape that would DMA past the
                 # no-map region) - same arithmetic as the 8x8 config
                 "pcm_ring_phys": 0x7f800000,
                 "pcm_ring_bytes": 0x200000,
                 "pcm_ring_stride": 0x100000},
    "clocking": {
        "sampling_rate_hz": 48000, "audio_unit_rates_hz": [48000],
        "media_clock_sources": ["internal", "input_stream", "crf"],
        "default_source": "internal", "crf_sink": True,
        # Milan 7.2.3: >=2 AAF media inputs make a CRF Media Clock Output
        # mandatory, and the builder REFUSES the config without it.
        "crf_output": {"enabled": True, "format": "0x041060010000BB80"},
        "audio_pll_hz": 24576000,
    },
    "audio_interface": {
        "kind": "i2s_philips",
        "word_length_bits": 24,
        # the board routes nothing, in either direction (see the docstring)
        "physical_channels": {"capture": 0, "render": 0},
        "cluster_mapping": {
            "policy": "role-pools",
            "pools": {"host": 2, "pilot": True, "loopback": 2},
            # task #65: this harness exists to pin the POOLED ROM shape, and
            # the shape it pins is the loopback-primary one (talker maps at
            # offsets 3/4 below). A pool is only allowed to be the power-on
            # source when the build elaborates its fabric lane, so the shape
            # has to say so - which also makes this harness the end-to-end
            # proof that the declaration reaches the ROM.
            "fabric": {"loopback_lane": True},
        },
    },
    "streams": {
        "listeners": [
            {"name": "Stream In 0", "channels": 2,
             "formats": ["0x0205022000806000"]},
            {"name": "Stream In 1", "channels": 2,
             "formats": ["0x0205022000806000"]},
        ],
        "talkers": [
            {"name": "Stream Out 0", "channels": 2,
             "formats": ["0x0205022000806000"]},
            {"name": "Stream Out 1", "channels": 2,
             "formats": ["0x0205022000806000"]},
        ],
    },
}

cfg_path = os.path.join(out, "pools_tb.yaml")
with open(cfg_path, "w") as f:
    yaml.safe_dump(CFG, f)

cfg = eb.load_config(cfg_path)
ovl = eb.emit_aem_overlay(cfg)
M = g.build_model(g.spec_from_overlay(ovl))

# --- assertions on the SHAPE, so a silently different pool never reaches
#     the C harness pretending to be the one it checks -------------------
P_in = ovl["stream_ports"]["input"]
P_out = ovl["stream_ports"]["output"]
assert [p["clusters"] for p in P_in] == [2, 2], P_in
assert [p["clusters"] for p in P_out] == [5, 5], P_out
assert [p["base_cluster"] for p in P_in] == [0, 2], P_in
assert [p["base_cluster"] for p in P_out] == [4, 9], P_out
assert ovl["descriptor_counts"]["AUDIO_CLUSTER"] == 14
assert [g_["role"] for g_ in P_out[0]["pool"]] == ["host", "pilot", "loopback"]
assert all(p["primary_role"] == "host" for p in P_out), P_out  # USER 08-06: host outranks loopback
assert all(p["primary_role"] == "host" for p in P_in), P_in
names = [c["name"] for c in sorted(ovl["audio_clusters"],
                                   key=lambda c: c["index"])]
assert names == ["Host Play 0", "Host Play 1",
                 "Host Play 0", "Host Play 1",
                 "Host Cap 0", "Host Cap 1", "Pilot Tone",
                 "Loopback S0 ch 0", "Loopback S0 ch 1",
                 "Host Cap 0", "Host Cap 1", "Pilot Tone",
                 "Loopback S1 ch 0", "Loopback S1 ch 1"], names
# 7.2.19: port-RELATIVE offsets - both talker maps carry the SAME offsets
maps = {m["index"]: m for m in ovl["audio_maps"]}
# USER 08-06: host outranks loopback - the static map wires the HOST run
assert maps[2]["mappings"] == [[0, 0, 0, 0], [0, 1, 1, 0]], maps[2]
assert maps[3]["mappings"] == [[1, 0, 0, 0], [1, 1, 1, 0]], maps[3]

g.emit_svh(M, os.path.join(out, "gen", "aecp_aem_rom.svh"))
with open(os.path.join(out, "pools_overlay.json"), "w") as f:
    json.dump(ovl, f, indent=1)
print(f"[gen_pools_shape] {len(M['directory'])} descriptors, "
      f"ROM {M['ROM_SIZE']} B, 14 role-pooled AUDIO_CLUSTERs "
      f"(host/pilot/loopback, 0 physical) -> {out}")
