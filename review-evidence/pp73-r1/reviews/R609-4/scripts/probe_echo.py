#!/usr/bin/env python3
"""Independent round-4 membership and response-boundary probes; read-only source."""
import copy
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
from aecp_gate.inputs import load, ucode_of
from aecp_gate.gate import check
from aecp_gate.table import check_schema
from aecp_gate.record import split_group, check_record
from aecp_gate.rom import check_rom

base = load(root)
assert not check(base)
results = []

def membership(label, edit, token=None):
    table = copy.deepcopy(base.table)
    edit(table)
    findings = check_schema(table)
    ok = not findings if token is None else any(token in f for f in findings)
    print(json.dumps(dict(case=label, pass_=ok, findings=findings)))
    assert ok, label
    results.append(label)

membership("implicit shared secondary accepted", lambda t: t["echo_entries"].append("TIZ4NS"))
membership("explicit shared first entry accepted", lambda t: (
    t["echo_entries"].append("EAVL"), t["shared_entries"].update(EAVL="declared shared")))
membership("private first entry refused", lambda t: t["echo_entries"].append("EAVL"), "echo_entries: EAVL")
membership("private secondary refused", lambda t: t["echo_entries"].append("RDESCENT"), "echo_entries: RDESCENT")
membership("unknown refused", lambda t: t["echo_entries"].append("UNKNOWN_R609"), "echo_entries: UNKNOWN_R609")
membership("shared with first owner refused without declaration", lambda t: (
    t["echo_entries"].append("EAVL"),
    next(c for c in t["commands"] if c["name"] == "GET_CONFIGURATION")["entries"].append("EAVL")),
    "echo_entries: EAVL")
membership("NSUPPE declaration required", lambda t: t["shared_entries"].pop("NSUPPE"), "echo_entries: NSUPPE")
membership("BADARG declaration required", lambda t: t["shared_entries"].pop("BADARG"), "echo_entries: BADARG")
membership("list shape refused", lambda t: t.update(echo_entries=None), "echo_entries must be a list")
membership("member shape refused", lambda t: t["echo_entries"].append(1), "echo_entries must be a list")

# Test the two consumers separately. None of these checks depend on a stale digest.
table = copy.deepcopy(base.table)
table["echo_entries"].append("EAVL")
table["shared_entries"]["EAVL"] = "declared shared"
assert not check_schema(table)
for answer in ("12", "echo"):
    rec = copy.deepcopy(base.record)
    split_group(rec, "AEM", 2)["EAVL"]["answers"] = {"0": answer}
    findings = check_record(table, rec)[0]
    named = [f for f in findings if "ENTITY_AVAILABLE: EAVL answered SUCCESS" in f]
    print(json.dumps(dict(case="SUCCESS observation " + answer, findings=named)))
    assert named
    results.append("SUCCESS observation " + answer)

uc = copy.deepcopy(ucode_of(base))
start = uc.entry["EAVL"]
end = min(p for p in uc.placed if p > start)
hits = [pc for pc in range(start, end) if uc.rom[pc] >> 43 == uc.ops["BUILD_FLD"]]
assert len(hits) == 3, hits
for pc in hits:
    uc.rom[pc] = 0
findings = check_rom(table, uc)
named = [f for f in findings if "ENTITY_AVAILABLE: E_EAVL answers SUCCESS at cdl 12" in f]
print(json.dumps(dict(case="SUCCESS ROM short fields", addresses=hits, findings=named)))
assert named
results.append("SUCCESS ROM short fields")

# An actual shared error echo remains legal; removing the exemption exposes it.
assert not check_rom(base.table, ucode_of(base))
no_echo = copy.deepcopy(base.table)
no_echo["echo_entries"] = []
findings = check_rom(no_echo, ucode_of(base))
named = [f for f in findings if "E_BADARG answers BAD_ARGUMENTS at cdl 12" in f]
assert named
print(json.dumps(dict(case="non-SUCCESS echo boundary retained", findings=named[:3])))
results.append("non-SUCCESS echo boundary retained")
print(f"Independent echo boundary probes: {len(results)} PASS, 0 FAIL")
