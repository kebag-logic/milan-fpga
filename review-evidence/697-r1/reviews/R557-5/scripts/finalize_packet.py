#!/usr/bin/env python3
"""Select public receipts, normalize machine locations, and hash the packet."""
import hashlib
import json
from pathlib import Path
import re
import sys

packet = Path(__file__).resolve().parents[1]
root = Path(sys.argv[1]).resolve()
patterns = [
    "REPLAY.md", "scripts/*.py", "scripts/prior/R556-3/scripts/*.py",
    "scripts/prior/R556-4/scripts/*.py", "scripts/prior/R557-4/scripts/full_comment_bypass.py",
    "receipts/assembly-*", "receipts/independent-probes.json", "receipts/independent-verdict.md",
    "receipts/production-preservation.json", "receipts/conditional-results.json",
    "receipts/independent-result-audit.json", "receipts/document-links.json",
    "receipts/checkout-final.json", "receipts/clang18-download.json", "receipts/lexer-version.txt",
    "receipts/local-versions.json", "receipts/local-linux/*", "receipts/local-rv32/**/*",
    "receipts/prior-replay/*", "receipts/prior-probe-provenance.json",
    "receipts/mutation*.json", "receipts/mutation-reused.log", "receipts/mutation-reused.rc",
    "receipts/mutation-xml/**/*.xml", "receipts/message-markers*.json",
    "receipts/*-instances.log", "receipts/linux.log", "receipts/linux.rc", "receipts/rv32.log", "receipts/rv32.rc",
    "receipts/review-runs.json", "receipts/pr-checks-final.json", "receipts/pr-run-jobs.json",
    "receipts/pr-run-artifacts.json", "receipts/hosted/*", "receipts/authority-*.md",
    "receipts/pr-body.md", "receipts/closed-pr1-body.md", "receipts/r1-gates.json",
    "receipts/r1-production-proof.json", "receipts/r1-versions.txt",
]
files = sorted({p for pattern in patterns for p in packet.glob(pattern) if p.is_file()})
replacements = [(str(packet / "scratch"), "<scratch>"), (str(root), "<review-tree>"),
                (str(packet), "<review-packet>"),
                ("<home-path>/work/tsn-c-stack/tsn-c-stack", "<hosted-tree>"),
                ("<home-path>/work/_temp", "<hosted-temp>")]
changes = []
raw = packet / "scratch/publication-originals"
for path in files:
    if "scripts" in path.relative_to(packet).parts:
        continue
    before = path.read_bytes()
    text = before.decode()
    for old, new in replacements:
        text = text.replace(old, new)
    after = text.encode()
    if after != before:
        saved = raw / path.relative_to(packet)
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_bytes(before)
        changes.append({"path": str(path.relative_to(packet)),
                        "original_sha256": hashlib.sha256(before).hexdigest(),
                        "published_sha256": hashlib.sha256(after).hexdigest()})
        path.write_bytes(after)
record = packet / "receipts/location-redactions.json"
record.write_text(json.dumps({"rule": "Replace only machine-specific locations; preserve result text and numeric data.", "files": changes}, indent=2) + "\n")
files.append(record)
manifest = packet / "MANIFEST.sha256"
manifest.write_text("".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + str(p.relative_to(packet)) + "\n" for p in sorted(files)))
report = (packet / "REPORT.md").read_text()
assert report.startswith("[R557] NEGATIVE - exact head 60c911b92825a720044e78bed540752c7dd0368e\n")
assert report.endswith("R557-5 FINISHED\n") and "SKELETON" not in report
assert all("scratch" not in p.relative_to(packet).parts for p in files)
print(json.dumps({"publishable_files": len(files), "location_normalized_files": len(changes), "manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest()}))
