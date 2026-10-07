#!/usr/bin/env python3
"""Rebuild the four-module size fixtures with a prebuilt bare-metal runtime."""
import json
from pathlib import Path
import subprocess
import sys

packet = Path(__file__).resolve().parent
reports = []
for shape in ("endstation_ax7101_1x1_tdm8", "endstation_ax7101_8x8"):
    for count in (1, 2):
        out = packet / "scratch" / f"srp-image-{shape}-if{count}"
        runtime = packet / "scratch/runtime"
        subprocess.run([sys.executable, "sw/firmware/ctrl/test/ctrl_srp_image.py",
                        "--config", f"configs/{shape}.yaml", "--interfaces", str(count),
                        "--output", str(out), "--libc", str(runtime / "libc.a"),
                        "--compiler-runtime", str(runtime / "libcompiler_rt.a")], check=True)
        reports.append(json.loads((out / "size.json").read_text()))
(packet / "receipts/srp-images-size.json").write_text(json.dumps(reports, indent=2) + "\n")
