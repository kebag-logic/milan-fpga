#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer-owned installer mutants (R227-2, issue #504 / PR #521).

Each mutant applies one exact textual weakening to scripts/ci_rv32_sdk.py
in a disposable copy beside an unmodified scripts/ci_rv32_sdk_selftest.py
and runs the self-test. A mutant is KILLED when the self-test exits
non-zero. Every replacement must apply exactly once, or the run aborts.

Usage: installer_mutants.py <checkout-root> <scratch-dir>
"""

import shutil
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ("I01 extract digest check deleted",
     "    if actual != ARCHIVE_SHA256:\n        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n",
     ""),
    ("I02 extract digest compares an 8-hex prefix",
     "if actual != ARCHIVE_SHA256:", "if actual[:8] != ARCHIVE_SHA256[:8]:"),
    ("I03 extract digest mismatch only warns",
     "        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n",
     "        print(f\"warning: digest {actual}\")\n"),
    ("I04 download path trusts the downloaded digest",
     "            extract(downloaded, destination)\n",
     "            globals()[\"ARCHIVE_SHA256\"] = digest(downloaded)\n"
     "            extract(downloaded, destination)\n"),
    ("I05 digest checked after the root listing",
     "    actual = digest(archive)\n    if actual != ARCHIVE_SHA256:\n"
     "        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n"
     "    print(f\"SDK archive verified: {archive} sha256={actual}\", flush=True)\n"
     "    # The digest authenticates this exact upstream tar layout. Reject an\n"
     "    # unexpected root before asking tar to strip it into the final prefix.\n"
     "    with tarfile.open(archive, \"r:xz\") as stream:\n"
     "        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n"
     "            raise ValueError(\"SDK archive root mismatch\")\n",
     "    with tarfile.open(archive, \"r:xz\") as stream:\n"
     "        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n"
     "            raise ValueError(\"SDK archive root mismatch\")\n"
     "    actual = digest(archive)\n    if actual != ARCHIVE_SHA256:\n"
     "        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n"),
    ("I06 digest checked after tar extraction",
     [("    if actual != ARCHIVE_SHA256:\n        raise ValueError(f\"SDK archive digest mismatch: {actual}\")\n", ""),
      ("                    \"-C\", str(destination)], check=True)\n",
       "                    \"-C\", str(destination)], check=True)\n"
       "    if actual != ARCHIVE_SHA256:\n        raise ValueError(\"SDK archive digest mismatch\")\n")],
     None),
    ("I07 download timeout dropped",
     "urlopen(ARCHIVE_URL, timeout=120)", "urlopen(ARCHIVE_URL)"),
    ("I08 offline archive precheck deleted (cache beside)",
     "    if archive is not None and digest(archive) != ARCHIVE_SHA256:\n"
     "        raise ValueError(\"SDK archive digest mismatch\")\n", ""),
    ("I09 provenance drops installer digest",
     "            \"installer_sha256\": digest(Path(__file__).resolve()),\n", ""),
    ("I10 provenance installer digest constant",
     "\"installer_sha256\": digest(Path(__file__).resolve()),",
     "\"installer_sha256\": ARCHIVE_SHA256,"),
    ("I11 provenance drops host",
     "            \"host\": host_identity(), \"destination\": str(destination)}",
     "            \"destination\": str(destination)}"),
    ("I12 provenance drops destination",
     "            \"host\": host_identity(), \"destination\": str(destination)}",
     "            \"host\": host_identity()}"),
    ("I13 inventory ignores symlinks",
     "            records[relative] = {\"link\": os.readlink(path)}",
     "            pass"),
    ("I14 inventory ignores modes",
     "            records[relative] = {\"sha256\": digest(path),\n"
     "                                 \"mode\": stat.S_IMODE(mode)}",
     "            records[relative] = {\"sha256\": digest(path)}"),
    ("I15 inventory ignores special files",
     "        elif not stat.S_ISDIR(mode):\n"
     "            raise ValueError(f\"unexpected SDK entry: {relative}\")\n", ""),
    ("I16 identify skips realpath containment",
     "    if not realpath.is_relative_to(destination):\n"
     "        raise ValueError(\"compiler realpath escapes SDK destination\")\n", ""),
    ("I17 identify skips version",
     "    if values[\"gcc_version\"] != \"14.3.0\":\n"
     "        raise ValueError(\"SDK GCC version mismatch\")\n", ""),
    ("I18 identify skips target",
     "    if values[\"target\"] != \"riscv32-buildroot-linux-gnu\":\n"
     "        raise ValueError(\"SDK target mismatch\")\n", ""),
    ("I19 identify skips sysroot containment",
     "    if not sysroot.is_relative_to(destination):\n"
     "        raise ValueError(\"SDK sysroot is not relocated into destination\")\n", ""),
    ("I20 identify skips relocation receipt",
     "    if (destination / \"share/buildroot/sdk-location\").read_text().strip() != str(destination):\n"
     "        raise ValueError(\"SDK relocation receipt mismatch\")\n", ""),
    ("I21 verify accepts a symlinked receipt",
     "if receipt_path.is_symlink() or not receipt_path.is_file():",
     "if not receipt_path.is_file():"),
    ("I22 verify accepts extra receipt sections",
     "set(receipt) != {\"provenance\", \"inventory\", \"tools\"}",
     "not {\"provenance\", \"inventory\", \"tools\"} <= set(receipt)"),
    ("I23 verify skips provenance",
     "    if receipt[\"provenance\"] != provenance(destination):\n"
     "        raise ValueError(\"SDK provenance mismatch\")\n", ""),
    ("I24 verify skips inventory",
     "    if not actual or receipt[\"inventory\"] != actual:\n"
     "        raise ValueError(\"SDK inventory mismatch; incomplete or corrupt install\")\n", ""),
    ("I25 verify skips tool identity",
     "    if receipt[\"tools\"] != identify(destination):\n"
     "        raise ValueError(\"SDK tool identification mismatch\")\n", ""),
    ("I26 cache hit skips verification",
     "    if destination.exists():\n        verify(destination)\n",
     "    if destination.exists():\n"),
    ("I27 archive root check deleted",
     "        if any(Path(member.name).parts[0] != RELEASE for member in stream):\n"
     "            raise ValueError(\"SDK archive root mismatch\")\n",
     "        pass\n"),
    ("I28 host identity accepts any host",
     "    if (system, machine) != (\"Linux\", \"x86_64\"):\n", "    if False:\n"),
    ("I29 symlinked destination adopted",
     "    if destination.is_symlink() or destination.absolute() != destination.resolve():\n",
     "    if False:\n"),
    ("I30 relocation not executed",
     "    subprocess.run(argv, cwd=destination, check=True)\n", ""),
    ("I31 receipt written without post-install verify",
     "    verify(destination)\n    print(\"SDK fresh installation: verified\")\n",
     "    print(\"SDK fresh installation: verified\")\n"),
]


def main() -> int:
    root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    source = (root / "scripts/ci_rv32_sdk.py").read_text()
    selftest = root / "scripts/ci_rv32_sdk_selftest.py"
    scratch.mkdir(parents=True, exist_ok=True)
    killed = 0
    for index, (label, before, after) in enumerate(MUTANTS):
        edits = before if isinstance(before, list) else [(before, after)]
        mutated = source
        for old, new in edits:
            assert mutated.count(old) == 1, f"{label}: anchor count {mutated.count(old)}"
            mutated = mutated.replace(old, new)
        work = scratch / f"m{index:02d}"
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir()
        (work / "ci_rv32_sdk.py").write_text(mutated)
        shutil.copy(selftest, work / "ci_rv32_sdk_selftest.py")
        run = subprocess.run([sys.executable, "ci_rv32_sdk_selftest.py"], cwd=work,
                             capture_output=True, text=True, timeout=300)
        verdict = "KILLED" if run.returncode else "SURVIVED"
        killed += run.returncode != 0
        failing = sorted({line.split()[1] for line in run.stderr.splitlines()
                          if line.startswith(("FAIL:", "ERROR:"))})
        print(f"{verdict:8s} {label}  failing={failing}")
    # the unmutated copy must pass, or every KILLED above is meaningless
    work = scratch / "pristine"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()
    shutil.copy(root / "scripts/ci_rv32_sdk.py", work / "ci_rv32_sdk.py")
    shutil.copy(selftest, work / "ci_rv32_sdk_selftest.py")
    pristine = subprocess.run([sys.executable, "ci_rv32_sdk_selftest.py"], cwd=work,
                              capture_output=True, text=True, timeout=300)
    print(f"PRISTINE exit={pristine.returncode}")
    print(f"SUMMARY {killed}/{len(MUTANTS)} KILLED")
    return 0 if pristine.returncode == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
