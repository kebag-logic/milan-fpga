#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Prove that the resource gate's self-test detects each removed enforcement point."""

import ast
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


MUTANTS = {
    "identity comparison": ("    if changed:\n", "    if False:\n"),
    "endpoint kind comparison": ('    if candidate["kind"] != base["kind"]:\n', "    if False:\n"),
    "identical-input refusal": (
        '    if candidate["inputs_sha256"] == base["inputs_sha256"] and candidate["figures"] != base["figures"]:\n',
        "    if False:\n"),
    "resource tolerance": ("    if after - before > tolerance:\n", "    if False:\n"),
    "resource tolerance boundary": ("    if after - before > tolerance:\n", "    if after - before >= tolerance:\n"),
    "timing floor": ("        if after < floor:\n", "        if False:\n"),
    "timing fall": ("        if before - after > tolerance:\n", "        if False:\n"),
    "ceiling": ('        if candidate["figures"][figure] > ceiling:\n', "        if False:\n"),
    "verdict status": ("        status = status if ok else 1\n", "        status = status\n"),
    "Slice row": ('"Slice": "SLICE",\n', "\n"),
    "row agreement": ("        if len(values) != 1:\n", "        if not values:\n"),
    "count format": ('        if not re.fullmatch(r"\\d+(\\.5)?", value):\n', "        if False:\n"),
    "timing columns": (
        '    if len(names) != len(values) or len(names) < 5 or names[0] != "WNS(ns)" or names[4] != "WHS(ns)":\n',
        "    if False:\n"),
    "tool build": ('    tool = re.match(r"(.+? Build \\d+)", header(report, "Tool Version"))\n',
                   '    tool = re.match(r"(.+?) Build \\d+", header(report, "Tool Version"))\n'),
    "flow commands": ('    flow = [GENERICS.sub("", INCLUDES.sub("", match.group(0))).strip()\n',
                      '    flow = [GENERICS.sub("", INCLUDES.sub("", match.group(0)))[:12]\n'),
    "standalone clock": ('re.findall(r"-period (\\S+)", clock.read_text()) if clock.is_file() else []}',
                         "[]}"),
    "generated-file normalization": ('            text = re.sub(r"//[^\\n]*", "", data.decode(errors="replace"))\n',
                                      '            text = data.decode(errors="replace")\n'),
    "include headers": ('            headers += sorted(path for path in folder.iterdir() if path.suffix in (".svh", ".vh"))\n',
                        "            headers += []\n"),
    "generic inputs": ("    for generic in GENERICS.findall(script):\n", "    for generic in []:\n"),
    "image inputs": ("    for image in sorted(images, key=lambda row: Path(row[\"path\"]).name):\n",
                     "    for image in []:\n"),
    "recipe script uniqueness": ("    if len(kinds) != 1:\n", "    if not kinds:\n"),
    "census header": ('    if not lines or lines[0] != "cell\\tprimitive":\n', "    if False:\n"),
    "baseline tolerance": ('            if not entry.get("tolerance", {}).get(figure, -1) >= 0:\n', "            if False:\n"),
    "baseline floor presence": ('            if figure in TIMING and figure not in entry.get("floor", {}):\n',
                                "            if False:\n"),
    "baseline ceiling": ("            if figures[figure] > ceiling:\n", "            if False:\n"),
}


def main() -> None:
    """Run a positive control and require every single mutant to fail the self-test."""
    here = Path(__file__).resolve().parent
    source = (here / "pp_resource_gate.py").read_text()
    with tempfile.TemporaryDirectory(prefix="pp-resource-gate-mutants-") as tmp:
        for name, change in [("control", None), *MUTANTS.items()]:
            changed = source
            if change is not None:
                old, new = change
                if source.count(old) != 1:
                    raise AssertionError(f"mutation is not unique: {name}")
                changed = source.replace(old, new)
            ast.parse(changed)
            folder = Path(tmp) / name.replace(" ", "_")
            folder.mkdir()
            for sibling in ("pp_baseline_rank.py", "pp_resource_gate_selftest.py"):
                shutil.copy2(here / sibling, folder / sibling)
            (folder / "pp_resource_gate.py").write_text(changed)
            result = subprocess.run([sys.executable, "-B", str(folder / "pp_resource_gate.py"), "--selftest"],
                                    capture_output=True, text=True, timeout=120)
            if (result.returncode == 0) != (change is None):
                raise AssertionError(f"{name}: rc={result.returncode}\n{result.stdout}\n{result.stderr}")
            print(f"{name}: rc={result.returncode} PASS")
    print(f"resource gate mutants: control passes, all {len(MUTANTS)} mutants fail")


if __name__ == "__main__":
    main()
