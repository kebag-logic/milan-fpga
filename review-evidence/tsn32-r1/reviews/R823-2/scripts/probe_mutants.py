#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer fault probes for tsn-c-stack #32 (disposable).

For each probe defect: copy the head tree's src/acmp.c into a probe tree, apply one exact
textual replacement (it must match once), build the ACMP host tests with the pinned GoogleTest,
run acmp_tests, acmp_wide and acmp_walk, and run the old-versus-new differential against main.
The probe tree's src/acmp.c is restored to the head bytes afterwards and checked by hash.

Usage: probe_mutants.py HEAD_PROBE_TREE MAIN_TREE OUT_DIR
"""
import hashlib, json, subprocess, sys
from pathlib import Path

P = Path(__file__).resolve().parents[1]
tree, main, out = (Path(a).resolve() for a in sys.argv[1:4])
src = tree / 'src/acmp.c'
pristine = src.read_bytes()
digest = hashlib.sha256(pristine).hexdigest()

PROBES = {
    'control-none': None,
    'release-marks-only-word-zero': (
        '\t\t\t\t\tmark(a, k);\n\t\t\t\t\ta->sinks[k].change_owed--;',
        '\t\t\t\t\tif (k < 32u) {\n\t\t\t\t\t\tmark(a, k);\n\t\t\t\t\t}\n\t\t\t\t\ta->sinks[k].change_owed--;'),
    'marks-never-cleared': (
        '\tmemset(a->dirty, 0, sizeof a->dirty);\n\ta->dirty_if = 0u;\n', ''),
    'walk-expiry-unmarked-control': (
        '\t\t\tmark(a, k);\n\t\t\tsm_expired(a, k);', '\t\t\tsm_expired(a, k);'),
    'walk-kind-unmarked-control': (
        '\tmark(a, sink);\n\ta->sinks[sink].tk_failed = failed;', '\ta->sinks[sink].tk_failed = failed;'),
    'walk-probe-left-unmarked-control': (
        '\t\tmark(a, o->probe_of - 1u);\n', ''),
    'probe-left-marks-only-word-zero': (
        '\t\tmark(a, o->probe_of - 1u);\n', '\t\tif (o->probe_of - 1u < 32u) {\n\t\t\tmark(a, o->probe_of - 1u);\n\t\t}\n'),
    'unbind-marks-only-word-zero': (
        '\tstruct acmp_sink *s = &a->sinks[k];\n\tmark(a, k);\n\tif (s->state',
        '\tstruct acmp_sink *s = &a->sinks[k];\n\tif (k < 32u) {\n\t\tmark(a, k);\n\t}\n\tif (s->state'),
    'bind-marks-only-word-zero': (
        '\tstruct acmp_sink *s = &a->sinks[k];\n\tmark(a, k);\n\tbool sw',
        '\tstruct acmp_sink *s = &a->sinks[k];\n\tif (k < 32u) {\n\t\tmark(a, k);\n\t}\n\tbool sw'),
}

def run(argv, cwd=None, log=None):
    r = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if log is not None:
        log.write_text(r.stdout)
    return r.returncode, r.stdout

results = {}
out.mkdir(parents=True, exist_ok=True)
build = out / 'build'
try:
    rc, text = run(['cmake', '-S', str(tree), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug'], log=out / 'configure.log')
    if rc:
        raise SystemExit('configure failed')
    for name, edit in PROBES.items():
        body = pristine.decode()
        if edit is not None:
            if body.count(edit[0]) != 1:
                results[name] = {'error': 'anchor matched %d times' % body.count(edit[0])}
                continue
            body = body.replace(edit[0], edit[1])
        src.write_text(body)
        rc, _ = run(['cmake', '--build', str(build), '-j8', '--target', 'acmp_tests', 'acmp_wide', 'acmp_walk'], log=out / (name + '-build.log'))
        entry = {'build_rc': rc}
        if rc == 0:
            for test in ('acmp_tests', 'acmp_wide', 'acmp_walk'):
                trc, ttext = run([str(build / test)], log=out / (name + '-' + test + '.log'))
                failed = sorted({line[len('[  FAILED  ] '):].split()[0] for line in ttext.splitlines()
                                 if line.startswith('[  FAILED  ] ') and 'listed below' not in line
                                 and '.' in line[len('[  FAILED  ] '):].split()[0]})
                entry[test] = {'rc': trc, 'failed': failed}
            drc, dtext = run(['sh', str(P / 'scripts/differential.sh'), str(tree), str(main), str(out / (name + '-diff')), '4'],
                             log=out / (name + '-differential.log'))
            entry['differential'] = {'rc': drc, 'divergent': [l for l in dtext.splitlines() if l.startswith('DIVERGE')][:8]}
        results[name] = entry
        print(name, json.dumps(entry), flush=True)
finally:
    src.write_bytes(pristine)
    assert hashlib.sha256(src.read_bytes()).hexdigest() == digest
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print('restored', digest)
