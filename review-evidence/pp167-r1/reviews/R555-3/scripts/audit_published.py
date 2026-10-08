#!/usr/bin/env python3
"""Check published receipt hashes, original-index provenance and return codes."""
import hashlib
import json
from pathlib import Path

packet = Path(__file__).resolve().parents[1]
r = packet / "receipts"
manifest = json.loads((r / "public-publication-manifest.json").read_text())
index = json.loads((r / "public-author/evidence-index.json").read_text())
records = []
for file in sorted((r / "public-author").glob("*.json")):
    path = "author-r2/round2/" + file.name
    m = next(x for x in manifest if x["file"] == path)
    assert hashlib.sha256(file.read_bytes()).hexdigest() == m["published_sha256"]
    original = next((x for x in index if x["file"] == file.name), None)
    if original:
        assert original["sha256"] == m["original_sha256"]
    records.append({"file": path, "publication_hash_verified": True,
                    "original_index_verified": bool(original), "path_redacted": m["path_redacted"]})
gates = json.loads((r / "public-author/final-receipts.json").read_text())
def return_codes(obj):
    if isinstance(obj, dict):
        if "rc" in obj:
            yield obj["rc"]
        for value in obj.values():
            yield from return_codes(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from return_codes(value)
codes = list(return_codes(gates))
assert len(codes) == 64 and all(x == 0 for x in codes)
plants = {}
for name in ("base", "head"):
    rows = json.loads((r / f"public-author/plant-{name}.json").read_text())
    assert all(x["passed"] for x in rows)
    plants[name] = len(rows)
result = {"publication_commit": "5a59492617aa18d116fe881ceffe24b17aa4f9ba",
          "files": records, "source_base": gates["base"], "source_head": gates["head"],
          "gate_return_codes": codes, "reported_successful_plant_operations": plants}
(r / "public-publication-audit.json").write_text(json.dumps(result, indent=2) + "\n")
print(f"PASS: {len(records)} publication hashes; 64 zero gate returns; plants {plants}")
