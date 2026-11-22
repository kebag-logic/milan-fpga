#!/usr/bin/env python3
"""Reviewer-owned planted defects for r879_identity.py, and the author's replay run over each plant as published.

    python3 -I r879_plants.py <identity-packet-dir> <work-dir> <r879_identity.py>

For each plant: a hard-linked copy of the packet, the one planted file written anew, the copy's MANIFEST.sha256
resealed (so only the claim under test can catch it), then the reviewer's diff over the copy. A plant is caught
when the diff exits 1 with a FAIL line. The unplanted control must exit 0 or 3 (3: listed operands absent)."""
import gzip
import hashlib
import lzma
import os
import shutil
import struct
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PACKET, WORK, DIFF = (Path(a).resolve() for a in sys.argv[1:4])


def flip(data, off, bit=0):
    return data[:off] + bytes([data[off] ^ (1 << bit)]) + data[off + 1:]


def fdri_start(bit):
    sync = bit.index(b"\xaa\x99\x55\x66")
    i = sync + 4
    while True:
        w = struct.unpack(">I", bit[i:i + 4])[0]
        if w == 0x30004000:
            return i + 8  # the type-2 header that follows carries the frame data
        i += 4


def section_off(elf, want):
    shoff, = struct.unpack_from("<I", elf, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", elf, 0x2E)
    rows = [struct.unpack_from("<IIIIIIIIII", elf, shoff + k * shentsize) for k in range(shnum)]
    names = rows[shstrndx][4]
    for r in rows:
        if elf[names + r[0]:elf.index(b"\0", names + r[0])].decode() == want:
            return r[4]
    raise SystemExit(want)


def line_edit(pick, change):
    def edit(data):
        lines = data.split(b"\n")
        k = next(i for i, ln in enumerate(lines) if pick(ln))
        lines[k] = change(lines[k])
        return b"\n".join(lines)
    return edit


def codec(path, edit):
    raw = path.read_bytes()
    if path.suffix == ".xz":
        return lzma.compress(edit(lzma.decompress(raw)), preset=1)
    if path.suffix == ".gz":
        return gzip.compress(edit(gzip.decompress(raw)), mtime=0)
    return edit(raw)


PLANTS = [
    ("control: nothing planted", None, None),
    ("a configuration bit outside the ROM frames (frame 100)", "shipping/1x1/flip/alinx_ax7101.bit",
     lambda p: codec(p, lambda d: flip(d, fdri_start(d) + 4 * (101 * 100 + 5)))),
    ("the part name in the .bit header", "shipping/1x1/flip/alinx_ax7101.bit",
     lambda p: codec(p, lambda d: flip(d, d.index(b"7a100t") + 2))),
    ("one more instruction byte in the platform image", "shipping/8x8/flip/ctrl_app.elf",
     lambda p: codec(p, lambda d: flip(d, section_off(d, ".text") + 0x100))),
    ("one ROM word the image does not hold", "shipping/1x1/flip/gateware/alinx_ax7101_rom_bank0.init",
     lambda p: codec(p, line_edit(lambda ln: ln.strip() != b"", lambda ln: b"%08x" % (int(ln, 16) ^ 1)))),
    ("a cell placed elsewhere (8x8; 1x1 cells not published)", "shipping/8x8/dump/flip.cells.xz",
     lambda p: codec(p, line_edit(lambda ln: b" RAMB36E1 RAMB36_X" in ln,
                                  lambda ln: ln.replace(b"RAMB36_X", b"RAMB36_Z", 1)))),
    ("a route changed", "shipping/1x1/dump/flip.nets.xz",
     lambda p: codec(p, line_edit(lambda ln: b"{" in ln, lambda ln: ln.replace(b"{", b"{ PLANTED", 1)))),
    ("a block RAM INIT bit outside the ROMs", "shipping/8x8/dump/flip.bram.xz",
     lambda p: codec(p, line_edit(lambda ln: b"INIT_00=256'h" in ln and b"rom_bank" not in ln and b"/csr/" not in ln,
                                  lambda ln: ln.replace(b"INIT_00=256'h0", b"INIT_00=256'h1", 1)))),
    ("a measured harness image swapped for the head's", "harness/1x1/none/measured.elf",
     lambda p: (p.parent / "head.elf").read_bytes()),
    ("one more data byte in a harness image", "harness/8x8-1if/answering-ports/head.elf",
     lambda p: codec(p, lambda d: flip(d, section_off(d, ".rodata")))),
    ("a group's CPU cycles changed", "groups/1x1/none/control.head.json",
     lambda p: codec(p, lambda d: d.replace(b'"cpu_cycles": ', b'"cpu_cycles": 1', 1))),
    ("a raw log digit changed other than the version's", "groups/1x1/none/aecp-held.head.log.gz",
     lambda p: codec(p, line_edit(lambda ln: ln.startswith(b"PASS ") and b"5" in ln,
                                  lambda ln: ln.replace(b"5", b"6", 1)))),
    ("PROBE (rule strength): a 2->3 digit planted in an unrelated log line", "groups/1x1/none/control.head.log.gz",
     lambda p: codec(p, line_edit(lambda ln: b"2" in ln and b"firmware" not in ln,
                                  lambda ln: ln.replace(b"2", b"3", 1)))),
]


def one(k, label, rel, plant):
    root = WORK / f"p{k:02d}"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(PACKET, root, copy_function=os.link)
    if rel:
        target = root / rel
        data = plant(target)
        target.unlink()
        target.write_bytes(data)
        rows = []
        for line in (root / "MANIFEST.sha256").read_text().splitlines():
            digest, name = line.split(None, 1)
            if name == rel:
                digest = hashlib.sha256(data).hexdigest()
            rows.append(f"{digest}  {name}")
        (root / "MANIFEST.sha256").unlink()
        (root / "MANIFEST.sha256").write_text("\n".join(rows) + "\n")
    run = subprocess.run([sys.executable, "-I", str(DIFF), str(root)], capture_output=True, text=True)
    fails = [ln.strip() for ln in run.stdout.splitlines() if ln.startswith("  FAIL")]
    shutil.rmtree(root)
    if rel is None:
        ok = run.returncode in (0, 3) and not fails
        return f"== {label}\n   diff exit {run.returncode}: {'CLEAN' if ok else 'CONTROL FAILED'}", ok
    ok = run.returncode == 1 and bool(fails)
    return (f"== {label} ({rel})\n   diff exit {run.returncode}: {'CAUGHT' if ok else 'MISSED'}\n" +
            "\n".join(f"   {f[:240]}" for f in fails[:2])), ok


WORK.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(max_workers=13) as pool:
    results = list(pool.map(lambda a: one(*a), [(k, *p) for k, p in enumerate(PLANTS)]))
for text, _ in results:
    print(text)
print(f"control clean: {results[0][1]}; plants caught: {sum(ok for _, ok in results[1:])} of {len(results) - 1}")
sys.exit(0 if all(ok for _, ok in results) else 1)
