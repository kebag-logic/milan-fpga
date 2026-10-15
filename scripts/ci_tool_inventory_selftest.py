#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise inventory drift with workflow and installer changes."""

import copy
import hashlib
import json
import shutil
from pathlib import Path
import tempfile

import ci_tool_inventory as inventory
import ci_command_table

# Walker semantics are tested without the census gate; ci_differential_selftest.py holds the gate.
ci_command_table.GATE = False


def comparison_control(root: Path, called: Path, workflow: Path, prefix: str) -> None:
    """A parser's comparison constants do not execute an installation."""
    called.write_text('tokens = []\nassert tokens != ["pip", "install"]\n')
    workflow.write_text(prefix + "      - run: python3 scripts/bootstrap.py\n")
    assert not inventory.derive(root)["tools"]
    print("PASS: comparison-only token data is not an installation")


def indirect_controls(root: Path, called: Path, workflow: Path, prefix: str) -> None:
    """Keep command indirection, actions and Makefiles fail-closed."""
    for source in (
        'cmd = ["pip", "install", "unlisted"]\nsubprocess.run(cmd)\n',
        'subprocess.run("python3 -m pip install unlisted", shell=True)\n',
        'os.system("apt-get install unlisted")\n',
    ):
        called.write_text(source)
        workflow.write_text(prefix + "      - run: python3 scripts/bootstrap.py\n")
        try:
            inventory.derive(root)
        except inventory.Refusal:
            print("PASS: indirect installation data refused")
        else:
            raise AssertionError(source)
    for step in (
        "      - uses: actions/setup-java@v4\n        with:\n          java-version: '21'\n",
        "      - uses: example/bootstrap@v1\n",
        "      - run: pipx install unlisted\n",
    ):
        workflow.write_text(prefix + step)
        try:
            inventory.derive(root)
        except inventory.Refusal:
            print("PASS: unsupported action or installer refused")
        else:
            raise AssertionError(step)
    makefile = root / "tb/verilator/fixture/Makefile"
    makefile.parent.mkdir(parents=True)
    makefile.write_text("all:\n\tpip install unlisted\n")
    workflow.write_text(prefix + "      - run: make -C tb/verilator/fixture\n")
    try:
        inventory.derive(root)
    except inventory.Refusal:
        print("PASS: Makefile installation refused")
    else:
        raise AssertionError("Makefile installation accepted")


def refuse(root: Path, expected: str) -> None:
    """Require the named refusal, so unrelated setup failures cannot pass."""
    try:
        inventory.derive(root)
    except inventory.Refusal as error:
        assert expected in str(error), (expected, str(error))
        print(f"PASS: {expected} refused")
    else:
        raise AssertionError(expected)


