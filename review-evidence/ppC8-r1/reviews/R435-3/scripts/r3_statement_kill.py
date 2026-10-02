#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Delete each refusal statement of the lint alone and require the gate to fail.

usage: r3_statement_kill.py TREE WORK [--jobs N]

A refusal statement is found by parsing (ast), not by the author's list: every
expression statement calling `<x>.bad(...)` in model_rules.py and model_lint.py,
and every `raise` statement in model_lint.py. Each is replaced, alone and in its
own copy of TREE under WORK, by `pass` at its own indentation (all of its source
lines); the packer gate tb/desc_store/test_gen_desc_image.py then runs on the
copy and must fail (KILLED). TREE is never written.
"""
import ast
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FILES = ("hdl/aecp/desc/model_rules.py", "hdl/aecp/desc/model_lint.py")


def targets(tree: Path):
    out = []
    for rel in FILES:
        text = (tree / rel).read_text(encoding="utf-8")
        for node in ast.walk(ast.parse(text)):
            hit = (isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
                   and isinstance(node.value.func, ast.Attribute) and node.value.func.attr == "bad")
            hit = hit or (isinstance(node, ast.Raise) and rel.endswith("model_lint.py"))
            if hit:
                out.append((rel, node.lineno, node.end_lineno, node.col_offset))
    return out


def run(tree: Path, work: Path, target) -> str:
    rel, first, last, col = target
    name = f"{Path(rel).stem}-{first}"
    copy = work / name
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(tree / "hdl/aecp/desc", copy / "hdl/aecp/desc")
    shutil.copytree(tree / "tb/desc_store", copy / "tb/desc_store",
                    ignore=shutil.ignore_patterns("obj_dir", "__pycache__", "*.bin", "*.map"))
    path = copy / rel
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    original = "".join(lines[first - 1:last]).strip().splitlines()[0][:90]
    lines[first - 1:last] = [" " * col + "pass\n"]
    path.write_text("".join(lines), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=copy / "tb/desc_store",
                          capture_output=True, text=True, timeout=600)
    shutil.rmtree(copy)
    verdict = "KILLED" if proc.returncode else "SURVIVED"
    return f"{name} {verdict} | {original}"


def main() -> int:
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    work.mkdir(parents=True, exist_ok=True)
    found = targets(tree)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        lines = list(pool.map(lambda t: run(tree, work, t), found))
    print("\n".join(lines))
    killed = sum(" KILLED " in ln for ln in lines)
    print(f"{killed} of {len(lines)} KILLED; {len(lines) - killed} SURVIVED")
    return 0 if killed == len(lines) else 1


if __name__ == "__main__":
    sys.exit(main())
