#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: compile and run GoogleTest controls, then ask the assertion gate.

usage: probe_assertions.py HEAD_TREE OLD_TREE WORK
HEAD_TREE and OLD_TREE are exported trees (git archive) of the exact head and of the
previous round head. Each control is compiled with the pinned pkg-config flags and run;
the source gate verdict is taken from both trees' scripts/assertion_forms.errors().
"""
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

head, old, work = (Path(a).resolve() for a in sys.argv[1:4])
work.mkdir(parents=True, exist_ok=True)


def gate(tree, source):
    code = ('import sys; sys.path.insert(0, sys.argv[1] + "/scripts");'
            'from assertion_forms import errors; import json;'
            'print(json.dumps(errors(sys.stdin.read())))')
    out = subprocess.run([sys.executable, '-c', code, str(tree)], input=source, text=True,
                         capture_output=True, cwd=str(work))
    if out.returncode:
        return 'GATE-ERROR: ' + out.stderr.strip().splitlines()[-1]
    return json.loads(out.stdout)


def flags(option):
    return shlex.split(subprocess.check_output(['pkg-config', option, 'gmock', 'gtest'], text=True))


HDR = '#include <gtest/gtest.h>\n#include <gmock/gmock.h>\n'
SPI = HDR + '#include <gtest/gtest-spi.h>\n'
CASES = [
    # label, source, honest?, expected head verdict ('refuse'|'accept')
    ('spi-nonfatal', SPI + 'static void helper() { EXPECT_TRUE(false) << "helper diagnostic"; }\n'
     'TEST(Probe, Spi) { EXPECT_NONFATAL_FAILURE(helper(), "helper diagnostic"); }\n', 'refuse'),
    ('spi-fatal', SPI + 'static void helper() { ASSERT_TRUE(false) << "helper diagnostic"; }\n'
     'TEST(Probe, Spi) { EXPECT_FATAL_FAILURE(helper(), "helper diagnostic"); }\n', 'refuse'),
    ('spi-nonfatal-all-threads', SPI + 'static void helper() { EXPECT_TRUE(false) << "helper diagnostic"; }\n'
     'TEST(Probe, Spi) { EXPECT_NONFATAL_FAILURE_ON_ALL_THREADS(helper(), "helper diagnostic"); }\n', 'refuse'),
    ('spi-fatal-all-threads', SPI + 'static void helper() { ASSERT_TRUE(false) << "helper diagnostic"; }\n'
     'TEST(Probe, Spi) { EXPECT_FATAL_FAILURE_ON_ALL_THREADS(helper(), "helper diagnostic"); }\n', 'refuse'),
    ('gtest-assert-lt', HDR + 'TEST(Probe, P) { GTEST_ASSERT_LT(2, 1); }\n', 'refuse'),
    ('gtest-fail', HDR + 'TEST(Probe, P) { GTEST_FAIL(); }\n', 'refuse'),
    ('expect-near', HDR + 'TEST(Probe, P) { EXPECT_NEAR(1.0, 2.0, 0.1); }\n', 'refuse'),
    ('expect-that', HDR + 'TEST(Probe, P) { EXPECT_THAT(1, ::testing::Eq(2)); }\n', 'refuse'),
    ('expect-gt', HDR + 'TEST(Probe, P) { EXPECT_GT(1, 2); }\n', 'refuse'),
    ('expect-pred2', HDR + 'static bool lt(int a, int b) { return a < b; }\n'
     'TEST(Probe, P) { EXPECT_PRED2(lt, 2, 1); }\n', 'refuse'),
    ('add-failure', HDR + 'TEST(Probe, P) { ADD_FAILURE() << "x"; }\n', 'refuse'),
    ('fail', HDR + 'TEST(Probe, P) { FAIL() << "x"; }\n', 'refuse'),
    ('succeed-skip', HDR + 'TEST(Probe, P) { SUCCEED(); GTEST_SKIP(); }\n', 'refuse'),
    ('no-fatal-failure', HDR + 'static void helper() { ASSERT_TRUE(false); }\n'
     'TEST(Probe, P) { EXPECT_NO_FATAL_FAILURE(helper()); }\n', 'refuse'),
    ('paste', HDR + '#define JOIN(a, b) a##b\nTEST(Probe, P) { JOIN(EXPECT_, TRUE)(false); }\n', 'refuse'),
    ('paste-digraph', HDR + '#define JOIN(a, b) a%:%:b\nTEST(Probe, P) { JOIN(EXPECT_, TRUE)(false); }\n', 'refuse'),
    ('allowed-forms', HDR + 'struct M { MOCK_METHOD(void, f, ()); };\n'
     'TEST(Probe, P) { M m; EXPECT_CALL(m, f()).Times(0); EXPECT_TRUE(true); ASSERT_FALSE(false);'
     ' EXPECT_EQ(1, 1); ASSERT_NE(1, 2); EXPECT_LE(1, 1); ASSERT_GE(2, 1) << "owned ## text"; }\n', 'accept'),
    ('literal-text', HDR + '// GTEST_FAIL ##\nstatic const char *t = "EXPECT_NEAR ## GTEST_FAIL";\n'
     'TEST(Probe, P) { EXPECT_TRUE(t != nullptr); }\n', 'accept'),
]

rows = []
for label, source, expected in CASES:
    path = work / (label + '.cpp')
    path.write_text(source)
    binary = work / label
    build = subprocess.run([os.environ.get('CXX', 'g++'), '-std=c++20', '-Wall', '-Wextra', '-Werror',
                            *flags('--cflags'), str(path), *flags('--libs'), '-lgtest_main', '-o', str(binary)],
                           capture_output=True, text=True)
    run_rc = None
    if build.returncode == 0:
        run_rc = subprocess.run([str(binary)], capture_output=True, timeout=60).returncode
    h, o = gate(head, source), gate(old, source)
    verdict = 'refuse' if h and not isinstance(h, str) else ('accept' if h == [] else 'error')
    outcome = 'AS-EXPECTED' if verdict == expected else 'UNEXPECTED'
    rows.append({'probe': label, 'compiled': build.returncode == 0, 'run_rc': run_rc,
                 'head_gate': h, 'previous_round_gate': o, 'expected_head': expected, 'outcome': outcome})
    print(f'{label}: compiled={build.returncode == 0} run_rc={run_rc} head={h} previous={o} -> {outcome}')
    if build.returncode:
        print(build.stderr[-1500:])
(work / 'probe_assertions.json').write_text(json.dumps(rows, indent=1) + '\n')
