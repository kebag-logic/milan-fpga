#!/usr/bin/env python3
"""Check the published receipt manifest and index without executing their content."""
import hashlib
import json
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
records = json.loads((root / "MANIFEST.json").read_text())
manifest = {r["file"]: r for r in records}
receipt_root = root / "author/receipts"
files = {p.relative_to(receipt_root).as_posix(): p for p in receipt_root.rglob("*") if p.is_file()}
rows = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$", (receipt_root / "INDEX.md").read_text(), re.M)
indexed = set()
errors = 0
redacted_index = 0
for name, size, digest in rows:
    indexed.add(name)
    p = files.get(name)
    if p is None:
        print("MISSING", name); errors += 1; continue
    b = p.read_bytes()
    actual = hashlib.sha256(b).hexdigest()
    m = manifest["author/receipts/" + name]
    if actual != m["published_sha256"]:
        print("MANIFEST MISMATCH", name); errors += 1
    if (len(b), actual) != (int(size.replace(",", "")), digest):
        known_redaction = m["path_redacted"] and digest == m["original_sha256"]
        print("INDEX DIFF", name, "indexed_bytes", size, "published_bytes", len(b),
              "known_publication_redaction", known_redaction)
        if known_redaction: redacted_index += 1
        else: errors += 1
for name in sorted(set(files) - indexed - {"INDEX.md"}):
    print("UNINDEXED", name); errors += 1
print("index_rows", len(rows), "receipt_files", len(files), "known_redaction_differences", redacted_index, "unexplained_errors", errors)
sys.exit(bool(errors))
