#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Grade a census whose live egress queue includes USB interference.

The inherited replay grades every phase and retains the held-egress ledger.
The extension changes only the queue at its documented completion point.
The expected queue declaration prevents grading an uninjected census here.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import egress_usb as usb


def grade(text: str, p: usb.base.Params) -> dict:
    """Require the live queue declaration before replaying its departures."""
    declaration = f"== USBQUEUE injected_ps={usb.INJECT_PS} handshake_ps={usb.HANDSHAKE_PS}"
    if declaration not in text.splitlines()[:400]:
        return dict(refused="the census did not run the USB interference envelope")
    inherited = usb.base.Queue
    try:
        usb.base.Queue = usb.Queue
        return usb.base.grade_case(text, p)
    finally:
        usb.base.Queue = inherited


def verdict(rows: dict, p: usb.base.Params) -> tuple[bool, list[str]]:
    """Retain the inherited margin and add the measured handshake explicitly.

    The live queue already charges this handshake before every busy period.
    Adding it again here is conservative, and keeps the separate fixed-path
    and handshake terms of the ruling visible in the final row.
    """
    ok, lines = usb.base.verdict(rows, p)
    wait = max((r.get("wait_ps", 0) for r in rows.values()), default=0)
    total_us = ((wait + usb.base.gptp_wire_ps(p)) * usb.base.MARGIN + usb.HANDSHAKE_PS) / 1_000_000
    total_us += usb.base.MII_FIXED_NS / 1000
    lines.append(f"USB EGRESS {total_us:.3f} us including separate {usb.HANDSHAKE_PS / 1000:.0f} ns "
                 f"handshake; bound {usb.base.BOUND_US} us")
    return ok and total_us <= usb.base.BOUND_US, lines


def main(argv: list[str]) -> int:
    """All cases of each named build, with an exact-departure agreement check."""
    rows = {}
    p = usb.base.params(usb.base.arty_spec())
    for directory in map(Path, argv):
        for path in sorted((directory / "results").glob("*.log")):
            name = directory.name + "/" + path.stem
            rows[name] = grade(path.read_text(), p)
            print(name, json.dumps(rows[name]), flush=True)
    ok, lines = verdict(rows, p)
    print("\n".join(lines), flush=True)
    print(f"RESULT: {'PASS' if ok else 'FAIL'} cases={len(rows)}", flush=True)
    return int(not ok)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
