#!/usr/bin/env python3
"""Fetch only public execution evidence at an immutable commit; verify published hashes."""
import base64, concurrent.futures, hashlib, json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parent
COMMIT = "8ed1c7b682059c1a97c191a756eb8b536098750d"
REPO = "repos/kebag-logic/milan-fpga"
def api(path):
    return json.loads(subprocess.check_output(["gh", "api", REPO + path]))
manifest = api("/contents/review-evidence/748-r1/MANIFEST.json?ref=" + COMMIT)
raw = base64.b64decode(manifest["content"])
(ROOT / "public-manifest.json").write_bytes(raw)
records = {r["file"]: r for r in json.loads(raw)}
tree = api("/git/trees/4d094697708c4bf8b20f338e88b59c4a815b915e?recursive=1")
selected = [r for r in tree["tree"] if r["type"] == "blob" and
            r["path"].startswith("author-r2/evidence/round2/") and
            "-d55bfa97/" not in r["path"]]
def fetch(row):
    data = base64.b64decode(api("/git/blobs/" + row["sha"])["content"])
    checksum = hashlib.sha256(data).hexdigest()
    assert checksum == records[row["path"]]["published_sha256"], row["path"]
    dest = ROOT / "public-evidence" / row["path"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {"path": row["path"], "sha256": checksum, "git_blob": row["sha"],
            "path_redacted": records[row["path"]]["path_redacted"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    checked = list(pool.map(fetch, selected))
verification = api("/commits/" + COMMIT)["commit"]["verification"]
report = {"commit": COMMIT, "verification": verification, "verified_files": checked}
(ROOT / "evidence-verification.json").write_text(json.dumps(report, indent=2) + "\n")
print(f"PASS: {len(checked)} public execution files match published SHA256 manifest")
print("Commit signature status:", verification["reason"])
