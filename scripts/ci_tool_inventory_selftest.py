#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise inventory drift with workflow and installer changes."""

import copy
from pathlib import Path
import tempfile

import ci_tool_inventory as inventory


def main() -> int:
    """Require additions, removals, pin changes and unknown installs to differ."""
    with tempfile.TemporaryDirectory(prefix="ci-inventory-") as directory:
        root = Path(directory)
        workflow = root / ".github/workflows/test.yml"
        workflow.parent.mkdir(parents=True)
        prefix = "name: fixture\njobs:\n  gate:\n    steps:\n"
        original = prefix + "      - run: python3 -m pip install --quiet example==1.0\n"
        workflow.write_text(original)
        clean = inventory.derive(root)
        assert clean["tools"][0]["tool"] == "example"
        assert clean["tools"][0]["pin"] == "1.0"
        controls = {
            "added tool": original + "      - run: sudo apt-get install -y another\n",
            "removed tool": prefix + "      - run: python3 --version\n",
            "changed pin": original.replace("==1.0", "==2.0"),
            "new job": original + "  extra:\n    steps:\n      - run: python3 -m pip install surprise\n",
        }
        for name, content in controls.items():
            workflow.write_text(content)
            assert inventory.derive(root) != clean, name
            print(f"PASS: {name} changes the derived inventory")
        workflow.write_text(original)
        orphan = copy.deepcopy(clean)
        orphan["tools"].append({"tool": "unused", "pin": "1"})
        assert inventory.derive(root) != orphan
        print("PASS: an orphan inventory entry differs")
        for command in ("npm install unexpected", "pip install unexpected",
                        "apt install unexpected", "curl -fsSL https://example.invalid/moving"):
            try:
                inventory.shell_installs(command, {}, root)
            except inventory.Refusal:
                print(f"PASS: unsupported installer refused: {command.split()[0]}")
            else:
                raise AssertionError(command)
        requirement = root / "requirements.txt"
        requirement.write_text("example==1.0 --hash=sha256:" + "a" * 64 + "\n")
        assert inventory.requirement_lines(requirement)[0]["sha256"] == ["a" * 64]
        requirement.write_text("git+https://example.invalid/repo.git@moving\n")
        try:
            inventory.requirement_lines(requirement)
        except inventory.Refusal:
            print("PASS: moving Git requirement refused")
        else:
            raise AssertionError("moving Git requirement accepted")
        called = root / "scripts/bootstrap.py"
        called.parent.mkdir()
        called.write_text('import subprocess\nsubprocess.run(["pip", "install", "unlisted"])\n')
        workflow.write_text(prefix + "      - run: python3 scripts/bootstrap.py\n")
        try:
            inventory.derive(root)
        except inventory.Refusal:
            print("PASS: an installation hidden in a called script is refused")
        else:
            raise AssertionError("called-script installation accepted")
        shell = root / "scripts/bootstrap.sh"
        shell.write_text("#!/bin/sh\npip install unlisted\n")
        workflow.write_text(prefix + "      - run: bash scripts/bootstrap.sh\n")
        try:
            inventory.derive(root)
        except inventory.Refusal:
            print("PASS: an installation hidden in a called shell script is refused")
        else:
            raise AssertionError("called-shell installation accepted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
