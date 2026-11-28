#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure the injection handshake on the shipping MII chain and its plants.

The returned term conservatively includes grant-to-wire startup and the
acknowledgement crossing. It subtracts frame serialization only, leaving
the inter-frame gap in the separate 1539-octet interference allowance.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import egress_chain
from egress_usb import HANDSHAKE_PS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def build(directory: Path, arbiter: Path | None = None) -> Path:
    """Use the production attachment, with only the named planted arbiter substituted."""
    chain = egress_chain.generate(directory)
    names = ("KL_usbnet_pkg.sv", "KL_usbnet_rx_copy.sv", "KL_usbnet_tx_inject.sv",
             "KL_usbnet_tx_arb.sv", "KL_usbnet_tap.sv")
    rtl = [str(arbiter if arbiter is not None and name == "KL_usbnet_tx_arb.sv"
               else ROOT / "hdl/usbnet" / name) for name in names]
    native = directory / "native"
    command = ["verilator", "--cc", "--exe", "--build", "-j", "4", "-O3", "-Wno-fatal",
               "--top-module", "usbnet_egress_chain", "--Mdir", str(native),
               "-CFLAGS", "-O2 -std=c++17", str(chain), *rtl, str(HERE / "sim_egress.cpp"), "-o", "Vegress"]
    (directory / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    with (directory / "build.log").open("w") as log:
        subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=True)
    return native / "Vegress"


def measured(binary: Path, log: Path) -> tuple[bool, int]:
    """All eight lengths at every pair of eight clock phases must be present."""
    result = subprocess.run([str(binary)], capture_output=True, text=True, check=False)
    log.write_text(result.stdout + result.stderr)
    rows = [tuple(map(int, line.split()[1:])) for line in result.stdout.splitlines()
            if line.startswith("HANDSHAKE ")]
    expected = {(length, d, e) for length in (14, 60, 64, 90, 127, 512, 1514, 1515)
                for d in range(8) for e in range(8)}
    present = {r[:3] for r in rows}
    worst = max((r[-1] for r in rows), default=0)
    return result.returncode == 0 and len(rows) == len(expected) and present == expected, worst


def plants(directory: Path) -> bool:
    """An early release and a delayed acknowledgement must each fail measurement."""
    original = (ROOT / "hdl/usbnet/KL_usbnet_tx_arb.sv").read_text()
    cases = {
        "released-before-phy": original.replace("A_WAIT: if (answered_w) ast_r <= A_IDLE;",
                                                "A_WAIT: ast_r <= A_IDLE;"),
        "handshake-too-long": original.replace("[1:0] ack_sync_r", "[31:0] ack_sync_r")
            .replace("{ack_sync_r[0], ack_r}", "{ack_sync_r[30:0], ack_r}")
            .replace("ack_sync_r[1] == req_r", "ack_sync_r[31] == req_r"),
    }
    passed = True
    for name, source in cases.items():
        if source == original:
            raise ValueError("missing arbiter plant anchor: " + name)
        target = directory / name
        target.mkdir(parents=True, exist_ok=True)
        rtl = target / "KL_usbnet_tx_arb.sv"
        rtl.write_text(source)
        valid, worst = measured(build(target, rtl), target / "run.log")
        if name == "released-before-phy":
            caught = not valid and "FAIL: datapath is held behind injection" in (target / "run.log").read_text()
        else:
            caught = valid and worst > HANDSHAKE_PS
        passed &= caught
        print("CAUGHT" if caught else "MISSED", name, worst, flush=True)
    return passed


def main() -> int:
    """The stated term is the measured maximum rounded up to ten nanoseconds."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--plants", action="store_true")
    args = parser.parse_args()
    directory = args.directory.resolve()
    valid, worst = measured(build(directory), directory / "handshake.log")
    rounded = -(-worst // 10_000) * 10_000
    ok = valid and rounded == HANDSHAKE_PS
    print(f"{'PASS' if ok else 'FAIL'}: 512 cases; maximum {worst} ps; stated {rounded} ps", flush=True)
    if args.plants:
        ok &= plants(directory)
    return int(not ok)


if __name__ == "__main__":
    raise SystemExit(main())
