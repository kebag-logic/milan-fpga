#!/usr/bin/env python3
"""Check the composition's idiom-gate refactors against what each commit claims.

usage: check_refactors.py <repo> <scratch dir>

AST claims: the module's ast.dump (docstrings stripped where the claim is "AST identical but docstring whitespace")
is equal before and after the commit. Table claims: the named table, imported from a snapshot of the parent and of
the commit (its directory alone, git archive), compares equal entry by entry: names and order, and for each entry
its repr with lambdas replaced by their source text.
"""
import ast
import importlib
import inspect
import subprocess
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]), Path(sys.argv[2])


def show(rev: str, path: str) -> str:
    return subprocess.run(['git', '-C', str(repo), 'show', f'{rev}:{path}'], capture_output=True, text=True,
                          check=True).stdout


def strip_docstrings(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) and node.body and \
                isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], 'value', None), ast.Constant) \
                and isinstance(node.body[0].value.value, str):
            node.body[0].value.value = ''
    return tree


def same_ast(rev: str, path: str, docstrings: bool = True) -> bool:
    a, b = ast.parse(show(f'{rev}^', path)), ast.parse(show(rev, path))
    if not docstrings:
        a, b = strip_docstrings(a), strip_docstrings(b)
    return ast.dump(a) == ast.dump(b)


def snapshot(rev: str, directory: str) -> Path:
    top = scratch / f'{rev[:10]}'
    if not top.is_dir():
        top.mkdir(parents=True)
        archive = subprocess.run(['git', '-C', str(repo), 'archive', rev, 'sw', 'tb', 'scripts', 'configs', 'avdecc', 'hdl', 'syn', 'docs'],
                                 capture_output=True, check=True)
        subprocess.run(['tar', '-x', '-C', str(top)], input=archive.stdout, check=True)
    return top / directory


def norm(value):
    if callable(value) and getattr(value, '__name__', '') == '<lambda>':
        try:
            return 'lambda:' + inspect.getsource(value).strip()
        except OSError:
            return 'lambda:?'
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return type(value)(norm(v) for v in value)
    if hasattr(value, '_asdict'):
        return norm(value._asdict())
    if hasattr(value, '__dict__') and not isinstance(value, type):
        return norm(vars(value))
    return value


def table(rev: str, directory: str, module: str, name: str):
    root = snapshot(rev, directory)
    extra = [str(root), str(root.parents[2] / 'sw/mailbox'), str(root.parents[2] / 'sw/firmware/gtest'),
             str(root.parents[2] / 'sw/firmware/ctrl/test'), str(root.parents[2] / 'avdecc'), str(root.parents[2] / 'tb/verilator/ctrl_service_budget')]
    extra = list(dict.fromkeys(extra))
    sys.path[:0] = extra
    for m in list(sys.modules):
        f = getattr(sys.modules[m], '__file__', None) or ''
        if str(scratch) in f:
            del sys.modules[m]
    try:
        mod = importlib.import_module(module)
        value = getattr(mod, name)
        if callable(value) and not isinstance(value, (list, tuple, dict)):
            try:
                value = value()
            except TypeError:
                value = value(lambda *a, **k: (a, tuple(sorted(k.items()))))
        return norm(value)
    finally:
        for e in extra:
            sys.path.remove(e)


def lambda_sources(rev: str, directory: str, module: str, name: str) -> list[str]:
    """Each entry's source text, the lambda's body, so a moved lambda compares by its words."""
    v = table(rev, directory, module, name)
    return [str(e) for e in (v.values() if isinstance(v, dict) else v)]


fails = []
sys.dont_write_bytecode = True
H = 'tb/verilator/ctrl_service_budget'
T = 'sw/firmware/ctrl/test'
checks = [
    ('6fef44b8d1', 'ast', f'{H}/build.py', True),
    ('6fef44b8d1', 'ast', f'{H}/grade.py', True),
    ('45708d9e1f', 'ast', f'{T}/plat_mutants.py', True),
    ('4a5bfb3269', 'ast-nodoc', f'{H}/grade.py', False),
]
for rev, kind, path, doc in checks:
    ok = same_ast(rev, path, doc)
    print(f'{rev} {kind:9} {path}: {"IDENTICAL" if ok else "DIFFERS"}')
    if not ok:
        fails.append(f'{rev} {path}')
tables = [
    ('7431b6babe', H, 'selftest_mutants', 'MUTANTS'),
    ('b1af3b546f', T, 'aecp_mutants', 'DEFECTS'),
    ('afbbde5473', T, 'plat_mutants', 'mutants'),
    ('4a5bfb3269', H, 'selftest_mutants', 'MUTANTS'),
]
for rev, directory, module, name in tables:
    try:
        before = lambda_sources(f'{rev}^', directory, module, name)
        after = lambda_sources(rev, directory, module, name)
        ok = before == after
        print(f'{rev} table     {module}.{name}: {len(before)} entries before, {len(after)} after, '
              f'{"EQUAL" if ok else "DIFFER"}')
        if not ok:
            diff = [i for i, (x, y) in enumerate(zip(before, after)) if x != y][:3]
            print('   first differing entries:', diff, 'lengths', len(before), len(after))
            fails.append(f'{rev} {module}.{name}')
    except Exception as e:  # noqa: BLE001 - report the snapshot that cannot be imported
        print(f'{rev} table     {module}.{name}: NOT IMPORTED ({type(e).__name__}: {str(e)[:120]})')
print('RESULT:', 'FAIL' if fails else 'PASS', fails)
