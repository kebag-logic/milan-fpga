#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Record the image's GNU Make built-in rules and default variables for the inventory.

Run inside the image: its pinned make prints the database it applies when no
makefile disables it. The inventory walker reads the generated file and never
runs make itself.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


OUTPUT = Path(__file__).resolve().parent / "make-builtins.json"
VERSION = "GNU Make 4.3"
#: Special and interpreter variables have their own walker rules; they are not defaults to model.
EXCLUDED = re.compile(r"\.|MAKE(?:$|_|FILES$|FLAGS$|OVERRIDES$|LEVEL$)|SHELL$|SUFFIXES$")


def database() -> str:
    """Print make's database with no makefile, in an empty directory and a minimal environment."""
    version = subprocess.run(["make", "--version"], capture_output=True, text=True, check=True).stdout
    if version.splitlines()[0] != VERSION:
        raise SystemExit(f"REFUSED: expected {VERSION}, found {version.splitlines()[0]!r}")
    with tempfile.TemporaryDirectory() as directory:
        result = subprocess.run(["make", "-p", "-f", "/dev/null"], cwd=directory, capture_output=True,
                                text=True, env={"LC_ALL": "C", "PATH": "/usr/bin:/bin"}, check=False)
    return result.stdout


def parse(text: str) -> dict[str, object]:
    """Keep default-origin variables and every implicit rule with its terminal flag."""
    lines = text.splitlines()
    variables = {}
    for previous, line in zip(lines, lines[1:]):
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_.]*) (:?)= ?(.*)", line)
        if previous == "# default" and match and not EXCLUDED.match(match[1]):
            variables[match[1]] = {"flavor": "simple" if match[2] else "recursive", "value": match[3]}
    start = lines.index("# Implicit Rules")
    rules = []
    for index in range(start, len(lines)):
        if lines[index].startswith("# ") and "implicit rules" in lines[index]:
            break
        match = re.fullmatch(r"(%[^\s:]*|\(%\)|[^\s:%]*%[^\s:]*)(::?)(.*)", lines[index])
        if not match:
            continue
        recipe = []
        for follow in lines[index + 1:]:
            if not follow:
                break
            if follow.startswith("\t"):
                recipe.append(follow[1:])
        rules.append({"target": match[1], "terminal": match[2] == "::",
                      "prerequisites": match[3].split(), "recipe": recipe})
    suffixes = next(line.split()[1:] for line in lines if line.startswith(".SUFFIXES:"))
    return {"version": VERSION, "variables": dict(sorted(variables.items())), "rules": rules,
            "suffixes": suffixes}


def main() -> int:
    """Generate or compare the recorded database."""
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = json.dumps(parse(database()), sort_keys=True, indent=2) + "\n"
    if args.write:
        OUTPUT.write_text(content)
    elif not OUTPUT.is_file() or OUTPUT.read_text() != content:
        print("REFUSED: make-builtins.json differs from the image's make database", file=sys.stderr)
        return 2
    print(f"PASS: {VERSION} built-in rules and default variables recorded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
