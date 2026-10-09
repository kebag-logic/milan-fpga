#!/usr/bin/env python3
"""Read pinned published execution receipts and verify publisher hashes.
Usage: fetch_public_evidence.py PACKET
"""
import concurrent.futures, hashlib, json, subprocess, sys
from pathlib import Path
packet = Path(sys.argv[1])
ref = "1570e00395c98ed4ea1c21e6abde28948346c82b"
prefix = "review-evidence/pp168-r1/"
def fetch(path):
    return subprocess.check_output(["gh", "api", "repos/kebag-logic/milan-fpga/contents/" + prefix + path + "?ref=" + ref,
        "-H", "Accept: application/vnd.github.raw+json"])
manifest = json.loads(fetch("MANIFEST.json"))
exact = {
    "author/round2-recovery/area-summary.json",
    "author/round2-recovery/head-logs/suites.log",
    "author/round2-recovery/base-logs/suites.log",
    "author/round2-recovery/head-logs/pp_top-acmp_mutants.log",
    "author/round2-recovery/head-logs/pp_top-acmp_mutants-receipt.json",
    "author/round2-recovery/head-logs/suites-receipt.json",
    "author/round2-recovery/base-logs/suites-receipt.json",
    "author/round2-recovery/head-campaigns/pp_top-acmp_mutants/retry_status_cleared@acmp_listener.log",
    "author/round2-recovery/head-campaigns/pp_top-acmp_mutants/retry_probe_status_cleared@acmp_listener.log",
    "author/round2-recovery/head-campaigns/pp_top-acmp_mutants/retry_probe_status_cleared@pp_top.log",
    "author/round2-recovery/comparison/processor-gate-records.json"
}
selected = [x for x in manifest if x["file"] in exact or
    (x["file"].endswith(".rc") and any(x["file"].startswith("author/round2-recovery/" + d + "/")
     for d in ["base-logs", "head-logs", "parent-base", "parent-head"]))]
assert exact <= {x["file"] for x in selected}
def one(item):
    raw = fetch(item["file"])
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == item["published_sha256"], item["file"]
    dest = packet / "receipts" / "public" / item["file"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    return {"path": str(dest.relative_to(packet)), "sha256": digest,
        "url": "https://github.com/kebag-logic/milan-fpga/blob/" + ref + "/" + prefix + item["file"]}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    records = list(pool.map(one, selected))
(packet / "receipts" / "public-evidence-fetch.json").write_text(json.dumps(records, indent=2) + "\n")
print("Verified published hashes for", len(records), "execution receipts at", ref)
