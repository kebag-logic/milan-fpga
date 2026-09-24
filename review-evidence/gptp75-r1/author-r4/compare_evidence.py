"""Require identical check order, mutant failures, and ledger results."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

out = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("engine_mutants", repo / "tb/verilator/engine/mutants.py")
mutants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mutants)
results = []


def same(before, after, label):
    a, b = before.read_bytes(), after.read_bytes()
    assert a == b, label
    results.append({"comparison": label, "identical": True, "sha256": hashlib.sha256(a).hexdigest()})


same(out / "before-engine-checks.txt", out / "after-engine-checks.txt", "ordered engine checks (1613 x 3)")
same(out / "before-engine-tallies.txt", out / "after-engine-tallies.txt", "engine tallies")
for name in ("source-evidence", "source-selftest"):
    for stream in ("stdout", "stderr"):
        same(out / f"before-{name}.{stream}.log", out / f"after-{name}.{stream}.log", name + " " + stream)
for prefix in ("before", "after"):
    rows = ["mutant\tverdict\tfirst failed check\trequired named check\tfailing checks"]
    for name, _, _, _, required in mutants.MUTATIONS:
        tag = "".join(c if c.isalnum() else "_" for c in name)
        log = (out / f"{prefix}-mutants" / (tag + ".log")).read_text()
        receipt = json.loads((out / f"{prefix}-mutants" / (tag + ".json")).read_text())
        answer = mutants.verdict(receipt["returncode"], log)
        assert answer == "caught", name
        failures = receipt["failures"]
        assert failures, name
        if required.startswith("slew:"):
            assert any(required in line for line in failures), name
        first = re.sub(r"\s+got .*", "", failures[0].removeprefix("FAIL ")).strip()
        rows.append("\t".join((name, answer, first, required if required.startswith("slew:") else "", str(len(failures)))))
    control = json.loads((out / f"{prefix}-mutants/clean.json").read_text())
    assert control == {"returncode": 0, "failures": []}
    (out / f"{prefix}-mutant-verdicts.tsv").write_text("\n".join(rows) + "\n")
    # The gate's own table excludes only observer progress, retaining named failures.
    table = [line for line in (out / f"{prefix}-mutants.stdout.log").read_text().splitlines()
             if line.startswith(("[PASS]", "[FAIL]", "FAIL ")) or " checks:" in line]
    (out / f"{prefix}-mutant-gate-table.txt").write_text("\n".join(table) + "\n")
for name, _, _, _, _ in mutants.MUTATIONS:
    tag = "".join(c if c.isalnum() else "_" for c in name)
    same(out / "before-mutants" / (tag + ".json"), out / "after-mutants" / (tag + ".json"), "mutant rc and all ordered failures: " + name)
    same(out / "before-mutants" / (tag + ".log"), out / "after-mutants" / (tag + ".log"), "complete mutant output: " + name)
same(out / "before-mutant-verdicts.tsv", out / "after-mutant-verdicts.tsv", "all 33 mutant verdicts and killing checks")
same(out / "before-mutant-gate-table.txt", out / "after-mutant-gate-table.txt", "shipped mutant gate table")
path = "scripts/check_source_evidence.py"
base = subprocess.run(["git", "show", "3face0914efd9d5e71f36da7e30108cfe09c837d:" + path], cwd=repo, capture_output=True, text=True, timeout=60, check=True).stdout
before, after = ast.parse(base), ast.parse((repo / path).read_text())
for tree in (before, after):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            node.returns = None
            for arg in node.args.args:
                arg.annotation = None
            if node.name == "main" and ast.get_docstring(node):
                node.body.pop(0)
assert ast.dump(before) == ast.dump(after)
results.append({"comparison": "Python executable AST excluding annotations and main docstring", "identical": True})
(out / "comparisons.json").write_text(json.dumps(results, indent=2) + "\n")
for result in results:
    print("IDENTICAL", result["comparison"])