def closed_controls(root: Path, workflow: Path, prefix: str) -> None:
    """Plant every reported surface, then prove declaration and hash boundaries."""
    (root / "tb/verilator/fixture/Makefile").unlink()
    commands = ["sudo dpkg -i fixture.deb", "npx --yes fixture@1.2.3", "go install fixture@v1",
                "snap install fixture", "uv tool install fixture", "docker run fixture:tag",
                "git -C somewhere fetch https://example.invalid/repo", "brand_new_command --version",
                "env MODE=check brand_new_command", "timeout 20 brand_new_command",
                "echo okay; brand_new_command", "echo $(brand_new_command)",
                "selected=brand_new_command; $selected",
                "f() { brand_new_command; }; f", r"find . -exec brand_new_command {} \;"]
    for command in commands:
        workflow.write_text(prefix + "      - run: |\n          " + command + "\n")
        refuse(root, "unclassified")
        print(f"PASS: closed command control: {command}")
    table_path = root / "ci/image/command-table.json"
    table = json.loads(table_path.read_text())
    table["commands"]["brand_new_command"] = {"class": "non-installing", "prefixes": [["--version"]]}
    table_path.write_text(inventory.serialized(table))
    workflow.write_text(prefix + "      - run: brand_new_command --version\n")
    assert not inventory.derive(root)["tools"]
    workflow.write_text(prefix + "      - run: brand_new_command install fixture\n")
    refuse(root, "unclassified")
    print("PASS: newly classified command permits only its reviewed form")
    called = root / "bootstrap.py"
    workflow.write_text(prefix + "      - run: python3 bootstrap.py\n")
    for source in (
        'import subprocess\nsubprocess.run(args="python3 -m pip install fixture==1.0", shell=True)\n',
        'import subprocess\nsubprocess.run(["pip", "install", "fixture"])\n',
        'import urllib.request\nurllib.request.urlretrieve("https://example.invalid/tool", "tool")\n',
    ):
        called.write_text(source)
        refuse(root, "undeclared executing or network script 'bootstrap.py'")
    called.write_text('import socket\n')
    table["scripts"]["bootstrap.py"] = {"class": "reviewed non-installing", "reason": "Local socket validation.",
                                         "sha256": hashlib.sha256(called.read_bytes()).hexdigest()}
    table_path.write_text(inventory.serialized(table))
    assert not inventory.derive(root)["tools"]
    called.write_text('print("changed")\n')
    refuse(root, "changed declared script 'bootstrap.py'")
    called.write_text('import subprocess\nsubprocess.run(args=["brand_new_command", "install"])\n')
    table["scripts"]["bootstrap.py"]["sha256"] = hashlib.sha256(called.read_bytes()).hexdigest()
    table_path.write_text(inventory.serialized(table))
    refuse(root, "unclassified")
    workflow.write_text(prefix + "      - run: python3 missing.py\n")
    refuse(root, "unresolved script 'missing.py'")
    (root / "Makefile").write_text("all: bootstrap\nbootstrap:\n\tcurl https://example.invalid/tool -o tool\n")
    workflow.write_text(prefix + "      - run: make\n")
    refuse(root, "installer needs an explicit pin reader")
    for recipe in ("all: ; npx fixture\n", "VALUE := $(shell npx fixture)\nall:\n\techo okay\n"):
        (root / "Makefile").write_text(recipe)
        refuse(root, "unclassified command 'npx'")
    for field in ('container: ', 'services:\n      oracle: '):
        prefix_image = "jobs:\n  gate:\n    " + field
        workflow.write_text(prefix_image + "example:latest\n")
        refuse(root, "image requires an exact digest")
        reference = "example@sha256:" + "a" * 64
        workflow.write_text(prefix_image + reference + "\n")
        rows = inventory.derive(root)["tools"]
        assert len(rows) == 1 and rows[0]["source"] == reference and rows[0]["pin"] == "sha256:" + "a" * 64
    print("PASS: container and service digests recorded; moving images refused")
    workflow.write_text(prefix + "      - run: python3 -m pip install example==1.0\n")
    clean = inventory.derive(root)
    missing = copy.deepcopy(clean)
    missing["tools"].clear()
    assert missing != inventory.derive(root)
    print("PASS: missing inventory entry differs")


def main() -> int:
    """Require additions, removals, pin changes and unknown installs to differ."""
    with tempfile.TemporaryDirectory(prefix="ci-inventory-") as directory:
        root = Path(directory)
        (root / "ci/image").mkdir(parents=True)
        shutil.copyfile(inventory.ROOT / "ci/image/command-table.json", root / "ci/image/command-table.json")
        shutil.copyfile(inventory.ROOT / "ci/image/sources.lock.json", root / "ci/image/sources.lock.json")
        shutil.copyfile(inventory.ROOT / "ci/image/syntax-census.json", root / "ci/image/syntax-census.json")
        shutil.copyfile(inventory.ROOT / "ci/image/make-builtins.json", root / "ci/image/make-builtins.json")
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
        comparison_control(root, called, workflow, prefix)
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
        indirect_controls(root, called, workflow, prefix)
        closed_controls(root, workflow, prefix)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
