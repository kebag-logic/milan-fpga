#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe: round-8 comment-gate refusals (.S includes/end, .ld escapes/hash/VERSION,
C/C++ source includes) with compiling or linking controls.

usage: probe_comment_gate.py HEAD_TREE OLD_TREE WORK
Every probe is first compiled, assembled or linked with the RV32 cross compiler or the host
compiler; the source gate verdict is then taken from check() of both exported trees.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

head, old, work = (Path(a).resolve() for a in sys.argv[1:4])
work.mkdir(parents=True, exist_ok=True)
cross = shutil.which('riscv64-unknown-elf-gcc') or shutil.which('riscv64-elf-gcc')
cxx = os.environ.get('CXX', 'g++')
cc = os.environ.get('CC', 'gcc')


def gate(tree, source, path, assembly=False, language='c'):
    code = ('import sys, json; sys.path.insert(0, sys.argv[1] + "/scripts");'
            'from check_comments import check;'
            'a = json.loads(sys.argv[2]);'
            'print(json.dumps(check(sys.stdin.read(), a["assembly"], a["language"], a["path"])))')
    args = json.dumps({'assembly': assembly, 'language': language, 'path': path})
    out = subprocess.run([sys.executable, '-c', code, str(tree), args], input=source, text=True,
                         capture_output=True, cwd=str(work))
    if out.returncode:
        return 'GATE-ERROR: ' + (out.stderr.strip().splitlines() or ['?'])[-1]
    return json.loads(out.stdout)


(work / 'included.h').write_text('nop # prose in included assembly\n')
(work / 'data.bin').write_bytes(b'\x13\x00\x00\x00')
(work / 'inc.c').write_text("#define IGNORE(a) 0\nenum { value_c = IGNORE(1'2 // prose '\n) };\n")
(work / 'inc.cpp').write_text("#define IGNORE2(a) 0\nenum { value_cpp = IGNORE2(1'2 // prose '\n) };\n")
(work / 'sub').mkdir(exist_ok=True)
(work / 'sub/inc.c').write_text('enum { value_sub = 0 };\n')
(work / 'other.ld').write_text('/* prose in an included script */\n')
(work / 'start.o').unlink(missing_ok=True)
subprocess.run([cross, '-march=rv32i', '-mabi=ilp32', '-c', '-x', 'assembler', '-', '-o', str(work / 'start.o')],
               input='.global _start\n_start:\nnop\n', text=True, check=True)

START = '.global _start\n_start:\nnop\n'
ASM = [
    ('asm-include', START + '.include "included.h"\n', 'refuse'),
    ('asm-include-upper', START + '.INCLUDE "included.h"\n', 'refuse'),
    ('asm-include-after-label', '.global _start\n_start: .include "included.h"\n', 'refuse'),
    ('asm-include-after-separator', START + 'nop; .include "included.h"\n', 'refuse'),
    ('asm-incbin', START + '.incbin "data.bin"\n', 'refuse'),
    ('asm-incbin-range', START + '.incbin "data.bin", 0, 4\n', 'refuse'),
    ('asm-end', START + '.end\nprose after end\n', 'refuse'),
    ('asm-end-separator', START + 'nop; .end\nprose after end\n', 'refuse'),
    ('asm-tracing', START + 'nop # REQ: PORT-01\n', 'accept'),
    ('asm-endfunc-control', START + '.func probe\n.endfunc\n', 'accept'),
]
LD = [
    ('ld-backslash', 'SECTIONS { .probe : { *("x\\" /* prose */ "y") } }\n', 'refuse'),
    ('ld-hash-version', 'VERSION { PROBE { local: *; # prose\n}; }\n', 'refuse'),
    ('ld-version', 'VERSION { PROBE { local: *; }; }\n', 'refuse'),
    ('ld-quote', "PROVIDE(probe' = 1);\n", 'refuse'),
    ('ld-version-in-comment', '/* VERSION */\n', 'refuse-or-accept'),
    ('ld-include-other', 'INCLUDE other.ld\n', 'out-of-listed-rules'),
    ('ld-tracing', '/* REQ: PORT-01 */\n', 'accept'),
]
INC = [
    ('cpp-include-quoted-c', '#include "inc.c"\n', 'tests/unit.cpp', 'c++', 'refuse'),
    ('cpp-include-angled-cpp', '#include <inc.cpp>\n', 'tests/unit.cpp', 'c++', 'refuse'),
    ('cpp-include-spaced', '#  include   "inc.c"\n', 'tests/unit.cpp', 'c++', 'refuse'),
    ('cpp-include-subdir', '#include "sub/inc.c" // REQ: PORT-01\n', 'tests/unit.cpp', 'c++', 'refuse'),
    ('cpp-include-comment-in-directive', '# /* REQ: PORT-01 */ include "inc.c"\n', 'tests/unit.cpp', 'c++', 'refuse'),
    ('cpp-include-spliced', '#inc\\\nlude "inc.c"\n', 'tests/unit.cpp', 'c++', 'refuse'),
    ('c-include-quoted-c', '#include "inc.c"\n', 'examples/unit.c', 'c', 'refuse'),
    ('h-include-quoted-c', '#include "sub/inc.c"\n', 'include/unit.h', 'c', 'refuse'),
    ('cpp-include-next', '#include_next "inc.c"\n', 'tests/unit.cpp', 'c++', 'suggestion'),
    ('cpp-include-header-control', '#include "included.h"\n', 'tests/unit.cpp', 'c++', 'accept'),
]

