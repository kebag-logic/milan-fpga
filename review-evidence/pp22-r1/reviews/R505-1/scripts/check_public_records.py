#!/usr/bin/env python3
"""Independently compare and cross-check the public executable evidence records."""
import hashlib
import json
from pathlib import Path
import re

packet = Path(__file__).resolve().parents[1]
evidence = packet / "public/evidence/author"
stats = []
for module in ["KL_pp_originator", "KL_pp_rx_validator", "protocol_processor_top"]:
    base = (evidence / f"base-{module}-stat.json").read_bytes()
    head = (evidence / f"head-{module}-stat.json").read_bytes()
    assert base == head, module
    parsed = json.loads(base)
    stats.append({"module": module, "bytes": len(base), "sha256": hashlib.sha256(base).hexdigest(), "byte_identical": True, "reached_modules": len(parsed["modules"])})
tables = {r: json.loads((evidence / f"{r}-analysis-table.json").read_text()) for r in ["base", "head"]}
assert len(tables["head"]) == len(tables["base"]) == 46
assert [r["file"] for r in tables["head"]] == [r["file"] for r in tables["base"]]
assert len(set(r["file"] for r in tables["head"])) == 46
assert all(r["rc"] == r["VRFC 10-3380"] == r["VRFC 10-8530"] == 0 for r in tables["head"])
bad_base = [r for r in tables["base"] if r["rc"]]
assert [r["file"] for r in bad_base] == ["hdl/packet_engine/KL_pp_originator.sv", "hdl/packet_engine/KL_pp_rx_validator.sv"]
assert all(r["rc"] == r["VRFC 10-3380"] == r["VRFC 10-8530"] == 1 for r in bad_base)
assert sum(r["VRFC 10-3380"] for r in tables["base"]) == sum(r["VRFC 10-8530"] for r in tables["base"]) == 2
handoff = (evidence / "HANDOFF.md").read_text()
suite_section = handoff.split("| Suite | Base checks | Head checks | Result |")[1].split("base: `suites:")[0]
suites = re.findall(r"^\| (\w+) \| (\d+) \| (\d+) \| identical \|$", suite_section, re.M)
assert len(suites) == 33 and all(b == h for _, b, h in suites)
assert sum(int(b) for _, b, _ in suites) == 1021651
integrity = json.loads((evidence / "final-integrity.json").read_text())
assert integrity["head"] == "2139f3dc10161b456dfbd51d2f73a63f9164e041"
assert integrity["suite_count"] == len(suites)
assert len(integrity["parent_consumers"]) == 17 and all(r["rc"] == 0 for r in integrity["parent_consumers"])
assert all(r["base_rc"] == r["head_rc"] == 0 for r in integrity["processor_gates"])
assert all(r["identical"] for r in integrity["retained_build_tallies"])
assert "ALL GATES PASS EXCEPT 1 NOT RUN" in handoff
result = {"statistics": stats, "analysis_files": 46, "base_failures": bad_base, "head_all_zero": True, "suite_count": len(suites), "suite_checks": sum(int(b) for _, b, _ in suites), "published_suite_table_identical": True, "public_raw_full_suite_logs_available": False, "parent_consumers_rc_zero": 17, "calibration": "NOT RUN", "note": "Statistics and analysis tables directly checked; complete-suite and parent runs are published records, not reviewer reruns."}
(packet / "receipts/public-records-check.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
