"""Check the published author-r2 evidence: every file's bytes against the
publication manifest, and every SHA256SUMS entry against the manifest's
original hash (paths redacted at publication change the published bytes)."""
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])            # .../review-evidence/640-m10-r1
lane = sys.argv[2]                          # author-r2
man = {e["file"]: e for e in json.load(open(root / "MANIFEST.json"))}
bad = 0; n = 0; red = 0
for p in sorted((root / lane).rglob("*")):
    if not p.is_file(): continue
    rel = str(p.relative_to(root)); n += 1
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    e = man.get(rel)
    if e is None: print("NOT IN MANIFEST", rel); bad += 1; continue
    if e["published_sha256"] != h: print("PUBLISHED MISMATCH", rel); bad += 1
    if e["path_redacted"]: red += 1
sums = root / lane / "evidence" / "SHA256SUMS"
for line in sums.read_text().splitlines():
    h, f = line.split(None, 1); f = f.lstrip("*").removeprefix("./")
    rel = f"{lane}/evidence/{f}"
    e = man.get(rel)
    if e is None: print("SUMS ENTRY NOT PUBLISHED", rel); continue
    if e["original_sha256"] != h: print("ORIGINAL MISMATCH", rel); bad += 1
missing = [k for k in man if k.startswith(lane + "/") and not (root / k).is_file()]
print(f"files {n}, redacted {red}, manifest-only {len(missing)}, mismatches {bad}")
for k in missing: print("MISSING LOCALLY", k)
sys.exit(1 if bad else 0)
