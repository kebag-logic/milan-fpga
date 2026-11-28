#!/usr/bin/env python3
"""Regenerate the AEM descriptors with the public generator and print them.

Usage: regen_image.py <milan-fpga checkout at 58f7673b> <config.yaml>
The checkout needs sw/builder, avdecc, sw/litex/platforms/board_audio_routing.py and the
protocol-processor gitlink's hdl/aecp/desc directory.  Output lines: "type index length hex".
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
for d in ("sw/builder", "avdecc", "protocol-processor/hdl/aecp/desc"):
    sys.path.insert(0, str(root / d))
import endstation_builder as builder  # noqa: E402
import gen_aem_store as aem  # noqa: E402
import gen_aemi_image as join  # noqa: E402

cfg = builder.load_config(sys.argv[2])
overlay = builder.emit_aem_overlay(cfg)
model = aem.build_model(aem.spec_from_overlay(overlay))
rom = join.apply_identity(model, join.identity_from_overlay(overlay))
for t, i, base, length in model["directory"]:
    print(t, i, length, bytes(rom[base:base + length]).hex())
