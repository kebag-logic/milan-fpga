#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Compile short probe lines and ask the tree's comment gate whether it sees their text.

Usage: hidden_text_probe.py TREE WORK
Environment: TSN_CLANG (Clang 18), RV32_CC (default riscv64-unknown-elf-gcc or riscv64-elf-gcc).
A row is GAP when every listed compiler accepts the probe, the compiler's own lexer
or assembler treats PROBE_TEXT as comment text, and the gate reports no error.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(TREE / 'scripts'))
from check_comments import check  # noqa: E402

RV32 = os.environ.get('RV32_CC') or shutil.which('riscv64-unknown-elf-gcc') or shutil.which('riscv64-elf-gcc')
CLANG = os.environ['TSN_CLANG']
TEXT = 'hidden probe words'
FLAGS = ['-Wall', '-Wextra', '-Werror']

PROBES = [
    # name, suffix, source, compilers, gate path
    ('asm-formfeed-before-hash', '.S', 'nop \f#define ' + TEXT + '\n', ['rv32'], 'examples/rv32/probe.S'),
    ('asm-define-body-formfeed', '.S', '#define V 4 \f#define ' + TEXT + '\n.word V\n', ['rv32'], 'examples/rv32/probe.S'),
    ('asm-verticaltab-before-hash', '.S', 'nop \v#include ' + TEXT + '\n', ['rv32'], 'examples/rv32/probe.S'),
    ('header-cxx-digit-separator', '.h',
     '#define PROBE_IGNORE(a) 0\nenum { probe_value = PROBE_IGNORE(1\'2 // ' + TEXT + " '\n) };\n",
     ['gcc-c', 'clang-c', 'g++', 'clang++'], 'include/probe.h'),
    # Controls: the gate must refuse the same text in plain comment positions.
    ('control-asm-hash', '.S', 'nop # ' + TEXT + '\n', ['rv32'], 'examples/rv32/probe.S'),
    ('control-c-line-comment', '.h', 'int probe_value; // ' + TEXT + '\n', ['gcc-c', 'g++'], 'include/probe.h'),
]


def compile_with(kind, path, out):
    if kind == 'rv32':
        cmd = [RV32, '-march=rv32i', '-mabi=ilp32', '-x', 'assembler-with-cpp']
    elif kind == 'gcc-c':
        cmd = ['gcc', '-x', 'c', '-std=c11']
    elif kind == 'clang-c':
        cmd = ['clang', '-x', 'c', '-std=c11']
    elif kind == 'g++':
        cmd = ['g++', '-x', 'c++', '-std=c++20']
    else:
        cmd = ['clang++', '-x', 'c++', '-std=c++20']
    r = subprocess.run([*cmd, *FLAGS, '-c', str(path), '-o', str(out)], capture_output=True, text=True)
    return r.returncode, r.stderr.strip()


def compiler_sees_comment(kind, source):
    if kind == 'rv32':
        pre = subprocess.run([RV32, '-E', '-P', '-x', 'assembler-with-cpp', '-'], input=source,
                             capture_output=True, text=True).stdout
        # The RV32 assembler treats text after # as a comment; the object holds no symbol of it.
        return any('#' in line and TEXT in line.split('#', 1)[1] for line in pre.splitlines())
    language = 'c++' if kind in ('g++', 'clang++') else 'c'
    std = 'c++20' if language == 'c++' else 'c11'
    dump = subprocess.run([CLANG, '-cc1', '-x', language, '-std=' + std, '-dump-raw-tokens', '-'],
                          input=source, capture_output=True, text=True).stderr
    return any(line.startswith('comment ') and TEXT in line for line in dump.splitlines())


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, suffix, source, compilers, gate_path in PROBES:
        path = WORK / (name + suffix)
        path.write_bytes(source.encode())
        builds = {}
        for kind in compilers:
            rc, err = compile_with(kind, path, WORK / (name + '.' + kind + '.o'))
            builds[kind] = {'rc': rc, 'stderr': err[-400:]}
        seen = {kind: compiler_sees_comment(kind, source) for kind in compilers}
        errors = check(source, suffix == '.S', 'c++' if suffix in ('.cpp', '.hpp') else 'c', gate_path)
        compiled = all(b['rc'] == 0 for b in builds.values())
        hidden = any(seen.values())
        verdict = ('GAP' if compiled and hidden and not errors else
                   'REFUSED' if errors else 'NOT-APPLICABLE')
        rows.append({'probe': name, 'compiled': builds, 'compiler_comment': seen,
                     'gate_errors': errors, 'verdict': verdict})
        print(f'{name}: {verdict} compiled={compiled} compiler_comment={seen} gate_errors={errors}')
    (WORK / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    gaps = sum(r['verdict'] == 'GAP' for r in rows if not r['probe'].startswith('control-'))
    controls = all(r['verdict'] == 'REFUSED' for r in rows if r['probe'].startswith('control-'))
    print(f'gaps: {gaps}; controls refused: {controls}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
