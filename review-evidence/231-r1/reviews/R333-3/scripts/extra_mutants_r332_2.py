#!/usr/bin/env python3
"""Reviewer mutation probe for syn/ooc/pp_baseline.py --selftest.

usage: extra_mutants.py <repo>

Applies single-line removals of enforcement points the committed pages claim
(missing, short, malformed and ambiguous inputs; ambiguous parameter blocks;
unsupported defaults; ROM promotion; attribution boundary) to a copy of the
helper outside the repository, and records whether --selftest fails and why.
A surviving mutant prints SURVIVED.
"""

import ast
from pathlib import Path
import subprocess
import sys
import tempfile

MUTANTS = {
    # maintained set, re-derived independently (removal semantics)
    "M01 ROM promotion removed": ("    prefix += ROM_ERROR\n", "    pass\n"),
    "M02 readmemh inventory equality": (
        '    if expected != {Path(row["path"]).name for row in inputs}:\n', "    if False:\n"),
    "M03 SRAM emptiness": ("inputs.append(image_record(path, 0, None))",
                           "inputs.append(image_record(path, None, None))"),
    "M04 parameter ROM depth": ("inputs.append(image_record(Path(matches[0]), count,",
                                "inputs.append(image_record(Path(matches[0]), None,"),
    "M05 outside-repository guard": ("    if output.is_relative_to(root):\n", "    if False:\n"),
    # additional claimed enforcement points
    "X01 ambiguous image parameter or package": (
        "        if len(matches) != 1 or len(packages) != 1:\n", "        if False:\n"),
    "X02 LiteX ROM geometry dropped": (
        "            inputs.append(image_record(path, int(words), int(width)))",
        "            inputs.append(image_record(path, None, None))"),
    "X03 parameter ROM width dropped": (
        "                                   package_number(text, width)))",
        "                                   None))"),
    "X04 duplicate wrapper parameter": ("        if name in values:\n", "        if False:\n"),
    "X05 unsupported parameter value": (
        '            raise ValueError(f"unsupported parameter value: {name}={raw}")',
        "            pass"),
    "X06 empty parameter block": ("    if not values:\n", "    if False:\n"),
    "X07 non-literal default": ('        if not re.fullmatch(r"\\d+", literal):\n',
                                "        if False:\n"),
    "X08 log vs declaration set": ("    if set(values) != set(declarations):\n",
                                   "    if False:\n"),
    "X09 template marker uniqueness": ("    if text.count(marker) != 1:\n", "    if False:\n"),
    "X10 package geometry uniqueness": ("    if len(hits) != 1:\n", "    if False:\n"),
    "X11 one synth_design command": ("    if len(commands) != 1:\n", "    if False:\n"),
    "X12 attribution needs integrated": (
        '            raise ValueError("attribution requires an integrated build")', "            pass"),
    "X13 CLI flag exclusion": (
        '        parser.error("--synthesis-only and --attribution-only require the integrated endpoint")',
        "        pass"),
    "X14 wrapper-count check in Tcl": (
        'if {[llength $pp] != 1} { error "Expected exactly one protocol wrapper" }\n', ""),
    "X15 image pathname characters": (
        "                if any(char in value for char in '{}\"\\n'):\n", "                if False:\n"),
    "X16 clock constraint before synthesis dropped": (
        '        script = (prefix + "\\nread_xdc clock.xdc\\n" + command',
        '        script = (prefix + "\\n" + command'),
}


def main() -> None:
    source = (Path(sys.argv[1]) / "syn/ooc/pp_baseline.py").read_text()
    with tempfile.TemporaryDirectory(prefix="r332-mutants-") as tmp:
        for name, change in [("control", None), *MUTANTS.items()]:
            changed = source
            if change is not None:
                old, new = change
                if source.count(old) != 1:
                    print(f"{name}: NOT-APPLICABLE (pattern count {source.count(old)})")
                    continue
                changed = source.replace(old, new)
            ast.parse(changed)
            target = Path(tmp) / name.split()[0] / "syn/ooc/pp_baseline.py"
            target.parent.mkdir(parents=True)
            target.write_text(changed)
            result = subprocess.run([sys.executable, "-B", str(target), "--selftest"],
                                    capture_output=True, text=True, timeout=120)
            tail = (result.stderr.strip().splitlines() or result.stdout.strip().splitlines()
                    or [""])[-1][:110]
            if change is None:
                verdict = "PASS" if result.returncode == 0 else "CONTROL-FAILED"
            else:
                verdict = "KILLED" if result.returncode != 0 else "SURVIVED"
            print(f"{name}: rc={result.returncode} {verdict} | {tail}")


if __name__ == "__main__":
    main()
