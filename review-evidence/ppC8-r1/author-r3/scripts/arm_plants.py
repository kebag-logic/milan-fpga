#!/usr/bin/env python3
"""Arm-deletion campaign: every refusal statement of the lint (a ctx.bad(...)
call in model_rules.py; a raise ValueError, refusals/problems/stale.append in
model_lint.py) is replaced by `pass`, one per disposable copy of TREE, and the
packer gate runs on each copy. usage: arm_plants.py TREE WORK [--jobs N]"""
import ast
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FILES = ("hdl/aecp/desc/model_rules.py", "hdl/aecp/desc/model_lint.py")


def arms(text: str) -> list[tuple[int, int]]:
    """(first line, last line) of each refusal statement, 1-based."""
    found = []
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Attribute) and (
                    (func.attr == "bad" and getattr(func.value, "id", "") == "ctx")
                    or (func.attr == "append" and getattr(func.value, "id", "") in ("refusals", "problems", "stale"))):
                found.append((node.lineno, node.end_lineno))
        if isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call) \
                and getattr(node.exc.func, "id", "") == "ValueError":
            found.append((node.lineno, node.end_lineno))
    return sorted(found)


def run(tree: Path, work: Path, rel: str, span: tuple[int, int]) -> str:
    name = f"{Path(rel).stem}:{span[0]}"
    copy = work / name.replace(":", "_")
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(tree / "hdl/aecp/desc", copy / "hdl/aecp/desc")
    shutil.copytree(tree / "tb/desc_store", copy / "tb/desc_store", ignore=shutil.ignore_patterns("obj_dir"))
    lines = (copy / rel).read_text(encoding="utf-8").splitlines(keepends=True)
    first = lines[span[0] - 1]
    indent = first[:len(first) - len(first.lstrip())]
    shown = first.strip()[:70]
    lines[span[0] - 1:span[1]] = [indent + "pass\n"]
    (copy / rel).write_text("".join(lines), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-B", "test_gen_desc_image.py"], cwd=copy / "tb/desc_store",
                          capture_output=True, text=True, timeout=600)
    fails = sorted({ln.split(" (")[0] for ln in proc.stderr.splitlines() if ln.startswith(("FAIL:", "ERROR:"))})
    shutil.rmtree(copy)
    verdict = "KILLED" if proc.returncode else "SURVIVED"
    return f"{name} {verdict} [{shown}] {fails[:2]}"


def main() -> int:
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    work.mkdir(parents=True, exist_ok=True)
    plants = [(rel, span) for rel in FILES for span in arms((tree / rel).read_text(encoding="utf-8"))]
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        lines = list(pool.map(lambda p: run(tree, work, *p), plants))
    print("\n".join(lines))
    print(f"{sum(' KILLED ' in ln for ln in lines)} of {len(lines)} arms KILLED")
    return 0 if all(" KILLED " in ln for ln in lines) else 1


if __name__ == "__main__":
    sys.exit(main())
