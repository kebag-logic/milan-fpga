"""Check a packet's manifest-1.jsonl (file, bytes, sha256) against the files.

Usage: python3 -I verify_manifest.py <receipts-dir>
Prints one line per entry and a tally; exit 1 if any entry mismatches or is missing.
"""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
ok = bad = 0
listed = set()
for line in (root / "manifest-1.jsonl").read_text().splitlines():
    if not line.strip():
        continue
    row = json.loads(line)
    listed.add(row["file"])
    path = root / row["file"]
    if not path.is_file():
        print("MISSING", row["file"]); bad += 1; continue
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    same = digest == row["sha256"] and len(data) == row["bytes"]
    ok += same; bad += not same
    print("OK " if same else "DIFF", row["file"], len(data), row["bytes"])
unlisted = sorted(p.name for p in root.iterdir() if p.name not in listed and p.name != "manifest-1.jsonl")
print(f"entries ok={ok} mismatched_or_missing={bad} unlisted_files={unlisted}")
sys.exit(1 if bad else 0)
