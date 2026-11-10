#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""For each named plant in TREE/tests/mutations.json: apply it once to a copy of src/acmp.c, build the 16-sink
acmp_tests and the 33-sink acmp_wide (shift,undefined, no recovery), then run each binary
  (a) with every registered killer test filtered out: the plant must escape (rc 0), and
  (b) with only the registered killer tests of that arm: the run must fail and print every registered needle.
usage: escape_kill.py TREE WORK JOBS NAME..."""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
tree, work, jobs, names = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
G = Path(os.environ['CMAKE_PREFIX_PATH'])
reg = {p['name']: p for p in json.loads((tree / 'tests/mutations.json').read_text())}
SAN = ['-fsanitize=shift,undefined', '-fno-sanitize-recover=shift,undefined']
ARMS = {'acmp_tests': ('16u', 'tests/test_acmp.cpp', []), 'acmp_wide': ('33u', 'tests/test_acmp_wide.cpp', SAN)}


def build(d, arm):
    n, test, extra = ARMS[arm]
    inc = ['-I', str(d / 'include'), '-I', str(tree / 'tests'), '-I', str(G / 'include')]
    b = d / arm
    for argv in (['gcc', '-std=c11', '-O0', '-g', '-Wall', '-Wextra', '-Werror', '-DNDEBUG', '-DCTRL_REENTRY_ASSERT',
                  '-DACMP_MAX_SINKS=' + n, *extra, *inc, '-c', str(d / 'src/acmp.c'), '-o', str(b) + '.o'],
                 ['g++', '-std=c++20', '-O0', '-g', '-DACMP_MAX_SINKS=' + n, *extra, *inc, str(tree / test),
                  str(tree / 'tests/main.cpp'), str(b) + '.o', str(G / 'lib/libgmock.a'), str(G / 'lib/libgtest.a'),
                  '-lpthread', '-o', str(b)]):
        r = subprocess.run(argv, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(r.stderr)
    return b


def go(name):
    p = reg[name]
    d = work / name
    shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(tree / 'include', d / 'include')
    shutil.copytree(tree / 'src', d / 'src')
    f = d / p['path']
    text = f.read_text()
    out = {'plant': name, 'old_count': text.count(p['old'])}
    if out['old_count'] != 1:
        return out
    f.write_text(text.replace(p['old'], p['new']))
    kills = p['kills']
    killers = sorted({k['test'] for k in kills})
    for arm in ARMS:
        b = build(d, arm)
        mine = [k for k in kills if k.get('arm', 'acmp_tests') == arm]
        r = subprocess.run([str(b), '--gtest_filter=-' + ':'.join(killers)], capture_output=True, text=True)
        out[arm + '_without_killers_rc'] = r.returncode
        out[arm + '_without_killers_summary'] = [l for l in r.stdout.splitlines() if 'PASSED  ]' in l or 'FAILED  ]' in l][:3]
        if mine:
            r = subprocess.run([str(b), '--gtest_filter=' + ':'.join(sorted({k['test'] for k in mine}))],
                               capture_output=True, text=True)
            log = r.stdout + r.stderr
            out[arm + '_killers_rc'] = r.returncode
            out[arm + '_needles_found'] = {k['needle']: (k['needle'] in log) for k in mine}
    return out


work.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(jobs) as pool:
    res = list(pool.map(go, names))
(work / 'results.json').write_text(json.dumps(res, indent=1) + '\n')
ok = True
for r in res:
    good = (r['old_count'] == 1 and all(r.get(a + '_without_killers_rc') == 0 for a in ARMS) and
            any(a + '_killers_rc' in r for a in ARMS) and
            all(r[a + '_killers_rc'] != 0 and all(r[a + '_needles_found'].values()) for a in ARMS if a + '_killers_rc' in r))
    ok &= good
    print(('OK  ' if good else 'BAD ') + json.dumps(r))
sys.exit(0 if ok else 1)
