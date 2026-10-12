#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independent removal-escape and gap-mutant probe for tsn-c-stack issue 24.

usage: escape_probe.py --tree <exported head tree> --work <dir> [--jobs N]

For every registered dafresh-* plant: apply it to a fresh copy, build, run the
whole GoogleTest suite with only its named killer excluded (must pass: the
plant escapes without its test), then run the killer alone (must fail with its
needle). Reviewer gap mutants run the whole suite and record which tests fail.
Python-gate mutants run the named script with and without the owning check.
"""
import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess

EXTRA = [
    ('x-no-expiry-clear', 'src/acmp.c', '\t\ts->answered = false;\n', ''),
    ('x-no-clock-refresh', 'src/acmp.c', '\t\ta->now_read = false;\n\t\ts->answered_at = now(a);',
     '\t\ts->answered_at = now(a);'),
    ('x-any-probe-status', 'src/acmp.c',
     'if (ok && frame[O_MSG] == ACMP_MSG_PROBE_TX_RESPONSE &&\n\t    ((frame[O_STATUS] >> 3) == ACMP_STATUS_SUCCESS ||\n'
     '\t     (frame[O_STATUS] >> 3) == ACMP_STATUS_TALKER_DEST_MAC_FAIL)) {',
     'if (ok && frame[O_MSG] == ACMP_MSG_PROBE_TX_RESPONSE && wire_be16(frame + O_TALKER_UID) < ACMP_MAX_SOURCES) {'),
    ('x-declaring-no-guard', 'src/acmp.c',
     '\tif (!enter(a)) {\n\t\treturn false;\n\t}\n\tif (source >= a->cfg.n_sources) {', '\tif (source >= a->cfg.n_sources) {'),
    ('x-listener-no-guard', 'src/acmp.c',
     '\tif (!enter(a)) {\n\t\treturn false;\n\t}\n\tif (source >= a->cfg.n_sources || interface',
     '\tif (source >= a->cfg.n_sources || interface'),
    ('x-listener-level-ignored', 'src/acmp.c', 'listener_registered = registered;', 'listener_registered = registered || true;'),
    ('x-window-minus-one', 'src/acmp.c', '>= a->cfg.da_fresh_ms', '>= a->cfg.da_fresh_ms - 1u'),
    ('x-declaring-bound', 'src/acmp.c', '\tif (source >= a->cfg.n_sources) {\n\t\treturn false;\n\t}\n\tstruct acmp_source *s',
     '\tif (source > a->cfg.n_sources) {\n\t\treturn false;\n\t}\n\tstruct acmp_source *s'),
    ('x-zero-never-expires', 'src/acmp.c', 'if (s->answered && (uint32_t)(now(a) - s->answered_at) >= a->cfg.da_fresh_ms) {',
     'if (s->answered && a->cfg.da_fresh_ms != 0u && (uint32_t)(now(a) - s->answered_at) >= a->cfg.da_fresh_ms) {'),
    ('x-signed-age', 'src/acmp.c', '(uint32_t)(now(a) - s->answered_at) >= a->cfg.da_fresh_ms',
     '(int32_t)(now(a) - s->answered_at) >= (int32_t)a->cfg.da_fresh_ms'),
]
PYGATES = [
    ('y-yaml-wide-range', 'scripts/entity_yaml.py', "integer(acmp['da_fresh_ms'], 15000, 15000,",
     "integer(acmp['da_fresh_ms'], 0, 2**31 - 1,", ['scripts/entity_selftest.py', '--work', '{work}/selftest'],
     ('scripts/entity_selftest.py', '    def test_dafresh_configuration(self):', '    def test_missing_golden_file(self):')),
    ('y-yaml-no-emit', 'scripts/entity_yaml.py', "    c += f'    .da_fresh_ms = {d[\"da_fresh_ms\"]}u,\\n'\n", '',
     ['scripts/entity_yaml.py', '--examples', '--check'], None),
    ('y-yaml-default-zero', 'scripts/entity_yaml.py', "d.get('acmp', {'da_fresh_ms': 15000})", "d.get('acmp', {'da_fresh_ms': 0})",
     ['scripts/entity_yaml.py', '--examples', '--check'], None),
]


def sh(argv, cwd, env, log):
    with open(log, 'w') as f:
        return subprocess.run(argv, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT).returncode


def plant(tree, work, name, path, old, new):
    copy = work / name / 'tree'
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(tree, copy)
    text = (copy / path).read_text()
    if text.count(old) != 1:
        raise SystemExit(f'{name}: anchor occurs {text.count(old)} times')
    (copy / path).write_text(text.replace(old, new))
    return copy


def build(copy, out, env):
    b = out / 'build'
    rc = sh(['cmake', '-S', str(copy), '-B', str(b), '-DCMAKE_BUILD_TYPE=Debug'], out, env, out / 'configure.log')
    if rc == 0:
        rc = sh(['cmake', '--build', str(b), '-j2'], out, env, out / 'build.log')
    return b, rc


def failed_tests(log):
    return sorted({l.split('] ')[1].split(' ')[0] for l in Path(log).read_text().splitlines()
                   if l.startswith('[  FAILED  ] ') and '.' in l.split('] ')[1].split(' ')[0]})


def registered(tree, work, env, item):
    name, path, old, new, killer, needle = item
    out = work / name
    out.mkdir(parents=True, exist_ok=True)
    copy = plant(tree, work, name, path, old, new)
    b, rc = build(copy, out, env)
    if rc:
        return {'plant': name, 'result': 'BUILD-ERROR'}
    e = dict(env, GTEST_FILTER='-' + killer)
    without = sh(['ctest', '--test-dir', str(b), '--output-on-failure', '-j2'], out, e, out / 'without-killer.log')
    e = dict(env, GTEST_FILTER=killer)
    alone = sh(['ctest', '--test-dir', str(b), '--output-on-failure', '-j2'], out, e, out / 'killer-alone.log')
    caught_needle = needle in (out / 'killer-alone.log').read_text()
    return {'plant': name, 'killer': killer, 'suite_without_killer_rc': without,
            'escapes_without_killer': without == 0,
            'other_failures': failed_tests(out / 'without-killer.log'),
            'killer_alone_rc': alone, 'killer_fails_with_needle': alone != 0 and caught_needle}


def extra(tree, work, env, item):
    name, path, old, new = item
    out = work / name
    out.mkdir(parents=True, exist_ok=True)
    copy = plant(tree, work, name, path, old, new)
    b, rc = build(copy, out, env)
    if rc:
        return {'plant': name, 'result': 'BUILD-ERROR'}
    e = {k: v for k, v in env.items() if k != 'GTEST_FILTER'}
    rc = sh(['ctest', '--test-dir', str(b), '--output-on-failure', '-j2'], out, e, out / 'suite.log')
    return {'plant': name, 'suite_rc': rc, 'result': 'CAUGHT' if rc else 'SURVIVED',
            'failing_tests': failed_tests(out / 'suite.log')}


def pygate(tree, work, env, item):
    name, path, old, new, argv, removal = item
    out = work / name
    out.mkdir(parents=True, exist_ok=True)
    copy = plant(tree, work, name, path, old, new)
    argv = ['python3'] + [a.format(work=out) for a in argv]
    (out / 'selftest').mkdir(exist_ok=True)
    rc = sh(argv, copy, env, out / 'gate.log')
    result = {'plant': name, 'gate': ' '.join(argv[1:2]), 'gate_rc': rc, 'caught': rc != 0}
    if removal:
        rel, start, stop = removal
        text = (copy / rel).read_text()
        i, j = text.index(start), text.index(stop)
        (copy / rel).write_text(text[:i] + text[j:])
        rc2 = sh(argv, copy, env, out / 'gate-without-owner.log')
        result.update(owner_removed_rc=rc2, escapes_without_owner=rc2 == 0)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--tree', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--jobs', type=int, default=8)
    p.add_argument('--only', default='', help='comma-separated plant names')
    a = p.parse_args()
    tree, work = a.tree.resolve(), a.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
    env['TMPDIR'] = str(work)
    plants = json.loads((tree / 'tests/mutations.json').read_text())
    reg = [(m['name'], m['path'], m['old'], m['new'], m['kills'][0]['test'], m['kills'][0]['needle'])
           for m in plants if m['name'].startswith('dafresh-')]
    only = set(filter(None, a.only.split(',')))
    keep = lambda items: [i for i in items if not only or i[0] in only]
    reg, extras, pys = keep(reg), keep(EXTRA), keep(PYGATES)
    with ThreadPoolExecutor(max_workers=a.jobs) as pool:
        jobs = [pool.submit(registered, tree, work, env, i) for i in reg]
        jobs += [pool.submit(extra, tree, work, env, i) for i in extras]
        jobs += [pool.submit(pygate, tree, work, env, i) for i in pys]
        results = [j.result() for j in jobs]
    (work / ('escape-probe' + ('-' + '-'.join(sorted(only)) if only else '') + '.json')).write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=1))


if __name__ == '__main__':
    main()
