#!/usr/bin/env python3
"""Independent timeout, scope, inventory and mutation probes at the reviewed head.

Usage: python3 focused_probe.py REPOSITORY PACKET
Only the packet scratch directory receives disposable files.
"""
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys

repo, packet = map(lambda x: Path(x).resolve(), sys.argv[1:])
head = "793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df"
base = "bd884631684ccf5060339efa92263d5c3e5c262c"
parent = "26bd6334a7b8b2a8582b36ae4729a71620546c14"

def git(*args):
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()

assert git("rev-parse", "HEAD") == head
assert git("rev-parse", "HEAD^{tree}") == "4044003424303525864889c45788aeb8a48c8501"
assert git("rev-parse", "HEAD^") == parent
docs = {"docs/testing/RUNNING_TESTS.md", "docs/testing/TESTING.md",
        "tb/verilator/milan_dp/README.md", "tb/verilator/milan_dp_gptp/README.md"}
assert set(git("diff", "--name-only", parent, head).splitlines()) == docs
full = set(git("diff", "--name-only", base, head).splitlines())
assert full == docs | {"docs/testing/CI_WORKFLOWS.md", "scripts/run_all_suites.sh",
                      "scripts/measure_test_evidence.py", "scripts/measure_test_evidence_selftest.py"}
print("PASS scope: four documentation files in round 2; eight total changed files")
print("PASS no RTL, suite executable, workflow, shard assignment, or gitlink change")

runner = (repo / "scripts/run_all_suites.sh").read_text()
subprocess.run(["bash", "-n", "scripts/run_all_suites.sh"], cwd=repo, check=True)

def function(name):
    found = re.findall(r"^" + name + r"\(\) \{\n.*?^\}", runner, re.M | re.S)
    assert len(found) == 1
    return found[0]

budgets = {"capture_coherence": 2400, "milan_dp": 4800, "milan_dp_mclk": 3600,
           "milan_dp_gptp": 5400, "mmcm_servo": 1800, "unknown_future_suite": 1800}
for label, override in (("unset", None), ("empty", ""), ("explicit", "17"),
                        ("fractional", "0.25"), ("zero", "0")):
    env = dict(os.environ)
    env.pop("SUITE_TIMEOUT", None)
    if override is not None:
        env["SUITE_TIMEOUT"] = override
    for suite, default in budgets.items():
        result = subprocess.check_output(["bash", "-c", function("suite_timeout") + '\nsuite_timeout "$1"',
                                          "probe", suite], env=env, text=True).strip()
        assert result == (override if override else str(default)), (label, suite, result)
    print(f"PASS six shell budget cases: {label}")

sys.path.insert(0, str(repo / "scripts"))
from measure_test_evidence import runner_contract
assert not runner_contract(runner)
mutations = [("SUITE_TIMEOUT:-" + str(old), "SUITE_TIMEOUT:-" + str(new))
             for old, new in ((1800, 1801), (2400, 1800), (3600, 1800),
                              (4800, 3600), (5400, 7200))]
mutations += [(suite + ")", suite + "_wrong)") for suite in
              ("capture_coherence", "milan_dp", "milan_dp_mclk", "milan_dp_gptp")]
mutations += [('TMO=$(suite_timeout "$suite")', 'TMO=1800')]
for old, new in mutations:
    assert runner.count(old) == 1, old
    findings = runner_contract(runner.replace(old, new))
    assert any("suite budgets changed" in finding for finding in findings), (old, findings)
    print("PASS mutation refused:", old)

selected = subprocess.check_output(["bash", "scripts/run_all_suites.sh", "--list"],
                                   cwd=repo, text=True).splitlines()
assert len(selected) == len(set(selected)) == 60
assert "milan_dp_gptp" not in selected and "nvm_capture_cpu" not in selected
physical = subprocess.check_output(["bash", "scripts/run_all_suites.sh", "--physical-gptp", "--list"],
                                   cwd=repo, text=True).splitlines()
assert physical == ["milan_dp_gptp"]
print("PASS live selection: 60 default suites, one separate scheduled suite")

# Execute the unchanged real guard on a bounded fake workload. The tally stub
# supplies no suite-check evidence; this probe measures deadline classification.
scratch = packet / "scratch/timeout-probe"
(scratch / "tb/verilator/capture_coherence").mkdir(parents=True, exist_ok=True)
(scratch / "scripts").mkdir(exist_ok=True)
(scratch / "logs").mkdir(exist_ok=True)
(scratch / "tb/verilator/capture_coherence/Makefile").write_text("all:\n\t@sleep 2\n")
(scratch / "scripts/suite_tally.py").write_text("raise SystemExit(0)\n")
program = "\n".join(function(name) for name in ("suite_timeout", "run_suites", "summarise"))
program += '\nROOT="$1"; OUT="$1/logs"; SHARD=0/1; suites=(capture_coherence)\nrun_suites\nsummarise\n'
result = subprocess.run(["bash", "-c", program, "probe", str(scratch)],
                        env=dict(os.environ, SUITE_TIMEOUT="0.05"),
                        text=True, capture_output=True, timeout=10)
assert result.returncode == 92, result
assert "TIMEOUT  capture_coherence" in result.stdout and "result UNKNOWN" in result.stdout
assert "passed: 0   failed: 0   timed out: 1" in result.stdout
print("PASS real 0.05-second deadline: UNKNOWN, zero passes, zero failures, exit 92")
print("PASS all focused probes; no source writes")
