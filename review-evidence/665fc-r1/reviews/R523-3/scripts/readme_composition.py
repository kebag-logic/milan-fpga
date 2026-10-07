#!/usr/bin/env python3
"""Check the README merge, documented arms and exclusion table without edits."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parents[1]
base = "6714181d0c8a16e2983f85b724f4d688f5111835"
parent = "af5be4710c3516cc247c353213d6939fa8d23f57"
source = "db9aa8c9b135b34ff3d070a979dee70440b37cc6"
head = "64e62816ad21791f6df3657fadb935aec5555881"
env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", PYTHONDONTWRITEBYTECODE="1")

def blob(rev, path):
    return subprocess.check_output(["git", "-c", "core.commitGraph=false", "show", f"{rev}:{path}"], cwd=root, env=env)

results = {}
with tempfile.TemporaryDirectory(dir=packet / "scratch", prefix="readme-") as tmp:
    for path in ("sw/firmware/ctrl/README.md", "sw/firmware/gtest/README.md"):
        files = []
        for rev in (parent, base, source):
            file = Path(tmp) / rev
            file.write_bytes(blob(rev, path))
            files.append(str(file))
        merged = subprocess.run(["git", "merge-file", "-p", *files], capture_output=True, env=env)
        expected = blob(head, path)
        assert merged.returncode == 0 and merged.stdout == expected, path
        results[path] = {"raw_three_way_merge": "exact candidate bytes", "sha256": hashlib.sha256(expected).hexdigest()}

sys.path.insert(0, str(root / "sw/firmware/gtest"))
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import fw_coverage
import fw_rv32
import ctrl_arms

gtest_path = "sw/firmware/gtest/README.md"
exclusions = {rev: fw_coverage.exclusions(blob(rev, gtest_path).decode()) for rev in (base, parent, source, head)}
assert all(rows == exclusions[head] for rows in exclusions.values())
assert len(exclusions[head]) == 14
results["exclusions"] = {"rows": len(exclusions[head]), "all_four_versions_identical": True}
arms = ["model", "port", "unit", "adp", "walk", "entity", "rv32", "lwsrp"]
doc = (root / "sw/firmware/ctrl/README.md").read_text()
for arm in arms:
    assert f"| `{arm}` |" in doc and callable(getattr(ctrl_arms, f"arm_{arm}"))
results["arms"] = {"default": [a for a in arms if a != "lwsrp"], "optional": "lwsrp", "lwsrp_revision": ctrl_arms.LWSRP_REV}
log = (packet / "receipts/ctrl-firmware.log").read_text()
for line in ("== mbx (host model): checks: 22   failures: 0 ==", "== ctrl port, driver and loop (host model): checks: 31   failures: 0 ==", "== ctrl units on the HAL and port-layer mocks: checks: 23   failures: 0 ==", "== ctrl MMIO platform (host window): checks: 2   failures: 0 =="):
    assert line in log
results["executed_counts"] = {"model": 22, "port": 31, "unit": 25, "unit_split": [23, 2]}

# Exercise the documented CLI parsers; every README option is accepted by its parser.
commands = {
    "sw/firmware/ctrl/test/test_ctrl_firmware.py": ["--require-rv32", "--self-test", "--lwsrp"],
    "sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py": ["--require-rv32", "--self-test", "--jobs"],
    "sw/firmware/gtest/tally_selftest.py": ["--mutants"],
    "sw/firmware/gtest/fw_coverage.py": ["--check", "--selftest", "--lwsrp"],
    "sw/firmware/gtest/fw_rv32_selftest.py": ["--require-rv32"],
}
for script, options in commands.items():
    help_result = subprocess.run([sys.executable, "-B", script, "--help"], cwd=root, env=env, text=True, capture_output=True, check=True)
    assert all(option in help_result.stdout for option in options), script
results["documented_cli_flags"] = commands
cc = fw_rv32.compiler()
assert cc
results["rv32_compiler"] = {"selector": "MILAN_RV32_CC", "basename": Path(cc).name}
for label, flag in (("version", "-dumpfullversion"), ("target", "-dumpmachine")):
    results["rv32_compiler"][label] = subprocess.check_output([cc, flag], text=True).strip()
print(json.dumps(results, indent=2))
