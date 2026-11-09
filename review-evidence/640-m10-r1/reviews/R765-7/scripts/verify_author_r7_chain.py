#!/usr/bin/env python3
"""Verify the author-r7 receipt hash chain on the public evidence commit.

Usage: python3 -I verify_author_r7_chain.py <repo> <evidence-commit> [prefix] [lane]

For every file under <prefix>/<lane> (default author-r7) in <evidence-commit>:
  - the published blob's sha256 must equal MANIFEST.json's published_sha256;
  - the author's evidence/SHA256SUMS entry must equal MANIFEST.json's
    original_sha256;
  - original != published only where MANIFEST.json sets path_redacted.
Exit status 0 only when every check holds.
"""
import hashlib, json, subprocess, sys

repo, commit = sys.argv[1], sys.argv[2]
prefix = sys.argv[3] if len(sys.argv) > 3 else "review-evidence/640-m10-r1"
lane = sys.argv[4] if len(sys.argv) > 4 else "author-r7"

def git(*a):
    return subprocess.check_output(["git", "-C", repo, *a])

manifest = json.loads(git("show", f"{commit}:{prefix}/MANIFEST.json"))
m = {e["file"]: e for e in manifest if e["file"].startswith(lane + "/")}
files = [p.decode() for p in git("ls-tree", "-r", "--name-only", commit, "--", f"{prefix}/{lane}").splitlines()]
rel = [f[len(prefix) + 1:] for f in files]
sums = {}
for line in git("show", f"{commit}:{prefix}/{lane}/evidence/SHA256SUMS").decode().splitlines():
    h, p = line.split(None, 1)
    p = p.lstrip("*")
    if p.startswith("./"):
        p = p[2:]
    sums[p] = h

bad = 0
redacted = 0
for r in rel:
    pub = hashlib.sha256(git("cat-file", "blob", f"{commit}:{prefix}/{r}")).hexdigest()
    e = m.get(r)
    if e is None:
        print("NOT IN MANIFEST", r); bad += 1; continue
    if pub != e["published_sha256"]:
        print("PUBLISHED MISMATCH", r); bad += 1
    if (e["original_sha256"] != e["published_sha256"]) != bool(e["path_redacted"]):
        print("REDACTION FLAG INCONSISTENT", r); bad += 1
    redacted += bool(e["path_redacted"])
    inner = r[len(lane) + 1:]
    if inner in sums and sums[inner] != e["original_sha256"]:
        print("SHA256SUMS != original", r); bad += 1
for inner, h in sums.items():
    r = f"{lane}/{inner}"
    if r not in m:
        print("SHA256SUMS entry absent from manifest/tree:", inner)
    elif r not in rel:
        print("SHA256SUMS entry not published:", inner)
extra = set(m) - set(rel)
for x in sorted(extra):
    print("MANIFEST entry not in tree:", x); bad += 1
print(f"files={len(rel)} manifest_entries={len(m)} sums_entries={len(sums)} redacted={redacted} bad={bad}")
sys.exit(1 if bad else 0)
