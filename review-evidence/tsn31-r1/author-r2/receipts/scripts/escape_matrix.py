#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""usage: escape_matrix.py TREE WORK

For each named plant (and an unplanted control), plant it into a copy of TREE's src and include, build the 16-sink
acmp_tests and the 33-sink acmp_wide with scripts/mutation.py's flags, and run each binary twice: once with the plant's
killing tests filtered out ("without its killer": every other test must pass, so the plant escapes) and once with only
those tests ("with its killer": rc 1 and every registered needle of that arm in the output)."""
import json
import shlex
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
NAMES = ['acmp-wide-release-word-off-by-one', 'acmp-wide-owed-count-word-off-by-one',
         'acmp-wide-release-loop-word-off-by-one', 'acmp-owed-release-not-cleared', 'acmp-wide-release-clears-one-word']
WIDE = ['-DACMP_MAX_SINKS=33u', '-fsanitize=shift,undefined', '-fno-sanitize-recover=shift,undefined']
ARMS = {'acmp': ('test_acmp.cpp', []), 'acmp_wide': ('test_acmp_wide.cpp', WIDE)}
CFLAGS = ['-std=c11', '-O0', '-g', '-Wall', '-Wextra', '-Werror', '-DNDEBUG', '-DCTRL_REENTRY_ASSERT']
CXXFLAGS = ['-std=c++20', '-O0', '-g', '-Wall', '-Wextra', '-Werror']
GT = shlex.split(subprocess.check_output(['pkg-config', '--cflags', 'gmock', 'gtest'], text=True))
GL = shlex.split(subprocess.check_output(['pkg-config', '--libs', 'gmock', 'gtest'], text=True))
registry = {m['name']: m for m in json.loads((tree / 'tests/mutations.json').read_text())}


def sh(argv, log):
    with open(log, 'a') as f:
        f.write('$ ' + ' '.join(map(str, argv)) + '\n')
        f.flush()
        return subprocess.run(list(map(str, argv)), stdout=f, stderr=subprocess.STDOUT, timeout=300).returncode


shutil.rmtree(work, ignore_errors=True)
base = work / 'baseline'
base.mkdir(parents=True)
assert sh(['g++', *CXXFLAGS, *GT, '-c', tree / 'tests/main.cpp', '-o', base / 'main.o'], base / 'log.txt') == 0
for arm, (source, extra) in ARMS.items():
    assert sh(['g++', *CXXFLAGS, *extra, *GT, '-I', tree / 'include', '-I', tree / 'tests', '-I', tree / 'examples',
               '-c', tree / 'tests' / source, '-o', base / (arm + '.cpp.o')], base / 'log.txt') == 0


def run(name):
    d = work / (name or 'unplanted')
    shutil.copytree(tree / 'include', d / 'include')
    shutil.copytree(tree / 'src', d / 'src')
    log = d / 'log.txt'
    plant = registry.get(name)
    if plant:
        target = d / plant['path']
        text = target.read_text()
        assert text.count(plant['old']) == 1, name
        target.write_text(text.replace(plant['old'], plant['new']))
    rows = []
    for arm, (source, extra) in ARMS.items():
        kills = [k for k in (plant or {}).get('kills', []) if k.get('arm', 'acmp') == arm]
        killers = sorted({k['test'] for k in kills})
        assert sh(['gcc', *CFLAGS, *extra, '-I', d / 'include', '-c', d / 'src/acmp.c', '-o', d / (arm + '.c.o')], log) == 0
        assert sh(['g++', d / (arm + '.c.o'), base / (arm + '.cpp.o'), base / 'main.o', *extra[1:2], *GL,
                   '-o', d / arm], log) == 0
        row = {'plant': name or 'unplanted', 'arm': arm, 'killers': killers}
        for mode, flt in (('without', '-' + ':'.join(killers)), ('with', ':'.join(killers))):
            if mode == 'with' and not killers:
                continue
            out = subprocess.run([str(d / arm), '--gtest_filter=' + (flt if killers else '*')],
                                 capture_output=True, text=True, timeout=300)
            text = out.stdout + out.stderr
            (d / f'{arm}-{mode}.out').write_text(text)
            summary = [l for l in text.splitlines() if l.startswith(('[  PASSED  ]', '[  FAILED  ]', '[==========]'))]
            row[mode] = {'rc': out.returncode, 'summary': summary,
                         'needles': {k['needle']: k['needle'] in text for k in kills} if mode == 'with' else {}}
        rows.append(row)
    return rows


with ThreadPoolExecutor(6) as pool:
    results = [r for rows in pool.map(run, [None] + NAMES) for r in rows]
(work / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
ok = True
for r in results:
    w = r['without']
    line = f"{r['plant']:42} {r['arm']:9} without killer: rc {w['rc']} {w['summary'][-1] if w['summary'] else ''}"
    good = w['rc'] == 0
    if 'with' in r:
        x = r['with']
        found = all(x['needles'].values())
        line += f" | with {', '.join(t.split('.')[1] for t in r['killers'])}: rc {x['rc']}, needles {'all found' if found else x['needles']}"
        good = good and x['rc'] == 1 and found
    print(line)
    ok = ok and good
print('every plant escapes without its killer and is caught by it' if ok else 'MISMATCH')
sys.exit(0 if ok else 1)
