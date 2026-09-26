#!/usr/bin/env python3
"""Reviewer probe for syn/ooc/pp_baseline.py --selftest at round 3.

usage: round3_probe.py <repo> <workdir>

Part A imports the repository's maintained MUTANTS list and records, for each
mutant, the final diagnostic line of the failing self-test, so a reader can
check that it dies at the refusal it is named for rather than at an unrelated
crash.

Part B applies reviewer-owned partial or boundary weakenings of the round-3
enforcement points (one family only, one direction only, suffix-matched names)
that the maintained list does not spell. A mutant that still passes the
self-test prints SURVIVED.

Copies are written only under <workdir>; the repository is never modified.
"""

import ast
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

EXTRA = {
    "B01 ambiguity checked for first family only": (
        "        if len(matches) != 1 or len(packages) != 1:\n",
        "        if (len(matches) != 1 or len(packages) != 1) and parameter == \"PP_TROM_HEX_P\":\n"),
    "B02 ambiguity checked for last family only": (
        "        if len(matches) != 1 or len(packages) != 1:\n",
        "        if (len(matches) != 1 or len(packages) != 1) and parameter == \"GPTP_UCODE_HEX_P\":\n"),
    "B03 binding: refuse only missing (duplicate takes first)": (
        "        if len(matches) != 1 or len(packages) != 1:\n",
        "        if len(matches) < 1 or len(packages) != 1:\n"),
    "B04 binding: refuse only duplicate (missing crashes)": (
        "        if len(matches) != 1 or len(packages) != 1:\n",
        "        if len(matches) > 1 or len(packages) != 1:\n"),
    "B05 package: refuse only missing (duplicate takes first)": (
        "        if len(matches) != 1 or len(packages) != 1:\n",
        "        if len(matches) != 1 or len(packages) < 1:\n"),
    "B06 package: refuse only duplicate (missing crashes)": (
        "        if len(matches) != 1 or len(packages) != 1:\n",
        "        if len(matches) != 1 or len(packages) > 1:\n"),
    "B07 declaration: refuse only missing (duplicate takes first)": (
        "    if len(hits) != 1:\n", "    if len(hits) < 1:\n"),
    "B08 declaration: refuse only duplicate": (
        "    if len(hits) != 1:\n", "    if len(hits) > 1:\n"),
    "B09 package matched by suffix": (
        "        packages = [path for path in files if path.name == package]\n",
        "        packages = [path for path in files if path.name.endswith(package)][-1:]\n"),
    "B10 binding regex without leading dot": (
        "        matches = re.findall(r\"\\.\" + parameter + r'\\s*\\(\"([^\"\\n]+)\"\\)', verilog)\n",
        "        matches = re.findall(parameter + r'\\s*\\(\"([^\"\\n]+)\"\\)', verilog)[-1:]\n"),
    "B11 width accepts narrower words": (
        "    if width is not None and any(len(word) != (width + 3) // 4 for word in tokens):\n",
        "    if width is not None and any(len(word) > (width + 3) // 4 for word in tokens):\n"),
    "B12 width accepts wider words": (
        "    if width is not None and any(len(word) != (width + 3) // 4 for word in tokens):\n",
        "    if width is not None and any(len(word) < (width + 3) // 4 for word in tokens):\n"),
    "B13 depth accepts longer images": (
        "    if words is not None and len(tokens) != words:\n",
        "    if words is not None and len(tokens) < words:\n"),
    "B14 depth accepts shorter images": (
        "    if words is not None and len(tokens) != words:\n",
        "    if words is not None and len(tokens) > words:\n"),
    "B15 parameter ROM depth from width declaration": (
        "        count = package_number(text, depth)\n",
        "        count = package_number(text, width) if depth == \"TROM_DEPTH_C\" else package_number(text, depth)\n"),
    "B16 parameter ROM width ignored for gPTP family": (
        "                                   package_number(text, width)))\n",
        "                                   None if parameter == \"GPTP_UCODE_HEX_P\" else package_number(text, width)))\n"),
    "B17 missing generated ROM crashes instead of inventory refusal": (
        "        if not path.exists():\n            continue\n",
        "        if not path.exists():\n            raise FileNotFoundError(path)\n"),
    "B18 unsupported log value dropped (pre-existing, not in delta)": (
        '            raise ValueError(f"unsupported parameter value: {name}={raw}")\n',
        "            continue\n"),
}


def run(target: Path) -> tuple[int, str]:
    result = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                            capture_output=True, text=True, timeout=180)
    tail = (result.stderr.strip().splitlines() or result.stdout.strip().splitlines()
            or [""])[-1][:150]
    return result.returncode, tail


def main() -> None:
    repo, work = Path(sys.argv[1]), Path(sys.argv[2])
    source = (repo / "syn/ooc/pp_baseline.py").read_text()
    spec = importlib.util.spec_from_file_location("mutants", repo / "syn/ooc/pp_baseline_mutants.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    work.mkdir(parents=True, exist_ok=True)
    groups = [("A", {"control": None, **module.MUTANTS}), ("B", EXTRA)]
    for part, mutants in groups:
        for index, (name, change) in enumerate(mutants.items()):
            changed = source
            if change is not None:
                old, new = change
                if source.count(old) != 1:
                    print(f"{part}\t{name}\tNOT-APPLIED (count {source.count(old)})")
                    continue
                changed = source.replace(old, new)
            ast.parse(changed)
            target = work / f"{part}{index:02d}" / "syn/ooc/pp_baseline.py"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(changed)
            code, tail = run(target)
            if change is None:
                verdict = "control-pass" if code == 0 else "CONTROL-FAIL"
            else:
                verdict = "killed" if code != 0 else "SURVIVED"
            print(f"{part}\t{name}\trc={code}\t{verdict}\t{tail}")
    shutil.rmtree(work)


if __name__ == "__main__":
    main()
