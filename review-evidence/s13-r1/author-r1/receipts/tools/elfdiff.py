#!/usr/bin/env python3
"""elfdiff.py A.elf B.elf: compare two ELF32 little-endian images' LOADED sections (SHF_ALLOC with file contents,
the bytes a ROM or RAM image holds), byte by byte.

Prints, per section: name, address, size on each side, and whether the contents are equal. For every differing byte
run: its address, the bytes on each side, and the symbol (from .symtab, the nearest STT_FUNC/STT_OBJECT at or below
the address, within its size) it lies in. Exit 0 when every loaded section is equal, 1 when any differs, 2 when the
section tables differ in name, address or size (the layout moved)."""
import struct
import sys
from pathlib import Path


def sections(path):
    b = Path(path).read_bytes()
    assert b[:4] == b"\x7fELF" and b[4] == 1 and b[5] == 1, f"{path}: not ELF32 LE"
    shoff, = struct.unpack_from("<I", b, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", b, 0x2E)
    rows = [struct.unpack_from("<IIIIIIIIII", b, shoff + i * shentsize) for i in range(shnum)]
    strtab = rows[shstrndx]
    name = lambda off: b[strtab[4] + off:b.index(b"\x00", strtab[4] + off)].decode()
    out = []
    for r in rows:
        nm, typ, flags, addr, off, size = name(r[0]), r[1], r[2], r[3], r[4], r[5]
        out.append(dict(name=nm, type=typ, flags=flags, addr=addr, off=off, size=size, link=r[6], entsize=r[9],
                        data=b[off:off + size] if typ != 8 else b""))
    return b, out


def symbols(b, secs):
    st = [s for s in secs if s["type"] == 2]
    if not st:
        return []
    st = st[0]
    strs = secs[st["link"]]
    syms = []
    for i in range(st["size"] // 16):
        nm, val, size, info, _other, shndx = struct.unpack_from("<IIIBBH", b, st["off"] + 16 * i)
        if info & 0xF in (1, 2) and size:
            s = b[strs["off"] + nm:b.index(b"\x00", strs["off"] + nm)].decode()
            syms.append((val, size, s))
    return sorted(syms)


def where(syms, addr):
    best = None
    for val, size, s in syms:
        if val <= addr < val + size:
            best = f"{s}+0x{addr - val:x}"
    return best or "(no sized symbol)"


def main():
    ba, a = sections(sys.argv[1])
    bb, b = sections(sys.argv[2])
    la = [s for s in a if s["flags"] & 2 and s["type"] != 8 and s["size"]]
    lb = [s for s in b if s["flags"] & 2 and s["type"] != 8 and s["size"]]
    ka = [(s["name"], s["addr"], s["size"]) for s in la]
    kb = [(s["name"], s["addr"], s["size"]) for s in lb]
    if ka != kb:
        print("LAYOUT DIFFERS")
        for x, y in zip(ka, kb):
            print(f"  A {x[0]} 0x{x[1]:08x} {x[2]}   B {y[0]} 0x{y[1]:08x} {y[2]}")
        return 2
    syms = symbols(bb, b)
    total = 0
    for sa, sb in zip(la, lb):
        diff = [i for i in range(sa["size"]) if sa["data"][i] != sb["data"][i]]
        total += len(diff)
        print(f"{sa['name']:<12} 0x{sa['addr']:08x} {sa['size']:>7} B  {'EQUAL' if not diff else f'{len(diff)} byte(s) differ'}")
        runs, start = [], None
        for i in diff:
            if start is None or i != prev + 1:
                if start is not None:
                    runs.append((start, prev))
                start = i
            prev = i
        if start is not None:
            runs.append((start, prev))
        for s0, s1 in runs:
            addr = sa["addr"] + s0
            print(f"    0x{addr:08x}..0x{sa['addr'] + s1:08x}  A {sa['data'][s0:s1 + 1].hex()}  "
                  f"B {sb['data'][s0:s1 + 1].hex()}  in {where(syms, addr)}")
    print(f"loaded bytes differing: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
