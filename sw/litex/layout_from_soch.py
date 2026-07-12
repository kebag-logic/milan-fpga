#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reconstruct <build>/flashboot_layout.json from the generated soc.h.

The sweep path skips main()'s json export, but the MILAN_FLASHBOOT_* constants
in software/include/generated/soc.h are what the BIOS actually compiled —
reconstructing from them can never drift from the gateware. Usage:

    layout_from_soch.py <build_dir>
"""
import json, os, re, sys

def main(build_dir):
    soc_h = os.path.join(build_dir, "software/include/generated/soc.h")
    text = open(soc_h).read()

    def const(name):
        m = re.search(rf"#define MILAN_FLASHBOOT_{name}\s+(0x[0-9a-fA-F]+|\d+)", text)
        return int(m.group(1), 0) if m else None

    images = [{"name": "bitstream", "offset": 0x0, "addr": 0x0}]
    for name in ("opensbi", "dtb", "kernel", "rootfs"):
        off = const(f"{name.upper()}_OFFSET")
        if off is None:
            continue
        images.append({"name": name, "offset": off,
                       "addr": const(f"{name.upper()}_ADDR")})
    images.sort(key=lambda i: i["offset"])

    layout = {"manifest": "full", "entry": const("ENTRY"),
              "complete": "MILAN_FLASHBOOT_COMPLETE" in text, "images": images}
    out = os.path.join(build_dir, "flashboot_layout.json")
    with open(out, "w") as f:
        json.dump(layout, f, indent=2)
    print(f"[layout] reconstructed from soc.h -> {out}")
    print("[layout]", [(i["name"], hex(i["offset"])) for i in images])

if __name__ == "__main__":
    main(sys.argv[1])
