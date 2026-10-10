#!/usr/bin/env python3
"""Rewrite host-specific paths and names in the packet's text receipts.
Usage: redact.py PACKET_DIR CLONE_DIR HOSTNAME USER [TOOLS_ROOT]
This script itself is skipped."""
import re, sys
from pathlib import Path
packet, clone, host, user = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3], sys.argv[4]
subs = [(str(packet), "$PACKET"), (clone, "$CLONE"), (f"/home/{user}/litex-milan", "$LITEX_ENV"),
        (f"/home/{user}/Xilinx/2026.1", "$VIVADO_ROOT"), (sys.argv[5] if len(sys.argv) > 5 else "/nonexistent-tools-root", "$TOOLS"),
        (f"/home/{user}", "$HOME")]
for f in sorted((packet / "receipts").rglob("*")) + sorted((packet / "scripts").rglob("*")):
    if not f.is_file() or f.resolve() == Path(__file__).resolve():
        continue
    try:
        text = f.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    new = text
    for old, rep in subs:
        new = new.replace(old, rep)
    new = re.sub(rf"\b{re.escape(host)}\b", "<host>", new)
    new = re.sub(rf"\b{re.escape(user)}\b", "<user>", new)
    if new != text:
        f.write_text(new, encoding="utf-8")
        print("redacted", f.relative_to(packet))
