#!/usr/bin/env python3
"""Mutation probes: does ci_rv32_sdk_selftest.py fail for each planted defect?

Usage: mutate_installer.py <clone> <scratch-dir>
Copies the exact-head installer and its self-test into a scratch directory
(never edits the clone), applies one textual mutation at a time, and runs
the self-test. A mutant that leaves the self-test green SURVIVES.
"""

import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

clone, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
source = (clone / "scripts/ci_rv32_sdk.py").read_text()
selftest = (clone / "scripts/ci_rv32_sdk_selftest.py").read_text()

MUTANTS = {
    "extract: drop digest check (download path)": (
        "    if actual != ARCHIVE_SHA256:\n        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n",
        ""),
    "extract: drop archive root check": (
        "        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n"
        "            raise ValueError(\"SDK archive root mismatch\")\n",
        "        pass\n"),
    "install: drop explicit --archive digest check": (
        "    if archive is not None and digest(archive) != ARCHIVE_SHA256:\n"
        "        raise ValueError(\"SDK archive digest mismatch\")\n", ""),
    "verify: drop inventory comparison": (
        "    if not actual or receipt[\"inventory\"] != actual:\n", "    if False:\n"),
    "verify: drop tools comparison": (
        "    if receipt[\"tools\"] != identify(destination):\n", "    if False:\n"),
    "verify: run tools before inventory": (
        "    actual = inventory(destination)\n",
        "    identify(destination)\n    actual = inventory(destination)\n"),
    "provenance: drop installer digest": (
        "            \"installer_sha256\": digest(Path(__file__).resolve()),\n", ""),
    "provenance: drop host": (
        "            \"host\": host_identity(), \"destination\": str(destination)}",
        "            \"destination\": str(destination)}"),
    "provenance: drop destination": (
        "            \"host\": host_identity(), \"destination\": str(destination)}",
        "            \"host\": host_identity()}"),
    "inventory: drop modes": (
        "            records[relative] = {\"sha256\": digest(path),\n"
        "                                 \"mode\": stat.S_IMODE(mode)}\n",
        "            records[relative] = {\"sha256\": digest(path)}\n"),
    "inventory: drop symlinks": (
        "            records[relative] = {\"link\": os.readlink(path)}\n", "            pass\n"),
    "inventory: accept special files": (
        "            raise ValueError(f\"unexpected SDK entry: {relative}\")\n", "            pass\n"),
    "identify: drop version check": (
        "    if values[\"gcc_version\"] != \"14.3.0\":\n", "    if False:\n"),
    "identify: drop target check": (
        "    if values[\"target\"] != \"riscv32-buildroot-linux-gnu\":\n", "    if False:\n"),
    "identify: drop compiler realpath containment": (
        "    if not realpath.is_relative_to(destination):\n", "    if False:\n"),
    "identify: drop sysroot containment": (
        "    if not sysroot.is_relative_to(destination):\n", "    if False:\n"),
    "identify: drop sdk-location check": (
        "    if (destination / \"share/buildroot/sdk-location\").read_text().strip() != str(destination):\n",
        "    if False:\n"),
    "host: accept any machine": (
        "    if (system, machine) != (\"Linux\", \"x86_64\"):\n", "    if False:\n"),
    "install: accept symlinked destination": (
        "    if destination.is_symlink() or destination.absolute() != destination.resolve():\n",
        "    if False:\n"),
    "verify: accept symlinked receipt": (
        "    if receipt_path.is_symlink() or not receipt_path.is_file():\n",
        "    if not receipt_path.is_file():\n"),
    "verify: accept extra receipt keys": (
        "    if not isinstance(receipt, dict) or set(receipt) != {\"provenance\", \"inventory\", \"tools\"}:\n",
        "    if not isinstance(receipt, dict):\n"),
    "extract: skip relocation": (
        "    subprocess.run(argv, cwd=destination, check=True)\n", "    pass\n"),
    "install: repair an existing tree": (
        "    if destination.exists():\n        verify(destination)\n"
        "        print(\"SDK cache hit: verified\")\n        return\n",
        "    if destination.exists():\n        try:\n            verify(destination)\n"
        "            print(\"SDK cache hit: verified\")\n            return\n"
        "        except ValueError:\n            shutil.rmtree(destination)\n"),
}


def run(label, old, new):
    work = scratch / (label.replace(" ", "_").replace(":", "").replace("/", "_"))
    work.mkdir(parents=True)
    assert source.count(old) == 1, f"mutation anchor not unique for {label}"
    mutated = source.replace(old, new)
    if "shutil.rmtree" in new:
        mutated = mutated.replace("import tempfile\n", "import tempfile\nimport shutil\n")
    (work / "ci_rv32_sdk.py").write_text(mutated)
    (work / "ci_rv32_sdk_selftest.py").write_text(selftest)
    done = subprocess.run([sys.executable, "ci_rv32_sdk_selftest.py"], cwd=work,
                          capture_output=True, text=True, timeout=600)
    tail = [l for l in done.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:", "Ran", "OK", "FAILED"))]
    return {"mutant": label, "selftest_exit": done.returncode,
            "verdict": "KILLED" if done.returncode else "SURVIVED", "evidence": tail[:6]}


baseline = subprocess.run([sys.executable, "scripts/ci_rv32_sdk_selftest.py"], cwd=clone,
                          capture_output=True, text=True)
print(json.dumps({"baseline_exit": baseline.returncode,
                  "baseline": baseline.stderr.strip().splitlines()[-3:]}))
with ThreadPoolExecutor(max_workers=8) as pool:
    for result in pool.map(lambda item: run(item[0], *item[1]), MUTANTS.items()):
        print(json.dumps(result))
