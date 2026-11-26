#!/usr/bin/env python3
"""Issue #113: focused equivalence and regression checks in disposable trees."""
import argparse
import ast
import concurrent.futures
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import resource
import subprocess
import tarfile

BASE = "3009f9a2a2d69375211d8355490675879033d940"
HEAD = "af11b3ef631eb44cdc1730cfb31bedda95c33dc5"
RUNNER = "tb/verilator/engine/pass_run.py"


def command(args, cwd):
    return subprocess.check_output(args, cwd=cwd)


class NoDocs(ast.NodeTransformer):
    def visit(self, node):
        node = super().visit(node)
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body.pop(0)
        return node


def ast_text(text):
    return ast.dump(NoDocs().visit(ast.parse(text)), include_attributes=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("packet", type=Path)
    ap.add_argument("--compiler-dir", type=Path, required=True)
    args = ap.parse_args()
    repo, packet = args.repo.resolve(), args.packet.resolve()
    scratch = packet / "scratch"
    logs = packet / "receipts"
    logs.mkdir(exist_ok=True)
    temporary = scratch / "tmp"
    temporary.mkdir(exist_ok=True)
    os.environ.update(TMPDIR=str(temporary), PYTHONDONTWRITEBYTECODE="1", MAKEFLAGS="",
                      PATH=str(args.compiler_dir) + os.pathsep + os.environ["PATH"])
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    sources = {}
    for label, rev in (("base", BASE), ("head", HEAD)):
        dest = scratch / label
        dest.mkdir(exist_ok=True)
        archive = command(["git", "archive", rev], repo)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tf:
            tf.extractall(dest, filter="data")
        sources[label] = dest
    base, head = sources["base"], sources["head"]
    assert ast_text((base / RUNNER).read_text()) == ast_text((head / RUNNER).read_text())
    old = (base / "tb/verilator/engine/passes_test.py").read_text()
    new = (head / "tb/engine_passes_test.py").read_text()
    old = old.replace('HERE = Path(__file__).resolve().parent', 'ENGINE = Path(__file__).resolve().parent / "verilator" / "engine"')
    old = old.replace('HERE /', 'ENGINE /')
    old = old.replace("Path(__file__).resolve().parent / 'pass_run.py'", "ENGINE / 'pass_run.py'")
    old = old.replace('Path(__file__).resolve().parent / "pass_run.py"', 'ENGINE / "pass_run.py"')
    old = old.replace('events: Path, stdout: int | None = None,', 'events: Path,')
    old = old.replace('stdout=subprocess.PIPE if stdout is None else stdout', 'stdout=subprocess.PIPE')
    old = old.replace('def caller(limit=limit)', 'def caller(limit: tuple[int, int] = limit)')
    assert ast_text(old) == ast_text(new)
    ast_old = ast.parse((base / "tb/verilator/engine/passes_test.py").read_text())
    calls = [n for n in ast.walk(ast_old) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'make']
    assert len(calls) == 6 and all(len(c.args) == 4 and not any(k.arg == 'stdout' for k in c.keywords) for c in calls)
    for path in ('hdl', 'tb/verilator/engine/sim_main.cpp'):
        assert not command(['git', 'diff', BASE, HEAD, '--', path], repo)
    before = (base / 'tb/verilator/engine/Makefile').read_text().split('passes-test:\n')[0]
    after = (head / 'tb/verilator/engine/Makefile').read_text().split('passes-test:\n')[0]
    assert '\n'.join(x for x in before.splitlines() if not x.startswith('#')) == '\n'.join(x for x in after.splitlines() if not x.startswith('#'))
    (logs / 'equivalence.log').write_text('PASS runner AST identical excluding docstrings\nPASS moved test AST identical after only documented path/signature substitutions\nPASS all six make() call sites use four positional arguments and never stdout\nPASS four production pass recipes unchanged\nPASS hdl and real engine harness unchanged\n')
    def run(label, argv, cwd):
        with (logs / (label + '.log')).open('w') as f:
            f.write('COMMAND ' + ' '.join(argv) + '\n')
            f.flush()
            result = subprocess.run(argv, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, timeout=480)
        (logs / (label + '.rc')).write_text(str(result.returncode) + '\n')
        print(label, 'rc=' + str(result.returncode), flush=True)
        return result.returncode
    tasks = [
        ('base-passes', ['make', '-j16', '--no-print-directory', '-C', 'tb/verilator/engine', 'passes-test'], base),
        ('head-passes', ['make', '-j16', '--no-print-directory', '-C', 'tb/verilator/engine', 'passes-test'], head),
        ('head-docs-contract-lint', ['make', '-j16', '--no-print-directory', 'docs', 'contract', 'lint'], head),
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda t: run(*t), tasks))
    assert not any(results), results
    for label in ('base-passes', 'head-passes'):
        text = (logs / (label + '.log')).read_text()
        assert sum(line.startswith('[PASS]') for line in text.splitlines()) == 73
        assert not any(line.startswith('[FAIL]') for line in text.splitlines())
    print('PASS both layouts: 73/73 checks; docs, diagrams, contract and lint pass', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
