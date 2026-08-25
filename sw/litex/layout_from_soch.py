#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reconstruct <build>/flashboot_layout.json from the generated soc.h.

The sweep path skips main()'s json export, but the MILAN_FLASHBOOT_* constants
in software/include/generated/soc.h are what the BIOS actually compiled —
reconstructing from them can never drift from the gateware. Usage:

    layout_from_soch.py <build_dir> [--bit <build/gateware/board.bit>]
"""
import argparse
import glob
import json
import os
import re

from gptp_owner_contract import GPTP_OWNER_BY_CODE
from qspi_owner_transition import TransitionError, bitstream_binding


def main(build_dir, bit_path=None):
    soc_h = os.path.join(build_dir, "software/include/generated/soc.h")
    text = open(soc_h).read()

    def const(name):
        m = re.search(rf"#define {re.escape(name)}\s+(0x[0-9a-fA-F]+|\d+)", text)
        return int(m.group(1), 0) if m else None

    owner_code = const("MILAN_GPTP_OWNER")
    if owner_code not in GPTP_OWNER_BY_CODE:
        raise SystemExit(
            "layout: soc.h has no valid MILAN_GPTP_OWNER "
              "(0=none, 1=fabric, 2=software); refusing an unowned layout")
    if GPTP_OWNER_BY_CODE[owner_code] == "software":
        raise SystemExit(
            "layout: soc.h records the retired software gPTP owner (#259): "
            "the bare-metal product's one owner is the fabric plane, and a "
            "verification-only option-off elaboration has no flashable layout")
    cpu_xlen = const("MILAN_CPU_XLEN")
    if cpu_xlen not in (32, 64):
        raise SystemExit(
            "layout: soc.h has no valid MILAN_CPU_XLEN (32 or 64); "
            "refusing an architecture-unbound layout")

    payloads = []
    for name in ("aem", "opensbi", "dtb", "kernel", "rootfs"):
        prefix = f"MILAN_FLASHBOOT_{name.upper()}"
        off = const(f"{prefix}_OFFSET")
        if off is None:
            continue
        row = {"name": name, "offset": off,
               "addr": const(f"{prefix}_ADDR")}
        budget = const(f"{prefix}_SIZE")
        if budget is not None:
            row["budget"] = budget
        payloads.append(row)

    names = {row["name"] for row in payloads}
    retired = sorted(names & {"kernel", "opensbi", "dtb", "rootfs"})
    if retired:
        raise SystemExit(
            f"layout: soc.h names retired Linux boot images {retired}: the "
            "product is bare-metal only (#259); this build predates that "
            "policy and cannot produce a flashable layout")
    if names == {"aem"}:
        manifest = "baremetal"
    elif not names:
        manifest = "none"
    else:
        raise SystemExit(
            f"layout: soc.h contains unsupported flashboot image set {sorted(names)}")

    images = []
    if payloads:
        # The bitstream slot is fixed by the v3 flash contract.  The BIOS does
        # not consume it, so historical soc.h files have no constants for it;
        # retaining the established values makes reconstructed sweep layouts
        # byte-for-byte equivalent in meaning to main()'s layout.
        images.append({"name": "bitstream", "offset": 0x0,
                       "addr": 0x0, "budget": 0x40_0000})
        images.extend(payloads)
    images.sort(key=lambda i: i["offset"])

    layout = {"manifest": manifest,
              "gptp_owner": GPTP_OWNER_BY_CODE[owner_code],
              "cpu_xlen": cpu_xlen,
              "entry": const("MILAN_FLASHBOOT_ENTRY"),
              "complete": "MILAN_FLASHBOOT_COMPLETE" in text,
              "images": images}
    if images:
        if bit_path is None:
            candidates = sorted(glob.glob(
                os.path.join(build_dir, "gateware", "*.bit")))
            if len(candidates) != 1:
                raise SystemExit(
                    "layout: expected exactly one gateware/*.bit for payload "
                    f"binding, found {len(candidates)}; pass --bit explicitly")
            bit_path = candidates[0]
        try:
            layout.update(bitstream_binding(bit_path))
        except TransitionError as exc:
            raise SystemExit(
                f"layout: cannot bind parsed bitstream {bit_path}: {exc}") from exc
    out = os.path.join(build_dir, "flashboot_layout.json")
    with open(out, "w") as f:
        json.dump(layout, f, indent=2)
    print(f"[layout] reconstructed from soc.h -> {out}")
    print("[layout]", [(i["name"], hex(i["offset"])) for i in images])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir")
    parser.add_argument("--bit")
    args = parser.parse_args()
    main(args.build_dir, args.bit)
