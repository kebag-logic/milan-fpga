#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Apply each source plant to a copy of src/acmp.c (or include/acmp.h) and run the 16-sink acmp_tests, the 33-sink
acmp_wide (shift,undefined, no recovery) and the review's every-sink probe at 33 sinks.
usage: plants.py TREE WORK JOBS"""
import json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
tree, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
here = Path(__file__).resolve().parent
G = Path(os.environ['CMAKE_PREFIX_PATH'])
reg = {p['name']: p for p in json.loads((tree / 'tests/mutations.json').read_text())}
def R(name): p = reg[name]; return (name, p['path'], p['old'], p['new'])
T = '\t\t'
plants = [('unplanted', None, None, None)] + [R(n) for n in (
    'acmp-wide-release-word-ignored', 'acmp-wide-owed-count-word-ignored', 'acmp-wide-release-loop-word-ignored',
    'acmp-unbind-echoes-the-talker', 'acmp-unbind-srp-after-response', 'acmp-unbind-change-before-response',
    'acmp-change-not-held-for-its-response', 'owed-bind-answer-lost-after-decline', 'owed-entry-widened',
    'acmp-first-owed-releases-every-change')] + [
    ('review-transmit-word-off-by-one', 'src/acmp.c', 'o->release[(release - 1u) / 32u] =', 'o->release[release / 32u] ='),
    ('review-transmit-unbounded-shift', 'src/acmp.c', '= 1u << ((release - 1u) % 32u);', '= 1u << (release - 1u);'),
    ('review-owed-count-word-off-by-one', 'src/acmp.c', 'change_owed + ((o->release[k / 32u]', 'change_owed + ((o->release[(k + 1u) / 32u]'),
    ('review-release-loop-word-off-by-one', 'src/acmp.c', 'change_owed - ((o->release[k / 32u]', 'change_owed - ((o->release[(k + 1u) / 32u]'),
    ('review-owed-count-unbounded-shift', 'src/acmp.c', 'change_owed + ((o->release[k / 32u] >> (k % 32u))', 'change_owed + ((o->release[k / 32u] >> k)'),
    ('review-release-loop-unbounded-shift', 'src/acmp.c', 'change_owed - ((o->release[k / 32u] >> (k % 32u))', 'change_owed - ((o->release[k / 32u] >> k)'),
    ('review-mask-not-cleared', 'src/acmp.c', '\tmemset(o->release, 0, sizeof o->release);\n', ''),
    ('review-mask-clears-one-word', 'src/acmp.c', 'memset(o->release, 0, sizeof o->release);', 'memset(o->release, 0, sizeof o->release[0]);'),
]
def sh(argv, log):
    with open(log, 'a') as f:
        f.write('$ ' + ' '.join(map(str, argv)) + '\n'); f.flush()
        return subprocess.run(argv, stdout=f, stderr=subprocess.STDOUT).returncode
SAN = ['-fsanitize=shift,undefined', '-fno-sanitize-recover=shift,undefined']
def run(plant):
    name, path, old, new = plant
    d = work / name; shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(tree / 'include', d / 'include'); shutil.copytree(tree / 'src', d / 'src')
    if path:
        f = d / path; text = f.read_text()
        assert text.count(old) == 1, (name, text.count(old)); f.write_text(text.replace(old, new))
    log = d / 'log.txt'; out = {'plant': name}
    inc = ['-I', str(d / 'include'), '-I', str(tree / 'tests'), '-I', str(G / 'include')]
    libs = [str(G / 'lib/libgmock.a'), str(G / 'lib/libgtest.a'), '-lpthread']
    for arm, n, test, extra in (('acmp_tests', '16u', tree / 'tests/test_acmp.cpp', []),
                                ('acmp_wide', '33u', tree / 'tests/test_acmp_wide.cpp', SAN),
                                ('every_sink_33', '33u', here / 'every_sink_probe.cpp', SAN)):
        b = d / arm
        rc = sh(['gcc', '-std=c11', '-O0', '-g', '-Wall', '-Wextra', '-Werror', '-DNDEBUG', '-DCTRL_REENTRY_ASSERT',
                 '-DACMP_MAX_SINKS=' + n, *extra, *inc, '-c', str(d / 'src/acmp.c'), '-o', str(b) + '.core.o'], log)
        if rc == 0:
            rc = sh(['g++', '-std=c++20', '-O0', '-g', '-DACMP_MAX_SINKS=' + n, *extra, *inc, str(test),
                     str(tree / 'tests/main.cpp'), str(b) + '.core.o', *libs, '-o', str(b)], log)
            if rc == 0:
                with open(d / (arm + '.out'), 'w') as f:
                    rc = subprocess.run([str(b)], stdout=f, stderr=subprocess.STDOUT, timeout=300).returncode
                out[arm] = 'pass' if rc == 0 else 'FAIL rc %d' % rc
                lines = (d / (arm + '.out')).read_text().splitlines()
                out[arm + '_summary'] = [l for l in lines if 'PASSED' in l or 'FAILED  ]' in l or 'runtime error' in l][:4]
                continue
        out[arm] = 'BUILD-REFUSED rc %d' % rc
    return out
work.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(jobs) as pool:
    results = list(pool.map(run, plants))
(work / 'results.json').write_text(json.dumps(results, indent=1) + '\n')
for r in results:
    print(r['plant'], '|', r['acmp_tests'], '|', r['acmp_wide'], '|', r['every_sink_33'])
