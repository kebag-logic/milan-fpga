#!/usr/bin/env python3
"""Compare two linked split images (base, head): section sizes, every symbol's address and size, and every
loaded byte outside the named functions. Also each image's stack-usage line for the named functions.

Usage: image_compare.py <nm-prefix> <base-image-dir> <head-image-dir> [function ...]
<nm-prefix> is the SDK's tool prefix, e.g. /path/bin/riscv32-linux- (nm, objcopy, readelf are taken from it).
"""
import subprocess
import sys
import tempfile
from pathlib import Path


def run(argv):
    return subprocess.run(argv, check=True, capture_output=True, text=True).stdout


def symbols(tool, elf):
    out = {}
    for line in run([tool + 'nm', '-S', '--defined-only', str(elf)]).splitlines():
        parts = line.split()
        if len(parts) == 4:
            addr, size, kind, name = parts
            out[(name, kind)] = (int(addr, 16), int(size, 16))
    return out


def sections(tool, elf):
    out = {}
    for line in run([tool + 'readelf', '-SW', str(elf)]).splitlines():
        line = line.replace('[ ', '[')
        parts = line.split()
        if len(parts) > 6 and parts[0].startswith('[') and parts[0] != '[Nr]':
            name, kind, addr, off, size = parts[1], parts[2], parts[3], parts[4], parts[5]
            out[name] = (kind, int(addr, 16), int(size, 16))
    return out


def loaded(tool, elf, tmp, tag):
    """Each allocated PROGBITS section's bytes, by name."""
    out = {}
    for name, (kind, addr, size) in sections(tool, elf).items():
        if kind == 'PROGBITS' and size and not name.startswith(('.comment', '.riscv', '.debug')):
            dst = Path(tmp) / f'{tag}{name.replace("/", "_")}.bin'
            subprocess.run([tool + 'objcopy', '-O', 'binary', '--only-section=' + name, str(elf), str(dst)],
                           check=True)
            out[name] = (addr, dst.read_bytes())
    return out


def main():
    tool, base_dir, head_dir, *funcs = sys.argv[1:]
    base_elf, head_elf = Path(base_dir) / 'ctrl_app.elf', Path(head_dir) / 'ctrl_app.elf'
    bs, hs = sections(tool, base_elf), sections(tool, head_elf)
    print('== sections (name kind addr size), base -> head')
    same_sections = True
    for name in sorted(set(bs) | set(hs)):
        b, h = bs.get(name), hs.get(name)
        flag = '' if b == h else '  DIFFERS'
        same_sections &= b == h
        print(f'{name:24} {b} -> {h}{flag}')
    bsym, hsym = symbols(tool, base_elf), symbols(tool, head_elf)
    moved = [(k, bsym.get(k), hsym.get(k)) for k in sorted(set(bsym) | set(hsym)) if bsym.get(k) != hsym.get(k)]
    print(f'== symbols differing in presence, address or size: {len(moved)}')
    for k, b, h in moved:
        print(f'  {k[0]} ({k[1]}): {b} -> {h}')
    for f in funcs:
        for k in ((f, 't'), (f, 'T')):
            if k in bsym or k in hsym:
                print(f'== {f}: base {bsym.get(k)} head {hsym.get(k)}')
    # loaded bytes outside the named functions
    skip = []
    for f in funcs:
        for k in ((f, 't'), (f, 'T')):
            if k in hsym and hsym.get(k) == bsym.get(k):
                skip.append(hsym[k])
    with tempfile.TemporaryDirectory() as tmp:
        bl, hl = loaded(tool, base_elf, tmp, 'b'), loaded(tool, head_elf, tmp, 'h')
        total_diff = 0
        outside = 0
        for name in sorted(set(bl) | set(hl)):
            if name not in bl or name not in hl or bl[name][0] != hl[name][0] or len(bl[name][1]) != len(hl[name][1]):
                print(f'== loaded section {name}: layout differs')
                outside += 1
                continue
            addr, b = bl[name]
            h = hl[name][1]
            diffs = [addr + i for i in range(len(b)) if b[i] != h[i]]
            total_diff += len(diffs)
            out = [a for a in diffs if not any(s <= a < s + n for s, n in skip)]
            outside += len(out)
            print(f'== loaded section {name}: {len(b)} B, {len(diffs)} bytes differ, {len(out)} outside '
                  f'{",".join(funcs) or "nothing"}' + (f' (first {hex(out[0])})' if out else ''))
        print(f'RESULT: {"IDENTICAL-OUTSIDE" if outside == 0 and same_sections and len(moved) == 0 else "DIFFERENT"}'
              f' (sections same: {same_sections}, symbols moved: {len(moved)}, bytes differing outside: {outside},'
              f' bytes differing in total: {total_diff})')


if __name__ == '__main__':
    main()
