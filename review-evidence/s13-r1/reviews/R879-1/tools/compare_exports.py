#!/usr/bin/env python3
"""compare_exports.py A B ELF_A ELF_B NM: every file of two milan_soc.py exports (A the bench head's, B the PR
head's), and the two platform images' loaded bytes, each difference printed.

  - the ELFs: every PT_LOAD segment's file bytes, each differing byte run with its address and the symbol holding it
    (NM is the RV32 SDK's nm);
  - gateware/*_rom_bank*.init and *_mem.init: word by word;
  - gateware/*.v: line by line outside `//` comments;
  - aem_desc.bin: byte by byte, each run's offset;
  - every other file: line by line (csr.csv without its banner line).
Exit 0 always; the report is the verdict's evidence."""
import bisect
import re
import difflib
import struct
import subprocess
import sys
from pathlib import Path


def segments(path):
    data = Path(path).read_bytes()
    assert data[:4] == b"\x7fELF" and data[4] == 1, "ELF32 expected"
    phoff, = struct.unpack_from("<I", data, 28)
    phentsize, phnum = struct.unpack_from("<HH", data, 42)
    out = []
    for i in range(phnum):
        p_type, p_off, p_vaddr, p_paddr, p_filesz, p_memsz, _f, _a = struct.unpack_from("<8I", data, phoff + i * phentsize)
        if p_type == 1 and p_filesz:
            out.append((p_paddr, p_vaddr, data[p_off:p_off + p_filesz]))
    return out


def symbols(nm, elf):
    rows = []
    for ln in subprocess.run([nm, "-n", "-S", elf], capture_output=True, text=True, check=True).stdout.splitlines():
        f = ln.split()
        if len(f) >= 3:
            try:
                rows.append((int(f[0], 16), f[-1]))
            except ValueError:
                pass
    rows.sort()
    return rows


def where(rows, addr):
    i = bisect.bisect_right([r[0] for r in rows], addr) - 1
    return f"{rows[i][1]}+0x{addr - rows[i][0]:x}" if i >= 0 else "?"


def runs(a, b, base=0):
    out, i = [], 0
    n = min(len(a), len(b))
    while i < n:
        if a[i] != b[i]:
            j = i
            while j < n and a[j] != b[j]:
                j += 1
            out.append((base + i, a[i:j], b[i:j]))
            i = j
        else:
            i += 1
    return out


def cmp_elf(ea, eb, nm):
    sa, sb = segments(ea), segments(eb)
    print(f"== ELF loaded segments: A {len(sa)}, B {len(sb)}")
    if [(p, v, len(d)) for p, v, d in sa] != [(p, v, len(d)) for p, v, d in sb]:
        print("  LAYOUT DIFFERS:", [(hex(p), hex(v), len(d)) for p, v, d in sa], [(hex(p), hex(v), len(d)) for p, v, d in sb])
    rows = symbols(nm, eb)
    total = 0
    for (pa, va, da), (_pb, _vb, db) in zip(sa, sb):
        for off, x, y in runs(da, db):
            total += len(x)
            print(f"  vaddr 0x{va + off - 0:08x} (paddr 0x{pa + off:08x}) A {x.hex()} B {y.hex()}  in {where(rows, va + off)}")
    print(f"  loaded bytes differing: {total}")


def cmp_words(name, a, b):
    wa, wb = a.read_text().split(), b.read_text().split()
    d = [(i, x, y) for i, (x, y) in enumerate(zip(wa, wb)) if x != y]
    print(f"== {name}: {len(wa)} vs {len(wb)} words, {len(d)} differ" + "".join(f"\n  word {i}: {x} -> {y}" for i, x, y in d))


CLONE = re.compile(r"$REVIEWS/s13-r879-1-packet/scratch/(c-[a-z0-9]+|work/[A-Za-z0-9_.-]+)")


def norm(text):
    """The clone's and work directory's absolute paths replaced by one token: the two heads build in two clones."""
    return CLONE.sub("<clone>", text)


def strip_comments(text):
    text = re.sub(r"/\*.*?\*/", "", norm(text), flags=re.S)
    return [ln.split("//", 1)[0].rstrip() for ln in text.splitlines()]


def cmp_lines(name, la, lb):
    diff = [ln for ln in difflib.unified_diff(la, lb, lineterm="", n=0) if not ln.startswith(("---", "+++"))]
    print(f"== {name}: {'EQUAL' if not diff else f'{sum(1 for l in diff if l[:1] in "+-")} changed lines'}")
    for ln in diff[:60]:
        print("  " + ln[:300])


def main():
    A, B, ea, eb, nm = map(Path, sys.argv[1:6])
    cmp_elf(ea, eb, str(nm))
    files = sorted({p.relative_to(A) for p in A.rglob("*") if p.is_file()} | {p.relative_to(B) for p in B.rglob("*") if p.is_file()})
    for rel in files:
        if rel.parts[0] == "software" or rel.name == "litex.log":
            continue
        a, b = A / rel, B / rel
        if not a.exists() or not b.exists():
            print(f"== {rel}: only in {'B' if not a.exists() else 'A'}")
            continue
        if a.read_bytes() == b.read_bytes():
            print(f"== {rel}: byte-identical")
            continue
        if rel.suffix not in (".bin", ".init") and norm(a.read_text()) == norm(b.read_text()):
            print(f"== {rel}: identical but for the clone path")
            continue
        if rel.suffix == ".init":
            cmp_words(str(rel), a, b)
        elif rel.suffix == ".v":
            cmp_lines(f"{rel} (outside // comments)", strip_comments(a.read_text()), strip_comments(b.read_text()))
        elif rel.suffix == ".bin":
            r = runs(a.read_bytes(), b.read_bytes())
            print(f"== {rel}: {len(a.read_bytes())} vs {len(b.read_bytes())} B, runs {[(hex(o), x, y) for o, x, y in r]}")
        else:
            la, lb = norm(a.read_text()).splitlines(), norm(b.read_text()).splitlines()
            if rel.name == "csr.csv":
                la, lb = [l for l in la if not l.startswith("#")], [l for l in lb if not l.startswith("#")]
            cmp_lines(str(rel), la, lb)


main()
