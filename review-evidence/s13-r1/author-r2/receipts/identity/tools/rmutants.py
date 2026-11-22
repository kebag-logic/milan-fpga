#!/usr/bin/env python3
"""rmutants.py PACKET WORK: the replay's planted defects. For each plant: a copy of PACKET (the planted file
written anew), one operand changed as named, MANIFEST.sha256 rewritten so only the claim under test can catch
it, then tools/replay.py over the copy; the plant is caught when replay exits non-zero with the named FAIL words."""
import gzip
import hashlib
import lzma

import shutil
import subprocess
import sys
from pathlib import Path

PACKET, WORK = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()


def copy():
    dst = WORK / "packet"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(PACKET, dst)
    (dst / "replay-output.txt").unlink()
    return dst


def rewrite(path, data):
    path.unlink()
    path.write_bytes(data)


def text_plant(path, edit):
    raw = path.read_bytes()
    if path.suffix == ".xz":
        rewrite(path, lzma.compress(edit(lzma.decompress(raw)), preset=1))
    elif path.suffix == ".gz":
        rewrite(path, gzip.compress(edit(gzip.decompress(raw)), mtime=0))
    else:
        rewrite(path, edit(raw))


def flip_bit(offset, bit=0):
    return lambda d: d[:offset] + bytes([d[offset] ^ (1 << bit)]) + d[offset + 1:]


def first_line_edit(pick, change):
    def edit(data):
        lines = data.split(b"\n")
        k = next(i for i, line in enumerate(lines) if pick(line))
        lines[k] = change(lines[k])
        return b"\n".join(lines)
    return edit


def seal(root):
    rows = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}"
            for p in sorted(root.rglob("*")) if p.is_file() and p.name != "MANIFEST.sha256"]
    (root / "MANIFEST.sha256").write_text("\n".join(rows) + "\n")


FDRI_FRAME_100 = 460 + 4 * 101 * 100 + 4 * 5  # 1x1 FDRI payload at byte 460: frame 100, word 5, outside the ROMs
PLANTS = [
    ("a configuration bit outside the ROM frames", "shipping/1x1/flip/alinx_ax7101.bit", flip_bit(FDRI_FRAME_100),
     "1x1 cells: 22 INIT bit(s) differ in 8 cell(s), the frame bits 23"),
    ("the part name in the .bit header", "shipping/1x1/flip/alinx_ax7101.bit", flip_bit(165),
     "header 'b' (part)"),
    ("one more instruction byte in the platform image", "shipping/8x8/flip/ctrl_app.elf",
     None, "8x8 ctrl_app.elf: 7 loaded bytes differ"),
    ("one ROM word the image does not hold", "shipping/1x1/flip/gateware/alinx_ax7101_rom_bank0.init",
     first_line_edit(lambda line: line.strip() != b"", lambda line: b"%08x" % (int(line, 16) ^ 1)),
     "1x1 flip: the 5 ROM bank init files"),
    ("a cell placed elsewhere", "shipping/1x1/dump/flip.cells.xz",
     first_line_edit(lambda line: b" RAMB36E1 RAMB36_X" in line,
                     lambda line: line.replace(b"RAMB36_X", b"RAMB36_Z", 1)),
     "1x1 cells: 86465 cells, every name, type and placement equal"),
    ("a route changed", "shipping/1x1/dump/flip.nets.xz",
     first_line_edit(lambda line: b"{" in line, lambda line: line.replace(b"{", b"{ PLANTED", 1)),
     "1x1 nets:"),
    ("a block RAM INIT bit outside the ROMs", "shipping/8x8/dump/flip.bram.xz",
     first_line_edit(lambda line: b"INIT_00=256'h" in line and b"rom_bank" not in line and b"/csr/" not in line,
                     lambda line: line.replace(b"INIT_00=256'h0", b"INIT_00=256'h1", 1)),
     "8x8 bram:"),
    ("a measured harness image swapped for the head's", "harness/1x1/none/measured.elf", "swap",
     "harness/1x1/none/measured.elf: equals the image rebuilt at bench head 8c5e2b4f"),
    ("one more data byte in a harness image", "harness/8x8-1if/answering-ports/head.elf", None,
     "8x8-1if/answering-ports: 7 loaded bytes differ"),
    ("a group's CPU cycles changed (a digit prefixed)", "groups/1x1/none/control.head.json",
     lambda d: d.replace(b'"cpu_cycles": ', b'"cpu_cycles": 1', 1), "1x1/none/control:"),
    ("a raw log digit changed other than the version's", "groups/1x1/none/aecp-held.head.log.gz",
     first_line_edit(lambda line: line.startswith(b"PASS ") and b"5" in line,
                     lambda line: line.replace(b"5", b"6", 1)), "1x1/none/aecp-held: raw log"),
]


def elf_text_byte(path, offset_in_text=0x100):
    """A byte inside .text (an instruction byte away from the CRC pair) or inside .rodata's first bytes, flipped."""
    data = path.read_bytes()
    import struct
    shoff, = struct.unpack_from("<I", data, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 0x2E)
    rows = [struct.unpack_from("<IIIIIIIIII", data, shoff + i * shentsize) for i in range(shnum)]
    names = rows[shstrndx][4]
    want = ".text" if "shipping" in str(path) else ".rodata"
    for r in rows:
        name = data[names + r[0]:data.index(b"\0", names + r[0])].decode()
        if name == want:
            return r[4] + offset_in_text
    raise SystemExit(f"no {want}")


results = []
for label, rel, plant, words in PLANTS:
    root = copy()
    target = root / rel
    if plant == "swap":
        rewrite(target, (root / rel.replace("measured.elf", "head.elf")).read_bytes())
    elif plant is None:
        text_plant(target, flip_bit(elf_text_byte(target)))
    else:
        text_plant(target, plant)
    seal(root)
    run = subprocess.run([sys.executable, "-I", str(root / "tools/replay.py"), str(root)], capture_output=True,
                         text=True)
    fails = [line for line in run.stdout.splitlines() if line.startswith("  FAIL")]
    hit = [line for line in fails if words in line]
    results.append((label, rel, run.returncode, hit or fails))
    print(f"== {label} ({rel})\n   replay exit {run.returncode}: {'CAUGHT' if run.returncode and hit else 'MISSED'}")
    for line in (hit or fails)[:2]:
        print(f"   {line.strip()[:260]}")
shutil.rmtree(WORK / "packet", ignore_errors=True)
caught = sum(1 for _, _, rc, hit in results if rc and hit)
print(f"plants caught: {caught} of {len(results)}")
sys.exit(0 if caught == len(results) else 1)
