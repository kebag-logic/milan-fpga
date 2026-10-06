#!/usr/bin/env python3
"""Recompute published envelopes and sample their original hosted timestamps.

Usage: python3 check_measurements.py REPOSITORY PACKET
Network access is read-only. Full retrieved logs remain in packet/scratch.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

repo, packet = map(lambda x: Path(x).resolve(), sys.argv[1:])
scratch = packet / "scratch"
base_url = "repos/kebag-logic/milan-fpga/"

def get_api(endpoint):
    return subprocess.check_output(["gh", "api", "--allow-escape-sequences", base_url + endpoint], timeout=90)

handoff = get_api("contents/review-evidence/673-r1/author/HANDOFF.md?ref=ff5010496ab2c4efdd8a7e89b36463f7d5fb0ee4")
# The contents endpoint returns base64 unless the raw media type is selected.
import base64
handoff = base64.b64decode(json.loads(handoff)["content"]).decode()
rows = re.findall(r"^\| (\d/\d) \| `([^`]+)` \| ([0-9.]+) s (PASS|TIMEOUT) \|", handoff, re.M)
assert len(rows) == 61
sys.path.insert(0, str(repo / "scripts"))
from suite_shards import shard_owner, sweep_suites
default = sweep_suites(repo / "tb/verilator")
assert {suite for shard, suite, value, verdict in rows if shard != "0/1"} == set(default)
changes = {"capture_coherence": 2400, "milan_dp_mclk": 3600, "milan_dp": 4800}
overheads = {1: Decimal("117.580"), 2: Decimal("86.448"), 4: Decimal("89.438")}
expected = {1: Decimal("5899.359"), 2: Decimal("6203.901"), 4: Decimal("4889.438")}
for owner in (1, 2, 4):
    selected = [(suite, Decimal(value)) for shard, suite, value, verdict in rows if shard == f"{owner}/5"]
    assert all(shard_owner(suite, 5) == owner for suite, value in selected)
    sibling = sum(value for suite, value in selected if suite not in changes)
    envelope = sum(Decimal(changes.get(suite, value)) for suite, value in selected) + overheads[owner]
    assert abs(envelope - expected[owner]) < Decimal("0.001"), envelope
    assert envelope < Decimal("6480")
    print(f"PASS shard {owner}/5: siblings {sibling:.6f}, envelope {envelope:.6f} < 6480 seconds")

jobs = {112155955445: ("capture_coherence", Decimal("1642.280")),
        112142195163: ("milan_dp", Decimal("3509.562")),
        112160880744: ("milan_dp_mclk", Decimal("1800.008")),
        112142195196: None, 112155955407: None}
ansi = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07]*(?:\x07|\x1b\\)")

def seconds(stamp):
    dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    return Decimal(str(dt.timestamp()))

def sample(item):
    jid, target = item
    raw = get_api(f"actions/jobs/{jid}/logs")
    (scratch / f"job-{jid}.log").write_bytes(raw)
    text = ansi.sub("", raw.decode())
    previous = None
    total = Decimal(0)
    windows = {}
    receipt = [f"job {jid}; raw log sha256 {hashlib.sha256(raw).hexdigest()}"]
    previous_line = None
    for line in text.splitlines():
        if re.search(r"\bshard: [0-9]+/[0-9]+ +selected suites:", line):
            previous = seconds(line.split()[0])
            previous_line = line
        match = re.search(r"\b(PASS|FAIL|TIMEOUT) +([a-z0-9_]+)(?: +\(|\s*$)", line)
        if previous is not None and match:
            stamp = seconds(line.split()[0])
            elapsed = stamp - previous
            windows[match[2]] = (elapsed, match[1])
            total += elapsed
            if target and match[2] == target[0]:
                receipt += [previous_line, line, f"measured window {elapsed} seconds; {match[1]}"]
            previous, previous_line = stamp, line
    if target:
        assert abs(windows[target[0]][0] - target[1]) < Decimal("0.001"), (jid, windows)
    meta = json.loads(get_api(f"actions/jobs/{jid}"))
    elapsed = seconds(meta["completed_at"]) - seconds(meta["started_at"])
    overhead = elapsed - total
    receipt += [f"job started_at={meta['started_at']}; completed_at={meta['completed_at']}",
                f"job span={elapsed}; suite windows={total}; overhead={overhead}"]
    overhead_expect = {112142195196: Decimal("117.580"),
                       112155955407: Decimal("86.448"),
                       112142195163: Decimal("89.438")}
    if jid in overhead_expect:
        assert abs(overhead - overhead_expect[jid]) < Decimal("0.001"), (jid, overhead)
    receipt.append("PASS timestamp sample")
    return "\n".join(receipt)

with ThreadPoolExecutor(max_workers=5) as pool:
    for result in pool.map(sample, jobs.items()):
        print(result)
print("PASS all published-envelope calculations and five original hosted-log samples")
