#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_fmt2_shape.py - emit the 2-AAF-input TB shape svh (per-stream tables).

Builds the builtin (deployed) spec with a SECOND AAF listener sink inserted
before the CRF sink (inputs = [AAF "Stream 1", AAF "Stream 2", CRF]) and
emits its aecp_aem_rom.svh into <out-dir>/gen/. That shape crosses the
per-stream gate (len(stream_inputs) > 2), so the svh carries the
`AEM_PER_STREAM_FMT layout the sim_fmt2 harness exercises. The Makefile
puts <out-dir> FIRST on the Verilator include path so it shadows the
tracked deployed svh (include order verified: -I beats file-relative).

Usage: python3 gen_fmt2_shape.py <out-dir>
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))

import gen_aem_store as g  # noqa: E402

out = sys.argv[1]
spec = g.builtin_spec()
second = dict(spec["stream_inputs"][0])
second["name"] = "Stream 2"
spec["stream_inputs"].insert(1, second)
# CRF sink moved to STREAM_INPUT[2]: keep the CRF clock source honest
spec["clock_sources"][2]["loc_index"] = 2

M = g.build_model(spec)
assert M["PER_STREAM"]["EMIT"], "2-AAF-input shape must emit per-stream tables"
assert M["PER_STREAM"]["IN_CRF"] == [False, False, True]

os.makedirs(os.path.join(out, "gen"), exist_ok=True)
g.emit_svh(M, os.path.join(out, "gen", "aecp_aem_rom.svh"))
print(f"[gen_fmt2_shape] {len(M['directory'])} descriptors, "
      f"ROM {M['ROM_SIZE']} B, per-stream tables emitted -> {out}")
