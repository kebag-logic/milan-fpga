#!/usr/bin/env python3
"""Compare receipt index and generated provenance to immutable source objects."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

p = argparse.ArgumentParser()
p.add_argument("repo", type=Path)
p.add_argument("packet", type=Path)
a = p.parse_args()
repo, packet = a.repo.resolve(), a.packet.resolve()
base = "e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f"
head = "07c6c72fce79e705bcf28a70071497d0ce7040e4"
def git(*args):
    return subprocess.check_output(["git", *args], cwd=repo)
def sha(data):
    return hashlib.sha256(data).hexdigest()

root = packet / "scratch/public/author/receipts"
rows = re.findall(r"^\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|$",
                  (root / "INDEX.md").read_text(), re.M)
files = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
assert {r[0] for r in rows} == files - {"INDEX.md"}
for path, count, digest in rows:
    data = (root / path).read_bytes()
    assert len(data) == int(count) and sha(data) == digest, path
(packet / "receipt-index-audit.json").write_text(json.dumps({
    "rows": len(rows), "membership_equal": True,
    "all_sizes_and_hashes_equal": True}, indent=2) + "\n")

inventory = json.loads((repo / "ci/image/tool-inventory.json").read_text())
stale = []
for path, recorded in inventory["inputs"].items():
    actual = sha((repo / path).read_bytes())
    if actual != recorded:
        previous = sha(git("show", f"{base}:{path}"))
        stale.append({"path": path, "recorded": recorded, "base": previous,
                      "head": actual, "introduced_by_delta": previous == recorded})
(packet / "inventory-provenance.json").write_text(json.dumps({
    "base": base, "head": head, "stale_inputs": stale}, indent=2) + "\n")
print("Receipt index verified:", len(rows), "rows")
print("Stale inventory inputs:", len(stale))
for row in stale:
    print(row["path"], "NEW" if row["introduced_by_delta"] else "PRE-EXISTING")

extract = (root / "round-b/gates/test_ctrl_firmware/extract.log").read_text()
campaign = [line for line in extract.splitlines() if line.startswith("[ok]")]
normal = [line for line in campaign if line.startswith("[ok] arm ")]
control = [line for line in campaign if line.startswith("[ok] mutant ")]
pins = [line for line in campaign if line.startswith("[ok] lwSRP pin,")]
import sys
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_mutants
start = len(normal) + len(control)
aecp = campaign[start:start + len(aecp_mutants.DEFECTS)]
assert all(line.startswith("[ok] " + d.name + ":")
           for line, d in zip(aecp, aecp_mutants.DEFECTS))
other = campaign[start + len(aecp):len(campaign) - len(pins)]
(packet / "public-gate-audit.json").write_text(json.dumps({
    "evidence_revision": "c262f8de6c498f412312ad3abd96437c9d25e594",
    "firmware_extract_final": extract.splitlines()[-1],
    "all_ok_lines_including_normal_arms": len(campaign),
    "normal_arm_outcomes": len(normal),
    "control_source_mutant_outcomes": len(control),
    "aecp_source_mutant_outcomes": len(aecp),
    "remaining_srp_source_mutant_outcomes": len(other),
    "pin_refusal_outcomes": len(pins),
    "source_mutant_outcomes_total": len(control) + len(aecp) + len(other),
    "new_mutants": [line for line in campaign if "nvm-empty-map-keeps-defaults" in line
                    or "nvm-unused-payload-reads-erased" in line],
    "published_full_log": False,
    "published_extract_and_summary": True,
    "source_evidence_owner": "author",
    "manager_source_bank": "not run",
}, indent=2) + "\n")
