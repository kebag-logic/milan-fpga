#!/usr/bin/env python3
"""Focused independent count, dispatch, receipt, schedule and merge controls."""
from collections import Counter
from contextlib import redirect_stdout
import copy
import hashlib
from io import StringIO
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
work = packet / "scratch" / "probes"
work.mkdir(parents=True, exist_ok=True)
os.chdir(work)
sys.path[:0] = [str(root / "scripts"), str(root / "sw/firmware/ctrl/test"), str(root / "sw/mailbox")]
import ci_events as events
import ci_gate_workflows as workflows
import ci_fast_legs as fast
import ci_fast_legs_selftest as checks
import test_ctrl_firmware as firmware
import test_ctrl_firmware_shards as dispatch
import census_legs as census
import suite_shards as suites

def git(*args):
    return subprocess.check_output(["git", *args], cwd=root)

world = events.parse_world(events.read_tree(root))
assert not events.check(world).findings
print("PASS unplanted full event contract")
for label, mutate, expected in events._fast_leg_arms():
    changed = copy.deepcopy(world)
    mutate(changed)
    c = events.Contract()
    events.check_fast_legs(c, changed[events.RTL_FAST])
    assert any(expected in f for f in c.findings), (label, c.findings)
print(f"PASS all {len(events._fast_leg_arms())} fast-leg planted contract arms")

source = (root / "scripts/ci_fast_legs.py").read_text()
anchor = "+ str(count) +"
assert source.count(anchor) == 1
namespace = {"__file__": str(root / "scripts/ci_fast_legs.py")}
exec(compile(source.replace(anchor, "+ str(count + 1) +"), "count-mutant", "exec"), namespace)
with patch.object(fast, "generate", namespace["generate"]):
    generated = workflows.generate("rtl-fast", workflows.load_template(root, "rtl-fast"))
    c = events.Contract()
    events.check_fast_legs(c, generated)
    for name in fast.CAMPAIGNS:
        assert any(name in f and "matrix's leg count" in f for f in c.findings)
    try:
        checks.workflow_controls()
    except AssertionError:
        print("PASS independent COUNT+1 generator fault rejected by contract and generator self-test")
    else:
        raise AssertionError("COUNT+1 escaped generator self-test")

for phase, count, wanted in ((1, 4, [212,212,212,211]), (2, 2, [199,199]), (3, 2, [332,330])):
    legs = dispatch.campaign_cases(firmware, (phase, 4), count)
    assert [len(leg) for leg in legs] == wanted
    if phase < 3:
        with patch.object(firmware, "campaign_leg", lambda args: args):
            try:
                dispatch.campaign_cases(firmware, (phase,4), count)
            except AssertionError:
                print(f"PASS phase {phase}: removing campaign_leg mapping is refused")
            else:
                raise AssertionError("removed campaign mapping escaped")
print("PASS merged control inventory 847; AECP 398; SRP 662; controls retained per leg")

receipt_dir = packet / "scratch/cicd4-r2/author/receipts/census-receipts"
for line in (receipt_dir / "SHA256SUMS").read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    assert hashlib.sha256((receipt_dir / name.lstrip("*")).read_bytes()).hexdigest() == digest
records = [json.loads(p.read_text()) for p in sorted(receipt_dir.glob("census-leg-*.json"))]
identity = tuple(records[0][key] for key in ("head", "tree"))
assert identity == ("530149b5dd1a94cc5011b17c9bb28af54bc79be3", "08e15b7d" + records[0]["tree"][8:])
assert git("rev-parse", identity[0] + "^{tree}").decode().strip() == identity[1]
assert git("show", identity[0] + ":sw/mailbox/census_legs.py") == (root / "sw/mailbox/census_legs.py").read_bytes()
every = census.inventory()
def judge(rows, ident=identity):
    output = StringIO()
    try:
        with redirect_stdout(output):
            rc = census.union(rows, every, ident)
    except ValueError as exc:
        return 1, str(exc)
    return rc, output.getvalue()
rc, output = judge(records)
assert rc == 0
assert output == (receipt_dir / "replay-union.log").read_text()
original = packet / "scratch/cicd4-r1/author/receipts/local/census/union.log"
if original.exists():
    assert output.strip() in original.read_text()
print("PASS five retained JSON hashes, execution head/tree, unchanged reader and byte-identical union output")
mutants = []
for label, leg, field, value in (("leg exit",3,"exit",1), ("wrong head",2,"head","f"*40),
                                ("wrong tree",2,"tree","f"*40), ("wrong inventory",1,"inventory",[])):
    changed = copy.deepcopy(records)
    changed[leg][field] = value
    mutants.append((label,changed))
changed = copy.deepcopy(records); changed[2]["rows"][0]["ok"] = False
mutants.append(("failed arm", changed))
changed = copy.deepcopy(records); changed[4]["rows"].pop()
mutants.append(("lost arm", changed))
changed = copy.deepcopy(records)
next(row for row in changed[1]["rows"] if row["through"] is not None)["through"] = False
mutants += [("lost rule witness",changed), ("missing leg",records[1:]), ("duplicate leg",records+[records[1]])]
for label, changed in mutants:
    assert judge(changed)[0] != 0, label
    print("PASS retained census receipts refuse " + label)
assert judge(records, (git("rev-parse","HEAD").decode().strip(),git("rev-parse","HEAD^{tree}").decode().strip()))[0] != 0
print("PASS historic receipts refuse current-head identity; no current-head execution claim")

inventory = suites.expand_suites(suites.sweep_suites(root / "tb/verilator"))
owners, loads = suites.balance(inventory, 27)
policy = (root / "docs/testing/CI_WORKFLOWS.md").read_text()
rows = re.findall(r"\| `verilator-shards (\d+)/27` \| (\d+) \| (\d+) \| (\d+) \|",policy)
assert len(rows) == 27
for index, seconds, bound, margin in rows:
    assert loads[int(index)] == int(seconds)
    assert int(bound)-int(seconds) == int(margin)
assert max(loads[:-1]) == 1275 and loads[-1] == 1530
assert suites.SUITE_SECONDS["gptp_shadow"] == 679
print("PASS all 27 policy rows equal live deal; regular max 1275, dedicated exception 1530")
docs = [int(n) for n in re.findall(r"\| `docs-gates-\d` \| (\d+) \|",policy)]
assert docs == [738,1302,981,1237,879]
assert max(docs)+60+60+120+30 == 1572
assert 1800-1572 == 228 and 1302-1276 == 26
print("PASS docs maximum 1302, over budget 26, workflow 1572, margin 228")
assert not git("diff", "5b5b0765", "HEAD", "--", ".github/workflows")
changed = git("diff", "--name-only", "4df125b8", "HEAD").decode().splitlines()
assert not any(p.startswith(("hdl/", "tb/", "syn/", "configs/")) for p in changed)
assert not git("diff", "4df125b8", "HEAD", "--", "gptp-processor", "third_party/tsn-c-stack", "sw/firmware/ctrl/test/ctrl_mutants.py")
print("PASS workflows unchanged across delta; imported RTL, tests, gitlinks equal merged donor")
print("PASS focused delta probes complete")
