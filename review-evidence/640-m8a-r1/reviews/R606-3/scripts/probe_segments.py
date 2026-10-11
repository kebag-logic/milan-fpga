#!/usr/bin/env python3
"""R606-3 probe: `load coverage` and `entry bytes` across PT_LOAD layouts.

usage: probe_segments.py <tree> <out>
Starts from test_ctrl_memory's GOOD ELF and rewrites only its program header
table (appended at the end of the file, e_phoff/e_phnum updated), so section
headers and file bytes are untouched. Prints ACCEPTED (with whether rom_words
equal the GOOD image's) or REFUSED <check> / <rule> per case, and the expected
outcome; exits 1 if any case differs from its expectation.
"""
import struct
import sys
from pathlib import Path

tree, out = map(Path, sys.argv[1:])
out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(tree / "sw/litex"))
import ctrl_memory as cm          # noqa: E402
import test_ctrl_memory as test   # noqa: E402

raw = test.elf(out, test.GOOD).read_bytes()
base = cm.read_elf(test.elf(out, test.GOOD))
base_words = cm.rom_words(base)
phoff, = struct.unpack_from("<I", raw, 28)
phentsize, phnum = struct.unpack_from("<HH", raw, 42)
table = [list(struct.unpack_from("<8I", raw, phoff + n * 32)) for n in range(phnum)]
print("GOOD program headers (type, offset, vaddr, paddr, filesz, memsz):", [p[:6] for p in table])
print("GOOD sections (name, vma, lma, size, loaded):",
      [(s.name, hex(s.vma), hex(s.lma), s.size, s.loaded) for s in base.sections])
reset = next(n for n, p in enumerate(table) if p[0] == 1 and p[3] == 0)


def write(name, headers):
    data = bytearray(raw)
    data += bytes(-len(data) % 4)
    struct.pack_into("<I", data, 28, len(data))
    struct.pack_into("<H", data, 44, len(headers))
    for p in headers:
        data += struct.pack("<8I", *p)
    path = out / f"{name}.elf"
    path.write_bytes(bytes(data))
    return path


def piece(p, start, length):
    q = p[:]
    q[1] += start; q[2] += start; q[3] += start; q[4] = length; q[5] = length
    return q


def split(k, gap=0, overlap=0):
    p = table[reset]
    return piece(p, 0, k + overlap), piece(p, k + gap, p[4] - k - gap)


cases = []
a, b = split(64)
cases.append(("control: table moved, unchanged", table, "ACCEPTED"))
cases.append(("reset segment split into two abutting pieces", [a, b] + table[reset + 1:], "ACCEPTED"))
cases.append(("abutting pieces listed in reverse order", [b, a] + table[reset + 1:], "ACCEPTED"))
a, b = split(64, gap=4)
cases.append(("4-byte hole between the pieces inside .text", [a, b] + table[reset + 1:], "load coverage"))
a, b = split(64, overlap=32)
cases.append(("pieces overlapping by 32 bytes", [a, b] + table[reset + 1:], "ACCEPTED"))
a, b = split(2)
cases.append(("first piece only 2 bytes, rest abutting", [a, b] + table[reset + 1:], "ACCEPTED"))
a, _ = split(2)
cases.append(("first piece only 2 bytes, nothing after it", [a] + table[reset + 1:], "entry bytes"))
shifted = table[reset][:]; shifted[3] += 4
cases.append(("reset segment's paddr moved up 4", [shifted] + table[reset + 1:], "entry bytes"))
short = [p[:] for p in table]
for p in short:
    if p[0] == 1 and p[4]:
        p[4] -= 1
cases.append(("every load segment one byte short", short, "load coverage"))
nodata = [p for p in table if not (p[0] == 1 and p[3] != 0 and p[4])]
cases.append(("only the reset segment kept (.data's segment dropped)", nodata, "load coverage"))

bad = 0
for name, headers, want in cases:
    path = write("".join(c if c.isalnum() else "-" for c in name), headers)
    try:
        img = cm.read_elf(path)
        cm.plan(img)
        same = cm.rom_words(img) == base_words
        got = "ACCEPTED"
        detail = f"rom_words equal GOOD: {same}"
        if want == "ACCEPTED" and not same:
            got = "ACCEPTED-BUT-WORDS-DIFFER"
    except cm.Refusal as exc:
        got, detail = exc.rule, f"REFUSED {exc.check} / {exc.rule}: {exc}"
    ok = got == want
    bad += not ok
    print(f"[{'ok' if ok else 'XX'}] {name}: expected {want}; {detail}")
print(f"probe_segments: {len(cases)} cases, {bad} unexpected")
sys.exit(1 if bad else 0)
