#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer-owned mutation probes of the #504 installer and its self-test.

Each mutation replaces ONE exact snippet of scripts/ci_rv32_sdk.py in a
disposable copy of scripts/ (the snippet must occur exactly once), runs the
head's own scripts/ci_rv32_sdk_selftest.py against it, and records whether
the self-test goes red. A mutation that leaves the self-test green is an
undetected defect class.

Usage: mutate_installer.py <checkout> <scratch-dir> <out.json>
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

CHECKOUT, SCRATCH, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])

MUTATIONS = {
    # F2: the download path's only authentication
    "F2-no-digest-in-extract": (
        "    if actual != ARCHIVE_SHA256:\n        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n",
        ""),
    "F2-prefix-digest-compare": (
        "    if actual != ARCHIVE_SHA256:\n",
        "    if actual[:16] != ARCHIVE_SHA256[:16]:\n"),
    "F2-digest-after-root-check": (
        "    actual = digest(archive)\n    if actual != ARCHIVE_SHA256:\n        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n    print(f\"SDK archive verified: {archive} sha256={actual}\", flush=True)\n    # The digest authenticates this exact upstream tar layout. Reject an\n    # unexpected root before asking tar to strip it into the final prefix.\n    with tarfile.open(archive, \"r:xz\") as stream:\n        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n            raise ValueError(\"SDK archive root mismatch\")\n",
        "    with tarfile.open(archive, \"r:xz\") as stream:\n        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n            raise ValueError(\"SDK archive root mismatch\")\n    actual = digest(archive)\n    if actual != ARCHIVE_SHA256:\n        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n"),
    "F2-digest-moved-after-extraction": (
        "    actual = digest(archive)\n    if actual != ARCHIVE_SHA256:\n        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n    print(f\"SDK archive verified: {archive} sha256={actual}\", flush=True)\n    # The digest authenticates this exact upstream tar layout. Reject an\n    # unexpected root before asking tar to strip it into the final prefix.\n    with tarfile.open(archive, \"r:xz\") as stream:\n        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n            raise ValueError(\"SDK archive root mismatch\")\n    destination.mkdir(parents=True)\n    subprocess.run([\"tar\", \"-xJf\", str(archive), \"--strip-components=1\",\n                    \"-C\", str(destination)], check=True)\n",
        "    try:\n        with tarfile.open(archive, \"r:xz\") as stream:\n            if any(Path(member.name).parts[0] != RELEASE for member in stream):\n                raise ValueError(\"SDK archive root mismatch\")\n    except tarfile.TarError:\n        pass\n    destination.mkdir(parents=True)\n    subprocess.run([\"tar\", \"-xJf\", str(archive), \"--strip-components=1\",\n                    \"-C\", str(destination)], check=False)\n    actual = digest(archive)\n    if actual != ARCHIVE_SHA256:\n        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n"),
    "offline-archive-unchecked-beside-cache": (
        "    if archive is not None and digest(archive) != ARCHIVE_SHA256:\n        raise ValueError(\"SDK archive digest mismatch\")\n",
        ""),
    "download-no-timeout": (
        "urllib.request.urlopen(ARCHIVE_URL, timeout=120)",
        "urllib.request.urlopen(ARCHIVE_URL)"),
    # F3: receipt bindings
    "F3-drop-destination": (
        "            \"host\": host_identity(), \"destination\": str(destination)}",
        "            \"host\": host_identity()}"),
    "F3-drop-installer-digest": (
        "            \"installer_sha256\": digest(Path(__file__).resolve()),\n", ""),
    "F3-installer-digest-of-wrong-file": (
        "digest(Path(__file__).resolve())",
        "digest(Path(__file__).resolve().parent / 'ci_rv32_sdk_selftest.py')"),
    "F3-drop-host": (
        "            \"host\": host_identity(), \"destination\": str(destination)}",
        "            \"destination\": str(destination)}"),
    "F3-drop-release": (
        "            \"release\": RELEASE, \"installer_revision\": INSTALLER_REVISION,\n",
        "            \"installer_revision\": INSTALLER_REVISION,\n"),
    "F3-truncated-archive-digest-binding": (
        "return {\"archive_url\": ARCHIVE_URL, \"archive_sha256\": ARCHIVE_SHA256,",
        "return {\"archive_url\": ARCHIVE_URL, \"archive_sha256\": ARCHIVE_SHA256[:8],"),
    "F3-constant-installer-revision": (
        "\"installer_revision\": INSTALLER_REVISION,",
        "\"installer_revision\": 1,"),
    "verify-skips-provenance": (
        "    if receipt[\"provenance\"] != provenance(destination):\n        raise ValueError(\"SDK provenance mismatch\")\n",
        ""),
    "verify-skips-inventory": (
        "    if not actual or receipt[\"inventory\"] != actual:\n",
        "    if not actual:\n"),
    "verify-skips-tools": (
        "    if receipt[\"tools\"] != identify(destination):\n        raise ValueError(\"SDK tool identification mismatch\")\n",
        "    identify(destination)\n"),
    "verify-accepts-extra-sections": (
        "set(receipt) != {\"provenance\", \"inventory\", \"tools\"}",
        "not {\"provenance\", \"inventory\", \"tools\"} <= set(receipt)"),
    "verify-follows-receipt-symlink": (
        "if receipt_path.is_symlink() or not receipt_path.is_file():",
        "if not receipt_path.is_file():"),
    "inventory-ignores-mode": (
        "            records[relative] = {\"sha256\": digest(path),\n                                 \"mode\": stat.S_IMODE(mode)}\n",
        "            records[relative] = {\"sha256\": digest(path)}\n"),
    "inventory-ignores-links": (
        "            records[relative] = {\"link\": os.readlink(path)}\n",
        "            pass\n"),
    "inventory-accepts-special": (
        "            raise ValueError(f\"unexpected SDK entry: {relative}\")\n",
        "            pass\n"),
    "identify-no-escape-check": (
        "    if not realpath.is_relative_to(destination):\n        raise ValueError(\"compiler realpath escapes SDK destination\")\n",
        ""),
    "identify-no-version-check": (
        "    if values[\"gcc_version\"] != \"14.3.0\":\n        raise ValueError(\"SDK GCC version mismatch\")\n",
        ""),
    "identify-no-target-check": (
        "    if values[\"target\"] != \"riscv32-buildroot-linux-gnu\":\n        raise ValueError(\"SDK target mismatch\")\n",
        ""),
    "identify-no-sysroot-check": (
        "    if not sysroot.is_relative_to(destination):\n        raise ValueError(\"SDK sysroot is not relocated into destination\")\n",
        ""),
    "identify-no-relocation-receipt": (
        "    if (destination / \"share/buildroot/sdk-location\").read_text().strip() != str(destination):\n        raise ValueError(\"SDK relocation receipt mismatch\")\n",
        ""),
    "extract-no-root-check": (
        "        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n            raise ValueError(\"SDK archive root mismatch\")\n",
        "        pass\n"),
    "install-no-symlink-destination-check": (
        "    if destination.is_symlink() or destination.absolute() != destination.resolve():\n        raise ValueError(\"SDK destination must be an absolute path without symlink parents\")\n",
        ""),
    "install-no-host-check": (
        "    if (system, machine) != (\"Linux\", \"x86_64\"):\n        raise ValueError(f\"unsupported SDK host: {system}/{machine}\")\n",
        ""),
    "install-repairs-existing-tree": (
        "    if destination.exists():\n        verify(destination)\n        print(\"SDK cache hit: verified\")\n        return\n",
        "    if destination.exists():\n        shutil.rmtree(destination)\n"),
    "install-hit-without-verify": (
        "    if destination.exists():\n        verify(destination)\n",
        "    if destination.exists():\n"),
    "receipt-written-before-relocation": (
        "    argv = [str(destination / \"relocate-sdk.sh\")]\n    print(\"SDK argv: \" + json.dumps(argv), flush=True)\n    subprocess.run(argv, cwd=destination, check=True)\n    tools = identify(destination)\n    receipt = {\"provenance\": provenance(destination),\n               \"inventory\": inventory(destination), \"tools\": tools}\n    (destination / RECEIPT).write_text(json.dumps(receipt, sort_keys=True) + \"\\n\")\n",
        "    (destination / RECEIPT).write_text(json.dumps({\"provenance\": provenance(destination), \"inventory\": inventory(destination), \"tools\": {}}, sort_keys=True) + \"\\n\")\n    argv = [str(destination / \"relocate-sdk.sh\")]\n    print(\"SDK argv: \" + json.dumps(argv), flush=True)\n    subprocess.run(argv, cwd=destination, check=True)\n    tools = identify(destination)\n    receipt = {\"provenance\": provenance(destination),\n               \"inventory\": inventory(destination), \"tools\": tools}\n    (destination / RECEIPT).write_text(json.dumps(receipt, sort_keys=True) + \"\\n\")\n"),
}


