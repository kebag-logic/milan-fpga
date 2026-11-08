#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the exact-head W1 test alone against the head wire.h, the base wire.h and a set of
planted wire.h defects (pinned GoogleTest), and record whether W1 fails on each."""
import argparse, json, os, subprocess, shlex
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HEAD = 'c687810b74b53b69c1fbdff7bfd0ec9da94eaa78'
LOOP = '\tfor (unsigned i = bytes; i > 0u; --i) {\n'
MUTANTS = {
    'head': None,
    'base-wire': 'BASE',
    'plant-skips-odd-first-byte': (LOOP, '\tfor (unsigned i = bytes; i > (bytes & 1u); --i) {\n'),
    'plant-writes-past-odd': (LOOP, '\tfor (unsigned i = bytes + (bytes & 1u); i > 0u; --i) {\n'),
    'high-shift-16': ('(high << 24)', '(high << 16)'),
    'high-never-shifted': ('\t\thigh >>= 8;\n', ''),
    'no-crossing': ('(low >> 8) | (high << 24)', '(low >> 8)'),
    'top-byte-never-written': ('i > 0u', 'i > 1u'),
    'starts-one-short': ('unsigned i = bytes;', 'unsigned i = bytes - 1u;'),
    'off-by-one-store': ('p[i - 1u]', 'p[i]'),
    'high-from-bit-31': ('(value >> 32)', '(value >> 31)'),
    'low-takes-high': ('uint32_t low = (uint32_t)value;', 'uint32_t low = (uint32_t)(value >> 32);'),
    'width-capped-at-7': (LOOP, '\tfor (unsigned i = bytes > 7u ? 7u : bytes; i > 0u; --i) {\n'),
    'odd-width-rounded-down': (LOOP, '\tfor (unsigned i = bytes & ~1u; i > 0u; --i) {\n'),
    'byte-store-from-high': ('p[i - 1u] = (uint8_t)low;', 'p[i - 1u] = (uint8_t)(bytes > 4u ? high : low);'),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clone', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=6)
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    show = lambda rev, path: subprocess.run(['git', '-C', str(a.clone), 'show', rev + ':' + path],
                                            stdout=subprocess.PIPE, check=True).stdout.decode()
    tests = show(HEAD, 'tests/test_acmp.cpp')
    start = tests.index('// REQ: ACMP-02\nTEST(Wire, W1PutBeWritesTheLowBytesMostSignificantFirst)')
    w1 = tests[start:]
    harness = ('#include <array>\n#include <cstdint>\n#include <gtest/gtest.h>\nextern "C" {\n#include "wire.h"\n}\n'
               + w1)
    (a.work / 'w1.cpp').write_text(harness)
    head_wire = show(HEAD, 'include/wire.h'); base_wire = show('70936b77', 'include/wire.h')
    flags = shlex.split(subprocess.check_output(['pkg-config', '--cflags', '--libs', 'gtest_main'], text=True))
    def one(item):
        name, spec = item
        d = a.work / name; d.mkdir(exist_ok=True)
        text = head_wire if spec is None else base_wire if spec == 'BASE' else None
        if text is None:
            old, new = spec
            assert head_wire.count(old) == 1, name
            text = head_wire.replace(old, new)
        (d / 'wire.h').write_text(text)
        b = subprocess.run(['g++', '-std=c++20', '-O0', '-Wall', '-Wextra', '-I' + str(d), str(a.work / 'w1.cpp'),
                            *flags, '-o', str(d / 'w1')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if b.returncode:
            return {'mutant': name, 'build_rc': b.returncode, 'log': b.stdout[-400:]}
        r = subprocess.run([str(d / 'w1')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60)
        (d / 'run.log').write_text(r.stdout)
        return {'mutant': name, 'build_rc': 0, 'w1_rc': r.returncode,
                'w1_failed': '[  FAILED  ] Wire.W1PutBeWritesTheLowBytesMostSignificantFirst' in r.stdout,
                'needle_seen': 'W1 wire_put_be writes the low bytes most significant first' in r.stdout}
    with ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(one, MUTANTS.items()))
    print(json.dumps(results, indent=1))

if __name__ == '__main__':
    main()
