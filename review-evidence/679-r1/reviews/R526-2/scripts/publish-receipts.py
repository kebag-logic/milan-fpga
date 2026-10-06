"""Copy selected raw receipts with local path/color normalization and hash provenance.

Usage: python3 publish-receipts.py CHECKOUT PACKET
Original outputs remain in scratch and are never in the publication manifest.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

root, packet = map(lambda x: Path(x).resolve(), sys.argv[1:])
names = ["sdk-install", "ctrl-campaign", "nvm-campaign", "coverage", "rv32-controls",
         "ctrl-unit", "nvm-unit", "sdk-controls", "tally-controls", "coverage-controls",
         "ci-events-check", "ci-events-controls", "ci-scope-controls", "docs-check", "doc-style",
         "em-dash", "toc-check", "renderer-install", "em-dash-locked", "toc-check-locked",
         "runtime-binding", "local-data"]
files = [name + ".log" for name in names] + ["check-results.json", "docs-rerun-results.json"]
records = []
for name in files:
    original = (packet / "scratch" / name).read_bytes()
    text = original.decode()
    text = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", text)
    text = text.replace(str(root), "<review-checkout>").replace(str(packet), "<review-packet>")
    text = re.sub(r"(SDK archive verified: )\S+\.tar\.xz", r"\1<sdk-archive>", text)
    text = re.sub(r"/home/[^/\s]+", "<user-home>", text)
    published = text.encode()
    (packet / "receipts" / name).write_bytes(published)
    records.append({"path": "receipts/" + name,
                    "raw_sha256": hashlib.sha256(original).hexdigest(),
                    "published_sha256": hashlib.sha256(published).hexdigest(),
                    "normalized": original != published})
(packet / "receipts/scrub-receipt.json").write_text(json.dumps({
    "policy": "Only local paths and terminal color normalized; no measurement, verdict or command option changed.",
    "files": records}, indent=2) + "\n")
print(f"Prepared {len(records)} receipts with raw and publication hashes")
