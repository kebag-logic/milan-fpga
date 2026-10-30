#!/usr/bin/env python3
"""Reviewer probe: decode the packed 1x1 AEM image's stream ports and clock
sources (IEEE 1722.1-2021 7.2.13, 7.2.9) to cross-check the guide's tree.

Usage: python3 decode_1x1_image.py <repo-root>
"""
import struct
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402

art = eb._derive_artifacts(str(root / "configs" / "endstation_ax7101_1x1_tdm8.yaml"))
img = eb._entity_model_image(art.cfg, art.overlay)
blob, amap = img["aem_desc.bin"], img["aem_desc.map"]
print(amap.split("semantic lint")[0])
rows = {}
for line in amap.splitlines():
    p = line.split()
    if len(p) == 8 and p[0].isdigit() and p[1].startswith("0x00"):
        rows.setdefault(int(p[1], 16), []).append((int(p[2]), int(p[3]), int(p[5]), int(p[6], 16)))


def descs(t):
    for first, count, stride, off in rows.get(t, []):
        for k in range(count):
            yield first + k, blob[off + k * stride: off + (k + 1) * stride]


for t, label in ((0x000E, "STREAM_PORT_INPUT"), (0x000F, "STREAM_PORT_OUTPUT")):
    for idx, d in descs(t):
        f = struct.unpack(">10H", d[:20])
        print(f"{label} {idx}: clock_domain {f[2]} flags 0x{f[3]:04X} clusters {f[6]} base_cluster {f[7]} maps {f[8]} base_map {f[9]}")
for idx, d in descs(0x000A):
    name = d[4:68].split(b"\0")[0].decode()
    flags, ctype = struct.unpack(">HH", d[70:74])
    loc_t, loc_i = struct.unpack(">HH", d[82:86])
    print(f"CLOCK_SOURCE {idx}: {name!r} type {ctype} location_type 0x{loc_t:04X} location_index {loc_i}")
for idx, d in descs(0x0024):
    name = d[4:68].split(b"\0")[0].decode()
    print(f"CLOCK_DOMAIN {idx}: {name!r}")
for idx, d in descs(0x001A):
    name = d[4:68].split(b"\0")[0].decode()
    print(f"CONTROL {idx}: {name!r}")
for t, label in ((0x0005, "STREAM_INPUT"), (0x0006, "STREAM_OUTPUT")):
    for idx, d in descs(t):
        print(f"{label} {idx}: {d[4:68].split(bytes(1))[0].decode()!r}")
for idx, d in descs(0x0014):
    if idx in (0, 7, 8, 15, 16, 17, 24):
        print(f"AUDIO_CLUSTER {idx}: {d[4:68].split(bytes(1))[0].decode()!r}")
