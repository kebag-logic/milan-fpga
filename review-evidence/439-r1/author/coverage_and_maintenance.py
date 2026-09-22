#!/usr/bin/env python3
"""Audit preserved populations and exercise full-check maintenance/record loss."""
import ast
from collections import Counter
import copy
import importlib.util
import json
from pathlib import Path
import sys
from unittest.mock import patch
root = Path.cwd()
out = Path(__file__).resolve().parent
sys.path.insert(0, str(root / "scripts"))
import ci_events as ci
spec = importlib.util.spec_from_file_location("base_ci_events", out / "base-ci_events.py")
base = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = base
spec.loader.exec_module(base)
world = ci.parse_world(ci.read_tree(root))
for name in ("CARRIER_STEP_LISTS", "ENV_FILE_WRITERS", "PHYSICAL_GPTP_CONTRACT", "AGGREGATE_SCRIPTS", "CANONICAL_OWNERSHIP_SCRIPT"):
    assert getattr(ci,name) == getattr(base,name), name
    print(f"unchanged canonical authority: {name}")
for key, entries in base.RTL_STEP_LISTS.items():
    current = ci.RTL_STEP_LISTS[key]
    assert len(current) == len(entries)
    assert tuple({k:v for k,v in entry.items() if k != "run"} for entry in current) == entries
print("all seven sequence records retain their original non-content fields")
for name in ("normalize_script", "refused_character", "carrier_entry_keys", "check_sequence_pin_coverage"):
    def node(module_path):
        tree = ast.parse(module_path.read_text())
        return next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name == name)
    assert ast.dump(node(root/"scripts/ci_events.py")) == ast.dump(node(out/"base-ci_events.py")), name
    print(f"unchanged executable authority: {name}")
old_arms = base._mutations(world)
new_arms = [arm for arm in ci._mutations(world) if not arm[0].startswith("rtl-script-439")]
assert len(old_arms) == len(new_arms)
for old, new in zip(old_arms, new_arms):
    assert (old[0], old[2]) == (new[0], new[2])
    old_world, new_world = copy.deepcopy(world), copy.deepcopy(world)
    old[1](old_world)
    new[1](new_world)
    assert old_world == new_world, old[0]
print(f"all {len(old_arms)} existing mutations retain identity, edit and required diagnostic")
# Derive this audit's target jobs from the public scope, not the implementation helper.
scoped = {
    ci.RTL_FULL: {"verilator-shards", "verilator-suites", "yosys-shards", "yosys-portability"},
    ci.RTL_FAST: {"verilator-lint", "bdd-conformance", "yosys-elaboration"},
}
targets = []
for path, names in scoped.items():
    for jid, job in ci.jobs(world[path]).items():
        if jid not in names:
            continue
        targets.extend((path,jid,at,step) for at,step in enumerate(ci.steps(job)) if "run" in step)
for at,step in enumerate(ci.steps(ci.jobs(world[ci.RTL_FULL])[ci.GATE_JOB])):
    if step.get("name") == "Print the event and pin the one SHA this run validates":
        targets.append((ci.RTL_FULL,ci.GATE_JOB,at,step))
assert {(p,j,a) for p,j,a,_ in targets} == {(p,j,a) for p,j,a,_ in ci._rtl_run_steps(world)}
arms = ci._rtl_script_arms(world)
summary = []
for path,jid,at,step in targets:
    lines = ci.normalize_script(step["run"])
    recorded = ci.RTL_SEQUENCE_PINS[(path,jid)][at]["run"]
    assert tuple(lines) == recorded and lines
    names = {name for name,_,_ in arms if name.startswith(f"rtl-script-439 {jid} step {at+1} ")}
    for n in range(1,len(lines)+1):
        for suffix in (f"delete-line-{n}",f"change-line-{n}","or-true" if n == len(lines) else f"or-true-line-{n}"):
            assert f"rtl-script-439 {jid} step {at+1} {suffix}" in names
    for lever in ("missing", "empty", "stale"):
        entries = copy.deepcopy(ci.RTL_SEQUENCE_PINS[(path,jid)])
        if lever == "missing":
            entries[at].pop("run")
        elif lever == "empty":
            entries[at]["run"] = ()
        else:
            entries[at]["run"] = ("echo stale record",*lines[1:])
        with patch.dict(ci.RTL_SEQUENCE_PINS, {(path,jid): entries}):
            findings = ci.check(world).findings
        what = f"job `{jid}` step {at+1} (`{step['name']}`)"
        want = (what + " script is not the canonical form: line 1 must be 'echo stale record'" if lever == "stale" else what + " must record a canonical normalized `run` script")
        assert any(want in f for f in findings), (lever,what,findings)
    summary.append(dict(path=path,job=jid,step=at+1,name=step["name"],normalized_lines=len(lines),mutations=len(names),record=list(recorded)))
(out/"content-coverage.json").write_text(json.dumps(summary,indent=2)+"\n")
print(f"scope: {len(targets)} scripts, {sum(row['normalized_lines'] for row in summary)} normalized lines, {len(arms)} content mutations")
print(f"full-check missing/empty/stale records: {len(targets)*3} attributable refusals")
for path,jid,name in (
    (ci.RTL_FAST,"bdd-conformance","Install behave"),
    (ci.RTL_FULL,ci.GATE_JOB,"Print the event and pin the one SHA this run validates"),
):
    maintained = copy.deepcopy(world)
    ss = ci.steps(ci.jobs(maintained[path])[jid])
    at = next(n for n,s in enumerate(ss) if s.get("name") == name)
    ss[at]["run"] += "\necho checked\n"
    assert any(f"job `{jid}` step {at+1} (`{name}`) script is not the canonical form" in f for f in ci.check(maintained).findings)
    entries = copy.deepcopy(ci.RTL_SEQUENCE_PINS[(path,jid)])
    entries[at]["run"] = (*entries[at]["run"],"echo checked")
    with patch.dict(ci.RTL_SEQUENCE_PINS, {(path,jid):entries}):
        findings = ci.check(maintained).findings
    assert not findings, findings
    print(f"full-check matched maintenance: {jid} / {name}: accepted; script-only change refused")
# Independent counted output comparison supplements the executable mutation comparison.
before = Counter(line for line in (out/"logs/baseline-selftest.stdout").read_text().splitlines() if line.startswith("  ok ") and "vacuity:" not in line)
after = Counter(line for line in (out/"logs/first-selftest.stdout").read_text().splitlines() if line.startswith("  ok ") and "vacuity:" not in line)
assert not before-after, before-after
print(f"baseline success output preserved: {sum(before.values())} original result lines, excluding the changed vacuity census")
print("coverage and maintenance audit: PASS")
