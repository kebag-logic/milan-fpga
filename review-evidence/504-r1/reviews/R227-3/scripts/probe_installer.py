#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R227-3 fault probes for the SDK installer and the workflow contract.

Usage: probe_installer.py <exact-head-tree> <work-dir> <receipt.json>

Installer probes: copy scripts/ci_rv32_sdk.py and its self-test into a fresh
directory, apply one exact-string fault (must apply once), run the self-test,
and record whether it FAILS (killed) and which tests failed.
Workflow probes: copy the whole tree, apply one exact-string edit to a workflow
file, run `scripts/ci_events.py --check`, and record whether it refuses.
"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

INSTALLER = {
    "I0-none": ("no fault: the self-test must pass", "", ""),
    "I1-no-extract-digest": ("R228-F2: the download path's only digest check removed",
        '    if actual != ARCHIVE_SHA256:\n        raise ValueError(f"SDK archive digest mismatch: {actual}")\n', ""),
    "I2-prefix-digest": ("R228-F2: digest compared on a prefix",
        "    if actual != ARCHIVE_SHA256:\n", "    if actual[:63] != ARCHIVE_SHA256[:63]:\n"),
    "I3-drop-destination": ("R228-F3: a provenance field dropped",
        ',\n            "host": host_identity(), "destination": str(destination)}',
        ',\n            "host": host_identity()}'),
    "I4-installer-digest-const": ("R228-F3: installer digest not measured",
        '"installer_sha256": digest(Path(__file__).resolve()),', '"installer_sha256": "fixed",'),
    "I5-no-symlink-records": ("symlinks left out of the inventory",
        '            records[relative] = {"link": os.readlink(path)}\n', "            pass\n"),
    "I6-no-realpath-escape": ("escaping compiler realpath accepted",
        '    if not realpath.is_relative_to(destination):\n        raise ValueError("compiler realpath escapes SDK destination")\n', ""),
    "I7-no-inventory-check": ("inventory not compared on a hit",
        '    if not actual or receipt["inventory"] != actual:\n', "    if False:\n"),
    "I8-identify-before-inventory": ("cached tools run before the inventory check",
        '    actual = inventory(destination)\n    if not actual or receipt["inventory"] != actual:\n'
        '        raise ValueError("SDK inventory mismatch; incomplete or corrupt install")\n'
        '    if receipt["tools"] != identify(destination):\n',
        '    tools_now = identify(destination)\n    actual = inventory(destination)\n'
        '    if not actual or receipt["inventory"] != actual:\n'
        '        raise ValueError("SDK inventory mismatch; incomplete or corrupt install")\n'
        '    if receipt["tools"] != tools_now:\n'),
    "I9-any-host": ("host identity not enforced",
        '    if (system, machine) != ("Linux", "x86_64"):\n', "    if False:\n"),
    "I10-no-root-check": ("archive root not checked",
        "        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n",
        "        if False:\n"),
    "I11-symlink-destination": ("symlinked destination adopted",
        "    if destination.is_symlink() or destination.absolute() != destination.resolve():\n",
        "    if False:\n"),
    "I12-no-sysroot-check": ("unrelocated sysroot accepted",
        "    if not sysroot.is_relative_to(destination):\n", "    if False:\n"),
    "I13-no-location-check": ("relocation receipt not read",
        '    if (destination / "share/buildroot/sdk-location").read_text().strip() != str(destination):\n',
        "    if False:\n"),
    "I14-no-mode-record": ("file modes left out of the inventory",
        '            records[relative] = {"sha256": digest(path),\n                                 "mode": stat.S_IMODE(mode)}\n',
        '            records[relative] = {"sha256": digest(path)}\n'),
    "I15-no-version-check": ("GCC version not enforced",
        '    if values["gcc_version"] != "14.3.0":\n', "    if False:\n"),
    "I16-no-offline-archive-check": ("offline --archive not checked beside a cache",
        "    if archive is not None and digest(archive) != ARCHIVE_SHA256:\n", "    if False:\n"),
}

