#!/usr/bin/env python3
"""Download only the selected published author receipts, verifying Git blob IDs."""
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess

packet = Path(__file__).resolve().parents[1]
revision = "2d87396a55ba902af635ae139d24509dc607378e"
prefix = "review-evidence/pp73-r1/author-r5/receipts/r5/"
cache = packet / "scratch/public-evidence-tree.json"
cache.parent.mkdir(exist_ok=True)
if not cache.exists():
    cache.write_bytes(subprocess.check_output(["gh", "api", f"repos/kebag-logic/milan-fpga/git/trees/{revision}?recursive=1"]))
metadata = json.loads(cache.read_text())
files = {f["path"]: f for f in metadata["tree"] if f["type"] == "blob"}
chosen = ["head.sha", "scope-identity.json", "merge-resolution.json", "final-audit.json",
          "observation-identity.json", "rom-identity.tsv", "elaboration-identity.tsv",
          "upstream-elaboration.json", "external-control-results.json", "disabled-checks.json",
          "head-tags.txt", "campaign-bank.json", "planted-drifts.tsv", "head-export-identity.json"]
for stem in ("head-check", "head-lint", "head-suites", "head-yosys", "head-record",
             "head-command-controls", "head-guard-portability", "round4-controls",
             "head-python-check", "head-parent", "rom-identity", "pr-reference-final"):
    chosen += ["logs/" + stem + suffix for suffix in (".log", ".rc", ".meta")]
chosen += ["trace/head/" + name for name in ("executed.log", "executed.rc", "plant.json",
                                             "missing-command-tag.log", "missing-command-tag.rc")]
for variant in ("echo-hide", "echo-control"):
    for step in ("gate", "suite", "write"):
        chosen += [f"review-probes/{variant}.{step}.{ext}" for ext in ("log", "rc")]

def fetch(relative):
    path = prefix + relative
    url = f"repos/kebag-logic/milan-fpga/contents/{path}?ref={revision}"
    data = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github.raw+json", url],
                          capture_output=True, check=True).stdout
    digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    assert digest == files[path]["sha"], path
    target = packet / "receipts/public-author-r5" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return dict(path=path, git_blob=digest, sha256=hashlib.sha256(data).hexdigest(),
                url=f"https://github.com/kebag-logic/milan-fpga/blob/{revision}/{path}")

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(fetch, chosen))
(packet / "receipts/public-provenance.json").write_text(json.dumps(records, indent=2)+"\n")
print(f"Verified and saved {len(records)} published author receipts; no reviewer reports fetched.")
