#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prepare the USB link-rate census without changing the inherited harness.

The existing queue gets one bounded injection at each empty-wire boundary.
Only that extension and its identifying log line differ. Both source copies
are written into the new build; their hashes join the usual input manifest.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from egress_usb import HANDSHAKE_PS, INJECT_PS, SERVICE


def replace_once(text: str, before: str, after: str) -> str:
    """Fail closed if the inherited queue changes its extension point."""
    if text.count(before) != 1:
        raise ValueError("inherited egress extension point changed: " + before)
    return text.replace(before, after)


def sources(directory: Path) -> tuple[Path, Path]:
    """The inherited testbench and queue with the additive USB envelope."""
    source = (SERVICE / "egress_queue.hpp").read_text()
    source = replace_once(source, "        const std::uint64_t start = t > wire_free_ ? t : wire_free_;",
                          f"        if (t >= wire_free_) wire_free_ = t + {INJECT_PS + HANDSHAKE_PS}ULL;\n"
                          "        const std::uint64_t start = t > wire_free_ ? t : wire_free_;")
    source = replace_once(source, "        if (p_.octet_ps == 0) return;",
                          "        if (p_.octet_ps == 0) return;\n"
                          f'        std::printf("== USBQUEUE injected_ps={INJECT_PS} handshake_ps={HANDSHAKE_PS}\\n");')
    queue = directory / "usbnet_egress_queue.hpp"
    queue.write_text(source)
    main = directory / "usbnet_census_main.cpp"
    main.write_text(replace_once((SERVICE / "sim_main.cpp").read_text(),
                                '#include "egress_queue.hpp"', '#include "usbnet_egress_queue.hpp"'))
    manifest = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in
                (SERVICE / "egress_queue.hpp", SERVICE / "sim_main.cpp", queue, main, Path(__file__))}
    (directory / "usbnet-extension.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return main, queue


if __name__ == "__main__":
    sources(Path(sys.argv[1]))
