#!/usr/bin/env python3
"""Round 3 structural and real-tree probes. usage: r3_probes.py <review clone> <disposable clone at head>"""
import ast
import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile

repo, clone = sys.argv[1], pathlib.Path(sys.argv[2])
HEAD, PRIOR = "171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22", "91c115b576601139c53038440f0987412d5172e8"


def show(commit):
    return subprocess.run(["git", "-C", repo, "show", f"{commit}:scripts/docs_inventory.py"], capture_output=True,
                          text=True, check=True).stdout


def defs(source):
    out = {}
    for node in ast.parse(source).body:
        name = getattr(node, "name", None) or (ast.unparse(node.targets[0]) if isinstance(node, ast.Assign) else None)
        if name:
            out[name] = ast.dump(node)
    return out


def arms(source):
    found = {}
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.FunctionDef) and node.name in ("selftest", "copy_controls"):
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Tuple) and len(sub.elts) >= 3 and isinstance(sub.elts[0], ast.Constant)
                        and isinstance(sub.elts[0].value, str) and isinstance(sub.elts[2], ast.Constant)
                        and sub.elts[2].value in (0, 1, 2)):
                    found[sub.elts[0].value] = ast.unparse(sub)
    return found


new, old = show(HEAD), show(PRIOR)
a, b = defs(new), defs(old)
print("AST: names", len(a), len(b), "changed", sorted(k for k in a if a[k] != b.get(k)), "added", sorted(set(a) - set(b)),
      "removed", sorted(set(b) - set(a)))
x, y = arms(new), arms(old)
print("arms", len(x), len(y), "added", sorted(set(x) - set(y)), "removed", sorted(set(y) - set(x)))
print("arms changed", [k for k in x if k in y and x[k] != y[k]])

spec = importlib.util.spec_from_file_location("inv", clone / "scripts/docs_inventory.py")
inv = importlib.util.module_from_spec(spec)
sys.modules["inv"] = inv
spec.loader.exec_module(inv)
page = "# Guide B\n\nCalls `protocol-processor/hdl/core.sv`.\n"
banner = "\n> Superseded by [A](A.md).\n"
for blank in (10, 11):
    lines = (page + "\n" * blank + banner).split("\n")
    print(f"fixture banner with {blank} blanks is on line", 1 + next(i for i, t in enumerate(lines) if "Superseded" in t))

with tempfile.TemporaryDirectory() as lanes:
    subprocess.run([sys.executable, "-I", "-B", str(clone / "scripts/docs_inventory.py"), "--findings-dir", lanes],
                   check=True, capture_output=True)
    total = wrong = 0
    names = []
    for path in sorted(pathlib.Path(lanes).glob("*.md")):
        text = path.read_text(encoding="utf-8")
        lane = text.split("\n", 1)[0].removeprefix("# D0 findings: ")
        names.append(path.stem)
        assert text.count("# D0 findings:") == 1
        for page_path in re.findall(r"^## D0-\d+: (.+?):[\d?]+$", text, re.M):
            total += 1
            wrong += inv.first_match(inv.LANES, page_path) != lane
    print("real tree lanes", names, "entries", total, "misfiled", wrong)


def check(label):
    done = subprocess.run([sys.executable, "-I", "-B", "scripts/docs_inventory.py", "--check"], cwd=clone,
                          capture_output=True, text=True)
    print(f"real tree {label}: --check rc {done.returncode}")


def restore():
    subprocess.run(["git", "checkout", "-q", "--", "."], cwd=clone, check=True)


check("unchanged")
target = clone / "docs/testing/CI_WORKFLOWS.md"
body = target.read_text(encoding="utf-8").split("\n")
assert len(body) > 40
for line in (15, 16):
    edited = list(body)
    edited[line - 1] = "> Superseded by [A](README.md)."
    target.write_text("\n".join(edited), encoding="utf-8")
    check(f"banner written over line {line} of docs/testing/CI_WORKFLOWS.md")
    restore()
for path in subprocess.run(["git", "ls-files", "*.md"], cwd=clone, capture_output=True, text=True).stdout.split():
    if (clone / path).is_file() and path != inv.OUTPUT:
        with (clone / path).open("a", encoding="utf-8") as handle:
            handle.write("\nAdded line.\n")
check("one line appended to every tracked page")
restore()
