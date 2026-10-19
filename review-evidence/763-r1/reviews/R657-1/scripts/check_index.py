#!/usr/bin/env python3
"""Compare a receipts INDEX.md (File | Bytes | sha256 table) with the files present beside it, and a publisher
MANIFEST.json (file, original_sha256, published_sha256, path_redacted) with the published tree. Args: evidence root."""
import hashlib, json, re, sys
from pathlib import Path
root = Path(sys.argv[1]); rec = root / "author/receipts"
listed = {m[0]: (int(m[1]), m[2]) for m in re.findall(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$", (rec / "INDEX.md").read_text(), re.M)}
present = {p.relative_to(rec).as_posix(): p for p in rec.rglob("*") if p.is_file() and p.name != "INDEX.md"}
bad = 0
for name in sorted(set(listed) | set(present)):
    if name not in present: print("INDEX lists absent", name); bad += 1; continue
    if name not in listed: print("present but unlisted", name); bad += 1; continue
    data = present[name].read_bytes(); n, h = listed[name]
    if len(data) != n or hashlib.sha256(data).hexdigest() != h:
        print("INDEX mismatch", name, len(data), n, hashlib.sha256(data).hexdigest()[:12], h[:12]); bad += 1
print(f"INDEX rows {len(listed)}, files {len(present)}, mismatches {bad}")
man = json.loads((root / "MANIFEST.json").read_text()); mbad = 0
files = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and p.name != "MANIFEST.json"}
for e in man:
    p = root / e["file"]
    if not p.is_file(): print("MANIFEST lists absent", e["file"]); mbad += 1; continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != e["published_sha256"]: print("MANIFEST mismatch", e["file"]); mbad += 1
    if e["original_sha256"] != e["published_sha256"] or e["path_redacted"]: print("redacted", e["file"], e["path_redacted"])
for f in sorted(files - {e["file"] for e in man}): print("published but not in MANIFEST", f); mbad += 1
print(f"MANIFEST entries {len(man)}, files {len(files)}, mismatches {mbad}")
sys.exit(1 if bad or mbad else 0)
