#!/usr/bin/env python3
"""End-to-end LiteX leg probe with a stub interpreter (reviewer probe, PR #836).

Usage: e2e_legs.py <checkout> <work dir>

Runs the checkout's own scripts/ci_litex_legs.py `run` for every leg around the
checkout's own scripts/run_litex_sims.sh, with MILAN_LITEX_PYTHON pointing at a
stub that passes the migen/litex probe and prints `RESULT: PASS` (or FAIL for
the members named in STUB_FAIL). The source identity is fixed so the probe also
runs on a dirty mutant tree. Then it judges the real receipts with the union and
with the elaborate aggregate verifier, and plants: a dropped row, a member moved
to another leg, a member duplicated into a second leg, a lost leg and a failing
member. Exit 0 only when the clean run passes both checks and every plant is
refused by both, naming the planted simulation where one is named.
"""
import copy
import hashlib
import json
import os
import shlex
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / "scripts"))
os.chdir(ROOT)

import ci_litex_legs  # noqa: E402
from ci_gate_receipts import Collected, StepContext, record, verify  # noqa: E402
from ci_gate_workflows import builder_command, case_inventory, load_template, worker_id, worker_legs  # noqa: E402
import ci_gate_workflows_selftest as gate_selftest  # noqa: E402
from ci_builder_legs import requirements  # noqa: E402

IDENTITY = ("a" * 40, "b" * 40)
ci_litex_legs.source_identity = lambda root: IDENTITY
problems = []


def stub(fail: str) -> Path:
    path = WORK / "stubpy"
    path.write_text("#!/bin/bash\n"
                    "[ \"$1\" = -c ] && exit 0\n"
                    "name=\"${1%.py}\"\n"
                    "case \",$STUB_FAIL,\" in *\",$name,\"*) echo 'RESULT: FAIL'; exit 1 ;; esac\n"
                    "echo 'RESULT: PASS'\n")
    path.chmod(0o755)
    os.environ["MILAN_LITEX_PYTHON"] = str(path)
    os.environ["STUB_FAIL"] = fail
    return path


def legs(tag: str, fail: str = "") -> tuple[list[dict], list[int]]:
    stub(fail)
    receipts, codes = [], []
    for leg in range(ci_litex_legs.LEGS):
        receipt = WORK / tag / f"litex-leg-{leg}.json"
        receipt.unlink(missing_ok=True)
        logs = WORK / tag / f"logs-{leg}"
        try:
            codes.append(ci_litex_legs.run(leg, receipt, ["scripts/run_litex_sims.sh", str(logs)]))
        except Exception as exc:  # a crash of the leg runner is a red leg
            print(f"{tag} leg {leg}: leg runner raised {type(exc).__name__}: {exc}")
            codes.append(-1)
            continue
        receipts.append(json.loads(receipt.read_text()))
    return receipts, codes


source = load_template(ROOT, "elaborate")
digest = hashlib.sha256(b"elaborate").hexdigest()
cases = case_inventory("elaborate", source)
workers = worker_legs("elaborate", source)
actual = {case["id"]: {"outcome": "success", "conclusion": "success"} for case in cases}
gate = [record("elaborate", leg, source, IDENTITY, digest, StepContext(actual, "true")) for leg in workers]
needs = {worker_id("elaborate", leg): {"result": "success"} for leg in workers}
builder = gate_selftest.builder_receipts(IDENTITY, flags=tuple(requirements(builder_command("elaborate", source))))


def judge(label: str, litex: list[dict], expect_pass: bool, words: str = "") -> None:
    for checker, call in (("union", lambda: ci_litex_legs.union(litex, *IDENTITY)),
                          ("aggregate", lambda: verify("elaborate", source, IDENTITY, digest,
                                                       Collected(gate, builder, litex), needs))):
        try:
            call()
            outcome, message = "pass", ""
        except (ValueError, KeyError, TypeError) as exc:
            outcome, message = "refused", str(exc)
        ok = (outcome == "pass") if expect_pass else (outcome == "refused" and words in message)
        print(f"{'ok  ' if ok else 'FAIL'} {label} / {checker}: {outcome} {message[:200]}")
        if not ok:
            problems.append(f"{label}/{checker}")


WORK.mkdir(parents=True, exist_ok=True)
good, codes = legs("clean")
print("clean leg exits:", codes, "selected:", [r["selected"] for r in good])
ran = sorted(row["simulation"] for r in good for row in r["results"])
inventory = ci_litex_legs.inventory()
if codes != [0] * ci_litex_legs.LEGS or ran != sorted(inventory):
    problems.append("clean legs did not run every simulation exactly once")
    print("FAIL clean legs ran", ran, "inventory", inventory)
judge("clean run", good, True)

if len(good) == ci_litex_legs.LEGS and all(r["results"] for r in good):
    owner = {row["simulation"]: i for i, r in enumerate(good) for row in r["results"]}
    victim = "test_pp_boot_bus_freeze" if "test_pp_boot_bus_freeze" in owner else sorted(owner)[0]
    v = owner[victim]
    other = (v + 1) % len(good)

    dropped = copy.deepcopy(good)
    dropped[v]["results"] = [row for row in dropped[v]["results"] if row["simulation"] != victim]
    judge(f"{victim} row dropped from leg {v}", dropped, False, victim)

    moved = copy.deepcopy(good)
    row = next(row for row in moved[v]["results"] if row["simulation"] == victim)
    moved[v]["results"].remove(row)
    moved[v]["selected"].remove(victim)
    moved[other]["results"].append(row)
    moved[other]["selected"].append(victim)
    judge(f"{victim} moved from leg {v} to leg {other}", moved, False, "selection differs")

    duplicated = copy.deepcopy(good)
    duplicated[other]["results"].append(copy.deepcopy(row))
    judge(f"{victim} duplicated into leg {other}", duplicated, False, "")

    judge(f"leg {v} lost", [r for i, r in enumerate(good) if i != v], False, victim)

    failing, fcodes = legs("fail", fail=victim)
    print("planted-failure leg exits:", fcodes)
    judge(f"{victim} failing in a real leg", failing, False, victim)
    if fcodes[v] == 0:
        problems.append("a failing member left its leg green")
        print(f"FAIL leg {v} exited 0 with {victim} failing")

print("e2e:", "PASS" if not problems else "FAIL " + shlex.join(problems))
raise SystemExit(1 if problems else 0)
