#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Round 2 reviewer probes for tsn-c-stack #32 at a530ecaf (disposable).

Each probe copies the head tree (HEAD_TREE, an export of the head) into OUT/<name>, applies exact textual
replacements that must each match once, builds and runs acmp_walk with the pinned GoogleTest, and records
the failing tests and the assertion messages they printed. Probes run concurrently. The head tree is only read.
Probe 'control-static-assert-removed' instead runs scripts/check_conditionals.py --selftest on its copy.

Usage: r2_probes.py HEAD_TREE OUT_DIR JOBS
"""
import concurrent.futures, json, re, shutil, subprocess, sys
from pathlib import Path

head, out, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])

PROBES = {
    'control-none': [],
    # The third interface: sink 32's mark sets interface 0's bit instead of its own.
    'sink32-marks-wrong-interface': [('src/acmp.c',
        '\ta->dirty_if |= 1u << a->sinks[k].interface;\n}',
        '\ta->dirty_if |= 1u << (k < 32u ? a->sinks[k].interface : 0u);\n}')],
    # The release loop marks sink k % 32 instead of k.
    'release-marks-folded-sink': [('src/acmp.c',
        '\t\t\t\t\tmark(a, k);\n\t\t\t\t\ta->sinks[k].change_owed--;',
        '\t\t\t\t\tmark(a, k % 32u);\n\t\t\t\t\ta->sinks[k].change_owed--;')],
    # The interface clear keeps interface 2's bit only (reachable only at 33 sinks).
    'clear-keeps-third-interface': [('src/acmp.c',
        '\ta->dirty_if = 0u;\n', '\ta->dirty_if &= 4u;\n')],
    # Test-side vacuity probes: undo each round 2 lift and see what the guards report.
    'test-no-poll-first': [('tests/test_acmp_walk.cpp',
        '        if (wide && walked.a.owed_count != 0u && walked.room && rng.below(2u) == 0u) {',
        '        if (false && wide && walked.a.owed_count != 0u && walked.room && rng.below(2u) == 0u) {')],
    'test-no-poll-first-with-probe-left-second-word-plant': [
        ('tests/test_acmp_walk.cpp',
         '        if (wide && walked.a.owed_count != 0u && walked.room && rng.below(2u) == 0u) {',
         '        if (false && wide && walked.a.owed_count != 0u && walked.room && rng.below(2u) == 0u) {'),
        ('src/acmp.c', '\t\tmark(a, o->probe_of - 1u);\n',
         '\t\tif (o->probe_of - 1u < 32u) {\n\t\t\tmark(a, o->probe_of - 1u);\n\t\t}\n')],
    'test-sink32-on-interface-0-with-probe-left-second-word-plant': [
        ('tests/test_acmp_walk.cpp', 'k < 32u ? (k * 7u + k / 3u) % 2u : 2u', '(k * 7u + k / 3u) % 2u'),
        ('src/acmp.c', '\t\tmark(a, o->probe_of - 1u);\n',
         '\t\tif (o->probe_of - 1u < 32u) {\n\t\t\tmark(a, o->probe_of - 1u);\n\t\t}\n')],
    'test-room-always-at-33': [('tests/test_acmp_walk.cpp',
        '            bool room = rng.below(3u) != 0u;', '            bool room = wide || rng.below(3u) != 0u;')],
    'test-no-clear-assertions-with-never-cleared-plant': [
        ('tests/test_acmp_walk.cpp', '            for (std::uint32_t word : walked.a.dirty) {',
         '            for (std::uint32_t word : std::array<std::uint32_t, 0>{}) {'),
        ('tests/test_acmp_walk.cpp', '            ASSERT_EQ(walked.a.dirty_if, 0u)', '            ASSERT_EQ(0u, 0u)'),
        ('src/acmp.c', '\tmemset(a->dirty, 0, sizeof a->dirty);\n\ta->dirty_if = 0u;\n', '')],
    'control-static-assert-removed': [('tests/test_acmp_walk.cpp',
        'static_assert(ACMP_MAX_INTERFACES <= sizeof(acmp::dirty_if) * 8u, "the interface mark holds a bit for every interface");\n',
        '')],
}

def run(argv, cwd=None, env=None):
    r = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return r.returncode, r.stdout

def probe(name):
    tree = out / name
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(head, tree)
    for path, old, new in PROBES[name]:
        f = tree / path
        text = f.read_text()
        if text.count(old) != 1:
            return name, {'error': f'{path}: anchor matched {text.count(old)} times'}
        f.write_text(text.replace(old, new))
    if name == 'control-static-assert-removed':
        rc, text = run([sys.executable, 'scripts/check_conditionals.py', '--selftest', '--work', str(out / (name + '-work')),
                        '--jobs', '4'], cwd=tree)
        (out / (name + '.log')).write_text(text)
        return name, {'rc': rc, 'last': text.strip().splitlines()[-1] if text.strip() else ''}
    build = tree / 'build'
    rc, text = run(['cmake', '-S', str(tree), '-B', str(build), '-DCMAKE_BUILD_TYPE=Debug'])
    if rc == 0:
        rc, text = run(['cmake', '--build', str(build), '-j2', '--target', 'acmp_walk'])
    if rc:
        (out / (name + '-build.log')).write_text(text)
        return name, {'build_rc': rc}
    trc, ttext = run([str(build / 'acmp_walk')])
    (out / (name + '.log')).write_text(ttext)
    failed = sorted({l.split()[3] for l in ttext.splitlines() if l.startswith('[  FAILED  ] ') and 'listed below' not in l
                     and len(l.split()) > 3 and '.' in l.split()[3]})
    messages = sorted({m for m in re.findall(r'^(?:the|a|at) [^\n]*?(?=, at step|, on the|$)', ttext, re.M)})
    return name, {'rc': trc, 'failed': failed, 'messages': messages[:8]}

out.mkdir(parents=True, exist_ok=True)
results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
    for name, entry in pool.map(probe, PROBES):
        results[name] = entry
        print(name, json.dumps(entry), flush=True)
(out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
