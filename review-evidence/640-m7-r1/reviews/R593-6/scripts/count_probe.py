#!/usr/bin/env python3
"""Check the documentation and exercise its stale-count example in memory."""
import copy
from pathlib import Path
import re
import sys
sys.dont_write_bytecode=True
root=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(root/"scripts"))
import ci_events as ci
w=ci.parse_world(ci.read_tree(root))
base=ci.check(w)
assert not base.findings,base.findings
print(f"baseline: {base.checked} checks, zero findings")
doc=(root/"docs/testing/CI_WORKFLOWS.md").read_text()
assert "worker matrix size, six for Verilator and four for Yosys," in doc
for worker,aggregate,n in [("verilator-shards","verilator-suites",6),("yosys-shards","yosys-portability",4)]:
    job=ci.jobs(w[ci.RTL_FULL])[worker]
    assert job["strategy"]["matrix"]["shard"]==list(range(n))
    assert job["strategy"]["matrix"]["total"]==[n]
    aggregate_job=ci.jobs(w[ci.RTL_FULL])[aggregate]
    assert ci.matrix_size(w[ci.RTL_FULL],aggregate_job)==n
    assert any(f"--expect {n} " in s.get("run","") for s in ci.steps(aggregate_job))
    print(f"{worker}: matrix size = total = verifier expectation = {n}")
assert not re.search(r"--expect\s+5\b",doc)
print("documentation --expect scan: no stale literal 5")
stale=copy.deepcopy(w)
ci._m_shard_denominator_stale(stale)
m=ci.jobs(stale[ci.RTL_FULL])["verilator-shards"]["strategy"]["matrix"]
assert m["shard"]==list(range(7)) and m["total"]==[6]
f=ci.check(stale).findings
assert any("shard denominator" in x for x in f),f
assert "matrix of seven and a stale total of six" in doc
assert "shard 6/7" in doc
print("stale-denominator fixture: seven workers, total six; detected")
for x in f:
    if "shard denominator" in x: print(x)
wrong=copy.deepcopy(w)
for s in ci.steps(ci.jobs(wrong[ci.RTL_FULL])["verilator-suites"]):
    if "--require-target-sha" in s.get("run",""):
        s["run"]=s["run"].replace("--expect 6","--expect 5")
f=ci.check(wrong).findings
assert any("--expect 6" in x for x in f),f
print("stale verifier expectation 5: detected")
for x in f:
    if "--expect 6" in x: print(x)
print("PASS: focused documentation/contract probe; no repository mutation")
