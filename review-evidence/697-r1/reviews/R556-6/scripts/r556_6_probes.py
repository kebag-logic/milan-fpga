#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R556-6 contract probes: each applies one short compiling form to a disposable
clone of the reviewed head, proves it builds (and, where relevant, links and runs),
then runs the repository gates and reports CAUGHT (some gate refuses) or GAP.

usage: r556_6_probes.py HEAD_CLONE WORK [probe ...]
Run with the reviewer environment (scripts/env.sh) loaded."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

PROBES = {}


def probe(name, rule, kind):
    def wrap(fn):
        PROBES[name] = (rule, kind, fn)
        return fn
    return wrap


def edit(tree, path, old, new, count=1):
    p = tree / path
    text = p.read_text()
    if text.count(old) != count:
        raise SystemExit(f'{path}: anchor {old!r} found {text.count(old)} times')
    p.write_text(text.replace(old, new))


@probe('ld-backslash-quote', 4, 'rv32')
def _(t):
    # GNU ld quoted names have no escapes; C11 treats \" as an escape, so the
    # C lexer sees a string where ld sees /* prose */ as a comment.
    edit(t, 'examples/rv32/link.ld', '*(.rodata .rodata.*) }',
         '*(.rodata .rodata.*) *("x\\" /* prose words */ "y") }')


@probe('ld-version-hash', 4, 'rv32')
def _(t):
    # A VERSION node accepts # comments in GNU ld; C11 sees a hash token mid-line.
    p = t / 'examples/rv32/link.ld'
    p.write_text(p.read_text() + 'VERSION { PROBE { local: *; # prose words\n}; }\n')


@probe('asm-include-ld', 5, 'rv32')
def _(t):
    # The assembler reads the included file; the gate lexes it as a linker script.
    (t / 'examples/rv32/include/probe.ld').write_text('/* SPDX-License-Identifier: MIT */\nnop # prose words\n')
    p = t / 'examples/rv32/start.S'
    p.write_text(p.read_text() + '.include "probe.ld"\n')


@probe('asm-include-h', 5, 'rv32')
def _(t):
    # Same with a header: C sees an object-like definition, the assembler a # comment line.
    (t / 'examples/rv32/include/probe.h').write_text('/* SPDX-License-Identifier: MIT */\n#define PROBE_VALUE 1 # prose words\n')
    p = t / 'examples/rv32/start.S'
    p.write_text(p.read_text() + '.include "probe.h"\n')


@probe('asm-end-trailer', 5, 'rv32')
def _(t):
    # Text after .end is ignored by the assembler; it is neither # comment nor conditional.
    p = t / 'examples/rv32/start.S'
    p.write_text(p.read_text() + '.end\nprose words after the end directive\n')


@probe('c-file-in-cpp-unit', 3, 'host')
def _(t):
    # A .c file lexed only as C11 but compiled only inside a C++20 test unit.
    (t / 'tests/probe_value.c').write_text(
        "// SPDX-License-Identifier: MIT\n#define TSN_PROBE_IGNORE(a) 0\nenum { probe_value = TSN_PROBE_IGNORE(1'2 // prose words '\n) };\n")
    # Appended at the end so generated line links stay current.
    p = t / 'tests/test_port.cpp'
    p.write_text(p.read_text() + '#include "probe_value.c"\n')


@probe('gtest-alias-forms', 6, 'host')
def _(t):
    # GoogleTest's GTEST_-prefixed aliases of assertion macros outside the allowed list.
    text = (t / 'tests/test_port.cpp').read_text()
    at = text.index('{', text.index('TEST(')) + 1
    (t / 'tests/test_port.cpp').write_text(
        text[:at] + '\n    GTEST_EXPECT_TRUE(true);\n    GTEST_ASSERT_EQ(1, 1);\n    GTEST_SUCCEED();' + text[at:])


@probe('token-pasted-near', 6, 'host')
def _(t):
    # EXPECT_NEAR spelled through token pasting; no raw identifier carries the name.
    text = (t / 'tests/test_port.cpp').read_text()
    at = text.index('{', text.index('TEST(')) + 1
    # Defined inside the body so generated line links stay current.
    (t / 'tests/test_port.cpp').write_text(
        text[:at] + '\n#define TSN_PROBE_PASTE(a, b) a##b\n    TSN_PROBE_PASTE(EXPE, CT_NEAR)(1.0, 1.0, 0.1);' + text[at:])


