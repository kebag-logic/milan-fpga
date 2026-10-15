#!/usr/bin/env python3
"""Prove the existing workflow contains round-four forbidden program text."""
import argparse
import hashlib
import json
from pathlib import Path
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
    return "".join(word(part) for part in value.get("Parts", []))


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("checkout", type=Path)
parser.add_argument("shell_parser", type=Path)
args = parser.parse_args()
root = args.checkout
lock = json.loads((root / "ci/image/sources.lock.json").read_text())
pin = lock["host_tools"]["shfmt"]["sha256"]
assert hashlib.sha256(args.shell_parser.read_bytes()).hexdigest() == pin
path = root / ".github/workflows/elaborate.yml"
lines = path.read_text().splitlines()
expected = "import pythondata_cpu_vexiiriscv as p; print(p.data_location)"
findings = []
for start, end in ((229, 231), (321, 322)):
    snippet = "\n".join(line[10:] for line in lines[start - 1:end]) + "\n"
    result = subprocess.run([str(args.shell_parser), "-ln", "bash", "--to-json"],
                            input=snippet, capture_output=True, text=True, check=True)
    calls = [[word(arg) for arg in node.get("Args", [])]
             for node in nodes(json.loads(result.stdout))
             if node.get("Type") == "CallExpr"]
    assert ["python3", "-c", expected] in calls
    findings.append({"path": path.relative_to(root).as_posix(),
                     "line": 230 if start == 229 else 321,
                     "argv": ["python3", "-c", expected],
                     "round4_required_result": "refusal: interpreter program text"})
inventory = json.loads((root / "ci/image/tool-inventory.json").read_text())
for name in ("scripts/run_all_suites.sh", "scripts/run_litex_sims.sh"):
    path = root / name
    assert name in inventory["inputs"]
    result = subprocess.run([str(args.shell_parser), "-ln", "bash", "--to-json"],
                            input=path.read_text(), capture_output=True, text=True, check=True)
    functions = [{"name": node["Name"]["Value"], "line": node["Pos"]["Line"]}
                 for node in nodes(json.loads(result.stdout)) if node.get("Type") == "FuncDecl"]
    assert functions
    findings.append({"path": name, "functions": functions,
                     "round4_required_result": "refusal: shell functions"})
name = "tb/verilator/milan_dp/Makefile"
assert name in inventory["inputs"]
line = (root / name).read_text().splitlines()[148]
assert "$(shell " in line
findings.append({"path": name, "line": 149, "text": line,
                 "round4_required_result": "refusal: Makefile shell expansion"})
workflow = root / ".github/workflows/elaborate.yml"
print(json.dumps({"result": "scope conflict reproduced", "findings": findings,
                  "workflow_sha256": hashlib.sha256(workflow.read_bytes()).hexdigest(),
                  "candidate_programs_executed": False}, indent=2))
