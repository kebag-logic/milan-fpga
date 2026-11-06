#!/usr/bin/env python3
"""Round 4 source probes of the supersede rule and its self-test, each on a disposable copy of the exact head.

usage: source_probes.py <clone> <scratch dir>
Each probe edits one anchored line in a copy of tb/verilator (plus what the self-test imports), runs the self-test
and reports: rc, the checks that fail, the mutants that escape. Nothing in the clone is written.
"""
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

CLONE, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])
H = 'tb/verilator/ctrl_service_hooks'
RULE = "if by and any((x['group'], x['path'], x['interface']) == (by, *r['path']) for x in rows):"
A_OTHER = "    expect(len(got['refusals']) == 1 and not got['superseded'], f'other interface: {got}')\n"
A_TABLE = "    expect(len(got['refusals']) == 1 and not got['superseded'], f'a path the table does not name: {got}')\n"
A_PATH = "    expect(len(got['refusals']) == 2 and not got['superseded'], f'another path: {got}')\n"
A_POS = "    expect(not got['refusals'] and len(got['superseded']) == 1, f'superseded: {got}')\n"
R, S = f'{H}/run.py', f'{H}/hooks_selftest.py'


def rule(new):
    return [(R, RULE, new)]


PROBES = {
    'baseline': [],
    'sup-no-path': rule("if by and any((x['group'], x['interface']) == (by, r['path'][1]) for x in rows):"),
    'sup-no-interface': rule("if by and any((x['group'], x['path']) == (by, r['path'][0]) for x in rows):"),
    'sup-no-group': rule("if by and any((x['path'], x['interface']) == tuple(r['path']) for x in rows):"),
    'sup-group-only': rule("if by and any(x['group'] == by for x in rows):"),
    'sup-no-row-needed': rule("if by:"),
    'sup-table-guard-dropped': [(R, "by = hooks.SUPERSEDED.get(r['path'][0])",
                                 "by = hooks.SUPERSEDED.get(r['path'][0], 'hooks-disc-aging')")],
    'sup-any-to-all': rule("if by and all((x['group'], x['path'], x['interface']) == (by, *r['path']) for x in rows):"),
    'sup-path-prefix': rule("if by and any((x['group'], x['path'].split('.')[0], x['interface']) == "
                            "(by, r['path'][0].split('.')[0], r['path'][1]) for x in rows):"),
    'sup-group-other-than-own': rule("if by and any(x['group'] != group and (x['path'], x['interface']) == "
                                     "tuple(r['path']) for x in rows):"),
    'sup-group-prefix': rule("if by and any(x['group'].split('-')[0] == by.split('-')[0] and "
                             "(x['path'], x['interface']) == tuple(r['path']) for x in rows):"),
    'del-positive': [(S, A_POS, '')],
    'del-other-interface': [(S, A_OTHER, '')],
    'del-table': [(S, A_TABLE, '')],
    'del-another-path': [(S, A_PATH, '')],
    'del-other+table': [(S, A_OTHER, ''), (S, A_TABLE, '')],
    'del-other+table+path': [(S, A_OTHER, ''), (S, A_TABLE, ''), (S, A_PATH, '')],
    'no-path+del-another-path': rule("if by and any((x['group'], x['interface']) == (by, r['path'][1]) for x in rows):")
    + [(S, A_PATH, '')],
}


def one(name, edits):
    tree = SCRATCH / name.replace('+', '_')
    shutil.rmtree(tree, ignore_errors=True)
    tree.mkdir(parents=True)
    subprocess.run(f'git -C {CLONE} archive HEAD tb sw scripts | tar -x -C {tree}', shell=True, check=True)
    for path, old, new in edits:
        p = tree / path
        text = p.read_text()
        if text.count(old) != 1:
            return name, f'ANCHOR {old[:50]!r} found {text.count(old)}', '', ''
        p.write_text(text.replace(old, new))
    got = subprocess.run([sys.executable, '-B', str(tree / H / 'run.py'), '--self-test'], capture_output=True, text=True)
    out = got.stdout + got.stderr
    fails = [re.sub(r'^FAIL ', '', x)[:95] for x in out.splitlines() if x.startswith('FAIL ')]
    esc = [x.split(': ESCAPED')[0].removeprefix('MUTANT ') for x in out.splitlines() if ': ESCAPED ' in x]
    tail = [x for x in out.splitlines() if 'self-test:' in x]
    shutil.rmtree(tree, ignore_errors=True)
    return name, got.returncode, (fails, esc), tail[-1] if tail else out[-300:]


with cf.ThreadPoolExecutor(8) as ex:
    results = list(ex.map(lambda kv: one(*kv), PROBES.items()))
for name, rc, detail, tail in results:
    fails, esc = detail if detail else ([], [])
    print(f'{name}: rc={rc} | {tail}')
    for x in fails:
        print(f'    check fails: {x}')
    for x in esc:
        print(f'    mutant escapes: {x}')
