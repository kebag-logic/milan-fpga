# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer-owned: re-hash every file an author packet's receipts/INDEX.md lists (16-hex sha256 prefix) and report
# mismatches, missing files and files present but unlisted.  usage: check_index.py RECEIPTS_DIR
import hashlib, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
rows = re.findall(r"^\| `([^`]+)` \| [\d,]+ \| `([0-9a-f]{16})` \|", (root / "INDEX.md").read_text(), re.M)
bad = missing = 0
listed = set()
for path, pre in rows:
    listed.add(path)
    f = root / path
    if not f.is_file():
        missing += 1; print("MISSING", path); continue
    if hashlib.sha256(f.read_bytes()).hexdigest()[:16] != pre:
        bad += 1; print("MISMATCH", path)
present = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {"INDEX.md"}
unlisted = sorted(present - listed)
print(f"listed {len(rows)} matched {len(rows)-bad-missing} mismatched {bad} missing {missing} unlisted {len(unlisted)}")
for u in unlisted[:20]:
    print("UNLISTED", u)
