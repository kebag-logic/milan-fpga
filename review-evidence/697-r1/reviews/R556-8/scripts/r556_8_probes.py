#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probes for round 9 of the assertion and package-prefix fixes.

usage: r556_8_probes.py HEAD_CLONE WORK
Run inside isolated.sh (scratch GoogleTest 1.14.0 prefix, ambient include/library paths unset).
Every probe works on a fresh `git archive HEAD` copy; the head clone is only read.
A: refused names regenerated with g++ and clang++ equal the shipped list; every macro name defined
   by any installed gtest/gmock header (public and internal) beginning EXPECT_, ASSERT_ or GTEST_
   outside the allowlist, and every FAIL*/ADD_FAILURE*/SUCCEED name, is refused by errors().
B: revert each round-9 change in a copy and require the shipped gate or control to fail.
C: project signedness warnings stay fatal in the real mutation build with both compilers,
   while the unmodified head builds with both compilers from the non-default prefix.
D: shipped tests/ contain no refused identifier.
"""
import io
import json
import os
import re
import subprocess
import sys
import tarfile
from pathlib import Path

head = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
work.mkdir(parents=True, exist_ok=True)
ARCHIVE = subprocess.check_output(['git', 'archive', 'HEAD'], cwd=head)
SHA = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=head, text=True).strip()
results = []


def tree(name):
    target = work / name
    if target.exists():
        subprocess.run(['rm', '-rf', str(target)], check=True)
    target.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(ARCHIVE)) as archive:
        archive.extractall(target, filter='data')
    return target


def edit(path, old, new, count=1):
    text = path.read_text()
    if text.count(old) != count:
        raise SystemExit(f'probe edit anchor changed in {path}: {old!r}')
    path.write_text(text.replace(old, new))


def run(name, argv, cwd, env=None):
    with (work / (name + '.log')).open('w') as log:
        rc = subprocess.run(argv, cwd=cwd, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    return rc, (work / (name + '.log')).read_text()


def record(probe, expected, observed, ok, detail=''):
    row = {'probe': probe, 'expected': expected, 'observed': observed,
           'verdict': 'PASS' if ok else 'FAIL', 'detail': detail}
    results.append(row)
    print(json.dumps(row), flush=True)


def gate_module(t):
    sys.path.insert(0, str(t / 'scripts'))
    import assertion_forms
    return assertion_forms


# A. vocabulary
t = tree('vocabulary')
forms = gate_module(t)
shipped = json.loads((t / 'scripts/assertion-defaults.json').read_text())['refused_macros']
for cxx in ('g++', 'clang++'):
    os.environ['CXX'] = cxx
    generated = forms.refused_macros()
    record('A1 regenerate refused names with ' + cxx, 'equal to shipped list',
           f'{len(generated)} names, equal={generated == shipped}', generated == shipped)
os.environ.pop('CXX', None)
spi = ['EXPECT_FATAL_FAILURE', 'EXPECT_FATAL_FAILURE_ON_ALL_THREADS',
       'EXPECT_NONFATAL_FAILURE', 'EXPECT_NONFATAL_FAILURE_ON_ALL_THREADS']
record('A2 failure-capturing names in shipped list', 'all four present',
       str([n in shipped for n in spi]), all(n in shipped for n in spi))
include = Path(subprocess.check_output(['pkg-config', '--variable=includedir', 'gtest'], text=True).strip())
every = sorted(str(p.relative_to(include)) for pkg in ('gtest', 'gmock') for p in (include / pkg).rglob('*.h'))
public = [h for h in every if '/internal/' not in h]
names = set()
for cxx in ('g++', 'clang++'):
    out = subprocess.run([cxx, '-std=c++20', *forms.package_flags('--cflags'), '-x', 'c++', '-dM', '-E', '-'],
                         input=''.join(f'#include <{h}>\n' for h in every), text=True,
                         capture_output=True, check=True).stdout
    names |= set(re.findall(r'^#define ([A-Za-z_]\w*)', out, re.M))
targets = sorted(n for n in names if n not in forms.ALLOWED and (
    n.startswith(('EXPECT_', 'ASSERT_', 'GTEST_', 'FAIL', 'ADD_FAILURE')) or n == 'SUCCEED'))
source = '\n'.join(n + '(x);' for n in targets) + '\n'
refused = {e.split(': ', 1)[1] for e in forms.errors(source) if e.startswith('unsupported assertion form: ')}
missing = sorted(set(targets) - refused)
record('A3 every installed-header EXPECT_/ASSERT_/GTEST_/FAIL*/ADD_FAILURE*/SUCCEED macro refused',
       f'{len(targets)} refused', f'{len(refused & set(targets))} refused; missing={missing[:20]}', not missing,
       f'{len(public)} public headers, {len(every)} headers in total')
allowed_hits = sorted(n for n in forms.ALLOWED
                      if forms.errors(n + '(x);'))
record('A4 the 14 allowed forms stay accepted', 'none refused', str(allowed_hits), not allowed_hits)
other = sorted(n for n in names if re.search(r'FAIL|SUCCEED|EXPECT|ASSERT', n) and n not in targets
               and n not in forms.ALLOWED)
(work / 'A-other-names.json').write_text(json.dumps(other, indent=2) + '\n')
record('A5 other installed macro names mentioning FAIL/SUCCEED/EXPECT/ASSERT (informational)',
       'listed', f'{len(other)} names, see A-other-names.json', True, ' '.join(other[:30]))
(work / 'A-public-headers.json').write_text(json.dumps(public, indent=2) + '\n')
record('A6 public header count', '21', str(len(public)), len(public) == 21)
lexer = forms.errors('EXPECT_UNLISTED_(1); GTEST_X; ASSERT_Y_; ok_EXPECT_Z(1);')
record('A7 prefix rule: trailing-underscore and object-like names', 'three refused, ok_EXPECT_Z accepted',
       str(lexer), lexer == ['unsupported assertion form: ASSERT_Y_', 'unsupported assertion form: EXPECT_UNLISTED_',
                             'unsupported assertion form: GTEST_X'])
sys.path.pop(0)
for module in ('assertion_forms', 'compiler_tokens'):
    sys.modules.pop(module, None)

# D. shipped tests
hits = []
for path in sorted((t / 'tests').rglob('*')):
    if path.suffix in ('.c', '.cc', '.cpp', '.h', '.hpp'):
        hits += [(str(path.relative_to(t)), e) for e in forms.errors(path.read_text())]
record('D1 shipped tests/ have no refused identifier', 'none', str(hits), not hits)

# B. regression controls: revert one round-9 change per copy; the shipped check must fail.
py = sys.executable
b1 = tree('B1-two-headers')
edit(b1 / 'scripts/assertion_forms.py',
     "input=''.join('#include <' + name + '>\\n' for name in sorted(headers)),",
     "input='#include <gtest/gtest.h>\\n#include <gmock/gmock.h>\\n',")
rc, log = run('B1-two-headers', [py, 'scripts/assertion_templates.py', '--check', '--work', str(work / 'B1-work')], b1)
record('B1 generator reverted to gtest.h+gmock.h only: --check', 'rc!=0, templates differ',
       f'rc={rc}', rc != 0 and 'assertion templates differ' in log)
b2 = tree('B2-no-prefix-rule')
edit(b2 / 'scripts/assertion_forms.py',
     "value in refused or value.startswith(('EXPECT_', 'ASSERT_', 'GTEST_'))", 'value in refused')
rc, log = run('B2-no-prefix-rule', [py, 'scripts/assertion_templates.py', '--check', '--selftest',
                                    '--work', str(work / 'B2-work')], b2)
record('B2 prefix rule removed: --check --selftest', 'rc!=0 at the internal control',
       f'rc={rc}', rc != 0 and 'internal' in log)
b3 = tree('B3-json-without-spi')
data = json.loads((b3 / 'scripts/assertion-defaults.json').read_text())
data['refused_macros'] = [n for n in data['refused_macros'] if n not in spi]
(b3 / 'scripts/assertion-defaults.json').write_text(json.dumps(data, indent=2) + '\n')
rc, log = run('B3-json-without-spi', [py, 'scripts/assertion_templates.py', '--check', '--work', str(work / 'B3-work')], b3)
record('B3 shipped list without the four failure-capturing names: --check', 'rc!=0',
       f'rc={rc}', rc != 0 and 'assertion templates differ' in log)
b4 = tree('B4-no-isystem')
edit(b4 / 'scripts/assertion_forms.py', "        if flag == '-I':", "        if False:")
edit(b4 / 'scripts/assertion_forms.py', "        elif flag.startswith('-I'):", "        elif False:")
rc, log = run('B4-no-isystem-dependency', [py, 'scripts/dependency_selftest.py', '--work', str(work / 'B4-dep'),
                                           '--jobs', '8'], b4)
record('B4a -isystem rewrite removed: dependency gate', 'rc!=0 (header warnings under -Werror)',
       f'rc={rc}', rc != 0, (re.findall(r'.*error:.*', log) or [log.strip().splitlines()[-1]])[0][:200])
rc, log = run('B4-no-isystem-mutation', [py, 'scripts/mutation.py', '--work', str(work / 'B4-mut'),
                                         '--select', 'acmp-header-no-resp-2s', '--jobs', '8'], b4)
record('B4b -isystem rewrite removed: mutation build from scratch prefix', 'rc!=0',
       f'rc={rc}', rc != 0, (re.findall(r'.*error:.*', log) or [''])[0][:200])
b5 = tree('B5-dependency-scratch-unused')
edit(b5 / 'scripts/dependency_selftest.py',
     "    flags['--cflags'] = ['-I' + str(include), *flags['--cflags']]\n", '')
rc, log = run('B5-dependency-scratch-unused', [py, 'scripts/dependency_selftest.py', '--work', str(work / 'B5-dep'),
                                               '--jobs', '8'], b5)
record('B5 dependency control without its scratch header copy (sensitivity, informational)',
       'informational', f'rc={rc}', True, 'rc=0 means the scratch copy is not itself observed by the control')

# C. signedness in the real mutation build, both compilers
for cc, cxx in (('gcc', 'g++'), ('clang', 'clang++')):
    env = dict(os.environ, CC=cc, CXX=cxx)
    c0 = tree('C0-head-' + cc)
    rc, log = run('C0-head-' + cc, [py, 'scripts/mutation.py', '--work', str(work / ('C0-mut-' + cc)),
                                    '--select', 'acmp-header-no-resp-2s', '--jobs', '8'], c0, env)
    record(f'C0 unmodified head, {cxx}: mutation build and catch from scratch prefix', 'rc=0',
           f'rc={rc}', rc == 0)
    c1 = tree('C1-signed-' + cc)
    test = c1 / 'tests/test_acmp.cpp'
    test.write_text(test.read_text() +
                    '[[maybe_unused]] static bool tsn_probe_compare(unsigned left, int right) { return left == right; }\n')
    rc, log = run('C1-signed-' + cc, [py, 'scripts/mutation.py', '--work', str(work / ('C1-mut-' + cc)),
                                      '--select', 'acmp-header-no-resp-2s', '--jobs', '8'], c1, env)
    record(f'C1 project signed comparison in a test, {cxx}: mutation build', 'rc!=0 with sign-compare',
           f'rc={rc}', rc != 0 and 'sign-compare' in log)

(work / 'results.json').write_text(json.dumps({'head': SHA, 'results': results}, indent=2) + '\n')
failed = [r['probe'] for r in results if r['verdict'] != 'PASS']
print('probes:', len(results), 'failed:', failed)
raise SystemExit(1 if failed else 0)
