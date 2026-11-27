"""Check a published author packet against its own inventory and the publisher manifest.

Usage: python3 -I verify_publication.py <artysplit-r1 dir> [<parent MANIFEST.json>]

1. Every row of author-r8/receipts/FILES.tsv (reassembled from its parts) is
   compared with the bytes on disk (size and SHA256).
2. Every publisher MANIFEST.json entry under author-r8/receipts/census-extract
   must have original_sha256 == published_sha256 == SHA256 of the file on disk,
   and equal the FILES.tsv row for that file.
3. If a parent MANIFEST.json is given, every entry that changed between the two
   manifests is listed, and its new published hash must equal the original.
"""
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
rec = root / "author-r8" / "receipts"
PFX = "author-r8/receipts/"
CE = PFX + "census-extract/"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


fm = json.loads((rec / "FILES.manifest.json").read_text())
tsv = b"".join((rec / p["file"]).read_bytes() for p in fm["parts"])
assert hashlib.sha256(tsv).hexdigest() == fm["sha256"] and len(tsv) == fm["bytes"], "FILES.tsv parts"
rows = {}
for line in tsv.decode().splitlines()[1:]:
    path, n, h = line.split("\t")
    rows[path] = (int(n), h)

bad = []
for path, (n, h) in sorted(rows.items()):
    p = rec / path
    if not p.is_file():
        bad.append(("missing", path))
        continue
    if p.stat().st_size != n or sha(p) != h:
        bad.append(("differs", path))
on_disk = {str(p.relative_to(rec)) for p in rec.rglob("*") if p.is_file()}
unlisted = sorted(on_disk - set(rows) - {"FILES.manifest.json"}
                  - {p["file"] for p in fm["parts"]})
print(f"inventory rows={len(rows)} differs_or_missing={len(bad)} unlisted={unlisted}")
for b in bad:
    print("  INVENTORY", *b)

man = json.loads((root / "MANIFEST.json").read_text())
ce = [e for e in man if e["file"].startswith(CE)]
mbad = 0
for e in ce:
    rel = e["file"][len(PFX):]
    disk = sha(root / e["file"])
    ok = (e["original_sha256"] == e["published_sha256"] == disk
          and rows.get(rel, (None, None))[1] == disk)
    if not ok:
        mbad += 1
        print("  MANIFEST-MISMATCH", e)
ce_files = {str(p.relative_to(root)) for p in (rec / "census-extract").rglob("*") if p.is_file()}
not_in_man = sorted(ce_files - {e["file"] for e in ce})
red = sum(1 for e in ce if e["path_redacted"])
print(f"census-extract manifest entries={len(ce)} files_on_disk={len(ce_files)} "
      f"mismatches={mbad} path_redacted_true={red} on_disk_not_in_manifest={not_in_man}")

if len(sys.argv) > 2:
    old = {e["file"]: e for e in json.loads(pathlib.Path(sys.argv[2]).read_text())}
    changed = [e for e in man if old.get(e["file"]) != e]
    print(f"manifest entries changed vs parent: {len(changed)}")
    for e in changed:
        o = old.get(e["file"])
        print(f"  {e['file']} parent_pub={o and o['published_sha256'][:12]} "
              f"parent_redacted={o and o['path_redacted']} now_pub={e['published_sha256'][:12]} "
              f"orig==pub={e['original_sha256'] == e['published_sha256']} redacted={e['path_redacted']}")
    gone = sorted(set(old) - {e['file'] for e in man})
    print(f"entries removed vs parent: {gone}")

ok = not bad and not mbad and not not_in_man
print("RESULT:", "PASS" if ok else "FAIL", f"listed={len(rows)}")
sys.exit(0 if ok else 1)
