#!/usr/bin/env python3
"""Authenticate reached sources and report remaining explicit subset conflicts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def nodes(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child)


def word(value):
    if value.get("Type") in ("Lit", "SglQuoted"):
        return value["Value"]
    if value.get("Type") == "ParamExp":
        return "${" + value["Param"]["Value"] + "}"
    return "".join(word(part) for part in value.get("Parts", []))


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("checkout", type=Path)
parser.add_argument("shell_parser", type=Path)
args = parser.parse_args()
root = args.checkout.resolve()
inventory = json.loads((root / "ci/image/tool-inventory.json").read_text())
lock = json.loads((root / "ci/image/sources.lock.json").read_text())
assert hashlib.sha256(args.shell_parser.read_bytes()).hexdigest() == lock["host_tools"]["shfmt"]["sha256"]
findings = []
for name, expected_hash in sorted(inventory["inputs"].items()):
    path = root / name
    if path.name != "Makefile" and path.suffix != ".mk":
        continue
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash, name
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if re.match(r"^\s*\.DEFAULT_GOAL\s*[:?+]?=", line):
            category = ".DEFAULT_GOAL"
        elif re.match(r"^[^#\s][^:=]*%[^:=]*:", line):
            category = "pattern rule"
        else:
            continue
        findings.append({"path": name, "line": number, "text": line,
                         "sha256": expected_hash, "required_refusal": category})
assert sum(f["required_refusal"] == ".DEFAULT_GOAL" for f in findings) == 6
assert any(f["path"] == "tb/verilator/nvm_backend/Makefile" and
           f["line"] == 96 for f in findings)
name = "scripts/run_litex_sims.sh"
source = (root / name).read_bytes()
assert hashlib.sha256(source).hexdigest() == inventory["inputs"][name]
result = subprocess.run([str(args.shell_parser), "-ln", "bash", "--to-json"],
                        input=source, capture_output=True, check=True)
for node in nodes(json.loads(result.stdout)):
    if node.get("Type") != "Subshell":
        continue
    calls = [[word(arg) for arg in child.get("Args", [])]
             for child in nodes(node) if child.get("Type") == "CallExpr"]
    if any(call and call[0] == "cd" for call in calls):
        findings.append({"path": name, "line": node["Pos"]["Line"],
                         "sha256": inventory["inputs"][name], "calls": calls,
                         "required_refusal": "subshell containing cd"})
assert any(f["required_refusal"] == "subshell containing cd" and f["line"] == 199
           for f in findings)
print(json.dumps({"result": "remaining scope conflicts reproduced",
                  "authority": [6170435035, 6170543242],
                  "inventory_sha256": hashlib.sha256((root / "ci/image/tool-inventory.json").read_bytes()).hexdigest(),
                  "findings": findings, "candidate_programs_executed": False}, indent=2))
