#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer gap mutants for the round-2 delta of tsn-c-stack PR 25.

usage: gap_mutants.py --tree <exported head tree> --work <dir> [--jobs N]

Each mutant is applied to a fresh copy, the hosted suite (all test binaries) is
built and run, and the failing tests are recorded.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

INIT_OLD = ('\t    cfg->n_sources > ACMP_MAX_SOURCES || cfg->da_fresh_ms >= UINT32_C(0x80000000)) {\n'
            '\t\treturn false;\n\t}\n')
INIT_NEW = '\t    cfg->n_sources > ACMP_MAX_SOURCES) {\n\t\treturn false;\n\t}\n'
EXPIRY = 'if (s->answered && (uint32_t)(now(a) - s->answered_at) >= a->cfg.da_fresh_ms) {'
MUTANTS = [
    # refusal moved after the instance is overwritten
    ('g-refusal-after-memset', 'src/acmp.c', [
        (INIT_OLD, INIT_NEW),
        ('\tmemset(a, 0, sizeof *a);\n\ta->cfg = *cfg;',
         '\tmemset(a, 0, sizeof *a);\n\tif (cfg->da_fresh_ms >= UINT32_C(0x80000000)) {\n\t\treturn false;\n\t}\n\ta->cfg = *cfg;')]),
    # refusal dropped entirely
    ('g-no-range-refusal', 'src/acmp.c', [(INIT_OLD, INIT_NEW)]),
    # zero interval refused instead of disabling the probe term
    ('g-zero-refused', 'src/acmp.c', [('cfg->da_fresh_ms >= UINT32_C(0x80000000)',
                                       'cfg->da_fresh_ms - 1u >= UINT32_C(0x7fffffff)')]),
    # expiry is not observed while a Listener holds the gate (PORTING: "even with a Listener")
    ('g-expiry-skipped-with-listener', 'src/acmp.c', [(EXPIRY, EXPIRY.replace('s->answered &&', 's->answered && !s->listener_registered &&'))]),
    # expiry is observed only after the destination is read valid (PORTING: "or an invalid destination")
    ('g-expiry-skipped-invalid-da', 'src/acmp.c', [
        (EXPIRY + '\n\t\ts->answered = false;\n\t}\n\tstruct acmp_source_state st;\n\tmemset(&st, 0, sizeof st);\n\tp_source(a, source, &st);\n',
         'struct acmp_source_state st;\n\tmemset(&st, 0, sizeof st);\n\tp_source(a, source, &st);\n\tif (st.dest_mac_valid && '
         + EXPIRY[4:] + '\n\t\ts->answered = false;\n\t}\n')]),
    # the PROBE_TX answer time is taken from the cached event clock (ages the window by the send time)
    ('g-answer-uses-event-clock', 'src/acmp.c', [('\t\ta->now_read = false;\n\t\ts->answered_at = now(a);',
                                                   '\t\ts->answered_at = a->now;')]),
]


def one(tree, work, env, mutant):
    name, path, edits = mutant
    out = work / name
    if out.exists():
        shutil.rmtree(out)
    copy = out / 'tree'
    shutil.copytree(tree, copy)
    text = (copy / path).read_text()
    for old, new in edits:
        if text.count(old) != 1:
            return {'mutant': name, 'result': 'ANCHOR-ERROR', 'anchor': old[:60]}
        text = text.replace(old, new)
    (copy / path).write_text(text)
    log = out / 'run.log'
    with open(log, 'w') as f:
        rc = subprocess.run(['cmake', '-S', str(copy), '-B', str(out / 'b'), '-DCMAKE_BUILD_TYPE=Debug'],
                            stdout=f, stderr=subprocess.STDOUT, env=env).returncode
        rc = rc or subprocess.run(['cmake', '--build', str(out / 'b'), '-j2'], stdout=f, stderr=subprocess.STDOUT, env=env).returncode
        if rc:
            return {'mutant': name, 'result': 'BUILD-ERROR'}
        rc = subprocess.run(['ctest', '--test-dir', str(out / 'b'), '--output-on-failure', '-j2'],
                            stdout=f, stderr=subprocess.STDOUT, env=env).returncode
    body = log.read_text()
    failing = sorted(set(re.findall(r'^\[  FAILED  \] (\w+\.\w+) \(', body, re.M)))
    return {'mutant': name, 'suite_rc': rc, 'result': 'CAUGHT' if rc else 'SURVIVED',
            'failing_tests': failing[:12], 'failing_count': len(failing)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tree', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--jobs', type=int, default=6)
    a = p.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
    a.work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        results = list(pool.map(lambda m: one(a.tree.resolve(), a.work.resolve(), env, m), MUTANTS))
    (a.work / 'gap-mutants.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=1))


if __name__ == '__main__':
    main()
