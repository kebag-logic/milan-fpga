#!/usr/bin/env python3
"""Copy receipts for publication, replacing only local workspace locations."""
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("repository", type=Path)
p.add_argument("packet", type=Path)
a = p.parse_args()
root, packet = a.repository.resolve(), a.packet.resolve()
raw = packet/"scratch/raw-checks"
items = [(f, packet/"receipts/checks"/f.name) for f in raw.iterdir() if f.is_file()]
items += [(packet/"scratch/probe-results.json", packet/"receipts/probe-results.json"), (packet/"scratch/checks/mutations/results.json", packet/"receipts/mutation-results.json"), (packet/"scratch/clone.log", packet/"receipts/clone.log")]
items += [(f,packet/"receipts/graphs"/f.name) for f in (packet/"scratch/checks/graphs").glob("*.svg")]
replacements = [(str(packet/"scratch"), "$REVIEW_SCRATCH"), (str(root), "$REPOSITORY"), (str(packet), "$REVIEW_PACKET")]
records = []
for source,target in items:
    original = source.read_bytes()
    text = original.decode()
    for old,new in replacements:
        text = text.replace(old,new)
    published = text.encode()
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(published)
    records.append({"receipt":str(target.relative_to(packet)),"original_sha256":hashlib.sha256(original).hexdigest(),"published_sha256":hashlib.sha256(published).hexdigest(),"location_redacted":published != original})
(packet/"receipts/location-redactions.json").write_text(json.dumps(records,indent=2)+"\n")
print(f"Prepared {len(records)} receipts; original outputs remain in scratch.")
