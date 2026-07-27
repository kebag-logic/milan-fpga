#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: every module `milan_datapath` instantiates must be registered as a
Vivado source in `sw/litex/milan_soc.py`.

Why this exists. There are THREE independent file lists in this repo:

  * each `tb/verilator/<suite>/Makefile`  -> what Verilator compiles
  * `syn/yosys/run.sh`'s `tops=()` array  -> what Yosys synthesises
  * `milan_soc.py`'s curated source list  -> what VIVADO is given

A new module can be added, get a Verilator suite, get a Yosys top, pass every
gate in CI - and still be missing from the Vivado list. Nothing catches it,
because nothing in CI runs Vivado. It surfaces only as

    ERROR: [Synth 8-439] module 'X' not found

~40 minutes into a bitstream build, which is exactly when it is most expensive.
That happened on 2026-07-27 with `KL_i2s_feed_mux`: it had a suite, a Yosys
top, and 55/55 green - and three parallel Vivado runs all died on it.

This gate closes the gap in under a second, with no toolchain at all.

Usage:
    python3 scripts/check_soc_sources.py          # gate (exit 1 on a miss)
    python3 scripts/check_soc_sources.py --list   # show the resolved sets
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATAPATH = REPO / "hdl/milan/milan_datapath.sv"
SOC = REPO / "sw/litex/milan_soc.py"

#: instantiation names we care about - project RTL, not language keywords or
#: generate-block labels. Anything matching a project prefix must be a real
#: module we own, so a typo in a prefix fails loudly rather than silently
#: shrinking the checked set.
PREFIXES = ("KL_", "avtp_", "adp_", "acmp_", "aaf_", "traffic_", "ptp_",
            "cdc_", "tcam", "rx_", "tx_", "axis_", "timestamp_",
            "ethernet_", "event_", "milan_")

#: `X #(...) inst (` or `X inst (` at an indent (module instantiation shape)
INST_RE = re.compile(r"^\s{2,}([A-Za-z_]\w*)\s+(?:#\s*\(|\w+\s*\()", re.M)
SRC_RE = re.compile(r'"(hdl/[^"]*/([A-Za-z_]\w*)\.sv)"')


def instantiated():
    text = DATAPATH.read_text()
    return {m for m in INST_RE.findall(text) if m.startswith(PREFIXES)}


def registered():
    return {name: path for path, name in SRC_RE.findall(SOC.read_text())}


def main():
    inst = instantiated()
    reg = registered()
    missing = sorted(inst - set(reg))

    if "--list" in sys.argv[1:]:
        print(f"instantiated by milan_datapath ({len(inst)}):")
        for m in sorted(inst):
            print(f"   {'ok ' if m in reg else 'MISS'}  {m}")
        print(f"\nregistered for Vivado ({len(reg)})")

    # A source file that no longer exists is the mirror-image defect: Vivado
    # would fail on a missing file rather than a missing module.
    gone = sorted(p for p in reg.values() if not (REPO / p).is_file())

    if missing or gone:
        for m in missing:
            print(f"MISSING SOURCE: milan_datapath instantiates '{m}' but "
                  f"sw/litex/milan_soc.py does not register it -> Vivado "
                  f"synthesis WILL fail with [Synth 8-439] module not found")
        for p in gone:
            print(f"STALE SOURCE: milan_soc.py registers '{p}' which does not exist")
        return 1

    print(f"SoC source gate: OK ({len(inst)} instantiated modules all registered, "
          f"{len(reg)} sources all present)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
