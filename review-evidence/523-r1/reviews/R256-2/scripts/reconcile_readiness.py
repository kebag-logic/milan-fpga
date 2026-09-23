#!/usr/bin/env python3
"""Reviewer receipt: reconcile the #523 readiness bundle's nested SHA256SUMS
with the outer immutable MANIFEST.json (original_sha256/published_sha256).

Usage: reconcile_readiness.py EXTRACTED_ROOT
EXTRACTED_ROOT holds review-evidence/517-r1/{MANIFEST.json,followups/523-readiness/}
from public commit b9a05dc9a31825fdbd7ffc5eb638dc9fe751fc6c.
"""
import hashlib, json, sys
from pathlib import Path

root = Path(sys.argv[1]) / "review-evidence/517-r1"
bundle = root / "followups/523-readiness"
manifest = {row["file"]: row for row in json.loads((root / "MANIFEST.json").read_text())}
nested = {}
for line in (bundle / "SHA256SUMS").read_text().splitlines():
    digest, name = line.split(None, 1)
    nested[name.lstrip("*")] = digest
files = sorted(str(p.relative_to(bundle)) for p in bundle.rglob("*") if p.is_file())
rows, problems = [], []
for name in files:
    public = hashlib.sha256((bundle / name).read_bytes()).hexdigest()
    entry = manifest.get(f"followups/523-readiness/{name}")
    if entry is None:
        problems.append(f"no outer manifest entry: {name}")
        continue
    row = dict(file=name, public_sha256=public,
               outer_published_matches=entry["published_sha256"] == public,
               outer_original=entry["original_sha256"],
               path_redacted=entry.get("path_redacted"),
               nested=nested.get(name),
               nested_matches_public=nested.get(name) == public,
               nested_matches_outer_original=nested.get(name) == entry["original_sha256"])
    rows.append(row)
    if not row["outer_published_matches"]:
        problems.append(f"public bytes differ from outer published digest: {name}")
    if name != "SHA256SUMS" and not row["nested_matches_public"]:
        if not row["nested_matches_outer_original"]:
            problems.append(f"nested digest matches neither public nor original: {name}")
        if entry["original_sha256"] == entry["published_sha256"]:
            problems.append(f"nested refusal without a recorded publication change: {name}")
refused = [r["file"] for r in rows if r["file"] != "SHA256SUMS" and not r["nested_matches_public"]]
print(json.dumps(dict(files=len(rows), outer_entries_for_bundle=sum(1 for k in manifest if k.startswith("followups/523-readiness/")),
                      nested_entries=len(nested), nested_refusals=refused,
                      refusals_explained_by_outer_original=all(r["nested_matches_outer_original"] for r in rows if r["file"] in refused),
                      refused_files_path_redacted=all(r["path_redacted"] for r in rows if r["file"] in refused),
                      unrefused_files_unchanged=all(r["outer_original"] == r["public_sha256"] for r in rows if r["file"] not in refused and r["file"] != "SHA256SUMS"),
                      problems=problems), indent=2))
print(json.dumps(rows, indent=1))
sys.exit(1 if problems else 0)
