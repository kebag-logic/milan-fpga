#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Plant compiling comment forms into a disposable tree copy and grade the comment gate.

argv[1] = pristine tree (exported exact head), argv[2] = empty work directory.
Each probe: the planted file must compile under the project flags, the planted prose must
not reach the preprocessor output (it is a comment or a disabled region), the core object
bytes must be unchanged, and the repository gate scripts/check_comments.py is run on the copy.
A probe the gate passes is a GAP.
"""
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

TREE, WORK = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
WORD = 'narrativeprobewords'
C = ['-std=c11', '-O2', '-g0', '-Wall', '-Wextra', '-Werror', '-DNDEBUG', '-DCTRL_REENTRY_ASSERT']
CXX = ['-std=c++20', '-O0', '-g0', '-Wall', '-Wextra', '-Werror']
RV = ['-march=rv32i', '-mabi=ilp32', '-Wall', '-Wextra', '-Werror']
PROBES = {
    # name: (file, appended text, scope)
    'identifier digit before character literal (C core)':
        ('src/adp.c', "#define TSN_PROBE_A x1'a' /* " + WORD + " */ 'b'\n", 'F1 literal recognition'),
    'identifier digit before character literal (C++ test)':
        ('tests/test_port.cpp', "#define TSN_PROBE_A x1'a' /* " + WORD + " */ 'b'\n", 'F1 literal recognition'),
    'identifier ending in R before string (C core)':
        ('src/maap.c', '#define TSN_PROBE_R\n#define TSN_PROBE_S TSN_PROBE_R"(" /* ' + WORD + ' */ ")"\n',
         'F1 literal recognition'),
    'identifier ending in R before string (C++ test)':
        ('tests/test_port.cpp', '#define TSN_PROBE_R\nstatic const char *tsn_probe_s = TSN_PROBE_R"(" /* ' + WORD + ' */ ")";\n'
         '[[maybe_unused]] static const char *tsn_probe_t = tsn_probe_s;\n', 'F1 literal recognition'),
    'character zero constant in #if (C core)':
        ('src/acmp.c', "#if '\\0'\n" + WORD + "\n#endif\n", 'F1 zero constant'),
    'wide character zero constant in #elif (C++ test)':
        ('tests/test_port.cpp', "#if 0x1\n#elif L'\\0'\n" + WORD + "\n#endif\n", 'F1 zero constant'),
    'bit-precise zero constant in #if (C core)':
        ('src/adp.c', '#if 0wb\n' + WORD + '\n#endif\n', 'F1 zero constant'),
    'pragma prose in assembly':
        ('examples/rv32/start.S', '#pragma ' + WORD + ' explains startup\n', 'outside enumerated forms'),
    'assembler disabled region':
        ('examples/rv32/start.S', '.if 0\n' + WORD + ' explains startup\n.endif\n', 'outside enumerated forms'),
    'undefined macro disabled region (C core)':
        ('src/maap.c', '#ifdef TSN_PROBE_NEVER\n' + WORD + '\n#endif\n', 'outside enumerated forms'),
    'negated constant disabled region (C core)':
        ('src/maap.c', '#if !1\n' + WORD + '\n#endif\n', 'outside enumerated forms'),
}


def run(argv, cwd=None):
    return subprocess.run(argv, cwd=cwd, text=True, capture_output=True)


def objects(root, rel, out):
    path = root / rel
    if path.suffix == '.c':
        cmds = {c: [c, *C, '-ffile-prefix-map=' + str(root) + '=.', '-I', str(root / 'include'), '-c', str(path), '-o', str(out) + '.' + c + '.o']
                for c in ('gcc', 'clang')}
    elif path.suffix == '.cpp':
        cmds = {c: [c, *CXX, '-ffile-prefix-map=' + str(root) + '=.', '-I', str(root / 'include'), '-I', str(root / 'examples'), '-c', str(path),
                    '-o', str(out) + '.' + c + '.o'] for c in ('g++', 'clang++')}
    else:
        cmds = {'rv32': ['riscv64-elf-gcc', *RV, '-c', str(path), '-o', str(out) + '.rv32.o']}
    result = {}
    for name, argv in cmds.items():
        r = run(argv)
        pre = run(argv[:argv.index('-c')] + ['-E', str(path)])  # prose must not survive preprocessing
        digest = hashlib.sha256(Path(argv[-1]).read_bytes()).hexdigest() if r.returncode == 0 else None
        if digest and path.suffix == '.S':
            digest = hashlib.sha256(run(['riscv64-elf-objdump', '-d', argv[-1]]).stdout.split('\n', 3)[3].encode()).hexdigest()
        result[name] = {'rc': r.returncode, 'stderr': r.stderr[-300:], 'sha256': digest,
                        'word_after_preprocessing': WORD in pre.stdout}
    return result


def main():
    WORK.mkdir(parents=True, exist_ok=False)
    base = WORK / 'base-objects'
    base.mkdir()
    baseline = {}
    rows = []
    gaps = 0
    for name, (rel, text, scope) in PROBES.items():
        if rel not in baseline:
            baseline[rel] = objects(TREE, rel, base / rel.replace('/', '_'))
        copy = WORK / ('tree-' + str(len(rows)))
        shutil.copytree(TREE, copy)
        target = copy / rel
        target.write_text(target.read_text() + text)
        planted = objects(copy, rel, WORK / (copy.name + '_' + rel.replace('/', '_')))
        gate = run([sys.executable, '-I', '-B', str(copy / 'scripts/check_comments.py')])
        compiles = all(v['rc'] == 0 for v in planted.values())
        hidden = not any(v['word_after_preprocessing'] for v in planted.values() if v['rc'] == 0)
        same = all(planted[k]['sha256'] == baseline[rel][k]['sha256'] for k in planted)
        gap = compiles and hidden and gate.returncode == 0
        gaps += gap
        rows.append((name, scope, rel, compiles, hidden, same, gate.returncode, gap))
        print(f"{'GAP' if gap else 'ok '} | {name} | {scope} | {rel} | compiles {compiles} | "
              f"prose hidden from compiler {hidden} | objects identical {same} | gate rc {gate.returncode} | "
              f"{gate.stdout.strip().splitlines()[-1] if gate.stdout.strip() else ''}")
        for k, v in planted.items():
            if v['rc']:
                print('   ', k, 'stderr:', v['stderr'].replace('\n', ' ')[:200])
        shutil.rmtree(copy)
    print('gaps:', gaps, 'of', len(PROBES))


if __name__ == '__main__':
    main()