rows = []


def record(label, built, verdict_head, verdict_old, expected):
    status = 'refuse' if verdict_head and not isinstance(verdict_head, str) else (
        'accept' if verdict_head == [] else 'error')
    rows.append({'probe': label, 'built': built, 'head_gate': verdict_head, 'previous_round_gate': verdict_old,
                 'head_status': status, 'expected': expected})
    print(f'{label}: built={built} head={status} {verdict_head} previous={verdict_old} expected={expected}')


for label, source, expected in ASM:
    path = work / (label + '.S')
    path.write_text(source)
    built = subprocess.run([cross, '-march=rv32i', '-mabi=ilp32', '-nostdlib', '-I' + str(work),
                            '-Wl,--fatal-warnings', str(path), '-o', str(work / (label + '.elf'))],
                           capture_output=True, text=True).returncode == 0
    record(label, built, gate(head, source, 'examples/rv32/probe.S', True),
           gate(old, source, 'examples/rv32/probe.S', True), expected)

for label, source, expected in LD:
    script = work / (label + '.ld')
    text = source + 'SECTIONS { . = 0x80000000; .text : { *(.text) } }\n'
    script.write_text(text)
    command = [cross, '-march=rv32i', '-mabi=ilp32', '-nostdlib', '-L' + str(work), '-T' + str(script),
               str(work / 'start.o'), '-o', str(work / (label + '.elf'))]
    plain = subprocess.run(command, capture_output=True, text=True, cwd=str(work)).returncode == 0
    fatal = subprocess.run([*command, '-Wl,--fatal-warnings'], capture_output=True, text=True,
                           cwd=str(work)).returncode == 0
    record(label + f' (link={plain}, fatal-link={fatal})', plain,
           gate(head, text, 'examples/rv32/link.ld'), gate(old, text, 'examples/rv32/link.ld'), expected)

for label, source, path, language, expected in INC:
    unit = work / (label + ('.cpp' if language == 'c++' else '.c'))
    unit.write_text(source)
    compiler = cxx if language == 'c++' else cc
    std = '-std=c++20' if language == 'c++' else '-std=c11'
    built = subprocess.run([compiler, std, '-Wall', '-Wextra', '-Werror', '-I' + str(work), '-c', str(unit),
                            '-o', str(work / (label + '.o'))], capture_output=True, text=True).returncode == 0
    record(label, built, gate(head, source, path, False, language), gate(old, source, path, False, language),
           expected)

(work / 'probe_comment_gate.json').write_text(json.dumps(rows, indent=1) + '\n')
