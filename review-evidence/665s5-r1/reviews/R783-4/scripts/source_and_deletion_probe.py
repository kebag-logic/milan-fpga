#!/usr/bin/env python3
"""Source mutants of the supersede rule and deletions of check_superseded's assertions, on copies inside a tree.

usage: source_and_deletion_probe.py <tree extracted at the exact head> [jobs]
Each variant is a copy of tb/verilator/ctrl_service_hooks beside the original, so the harness's relative imports
hold. A variant must change the bytes it names, or the probe stops.
"""
import ast
import hashlib
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
JOBS = int(sys.argv[2]) if len(sys.argv) > 2 else 12
SRC = TREE / 'tb/verilator/ctrl_service_hooks'
RULE = "if by and any((x['group'], x['path'], x['interface']) == (by, *r['path']) for x in rows):"
LOOKUP = "by = hooks.SUPERSEDED.get(r['path'][0])"
TABLE = "SUPERSEDED = {'acmp.tmr_no_adp': 'hooks-disc-aging'}"
NAMED = "if r.get('missing'):\n            findings.append("
MARGIN = "margin_ms=round(timeout - row['wait_ms'] - row['ms'], 5)"

SOURCE = {
    'path term dropped (sup-no-path)': ('run.py', RULE,
        "if by and any((x['group'], x['interface']) == (by, r['path'][1]) for x in rows):"),
    'interface term dropped': ('run.py', RULE, "if by and any((x['group'], x['path']) == (by, r['path'][0]) for x in rows):"),
    'group term dropped': ('run.py', RULE, "if by and any((x['path'], x['interface']) == tuple(r['path']) for x in rows):"),
    'group alone: path and interface dropped': ('run.py', RULE, "if by and any(x['group'] == by for x in rows):"),
    'path compared by family prefix': ('run.py', RULE,
        "if by and any((x['group'], x['path'].split('.')[0], x['interface']) == (by, r['path'][0].split('.')[0], r['path'][1]) for x in rows):"),
    'path or interface, not both': ('run.py', RULE,
        "if by and any(x['group'] == by and (x['path'] == r['path'][0] or x['interface'] == r['path'][1]) for x in rows):"),
    'all rows instead of any': ('run.py', RULE, RULE.replace('any(', 'all(')),
    'no row needed': ('run.py', RULE, 'if by:'),
    'table guard dropped': ('run.py', LOOKUP, "by = hooks.SUPERSEDED.get(r['path'][0], 'hooks-disc-aging')"),
    'second table entry (sup-second-entry)': ('hooks.py', TABLE,
        "SUPERSEDED = {'acmp.tmr_no_adp': 'hooks-disc-aging', 'acmp.bind_rx': 'hooks-disc-aging'}"),
    'held finding by name dropped at its source': ('run.py', NAMED, "if False:\n            findings.append("),
    'margin from a timeout of zero at its source': ('run.py', MARGIN, "margin_ms=round(0.0 - row['wait_ms'] - row['ms'], 5)"),
}


def expects(text: str) -> list[ast.Expr]:
    """check_superseded's expect statements, in order."""
    fn = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == 'check_superseded')
    return [s for s in fn.body if isinstance(s, ast.Expr) and isinstance(s.value, ast.Call)
            and getattr(s.value.func, 'id', '') == 'expect']


def without(text: str, picks: list[int]) -> str:
    """The self-test with the picked expect statements of check_superseded removed."""
    lines = text.split('\n')
    found = expects(text)
    for i in sorted(picks, reverse=True):
        s = found[i]
        lines[s.lineno - 1:s.end_lineno] = ['    pass']
    return '\n'.join(lines)


def run_variant(name: str, edit) -> str:
    """One copy, one edit, one self-test."""
    slug = hashlib.sha256(name.encode()).hexdigest()[:12]
    copy = SRC.parent / f'probe_{slug}'
    shutil.rmtree(copy, ignore_errors=True)
    shutil.copytree(SRC, copy, ignore=shutil.ignore_patterns('__pycache__'))
    edit(copy)
    out = subprocess.run([sys.executable, '-B', str(copy / 'hooks_selftest.py')], capture_output=True, text=True)
    shutil.rmtree(copy)
    text = out.stdout + out.stderr
    failing = [x[5:].split(': ')[0:2] for x in text.splitlines() if x.startswith('FAIL ')]
    fail = [' | '.join(f)[:88] for f in failing]
    escaped = [x.split(': ESCAPED')[0][7:] if ': ESCAPED' in x else x[7:] for x in text.splitlines()
               if x.startswith('MUTANT') and 'ESCAPED' in x]
    verdict = 'KILLED' if out.returncode else 'SURVIVED'
    return f'{verdict} rc={out.returncode} | {name} | checks failing {fail} | mutants escaping {escaped}'


def source_edit(file: str, old: str, new: str):
    def edit(copy: Path) -> None:
        p = copy / file
        t = p.read_text()
        assert t.count(old) == 1, (file, old, t.count(old))
        p.write_text(t.replace(old, new))
    return edit


def deletion_edit(picks: list[int]):
    def edit(copy: Path) -> None:
        p = copy / 'hooks_selftest.py'
        t = p.read_text()
        assert len(expects(t)) == 4
        p.write_text(without(t, picks))
    return edit


NAMES = ['positive case', 'other interface', 'a path the table does not name', 'another path']
DELETIONS = [[0], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
jobs = [(n, source_edit(*v)) for n, v in SOURCE.items()]
jobs += [('deleted: ' + ' + '.join(NAMES[i] for i in d), deletion_edit(d)) for d in DELETIONS]
print(f'tree {TREE}')
with ThreadPoolExecutor(JOBS) as pool:
    for line in pool.map(lambda j: run_variant(*j), jobs):
        print(line)