WORKFLOW = {
    "W1-builder-no-require-rv32": (".github/workflows/docs.yml",
        "python3 sw/builder/test_builder.py --require-rv32", "python3 sw/builder/test_builder.py"),
    "W2-no-absent-control": (".github/workflows/docs.yml",
        '      - name: Compiler-absent firmware controls\n        run: |\n          set -euo pipefail\n'
        '          python3 sw/builder/test_firmware_compiler.py --selftest\n'
        '          python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"\n', ""),
    "W3-elaborate-install-unguarded": (".github/workflows/elaborate.yml",
        "      - name: Install and verify the pinned RV32 SDK\n        if: ${{ steps.scope.outputs.rtl == 'true' }}\n",
        "      - name: Install and verify the pinned RV32 SDK\n"),
    "W4-cache-path": (".github/workflows/elaborate.yml",
        "          path: ~/br-milan-rv32/host\n", "          path: ~/br-milan-rv32\n"),
    "W5-no-installer-bytes-in-key": (".github/workflows/docs.yml",
        "-${{ hashFiles('scripts/ci_rv32_sdk.py') }}", ""),
    "W6-absent-without-audit": (".github/workflows/docs.yml",
        'python3 sw/builder/test_firmware_compiler.py --absent --audit "$RUNNER_TEMP/rv32-absent.jsonl"',
        'python3 sw/builder/test_firmware_compiler.py --selftest'),
    "W7-install-continue-on-error": (".github/workflows/docs.yml",
        "      - name: Install and verify the pinned RV32 SDK\n",
        "      - name: Install and verify the pinned RV32 SDK\n        continue-on-error: true\n"),
    "W8-selftest-dropped": (".github/workflows/elaborate.yml",
        "          python3 scripts/ci_rv32_sdk_selftest.py\n", ""),
}


def installer_probe(head, work, pid):
    what, old, new = INSTALLER[pid]
    where = work / pid
    shutil.rmtree(where, ignore_errors=True)
    where.mkdir(parents=True)
    for name in ("ci_rv32_sdk.py", "ci_rv32_sdk_selftest.py"):
        shutil.copy2(head / "scripts" / name, where / name)
    src = where / "ci_rv32_sdk.py"
    text = src.read_text()
    if old:
        assert text.count(old) == 1, f"{pid}: anchor count {text.count(old)}"
        src.write_text(text.replace(old, new, 1))
    run = subprocess.run([sys.executable, "-B", "ci_rv32_sdk_selftest.py"], cwd=where,
                         capture_output=True, text=True, timeout=300)
    failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (\w+)", run.stderr, re.M)))
    ran = re.search(r"Ran (\d+) tests", run.stderr)
    shutil.rmtree(where)
    return {"id": pid, "reverts": what, "exit": run.returncode,
            "verdict": "KILLED" if run.returncode else "SURVIVED",
            "tests_ran": int(ran.group(1)) if ran else None, "failed_tests": failed}


def workflow_probe(head, work, pid):
    path, old, new = WORKFLOW[pid]
    where = work / pid
    shutil.rmtree(where, ignore_errors=True)
    shutil.copytree(head, where, symlinks=True)
    target = where / path
    text = target.read_text()
    assert text.count(old) == 1, f"{pid}: anchor count {text.count(old)}"
    target.write_text(text.replace(old, new, 1))
    run = subprocess.run([sys.executable, "-B", "scripts/ci_events.py", "--check"],
                         cwd=where, capture_output=True, text=True, timeout=300)
    lines = [line.strip() for line in (run.stdout + run.stderr).splitlines()
             if "FAIL" in line or "must" in line or "error" in line.lower()]
    shutil.rmtree(where)
    return {"id": pid, "file": path, "exit": run.returncode,
            "verdict": "REFUSED" if run.returncode else "ACCEPTED",
            "first_refusal": lines[:2]}


def main():
    head, work, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    work.mkdir(parents=True, exist_ok=True)
    results = {"installer": [installer_probe(head, work, pid) for pid in INSTALLER],
               "workflow": [workflow_probe(head, work, pid) for pid in WORKFLOW]}
    out.write_text(json.dumps(results, indent=1) + "\n")
    for rec in results["installer"]:
        print(f"{rec['id']}: {rec['verdict']} ran={rec['tests_ran']} failed={rec['failed_tests']}")
    for rec in results["workflow"]:
        print(f"{rec['id']}: {rec['verdict']} exit={rec['exit']} {rec['first_refusal'][:1]}")


if __name__ == "__main__":
    main()
