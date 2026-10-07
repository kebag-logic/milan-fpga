#!/usr/bin/env python3
"""Redact local prefixes from receipt text and hash the complete publication set."""
import argparse
import hashlib
import json
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("root", type=Path)
ap.add_argument("packet", type=Path)
ap.add_argument("--default-sdk", type=Path, required=True)
ap.add_argument("--tools", type=Path, required=True)
args = ap.parse_args()
packet = args.packet.resolve()
replacements = [(str(packet), "$PACKET"), (str(args.root.resolve()), "$CHECKOUT"),
                (str(args.default_sdk.resolve()), "$DEFAULT_SDK"),
                (str(args.tools.resolve()), "$TOOLS"), (str(Path.home()), "$HOME")]
originals = packet / "scratch/raw-publication-inputs"
originals.mkdir(exist_ok=True)
rows = []
for path in sorted((packet / "receipts").iterdir()):
    if path.name == "path-redactions.json":
        continue
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    used = []
    for local, neutral in replacements:
        if local in text:
            text = text.replace(local, neutral)
            used.append(neutral)
    published = text.encode("utf-8")
    if published != raw:
        (originals / path.name).write_bytes(raw)
        path.write_bytes(published)
    rows.append({"file": str(path.relative_to(packet)),
                 "original_sha256": hashlib.sha256(raw).hexdigest(),
                 "published_sha256": hashlib.sha256(published).hexdigest(),
                 "redacted_prefixes": used})
(packet / "receipts/path-redactions.json").write_text(json.dumps(rows, indent=2) + "\n")
files = [packet / "REPORT.md", *sorted((packet / "scripts").glob("*")), *sorted((packet / "receipts").glob("*"))]
assert all(f.is_file() for f in files)
(packet / "MANIFEST.sha256").write_text("".join(hashlib.sha256(f.read_bytes()).hexdigest() + "  " + str(f.relative_to(packet)) + "\n" for f in files))
print("Publication files:", len(files))
