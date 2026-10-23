"""Check an evidence commit's MANIFEST.json entries against the blobs in that commit.

usage: python3 -I verify_evidence_manifest.py <bare-repo> <commit> <dir> <path-prefix>
Prints the manifest's entry shape, then hashes every listed file under the prefix.
"""
import hashlib, json, subprocess, sys

repo, commit, base, prefix = sys.argv[1:5]

def show(path):
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:{path}"],
                          check=True, capture_output=True).stdout

m = json.loads(show(f"{base}/MANIFEST.json"))
print("entries", len(m), "example", json.dumps(m[0])[:300])
keys = m[0].keys()
pk = next(k for k in ("path", "file", "name") if k in keys)
hk = next(k for k in ("published_sha256", "sha256", "hash", "digest") if k in keys)
sel = [e for e in m if e[pk].startswith(prefix)]
bad = 0
for e in sel:
    p = e[pk]
    full = p if p.startswith(base) else f"{base}/{p}"
    try:
        h = hashlib.sha256(show(full)).hexdigest()
    except subprocess.CalledProcessError:
        print("MISSING", p); bad += 1; continue
    if h != e[hk]:
        print("MISMATCH", p); bad += 1
print(f"prefix {prefix}: {len(sel)} listed, {bad} missing or mismatched")