def main() -> None:
    results = {}
    source = (CHECKOUT / "scripts/ci_rv32_sdk.py").read_text()
    for name, (old, new) in MUTATIONS.items():
        work = SCRATCH / f"inst-{name}"
        if work.exists():
            shutil.rmtree(work)
        work.mkdir(parents=True)
        for leaf in ("ci_rv32_sdk.py", "ci_rv32_sdk_selftest.py"):
            shutil.copy2(CHECKOUT / "scripts" / leaf, work / leaf)
        count = source.count(old)
        if count != 1:
            results[name] = {"applied": False, "occurrences": count}
            continue
        mutated = source.replace(old, new, 1)
        if "shutil." in new and "import shutil" not in mutated:
            mutated = mutated.replace("import stat\n", "import shutil\nimport stat\n", 1)
        (work / "ci_rv32_sdk.py").write_text(mutated)
        run = subprocess.run([sys.executable, "ci_rv32_sdk_selftest.py"], cwd=work,
                             capture_output=True, text=True, timeout=600)
        failing = sorted({line.split(" (")[0].replace("FAIL: ", "").replace("ERROR: ", "")
                          for line in run.stderr.splitlines()
                          if line.startswith(("FAIL: ", "ERROR: "))})
        results[name] = {"applied": True, "selftest_exit": run.returncode,
                         "detected": run.returncode != 0, "failing_tests": failing,
                         "summary": run.stderr.strip().splitlines()[-1:]}
    # control: the unmutated copy must pass
    work = SCRATCH / "inst-pristine"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for leaf in ("ci_rv32_sdk.py", "ci_rv32_sdk_selftest.py"):
        shutil.copy2(CHECKOUT / "scripts" / leaf, work / leaf)
    run = subprocess.run([sys.executable, "ci_rv32_sdk_selftest.py"], cwd=work,
                         capture_output=True, text=True, timeout=600)
    results["pristine-control"] = {"selftest_exit": run.returncode,
                                   "summary": run.stderr.strip().splitlines()[-3:]}
    OUT.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n")
    for name, rec in results.items():
        print(f"{name:<42} {'DETECTED' if rec.get('detected') else ('pristine exit=' + str(rec.get('selftest_exit')) if name == 'pristine-control' else 'UNDETECTED' if rec.get('applied', True) else 'NOT-APPLIED')}  {rec.get('failing_tests', '')}")


if __name__ == "__main__":
    main()
