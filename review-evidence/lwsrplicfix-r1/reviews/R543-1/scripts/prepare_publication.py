#!/usr/bin/env python3
"""Preserve raw local logs in scratch, redact local prefixes, and hash public files."""
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
args = p.parse_args()
repo, packet = args.repo.resolve(), args.packet.resolve()
excluded = {"issue1.json", "issue1-comments.json", "cgreen-release.json"}
receipts = sorted(f for f in (packet / "receipts").rglob("*")
                  if f.is_file() and f.name not in excluded and f.name != "path-redaction.json")
redactions = []
for path in receipts:
    original = path.read_bytes()
    published = original.replace(str(packet).encode(), b"<packet>").replace(str(repo).encode(), b"<clone>")
    if published != original:
        relative = path.relative_to(packet)
        raw = packet / "scratch/raw-receipts" / relative
        raw.parent.mkdir(parents=True, exist_ok=True)
        # Do not overwrite the original if packaging is repeated.
        if not raw.exists():
            raw.write_bytes(original)
        path.write_bytes(published)
        redactions.append(dict(file=relative.as_posix(),
            original_sha256=hashlib.sha256(original).hexdigest(),
            published_sha256=hashlib.sha256(published).hexdigest(),
            transformation="Local packet/clone prefixes replaced by <packet>/<clone>; raw copy retained only in scratch"))
redaction_path = packet / "receipts/path-redaction.json"
if redactions or not redaction_path.exists():
    redaction_path.write_text(json.dumps(redactions, indent=2) + "\n")
files = [packet / "REPORT.md", packet / "REPRODUCE.md", redaction_path]
files += sorted((packet / "scripts").glob("*.py")) + receipts
with (packet / "MANIFEST.sha256").open("w") as out:
    for path in sorted(set(files)):
        relative = path.relative_to(packet).as_posix()
        assert not relative.startswith("scratch/")
        out.write(hashlib.sha256(path.read_bytes()).hexdigest() + "  " + relative + "\n")
print("Publishable files:", len(set(files)))
print("Redacted receipts this run:", len(redactions))
