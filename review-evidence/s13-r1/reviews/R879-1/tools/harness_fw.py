#!/usr/bin/env python3
"""harness_fw.py CLONE OUT POINT: the CPU budget harness's arm images at one point in one clone, built as its
build.build() builds them (build.flash_map, then build.firmware with that map; no XIP), without the SoC or native
model. One image per arm (variant) under OUT/<point>/<arm>/image/ctrl_app.elf; prints `<point> <arm> <sha256>`."""
import hashlib
import sys
from pathlib import Path

clone, out, point = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
harness = clone / "tb/verilator/ctrl_service_budget"
sys.path.insert(0, str(harness))
import build as builder  # noqa: E402
import run  # noqa: E402
import split_soc  # noqa: E402

assert builder.ROOT == clone, (builder.ROOT, clone)
shape, n_if = run.POINTS[point]
ARMS = ("none", "answering-ports", "shutdown-entry", "answering-later", "answering-every-port", "valid-destinations",
        "talker-notices", "declaring-outputs")
base = out / point
flash = builder.flash_map(base / "map" / split_soc.FLASH_MAP, shape)
for arm in ARMS:
    elf = builder.firmware(base / arm, shape, n_if, "none", arm, flash)
    print(point, arm, hashlib.sha256(elf.read_bytes()).hexdigest(), flush=True)
