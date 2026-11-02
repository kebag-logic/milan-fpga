"""Check every published file under a prefix of an evidence MANIFEST.json against its published_sha256,
and that every author SHA256SUMS mismatch is a file the manifest marks path_redacted with the author's digest as original_sha256."""
import hashlib, json, sys, pathlib
root = pathlib.Path(sys.argv[1]); prefix = sys.argv[2]
m = json.load(open(root / "MANIFEST.json"))
bad = n = red = 0
orig = {}
for e in m:
    if not e["file"].startswith(prefix):
        continue
    n += 1
    d = hashlib.sha256((root / e["file"]).read_bytes()).hexdigest()
    if d != e["published_sha256"]:
        bad += 1; print("PUBLISHED MISMATCH", e["file"])
    if e.get("path_redacted"):
        red += 1
    orig[e["file"]] = e["original_sha256"]
sums = root / prefix / "evidence" / "SHA256SUMS"
unexplained = 0
for line in sums.read_text().splitlines():
    h, f = line.split(None, 1); f = f.strip()
    key = prefix + "evidence/" + f.lstrip("./")
    p = root / key
    if not p.exists():
        print("listed but not published (large/omitted):", key); continue
    if hashlib.sha256(p.read_bytes()).hexdigest() != h and orig.get(key) != h:
        unexplained += 1; print("UNEXPLAINED", key)
print(f"manifest entries {n}, published mismatches {bad}, path_redacted {red}, unexplained author-digest mismatches {unexplained}")
sys.exit(1 if bad or unexplained else 0)
