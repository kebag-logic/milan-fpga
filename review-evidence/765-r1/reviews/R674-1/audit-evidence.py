#!/usr/bin/env python3
"""Check the published receipt hashes and selected exact-head claims."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

repo, packet = map(lambda p: Path(p).resolve(), sys.argv[1:])
public = packet / "scratch/review-evidence/765-r1"
receipts = public / "author/receipts"
head = "75db4b57cff47bb614d14dead084649a4c2aa2a3"
base = "78ca9bdf104819265588726bce4322696c38b8c2"
def git(*args):
    return subprocess.check_output(["git", "-C", str(repo), *args])
count = 0
for item in json.loads((public / "MANIFEST.json").read_text()):
    if not item["file"].startswith("author/receipts/"):
        continue
    data = (public / item["file"]).read_bytes()
    assert hashlib.sha256(data).hexdigest() == item["published_sha256"], item["file"]
    count += 1
print("Published author receipt hashes verified:", count)
for ancestor in ["4191b098", "cc71db3a", "2f33a9ce", "4605409b", base]:
    subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", ancestor, head], check=True)
    print("Preserved ancestor:", ancestor)
for path in ["hdl/milan/milan_datapath.sv"]:
    assert git("show", f"{base}:{path}") == git("show", f"{head}:{path}")
    print("Byte-identical to merged dev:", path)
for path in ["hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv", "hdl/ieee1722/crf/KL_crf_rx.sv"]:
    before, after = [git("show", f"{rev}:{path}").decode() for rev in [base, head]]
    assert before[before.index("\nmodule "):before.index("\n);")] == after[after.index("\nmodule "):after.index("\n);")]
    if "avtp" in path:
        # Everything downstream of the format comparator is unchanged.
        marker = "  wire [7:0] expected_w"
    else:
        marker = "  wire [63:0] w_crf_ts"
    assert before[before.index(marker):] == after[after.index(marker):]
    print("Unchanged module interface and downstream state/counter logic:", path)
subdiff = git("diff", "--raw", base, head, "--", "protocol-processor", "gptp-processor", "third_party", "hdl/common/csr", "configs").strip()
assert not subdiff
print("No #765 CSR decode, configuration or gitlink delta")
r = receipts / "round1c"
for name in ["sweep-s0", "sweep-s1", "static", "tsnfuzz", "yosys", "xvlog", "builder", "dp762-mutants", "unb"]:
    assert head in (r / name / "HEAD.txt").read_text()
    print("Exact source head recorded:", name)
summary = (r / "dp762-mutants/SUMMARY.tsv").read_text().splitlines()
assert len(summary) == 8
assert sum("\tPASS\t" in line for line in summary) == 2
assert sum("\tCAUGHT\t" in line for line in summary) == 6
for name in ["clean", "mut-tie0", "mut-sink1", "mut-bound"]:
    for shape, suffix in [("dynmap", ".log"), ("nxn4c", ".log.tail")]:
        text = (r / "dp762-mutants" / f"{name}.{shape}{suffix}").read_text()
        failed = [line.strip() for line in text.splitlines() if "[FAIL]" in line]
        print("DP wiring receipt:", name, shape, "failure lines:", len(failed))
        for line in failed:
            print(" ", line)
        expected_failures = 0 if name == "clean" else 1 if name == "mut-bound" else 2
        assert re.search(rf"checks:\s+\d+\s+failures:\s+{expected_failures}\b", text)
        if shape == "dynmap":
            assert len(failed) == expected_failures
        else:
            print("  Published 200-line tail verifies total only; named failures are in driver.log and SUMMARY.tsv.")
        if shape == "dynmap":
            parameters = "\n".join(line for line in text.splitlines() if "[i]    elaborated" in line) + "\n"
            digest = hashlib.sha256(parameters.encode()).hexdigest()
            assert digest.startswith("d2094321fbb6f594")
            print("  elaborated-parameter SHA-256:", digest)
print("DP mutation matrix: two controls and six named rejections; dynmap digest unchanged")
check = (r / "route/head-75db4b57/check.log").read_text()
assert re.search(r"LUT\s+49613\s+49857\s+244\s+ok", check)
assert "RESULT: PASS" in check
print("Published route gate: LUT 49857 - 49613 = +244, PASS")
for shard in ["sweep-s0", "sweep-s1"]:
    text = (r / shard / "runner.out").read_text()
    print(shard)
    print("\n".join(line for line in text.splitlines() if line.startswith(("suites:", "checks:", "declared skips", "  SKIPPED"))))
print("Builder limitation:", (r / "builder/union.log").read_text().strip())
print("Separate field campaign:")
print("\n".join(line for line in (r / "tsnfuzz/tsnfuzz.log").read_text().splitlines()
                if "field campaign (tsn-gen driven):" in line or "campaign artifact freshness" in line))
print("EVIDENCE AUDIT PASS")
