#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Decode AUDIO_CLUSTER (0x0014) and STREAM_PORT_INPUT/OUTPUT (0x000E/0x000F)
descriptors from the descriptor ROM the builder model serialises, for the
default and enabled overlays of both shipping shapes (IEEE 1722.1-2021
7.2.13, 7.2.16; Milan v1.2 5.3.3.8).

Usage: descriptors.py <tree> <artifact root containing default/ and enabled/>
"""
import collections
import json
import struct
import sys
from pathlib import Path

tree, root = Path(sys.argv[1]), Path(sys.argv[2])
sys.path[:0] = [str(tree / "avdecc"), str(tree / "protocol-processor/hdl/aecp/desc")]
import gen_aem_store  # noqa: E402

ok = True
for label in ("default", "enabled"):
    for name in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
        overlay = json.loads((root / label / name / "aem_overlay.json").read_text())
        model = gen_aem_store.build_model(gen_aem_store.spec_from_overlay(overlay))
        rom = model["rom"]
        clusters, ports = [], []
        for dtype, index, offset, length in model["directory"]:
            body = rom[offset:offset + length]
            if dtype == 0x0014:
                t, i = struct.unpack(">HH", body[:4])
                objname = body[4:68].split(b"\0")[0].decode()
                channel_count = struct.unpack(">H", body[84:86])[0]
                fmt = body[86]
                clusters.append((i, objname, channel_count, fmt))
            elif dtype in (0x000E, 0x000F):
                # descriptor_type, index, clock_domain_index, port_flags,
                # number_of_controls, base_control, number_of_clusters,
                # base_cluster, number_of_maps, base_map (7.2.13)
                f = struct.unpack(">10H", body[:20])
                ports.append(("in" if dtype == 0x000E else "out", f[1], f[6], f[7], f[8]))
        counts = collections.Counter(c[2] for c in clusters)
        print(f"{label} {name}: {len(clusters)} AUDIO_CLUSTER, channel_count histogram {dict(counts)}")
        for p in ports:
            print(f"  STREAM_PORT_{p[0].upper()} {p[1]}: clusters={p[2]} base_cluster={p[3]} number_of_maps={p[4]}")
        if label == "enabled":
            loop = [c for c in clusters if c[1].startswith("Input Loopback")]
            print(f"  Input Loopback clusters: {len(loop)}; names {loop[0][1]!r} .. {loop[-1][1]!r}")
        ok &= set(counts) == {1}
print("CHANNEL_COUNT_ONE", "PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
