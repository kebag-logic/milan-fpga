#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reconstruct <build>/flashboot_layout.json from the generated soc.h.

The sweep path skips main()'s json export, but the MILAN_FLASHBOOT_* constants
in software/include/generated/soc.h are what the BIOS actually compiled —
reconstructing from them can never drift from the gateware. Usage:

    layout_from_soch.py <build_dir> [--bit <build/gateware/board.bit>]
"""
import argparse
import json
import re
from pathlib import Path

from gptp_owner_contract import GPTP_OWNER_BY_CODE
from qspi_owner_transition import (
    TransitionError,
    aem_image_binding,
    bitstream_binding,
)


def _soc_header(build_dir):
    """The generated soc.h text — the constants the BIOS actually compiled."""
    return (build_dir / "software/include/generated/soc.h").read_text()


def _const(text, name):
    """The integer a `#define <name>` binds in soc.h, or None when absent."""
    m = re.search(rf"#define {re.escape(name)}\s+(0x[0-9a-fA-F]+|\d+)", text)
    return int(m.group(1), 0) if m else None


def _owner_and_xlen(text):
    """(gptp owner name, cpu xlen), refusing an unowned or non-product soc.h."""
    owner_code = _const(text, "MILAN_GPTP_OWNER")
    if owner_code not in GPTP_OWNER_BY_CODE:
        raise SystemExit(
            "layout: soc.h has no valid MILAN_GPTP_OWNER "
              "(0=none, 1=fabric); refusing an unowned layout")
    cpu_xlen = _const(text, "MILAN_CPU_XLEN")
    if cpu_xlen != 32:
        raise SystemExit(
            "layout: soc.h must record the product CPU width (32)")
    return GPTP_OWNER_BY_CODE[owner_code], cpu_xlen


def _flashboot_payloads(text):
    """The MILAN_FLASHBOOT_* payload rows soc.h carries, in contract order."""
    payloads = []
    for name in ("aem",):
        prefix = f"MILAN_FLASHBOOT_{name.upper()}"
        off = _const(text, f"{prefix}_OFFSET")
        if off is None:
            continue
        row = {"name": name, "offset": off,
               "addr": _const(text, f"{prefix}_ADDR")}
        budget = _const(text, f"{prefix}_SIZE")
        if budget is not None:
            row["budget"] = budget
        payloads.append(row)
    return payloads


def _manifest_and_images(payloads):
    """(manifest kind, the offset-sorted image table) for those payloads."""
    names = {row["name"] for row in payloads}
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
    return manifest, images


def _aem_binding(text, build_dir):
    """The AEM identity fields, proved against the length and CRC32 in soc.h."""
    expected_bytes = _const(text, "MILAN_AEM_IMAGE_BYTES")
    expected_crc = _const(text, "MILAN_AEM_IMAGE_CRC32")
    if expected_bytes is None or expected_bytes <= 0 or expected_crc is None:
        raise SystemExit(
            "layout: soc.h does not bind the compiled AEM length and "
            "CRC32; refusing a legacy artifact set")
    aem_path = build_dir / "aem_desc.bin"
    try:
        # `aem_image_binding` is annotated `path: str`; the boundary stays a str
        # so this module's Paths do not leak into a contract it does not own.
        aem_binding = aem_image_binding(str(aem_path))
    except TransitionError as exc:
        raise SystemExit(
            f"layout: cannot bind generated AEM image {aem_path}: {exc}") \
            from exc
    if aem_binding["aem_image_bytes"] != expected_bytes:
        raise SystemExit(
            "layout: generated AEM length "
            f"{aem_binding['aem_image_bytes']} differs from compiled "
            f"MILAN_AEM_IMAGE_BYTES {expected_bytes}")
    if aem_binding["aem_image_crc32"] != expected_crc:
        raise SystemExit(
            "layout: generated AEM CRC32 "
            f"0x{aem_binding['aem_image_crc32']:08x} differs from compiled "
            f"MILAN_AEM_IMAGE_CRC32 0x{expected_crc:08x}")
    return aem_binding


def _payload_bitstream_binding(build_dir, bit_path):
    """The parsed-bitstream fields, locating gateware/*.bit when none is given."""
    if bit_path is None:
        candidates = sorted(str(p) for p in (build_dir / "gateware").glob("*.bit"))
        if len(candidates) != 1:
            raise SystemExit(
                "layout: expected exactly one gateware/*.bit for payload "
                f"binding, found {len(candidates)}; pass --bit explicitly")
        bit_path = candidates[0]
    try:
        # `bitstream_binding` is annotated `path: str`, and --bit arrives from
        # argv as one; the str boundary is kept rather than widened here.
        return bitstream_binding(str(bit_path))
    except TransitionError as exc:
        raise SystemExit(
            f"layout: cannot bind parsed bitstream {bit_path}: {exc}") from exc


def main(build_dir: str, bit_path: str | None = None) -> None:
    """Write <build_dir>/flashboot_layout.json from the constants soc.h carries.

    Reconstructed rather than copied: soc.h is what the BIOS was compiled
    against, so a layout derived from it cannot disagree with the gateware
    that shipped beside it. `bit_path` names the payload bitstream when the
    build holds more than the one gateware/*.bit this would otherwise find.
    """
    build = Path(build_dir)
    text = _soc_header(build)
    gptp_owner, cpu_xlen = _owner_and_xlen(text)
    payloads = _flashboot_payloads(text)
    manifest, images = _manifest_and_images(payloads)

    layout = {"manifest": manifest,
              "gptp_owner": gptp_owner,
              "cpu_xlen": cpu_xlen,
              "entry": None,
              "complete": False,
              "images": images}
    if any(row["name"] == "aem" for row in payloads):
        layout.update(_aem_binding(text, build))
    if images:
        layout.update(_payload_bitstream_binding(build, bit_path))

    out = build / "flashboot_layout.json"
    out.write_text(json.dumps(layout, indent=2))
    print(f"[layout] reconstructed from soc.h -> {out}")
    print("[layout]", [(i["name"], hex(i["offset"])) for i in images])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir")
    parser.add_argument("--bit")
    args = parser.parse_args()
    main(args.build_dir, args.bit)