@probe('control-expect-near', 6, 'host')
def _(t):
    # Positive control: the literal form is refused by the assertion gate.
    text = (t / 'tests/test_port.cpp').read_text()
    at = text.index('{', text.index('TEST(')) + 1
    (t / 'tests/test_port.cpp').write_text(text[:at] + '\n    EXPECT_NEAR(1.0, 1.0, 0.1);' + text[at:])


@probe('control-asm-hash', 5, 'rv32')
def _(t):
    # Positive control: a direct # prose comment in start.S is refused.
    p = t / 'examples/rv32/start.S'
    p.write_text(p.read_text() + 'nop # prose words\n')


@probe('control-ld-comment', 4, 'rv32')
def _(t):
    # Positive control: a direct prose comment in link.ld is refused.
    p = t / 'examples/rv32/link.ld'
    p.write_text(p.read_text() + '/* prose words */\n')


def run(name, argv, cwd, log):
    r = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=1800)
    log.write(f'### {name}: rc {r.returncode}\n$ {" ".join(map(str, argv))}\n{r.stdout[-6000:]}\n')
    return r.returncode


def main():
    head, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    names = sys.argv[3:] or list(PROBES)
    work.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    results = []
    for name in names:
        rule, kind, apply = PROBES[name]
        tree = work / name
        shutil.rmtree(tree, ignore_errors=True)
        subprocess.run(['git', 'clone', '-q', '--no-hardlinks', str(head), str(tree)], check=True)
        apply(tree)
        diff = subprocess.run(['git', 'diff', '--no-color'], cwd=tree, capture_output=True, text=True).stdout
        diff += ''.join(f'--- untracked {u}\n' + (tree / u).read_text()
                        for u in subprocess.run(['git', 'ls-files', '-o', '--exclude-standard'], cwd=tree,
                                                capture_output=True, text=True).stdout.split())
        with (work / (name + '.log')).open('w') as log:
            log.write(f'probe {name} (rule {rule})\n{diff}\n')
            if kind == 'rv32':
                build = run('rv32-build-link-smoke', [py, 'scripts/baremetal.py', '--work', str(tree / 'build-rv32'), '--jobs', '16'], tree, log)
            else:
                build = run('host-configure', ['cmake', '-S', '.', '-B', 'build-host', '-DCMAKE_BUILD_TYPE=Debug'], tree, log)
                build = build or run('host-build', ['cmake', '--build', 'build-host', '-j16'], tree, log)
                build = build or run('host-test', ['ctest', '--test-dir', 'build-host', '-j16', '--output-on-failure'], tree, log)
            gates = {
                'comments': [py, 'scripts/check_comments.py'],
                'needles': [py, 'scripts/needle_audit.py'],
                'conditionals': [py, 'scripts/check_conditionals.py', '--work', str(tree / 'build-cond'), '--jobs', '16'],
                'boundary': [py, 'scripts/check_boundary.py', '--work', str(tree / 'build-boundary'), '--jobs', '16'],
                'traceability': [py, 'scripts/traceability.py', '--build', str(tree / 'build-reg'), '--jobs', '16'],
                'test-inventory': [py, 'scripts/test_inventory.py', '--build', str(tree / 'build-reg'), '--jobs', '16'],
                'license': [py, 'scripts/check_license.py'],
                'port-contracts': [py, 'scripts/check_port_contracts.py'],
            }
            rcs = {g: run(g, argv, tree, log) for g, argv in gates.items()}
        refused = sorted(g for g, rc in rcs.items() if rc)
        verdict = ('NOT-COMPILING' if build else 'CAUGHT' if refused else 'GAP')
        results.append({'probe': name, 'rule': rule, 'build_rc': build, 'gate_rc': rcs,
                         'refused_by': refused, 'result': verdict})
        print(f'{name} (rule {rule}): build rc {build}; refused by {refused or "none"} -> {verdict}', flush=True)
    (work / 'probes.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
