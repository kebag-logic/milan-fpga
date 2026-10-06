#!/usr/bin/env python3
"""Read-only, independently specified checks for issue 673; usage: REPO."""
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys

repo = Path(sys.argv[1]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "scripts"))
from measure_test_evidence import runner_contract
from suite_shards import sweep_suites, shard_owner
import measure_test_evidence_selftest as selftest

runner = (repo / "scripts/run_all_suites.sh").read_text()
function = re.search(r"^suite_timeout\(\) \{\n.*?^\}", runner, re.M | re.S).group()
defaults = {"capture_coherence": "2400", "milan_dp_mclk": "3600",
            "milan_dp": "4800", "milan_dp_gptp": "5400"}
names = sweep_suites(repo / "tb/verilator")
assert len(names) == 60, len(names)
assert "milan_dp_gptp" not in names and "nvm_capture_cpu" not in names
assert sweep_suites(repo / "tb/verilator", physical=True) == ["milan_dp_gptp"]
assert {n: shard_owner(n, 5) for n in defaults} == {
    "capture_coherence": 1, "milan_dp_mclk": 2, "milan_dp": 4, "milan_dp_gptp": 3}
print("PASS: 60 default suites; physical/manual exclusions; unchanged affected owners")
population = names + ["milan_dp_gptp", "unknown_suite"]
for override in (None, "", "0", "17", "0.125", "5400"):
    env = os.environ.copy()
    env.pop("SUITE_TIMEOUT", None)
    if override is not None:
        env["SUITE_TIMEOUT"] = override
    for name in population:
        got = subprocess.check_output(["bash", "-c", function + '\nsuite_timeout "$1"',
                                       "probe", name], env=env, text=True).strip()
        expected = override if override else defaults.get(name, "1800")
        assert got == expected, (name, override, got, expected)
    print(f"PASS: shell dispatch for {len(population)} names, override={override!r}")
assert not runner_contract(runner)
mutations = [
    ("capture_coherence", "SUITE_TIMEOUT:-2400", "SUITE_TIMEOUT:-1800"),
    ("milan_dp_mclk", "SUITE_TIMEOUT:-3600", "SUITE_TIMEOUT:-1800"),
    ("milan_dp", "SUITE_TIMEOUT:-4800", "SUITE_TIMEOUT:-3600"),
    ("physical", "SUITE_TIMEOUT:-5400", "SUITE_TIMEOUT:-7200"),
    ("fallback", "SUITE_TIMEOUT:-1800", "SUITE_TIMEOUT:-2400"),
    ("capture name", "capture_coherence)", "capture_coherence_typo)"),
    ("mclk name", "milan_dp_mclk)", "milan_dp_render)"),
    ("dp name", "milan_dp)", "milan_dp_render)"),
    ("override", '${SUITE_TIMEOUT:-4800}', '4800'),
    ("dispatch", 'TMO=$(suite_timeout "$suite")', 'TMO=4800'),
    ("guard", 'timeout "$TMO" make', 'make'),
    ("unknown exit", '[ "$tmo"  -gt 0 ] && exit 92', '[ "$tmo"  -gt 0 ] && exit 0'),
]
for label, old, new in mutations:
    assert old in runner
    problems = runner_contract(runner.replace(old, new))
    assert problems, label
    print(f"KILLED: {label}: {'; '.join(problems)}")
original = selftest.runner_contract
results = []
try:
    selftest.runner_contract = lambda _: []
    selftest._arms_runner_contract(lambda label, ok, *detail: results.append((label, ok)))
finally:
    selftest.runner_contract = original
assert results[0][1]
assert all(not ok for _, ok in results[1:]), results
print(f"KILLED: inert contract checker; {len(results) - 1} negative self-test assertions fail")
for shard, limit, siblings, overhead in ((1, 2400, 3381.779, 117.580),
                                       (2, 3600, 2517.453, 86.448),
                                       (4, 4800, 0, 89.438)):
    envelope = limit + siblings + overhead
    assert envelope < 6480
    print(f"PASS: documented shard {shard}/5 arithmetic {envelope:.3f}s < 6480s; "
          f"headroom {(7200-envelope)/72:.2f}%")
print("PASS: focused probe; no source writes; arithmetic does not remeasure hosted jobs")
