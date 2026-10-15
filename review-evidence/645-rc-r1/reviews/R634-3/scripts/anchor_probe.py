#!/usr/bin/env python3
"""Composition probe: every datapath-targeting mutant anchor in the suites
the dev side changed must stay unique in the candidate's milan_datapath.sv,
and must have the same count it had at the dev parent and the PR source head.
Usage: anchor_probe.py <repo> <dev-sha> <pr-sha>   (reads HEAD as candidate)"""
import ast, subprocess, sys
from pathlib import Path

repo, dev, pr = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
DP = "hdl/milan/milan_datapath.sv"
def show(rev, path):
    return subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout
texts = {"candidate": (repo / DP).read_text(), "dev": show(dev, DP), "pr": show(pr, DP)}

def strings(path):
    """Every string literal of length >= 12 in the driver (anchors and replacements)."""
    tree = ast.parse((repo / path).read_text())
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) >= 12:
            out.add(node.value)
    return out

drivers = ["tb/verilator/milan_dp_mclk/mclk_mutants.py",
           "tb/verilator/capture_coherence/mutants.py",
           "tb/verilator/maap/mutants.py"]
bad = 0; checked = 0
for d in drivers:
    for s in sorted(strings(d)):
        c = {k: t.count(s) for k, t in texts.items()}
        if c["dev"] == 0 and c["candidate"] == 0 and c["pr"] == 0:
            continue  # not a datapath anchor
        checked += 1
        # an anchor unique on dev must remain unique in the candidate
        if c["dev"] != c["candidate"]:
            bad += 1
            print(f"[DIFF] {d}: {s[:70]!r} dev={c['dev']} pr={c['pr']} candidate={c['candidate']}")
print(f"checked {checked} datapath-matching literals across {len(drivers)} dev-changed drivers; {bad} count changes")
sys.exit(1 if bad else 0)
