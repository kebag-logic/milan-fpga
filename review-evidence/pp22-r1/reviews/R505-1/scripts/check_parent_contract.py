#!/usr/bin/env python3
"""Check the assigned parent patches and derive the exact processor census."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import urllib.request

sys.dont_write_bytecode = True
packet = Path(__file__).resolve().parents[1]
repo = Path(sys.argv[1]).resolve()
root = packet / "scratch/parent-contract"
pin = "28f9666feab2b2ba287643c63ed3a16b1e0bb863"
paths = ["scripts/xvlog.budget", "scripts/xvlog_gate.py", "scripts/pp_srcs.py", "tb/verilator/milan_dp/sim_nxn.cpp", ".gitmodules"]
source_hashes = {}
for path in paths:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    data = urllib.request.urlopen(f"https://raw.githubusercontent.com/kebag-logic/milan-fpga/{pin}/{path}", timeout=60).read()
    target.write_bytes(data)
    source_hashes[path] = hashlib.sha256(data).hexdigest()

def load(name):
    spec = importlib.util.spec_from_file_location(name, root / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

generator = load("pp_srcs")
generator.PP_HDL = repo / "hdl"
derived = generator.pp_sources(prefix="hdl")
published = json.loads((packet / "public/evidence/author/head-analysis-table.json").read_text())
assert derived == [r["file"] for r in published] and len(derived) == 46
(packet / "receipts/derived-sources.json").write_text(json.dumps(derived, indent=2) + "\n")
gate = load("xvlog_gate")
budget = root / "scripts/xvlog.budget"
before = gate.read_budget(budget)
assert len(before["submodules"]) == 2 and not before["hdl"]
commands = []
for patch in ["parent-adoption-148-6c22d3ca.patch", "parent-adoption-22-28f9666f.patch"]:
    argv = ["git", "apply", str(packet / "public/evidence/author" / patch)]
    p = subprocess.run(argv, cwd=root, capture_output=True, text=True)
    commands.append({"patch": patch, "rc": p.returncode, "stdout": p.stdout, "stderr": p.stderr})
    assert p.returncode == 0, commands[-1]
after = gate.read_budget(budget)
assert after == {"hdl": set(), "submodules": set()}
assert "# --- section submodules: 0 finding(s) (pinned processors) ---" in budget.read_text()
result = {"parent_base": pin, "source_sha256_before": source_hashes, "derived_source_count": len(derived), "derived_order_matches_published_tables": True, "patches_in_order": commands, "budget_before": {k:sorted(v) for k,v in before.items()}, "budget_after": {k:sorted(v) for k,v in after.items()}, "xvlog_path": gate.find_xvlog(), "scope": "Patch application and budget/parser check only; no parent bank rerun."}
(packet / "receipts/parent-contract.json").write_text(json.dumps(result, indent=2) + "\n")
(packet / "receipts/parent-budget-after.txt").write_bytes(budget.read_bytes())
print(json.dumps(result, indent=2))
