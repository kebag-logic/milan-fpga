#!/usr/bin/env python3
"""Check composition-facing budget, document, inventory and registry contracts."""
import os
from pathlib import Path
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", GIT_NO_REPLACE_OBJECTS="1")
env.pop("SUITE_TIMEOUT", None)
driver = (repo / "scripts/run_all_suites.sh").read_text()
policy = (repo / "docs/testing/CI_WORKFLOWS.md").read_text()
function = re.search(r"^suite_timeout\(\) \{\n.*?^\}", driver, re.M | re.S).group()
expected = {"capture_coherence": 2400, "milan_dp": 4800,
            "milan_dp_gptp": 5400, "milan_dp_mclk": 3600,
            "mmcm_servo": 1800, "aaf": 1800}
for override in [None, "17", ""]:
    active_env = dict(env)
    if override is not None:
        active_env["SUITE_TIMEOUT"] = override
    for suite, budget in expected.items():
        actual = subprocess.check_output(["rtk", "proxy", "bash", "-c",
                                          function + '\nsuite_timeout "$1"',
                                          "budget-probe", suite], env=active_env, text=True).strip()
        assert int(actual) == (int(override) if override else budget)
        print("PASS budget", suite, "override=" + repr(override), "result=" + actual)
for suite, budget in expected.items():
    if suite == "aaf":
        assert "| every other default suite | 1800 s |" in policy
    else:
        assert re.search(r"^\| `" + suite + r"`(?: \(scheduled\))? \| " + str(budget) + r" s \|", policy, re.M)
print("PASS policy table agrees with executed suite_timeout function")
for shard, suite in [(1, "capture_coherence"), (2, "milan_dp_mclk"), (4, "milan_dp")]:
    selected = subprocess.check_output(["rtk", "proxy", "bash", "scripts/run_all_suites.sh",
                                       "--shard", f"{shard}/5", "--list"], cwd=repo, env=env, text=True).splitlines()
    assert suite in selected
    print("PASS shard", str(shard) + "/5", "owns", suite, "inventory", ",".join(selected))
for shard, changed, siblings, overhead in [(1, 2400, 3381.779, 117.580),
                                         (2, 3600, 2517.453, 86.448),
                                         (4, 4800, 0, 89.438)]:
    envelope = changed + siblings + overhead
    assert envelope < 6480
    assert f"{envelope:.3f} s" in policy
    print("PASS preserved historical envelope", shard, f"{envelope:.3f}", "below 6480; not a new timing measurement")
sys.path.insert(0, str(repo / "scripts"))
from measure_test_evidence import DUT_READER_DISPOSITIONS, runner_contract
assert not runner_contract(driver)
key = "tb/verilator/aaf/start_mutants.py"
assert key in DUT_READER_DISPOSITIONS
print("PASS predecessor AAF mutation-reader registry remains imported by changed evidence checker", key)
print("PASS 18 budget probes, documentation mapping, affected shard ownership, historical arithmetic and registry integration")
