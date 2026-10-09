#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Regenerate the parent's 1x1 TDM8 and 8x8 descriptor images at a pinned parent.

Run from the root of a parent checkout whose protocol-processor/hdl/aecp/desc
holds the processor packer. Writes <out>/<shape>.overlay.json, .img.bin, .map.

usage: gen_parent_images.py OUTDIR
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, "sw/builder")
import endstation_builder as eb  # noqa: E402

out = Path(sys.argv[1]).resolve()
out.mkdir(parents=True, exist_ok=True)
for shape, cfg in (("1x1", "configs/endstation_ax7101_1x1_tdm8.yaml"),
                   ("8x8", "configs/endstation_ax7101_8x8.yaml")):
    ovl = eb.emit_aem_overlay(eb.load_config(cfg))
    p = out / f"{shape}.overlay.json"
    p.write_text(json.dumps(ovl, indent=1) + "\n")
    subprocess.run([sys.executable, "avdecc/gen_aemi_image.py", "--overlay", str(p),
                    "-o", str(out / f"{shape}.img.bin"), "-m", str(out / f"{shape}.map")],
                   check=True)
    data = (out / f"{shape}.img.bin").read_bytes()
    print(shape, len(data), hashlib.sha256(data).hexdigest())
