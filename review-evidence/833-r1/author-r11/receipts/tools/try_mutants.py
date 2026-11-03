"""Apply each named reviewer edit set to a copy of a tree's scripts/ and run one control; print rc and last line.

usage: python3 -I try_mutants.py TREE CONTROL SOURCE.py NAME... (SOURCE defines MUTANTS: name -> [(old, new)])
"""
import concurrent.futures
import os
import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

tree, control, source = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
# Only the source's top-level constant assignments run, never its main().
module = ast.parse(Path(source).read_text())
keep = [node for node in module.body if isinstance(node, ast.Assign)
        and all(isinstance(t, ast.Name) and t.id.isupper() and t.id not in ("CLEAN", "SCRATCH", "JOBS", "PROBE")
                for t in node.targets)]
space = {}
exec(compile(ast.Module(body=keep, type_ignores=[]), source, "exec"), space)
table = space["MUTANTS"]
env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
env["TMPDIR"] = "$VALIDATION_STORAGE/833-a726j/tmp"


def one(name: str) -> str:
    with tempfile.TemporaryDirectory(dir="$VALIDATION_STORAGE/833-a726j/tmp") as scratch:
        root = Path(scratch)
        shutil.copytree(tree / "scripts", root / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
        product = root / "scripts/owned_process.py"
        text = product.read_text()
        for old, new in table[name]:
            assert text.count(old) == 1, (name, old)
            text = text.replace(old, new)
        product.write_text(text)
        p = subprocess.run([sys.executable, "-B", "scripts/test_suite_cancellation.py", "--control", control],
                           cwd=root, env=env, capture_output=True, text=True, timeout=150, start_new_session=True)
        lines = [line for line in (p.stdout + p.stderr).splitlines() if line.strip()]
        return f"{name}: rc {p.returncode}: {lines[-1][:220] if lines else ''}"


with concurrent.futures.ThreadPoolExecutor(8) as pool:
    for line in pool.map(one, sys.argv[4:]):
        print(line, flush=True)
