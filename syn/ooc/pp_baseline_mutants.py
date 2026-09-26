#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Prove that the baseline self-test detects removed enforcement points."""

import ast
from pathlib import Path
import subprocess
import sys
import tempfile


MUTANTS = {
    "ROM error promotion": ("    prefix += ROM_ERROR\n", "    pass\n"),
    "readmemh inventory equality": (
        '    if expected != {Path(row["path"]).name for row in inputs}:\n',
        "    if False:\n"),
    "empty SRAM requirement": (
        "inputs.append(image_record(path, 0, None))",
        "inputs.append(image_record(path, None, None))"),
    "parameter ROM depth": (
        "inputs.append(image_record(Path(matches[0]), count,",
        "inputs.append(image_record(Path(matches[0]), None,"),
    "outside repository guard": (
        "    if output.is_relative_to(root):\n", "    if False:\n"),
    "image depth": (
        "    if words is not None and len(tokens) != words:\n", "    if False:\n"),
    "image width": (
        "    if width is not None and any(len(word) != (width + 3) // 4 for word in tokens):\n",
        "    if False:\n"),
    "hexadecimal image words": (
        '    if not all(re.fullmatch(r"[0-9a-fA-F]+", word) for word in tokens):\n',
        "    if False:\n"),
    "attribution constraint loading": (
        '        prefix += "read_xdc baseline_boundary.xdc\\n"\n', "        pass\n"),
    "attribution boundary preservation": (
        '        constraint = "set_property KEEP_HIERARCHY TRUE [get_cells milan_datapath/pp_shadow]\\n"\n',
        '        constraint = "set_property KEEP_HIERARCHY FALSE [get_cells milan_datapath/pp_shadow]\\n"\n'),
}


def main() -> None:
    """Run a positive control and require every single mutant to fail."""
    pristine = Path(__file__).with_name("pp_baseline.py")
    source = pristine.read_text()
    with tempfile.TemporaryDirectory(prefix="pp-baseline-mutants-") as tmp:
        for name, change in [("control", None), *MUTANTS.items()]:
            changed = source
            if change is not None:
                old, new = change
                if source.count(old) != 1:
                    raise AssertionError(f"mutation is not unique: {name}")
                changed = source.replace(old, new)
            ast.parse(changed)
            target = Path(tmp) / name / "syn/ooc/pp_baseline.py"
            target.parent.mkdir(parents=True)
            target.write_text(changed)
            result = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                                    capture_output=True, text=True, timeout=60)
            if (result.returncode == 0) != (change is None):
                raise AssertionError(f"{name}: rc={result.returncode}\n"
                                     f"{result.stdout}\n{result.stderr}")
            print(f"{name}: rc={result.returncode} PASS")


if __name__ == "__main__":
    main()
