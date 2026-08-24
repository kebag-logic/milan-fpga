#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reconstruct <build>/flashboot_layout.json from the generated soc.h.

The sweep path skips main()'s json export, but the MILAN_FLASHBOOT_* constants
in software/include/generated/soc.h are what the BIOS actually compiled —
reconstructing from them can never drift from the gateware. Usage:

    layout_from_soch.py <build_dir>
"""
import json, os, re, sys

from gptp_owner_contract import GPTP_OWNER_BY_CODE


def main(build_dir):
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
    if names == {"aem"}:
        manifest = "baremetal"
    elif names == {"kernel"}:
        manifest = "kernel"
    elif names == {"opensbi", "dtb", "kernel", "rootfs"}:
        manifest = "full"
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
              "entry": const("MILAN_FLASHBOOT_ENTRY"),
              "complete": "MILAN_FLASHBOOT_COMPLETE" in text,
              "images": images}
    out = os.path.join(build_dir, "flashboot_layout.json")
    with open(out, "w") as f:
        json.dump(layout, f, indent=2)
    print(f"[layout] reconstructed from soc.h -> {out}")
    print("[layout]", [(i["name"], hex(i["offset"])) for i in images])

if __name__ == "__main__":
    main(sys.argv[1])
