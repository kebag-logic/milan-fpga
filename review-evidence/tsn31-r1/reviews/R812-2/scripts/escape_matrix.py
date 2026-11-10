#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Escape/catch matrix for registered plants (tsn-c-stack issue 31), reviewer-owned.

usage: escape_matrix.py <clean head clone> <scratch work dir> <receipt json> <jobs> <plant name>...

For each named plant of tests/mutations.json: export the head (git archive) into a private copy, apply the plant's
old->new exactly once, configure and build the whole CMake project (GCC, Debug, as the CI's gcc build without
coverage), then
  (a) run the whole CTest suite with GTEST_FILTER excluding every killer test of the plant: the plant must ESCAPE;
  (b) run acmp_tests and acmp_wide with only the killer tests: the plant must be CAUGHT, with every registered
      needle in the output.
An unplanted control runs (a) with every registered killer of the named plants excluded, and (b) must pass.
"""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

CLONE, WORK, OUT, JOBS = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(), int(sys.argv[4])
NAMES = sys.argv[5:]
REG = {p['name']: p for p in json.loads((CLONE / 'tests/mutations.json').read_text())}


def sh(argv, log, env=None, cwd=None):
    with open(log, 'a') as f:
        f.write('$ ' + ' '.join(map(str, argv)) + '\n'); f.flush()
        return subprocess.run(argv, stdout=f, stderr=subprocess.STDOUT, env=env, cwd=cwd, timeout=1200).returncode


def one(name):
    d = WORK / name
    shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
    subprocess.run('git -C "%s" archive HEAD | tar -x -C "%s"' % (CLONE, d), shell=True, check=True)
    row = {'plant': name}
    if name == 'unplanted':
        kills = [k for n in NAMES if n != 'unplanted' for k in REG[n]['kills']]
    else:
        p = REG[name]; f = d / p['path']; text = f.read_text()
        row['matches'] = text.count(p['old'])
        if row['matches'] != 1:
            row['error'] = 'plant must apply exactly once'; return row
        f.write_text(text.replace(p['old'], p['new'])); kills = p['kills']
    killers = sorted({k['test'] for k in kills})
    row['killers'] = killers
    log = d / 'log.txt'; b = d / 'b'
    if sh(['cmake', '-S', d, '-B', b, '-DCMAKE_BUILD_TYPE=Debug', '-DCMAKE_C_COMPILER=gcc', '-DCMAKE_CXX_COMPILER=g++'], log) or \
            sh(['cmake', '--build', b, '-j4'], log):
        row['build'] = 'FAILED'; return row
    env = dict(os.environ, GTEST_FILTER='-' + ':'.join(killers))
    rc = sh(['ctest', '--test-dir', b, '-j4', '--output-on-failure'], d / 'without-killers.log', env=env)
    tail = [l for l in (d / 'without-killers.log').read_text().splitlines() if 'tests passed' in l or 'Failed' in l or '***' in l]
    row['without_killers'] = {'ctest_rc': rc, 'summary': tail[:6], 'verdict': 'ESCAPES' if rc == 0 else 'CAUGHT-BY-OTHER'}
    out = ''
    rcs = {}
    for binary in ('acmp_tests', 'acmp_wide'):
        lg = d / ('only-killers-' + binary + '.log')
        rcs[binary] = sh([b / binary, '--gtest_filter=' + ':'.join(killers)], lg)
        out += lg.read_text()
    needles = {k['needle']: (k['needle'] in out) for k in kills}
    failed = sorted({l.split('] ')[1].split(' ')[0] for l in out.splitlines() if l.startswith('[  FAILED  ] ') and '.' in l and 'listed below' not in l})
    row['only_killers'] = {'rc': rcs, 'failed_tests': failed, 'needles_present': needles,
                           'verdict': ('PASSES' if not any(rcs.values()) else
                                       ('CAUGHT-WITH-ALL-NEEDLES' if all(needles.values()) else 'CAUGHT-NEEDLE-MISSING'))}
    return row


WORK.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(JOBS) as pool:
    rows = list(pool.map(one, NAMES))
OUT.write_text(json.dumps(rows, indent=1) + '\n')
for r in rows:
    print(f"{r['plant']:42s} matches={r.get('matches', '-')} without-killers={r.get('without_killers', {}).get('verdict')} "
          f"only-killers={r.get('only_killers', {}).get('verdict')} {r.get('error', '')}{r.get('build', '')}")
