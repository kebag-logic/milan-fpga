#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Require invalid audio configurations to fail before simulation starts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

# Each row names a module and one independently invalid parameter binding.
INVALID = (
    ("bridge", "BUS_HZ_P", 0), ("bridge", "BUS_HZ_P", 50000001),
    ("bridge", "WINDOW_LOG2_P", 3), ("bridge", "WINDOW_LOG2_P", 17),
    ("bridge", "DIGEST_P", 0),
    ("crossing", "WIDTH_P", 0), ("crossing", "DEPTH_P", 2),
    ("crossing", "DEPTH_P", 6),
    ("feedback", "WINDOW_LOG2_P", 2), ("feedback", "WINDOW_LOG2_P", 17),
    ("feedback", "INTERVAL_LOG2_P", 13),
    ("gpif", "BUS_HZ_P", 1999),
    ("media", "PREFILL_FRAMES_P", 0), ("media", "PREFILL_FRAMES_P", 65),
    ("packet", "BUS_HZ_P", 7999),
    ("reference", "BUS_HZ_P", 0), ("reference", "BUS_HZ_P", 50000001),
    ("reference", "WINDOW_LOG2_P", 3), ("reference", "WINDOW_LOG2_P", 17),
    ("ingress", "DIGEST_P", 0), ("record", "DIGEST_P", 0), ("status", "DIGEST_P", 0),
)
VALID = (
    ("crossing", "DEPTH_P", 4), ("crossing", "WIDTH_P", 1),
    ("feedback", "WINDOW_LOG2_P", 3), ("feedback", "WINDOW_LOG2_P", 16),
    ("media", "PREFILL_FRAMES_P", 1), ("media", "PREFILL_FRAMES_P", 64),
    ("reference", "BUS_HZ_P", 1000), ("reference", "WINDOW_LOG2_P", 4),
    ("reference", "WINDOW_LOG2_P", 16),
    ("gpif", "BUS_HZ_P", 2000), ("packet", "BUS_HZ_P", 8000),
)


def main() -> None:
    """Elaborate valid controls and demand each illegal binding's own refusal."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[3]
    sources = sorted((root/"hdl/milan/usbaudio").glob("*.sv"))
    sources.append(root/"third_party/verilog-axis/rtl/axis_async_fifo.v")
    controls = [(leaf, "", 0) for leaf in sorted({row[0] for row in INVALID})]
    rows = []
    for expected_ok, cases in ((True, controls + list(VALID)), (False, INVALID)):
        for leaf, parameter, value in cases:
            name = f"{leaf}-{parameter or 'default'}-{value}"
            command = [args.engine, "--lint-only", "--timing", "-Wno-fatal", "-Werror-USERERROR",
                       "--top-module", "KL_usbaudio_"+leaf,
                       "--Mdir", str(args.out/name)]
            if parameter:
                command.append(f"-G{parameter}={value}")
            result = subprocess.run(command + [str(p) for p in sources], text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            (args.out/(name+".log")).write_text(result.stdout)
            refused = result.returncode != 0 and "AUDIO_PARAMETER_"+leaf.upper() in result.stdout
            if (expected_ok and result.returncode != 0) or (not expected_ok and not refused):
                raise RuntimeError(f"parameter control failed: {name}")
            rows.append({"case": name, "result": "ACCEPTED" if expected_ok else "REFUSED"})
    (args.out/"results.json").write_text(json.dumps(rows, indent=2)+"\n")
    print(f"PASS audio parameter boundaries: {len(controls)+len(VALID)} valid, {len(INVALID)} refused")


if __name__ == "__main__":
    main()
