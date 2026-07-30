#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
gen_fmt4_shape.py - emit the 4-AAF-input TB shape svh (per-stream tables).

Builds the builtin (deployed) spec with THREE extra AAF listener sinks
inserted before the CRF sink (inputs = [AAF "Stream 1" .. AAF "Stream 4",
CRF]) and emits its aecp_aem_rom.svh into <out-dir>/gen/. That is the
arty_4x4 SHIPPED listener input count - four AAF sinks then one CRF sink -
so the sim_fmt4 harness round-trips SET/GET_STREAM_FORMAT on the MIDDLE
sinks (descriptor_index 2 and 3), the band the 2-AAF fmt2 shape and the 8x8
GET_STREAM_INFO harness never reach. Index 0/1-only coverage is exactly
what hid "SET/GET_STREAM_FORMAT works only on inputs 0 and 1" for months.

With --else-arm the emitted svh has its `AEM_PER_STREAM_FMT define stripped,
which selects the legacy 2-input else path in KL_aecp_response_builder (the
pre-per-descriptor behaviour - the legacy WB_STREAM_IN0/IN1_FMT_C and
AEM_FMTS_C symbols are always emitted, so the else arm still compiles). The
same harness then MUST answer NO_SUCH_DESCRIPTOR on inputs 2..4: that is the
bite the per-descriptor fix answers.

Usage: python3 gen_fmt4_shape.py <out-dir> [--else-arm]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "avdecc"))

import gen_aem_store as g  # noqa: E402

out = sys.argv[1]
else_arm = "--else-arm" in sys.argv[2:]

spec = g.builtin_spec()
# grow the single AAF sink to FOUR AAF sinks, keeping the CRF sink last
base_aaf = dict(spec["stream_inputs"][0])
for k in range(2, 5):                       # Stream 2, Stream 3, Stream 4
    extra = dict(base_aaf)
    extra["name"] = f"Stream {k}"
    spec["stream_inputs"].insert(k - 1, extra)
# the CRF sink is now STREAM_INPUT[4]; keep its clock source honest
spec["clock_sources"][2]["loc_index"] = 4

M = g.build_model(spec)
assert M["PER_STREAM"]["EMIT"], "4-AAF-input shape must emit per-stream tables"
assert M["PER_STREAM"]["IN_CRF"] == [False, False, False, False, True]

os.makedirs(os.path.join(out, "gen"), exist_ok=True)
dst = os.path.join(out, "gen", "aecp_aem_rom.svh")
g.emit_svh(M, dst)

if else_arm:
    with open(dst) as f:
        lines = f.readlines()
    with open(dst, "w") as f:
        for ln in lines:
            if ln.strip() == "`define AEM_PER_STREAM_FMT":
                f.write("// [gen_fmt4_shape --else-arm] AEM_PER_STREAM_FMT "
                        "stripped: selects the legacy 2-input else path\n")
                continue
            f.write(ln)

tag = "else-arm (pre-fix path)" if else_arm else "per-stream tables"
print(f"[gen_fmt4_shape] {len(M['directory'])} descriptors, "
      f"ROM {M['ROM_SIZE']} B, {tag} -> {out}")
