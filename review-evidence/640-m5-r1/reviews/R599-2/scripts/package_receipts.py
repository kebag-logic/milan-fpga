#!/usr/bin/env python3
"""Run in the packet directory; preserve complete logs with local paths normalized.

Only the explicit allowlist is prepared for publication. No scratch tree or
private material is included. The manifest is written separately after REPORT.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

packet = Path.cwd()
repo = Path(sys.argv[1]).resolve()
scratch = packet / "scratch"
receipts = packet / "receipts"
receipts.mkdir(exist_ok=True)
metadata = []


def public(text):
    text = text.replace(str(packet), "<review-packet>")
    text = text.replace(str(repo), "<review-checkout>")
    text = re.sub(r"/[^\s\"'<>]+/pinned-verilator-5\.050/verilator", "<pinned-tools>/verilator", text)
    return re.sub(r"/home/[^\s\"'<>]+", "<local-tool-path>", text)


def copy_log(source, target):
    raw = (scratch / source).read_bytes()
    cleaned = public(raw.decode()).encode()
    (receipts / target).write_bytes(cleaned)
    metadata.append({"receipt": target, "original_sha256": hashlib.sha256(raw).hexdigest(),
                     "published_sha256": hashlib.sha256(cleaned).hexdigest(),
                     "path_normalized": raw != cleaned})


for source, target in [
    ("verified-csr.log", "csr-suite.log"), ("verified-csr.rc", "csr-suite.rc"),
    ("docs-final.log", "docs-final.log"), ("docs-final.rc", "docs-final.rc"),
    ("netlist-verified/summary.txt", "netlist-compare.txt"),
    ("netlist-verified.rc", "netlist-compare.rc"),
    ("netlist-verified/A/yosys.log", "netlist-before.log"),
    ("netlist-verified/B/yosys.log", "netlist-after.log"),
]:
    copy_log(source, target)

pr = json.loads((scratch / "pr722.json").read_text())
head = "c0cba330fd485e52fcb90d5ccc69169edf9f0c2b"
assert pr["head"]["sha"] == head
(receipts / "pr-body-at-review.md").write_text(pr["body"])
issue = json.loads((scratch / "issue640.json").read_text())
scope = [issue["html_url"], issue["body"]]
ids = {5990755268, 5991591637, 5993114362, 6081706413,
       6098404907, 6104904445, 6105372796, 6105430562}
for c in sum(json.loads((scratch / "issue640-comments.json").read_text()), []):
    if c["id"] in ids:
        scope.extend([c["html_url"], c["body"]])
(receipts / "public-scope.txt").write_text("\n\n".join(scope) + "\n")

def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args]).decode()

(receipts / "delta.diff").write_text(git("diff", "988ec7f6", head))
(receipts / "history.txt").write_text(git("log", "--format=%H %P %s", "e8454e27.." + head))

handoff = (scratch / "public-HANDOFF.md").read_bytes()
entry = next(x for x in json.loads((scratch / "public-MANIFEST.json").read_text())
             if x["file"] == "author/HANDOFF.md")
assert hashlib.sha256(handoff).hexdigest() == entry["published_sha256"]
measurement = [
    "Public round-one evidence: https://github.com/kebag-logic/milan-fpga/blob/648503cfeee36d03d7baf2a7b8608e1310caae49/review-evidence/640-m5-r1/author/HANDOFF.md",
    "Downloaded bytes match published MANIFEST.json: " + entry["published_sha256"],
    "This immutable round-one snapshot precedes the public round-two correction.",
    "Current correction: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6105430562",
    "Current PR body captured in pr-body-at-review.md.",
    "Disjoint routed change: -121 + -342 + -227 = " + str(-121 - 342 - 227),
    "Outside CSR: -690 - (-121) = " + str(-690 + 121),
    "Nested u_pp -344 lies inside wrapper -342 and is not added.",
    "Partial central: 37957 + (600 - 121) = " + str(37957 + 600 - 121),
    "Excess above target: 38436 - 38040 = " + str(38436 - 38040),
]
for name, a, b in [("base alone", 2955, 3038), ("base proxy", 2058, 2494),
                   ("M5 alone", 2515, 2859), ("M5 proxy", 1903, 2295)]:
    measurement.append(f"{name}: ({b} - {a}) / (8 - 1) = {(b-a)/7:.6f} LUT per stream")
measurement += ["#649 in-datapath fit: 210.6 LUT/stream, N=1,2,4; tracked 8x8 excluded as another shape.",
                "These slopes are not a like-for-like reproduction of that fit.",
                "Routed CSR saving 3037 - 2916 = 121; post-synthesis 3130 - 3003 = 127.",
                "Timing: +0.097 >= max(+0.030, +0.299 - 0.250) = +0.049 ns.",
                "No new route executed; figures above are checked arithmetic over published author receipts."]
(receipts / "measurement-check.txt").write_text("\n".join(measurement) + "\n")

jobs = ["name\tstatus\tconclusion\thead\turl\tsuccessful steps\tskipped steps"]
steps = ["job\tstep\tname\tstatus\tconclusion"]
for source in sorted(scratch.glob("hosted-jobs-*.json")):
    for j in json.loads(source.read_text()).get("jobs", []):
        assert j["head_sha"] == head
        ss = j.get("steps", [])
        jobs.append("\t".join(map(str, [j["name"], j["status"], j["conclusion"],
            j["head_sha"], j["html_url"], sum(s["conclusion"] == "success" for s in ss),
            sum(s["conclusion"] == "skipped" for s in ss)])))
        for s in ss:
            steps.append("\t".join(map(str, [j["name"], s["number"], s["name"], s["status"], s["conclusion"]])))
stamp = "Captured " + datetime.now(timezone.utc).isoformat() + "; read-only snapshot, not acceptance.\n"
(receipts / "hosted-jobs.tsv").write_text(stamp + "\n".join(jobs) + "\n")
(receipts / "hosted-steps.tsv").write_text(stamp + "\n".join(steps) + "\n")
(receipts / "log-provenance.json").write_text(json.dumps(metadata, indent=2) + "\n")
print("Prepared explicit receipt allowlist; private paths normalized, no verdicts or counts changed.")
