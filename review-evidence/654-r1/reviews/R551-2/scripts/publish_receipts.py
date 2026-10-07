#!/usr/bin/env python3
"""Retain raw check output and location-redacted export logs with provenance."""
import hashlib
import json
from pathlib import Path
import re
import sys

packet = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1]).resolve()
provenance = []
for source in sorted((packet / "scratch").glob("ax-*.raw.log")):
    raw = source.read_bytes()
    text = raw.decode()
    text = text.replace(str(packet / "scratch"), "<review-scratch>")
    text = text.replace(str(root), "<source-root>")
    text = re.sub(r"/home/[^/\s]+/litex-milan", "<dependency-root>", text)
    target = packet / "receipts" / source.name.replace(".raw.log", ".log")
    target.write_text(text)
    provenance.append({"receipt": str(target.relative_to(packet)),
                       "raw_sha256": hashlib.sha256(raw).hexdigest(),
                       "published_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                       "redactions": "source, scratch and dependency locations only"})
(packet / "receipts/log-provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
commands = json.loads((packet / "scratch/focused-commands.json").read_text())
for row in commands:
    row["command"] = [arg.replace(str(packet), "<packet>").replace(str(root), "<source-root>")
                      if not arg.endswith("/venv/bin/python3") else "<dependency-python>"
                      for arg in row["command"]]
(packet / "receipts/focused-commands.json").write_text(json.dumps(commands, indent=2) + "\n")
print("PASS: export logs retained with location-only redactions and both digests")
