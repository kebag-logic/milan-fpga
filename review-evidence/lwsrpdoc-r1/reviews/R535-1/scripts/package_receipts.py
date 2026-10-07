#!/usr/bin/env python3
"""Audit and hash publishable artifacts, excluding all disposable content.

Usage: python3 scripts/package_receipts.py SOURCE PACKET
REVIEW_FORBIDDEN_PATTERN supplies an optional local privacy pattern.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

source, packet = map(lambda p: Path(p).resolve(), sys.argv[1:3])
head = "5f9b9d99e1d94485fc00a1b1539baf2ae861cb65"
pattern = os.environ.get("REVIEW_FORBIDDEN_PATTERN")
privacy = re.compile(pattern, re.IGNORECASE) if pattern else None
pages = sorted(list(source.glob("*.md")) + list((source / "doc").rglob("*.md")))
source_issues = []
for path in pages:
    body = path.read_text()
    assert body.startswith("<!-- SPDX-License-Identifier: Apache-2.0 -->")
    if privacy and privacy.search(body):
        source_issues.append(str(path.relative_to(source)))
assert not source_issues
paths = [packet / "REPORT.md"]
for folder in ("scripts", "receipts", "graphs", "diagrams"):
    paths.extend(p for p in (packet / folder).rglob("*") if p.is_file())
leaks = []
for path in paths:
    if path.suffix == ".png":
        continue
    text = path.read_text()
    if privacy and privacy.search(text):
        leaks.append(str(path.relative_to(packet)))
assert not leaks, leaks
report = (packet / "REPORT.md").read_text()
assert report.startswith("[R535] NEGATIVE - exact head " + head + "\n")
assert report.rstrip().endswith("R535-1 FINISHED")
assert "SKELETON" not in report
assert "[R535] INCOMPLETE" not in report
missing = []
for href in re.findall(r"\]\(([^)]+)\)", report):
    if "://" not in href and not (packet / href.split("#")[0]).exists():
        # The two files below are created by this packaging operation.
        if href not in ("MANIFEST.sha256", "receipts/publication-audit.json"):
            missing.append(href)
assert not missing, missing
result = dict(exact_head=head, source_pages=len(pages), all_page_license_identifiers=True,
              source_privacy_matches=source_issues, packet_privacy_matches=leaks,
              report_relative_links_missing=missing, skeleton_absent=True,
              scratch_excluded=True, privacy_pattern_supplied=bool(privacy))
(packet / "receipts/publication-audit.json").write_text(json.dumps(result,indent=2)+"\n")
paths = [packet / "REPORT.md"]
for folder in ("scripts", "receipts", "graphs", "diagrams"):
    paths.extend(p for p in (packet / folder).rglob("*") if p.is_file())
manifest = []
for path in sorted(paths):
    manifest.append(hashlib.sha256(path.read_bytes()).hexdigest()+"  "+str(path.relative_to(packet)))
(packet / "MANIFEST.sha256").write_text("\n".join(manifest)+"\n")
subprocess.run(["sha256sum", "--check", "--quiet", "MANIFEST.sha256"],cwd=packet,check=True)
print(json.dumps(dict(published_files=len(paths), checksum_verification_rc=0, **result),indent=2))
