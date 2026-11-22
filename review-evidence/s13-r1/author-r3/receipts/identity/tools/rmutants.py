#!/usr/bin/env python3
"""rmutants.py PACKET WORK: the replay's planted defects.

First the control: tools/replay.py over an unmodified copy of PACKET, exactly as it is (its own manifests, nothing
re-sealed), must exit 0 and end `== RESULT: ALL CLAIMS HOLD`; otherwise no plant is graded and the exit is 2.

Then each plant: a fresh copy of PACKET, one operand changed as named (or removed), MANIFEST.sha256 and
MANIFEST.content.sha256 rewritten so that only the claim under test can catch it, then tools/replay.py over the
copy. A plant is CAUGHT only when the replay exits non-zero, reaches its RESULT line, and prints a FAIL line holding
the plant's own named marker; a failure elsewhere is MISSED. The grader is itself checked on synthetic outputs first.
Exit 0 only when every plant is caught."""
import gzip
import hashlib
import lzma
import shutil
import struct
import subprocess
import sys
from pathlib import Path

PACKET, WORK = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
RESULT_OK = "== RESULT: ALL CLAIMS HOLD"


def graded(rc, stdout, marker):
    """CAUGHT: a non-zero exit, the RESULT line reached, and a FAIL line holding the plant's marker."""
    fails = [line for line in stdout.splitlines() if line.startswith("  FAIL")]
    return rc != 0 and "\n== RESULT: " in "\n" + stdout and any(marker in line for line in fails)


def grader_self_check():
    cases = (("a failure elsewhere only", 1, "  FAIL  unrelated\n== RESULT: 1 FAILED\n", False),
             ("the marker, but exit 0", 0, "  FAIL  the marker\n== RESULT: 1 FAILED\n", False),
             ("the marker, but no RESULT line (a crash)", 1, "  FAIL  the marker\nTraceback\n", False),
             ("the marker, exit 1, RESULT reached", 1, "  FAIL  unrelated\n  FAIL  the marker\n== RESULT: 2 FAILED\n",
              True))
    bad = [label for label, rc, out, want in cases if graded(rc, out, "the marker") != want]
    print(f"grader self-check: {len(cases) - len(bad)} of {len(cases)}" + (f"; WRONG {bad}" if bad else ""))
    return not bad


def copy():
    dst = WORK / "packet"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(PACKET, dst)
    return dst


def replay(root):
    return subprocess.run([sys.executable, "-I", str(root / "tools/replay.py"), str(root)], capture_output=True,
                          text=True)


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


def content(path):
    data = path.read_bytes()
    return lzma.decompress(data) if path.suffix == ".xz" else gzip.decompress(data)


def seal(root):
    files = [p for p in sorted(root.rglob("*")) if p.is_file() and not p.name.startswith("MANIFEST.")]
    rows = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}" for p in files]
    rows.append(f"{hashlib.sha256(b'').hexdigest()}  MANIFEST.content.sha256")  # replaced below
    packed = [f"{hashlib.sha256(content(p)).hexdigest()}  {p.relative_to(root)}"
              for p in files if p.suffix in (".xz", ".gz")]
    (root / "MANIFEST.content.sha256").write_text("\n".join(packed) + "\n")
    rows[-1] = f"{hashlib.sha256((root / 'MANIFEST.content.sha256').read_bytes()).hexdigest()}  MANIFEST.content.sha256"
    (root / "MANIFEST.sha256").write_text("\n".join(sorted(rows, key=lambda r: r.split(None, 1)[1])) + "\n")


def elf_text_byte(path, offset_in_text=0x100):
    """A byte inside .text (an instruction byte away from the CRC pair) or inside .rodata's first bytes."""
    data = path.read_bytes()
    shoff, = struct.unpack_from("<I", data, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", data, 0x2E)
    rows = [struct.unpack_from("<IIIIIIIIII", data, shoff + i * shentsize) for i in range(shnum)]
    names = rows[shstrndx][4]
    want = ".text" if "shipping" in str(path) else ".rodata"
    for r in rows:
        if data[names + r[0]:data.index(b"\0", names + r[0])].decode() == want:
            return r[4] + offset_in_text
    raise SystemExit(f"no {want}")


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
     "1x1 nets: 95172 nets, every route byte-identical"),
    ("a block RAM INIT bit outside the ROMs", "shipping/8x8/dump/flip.bram.xz",
     first_line_edit(lambda line: b"INIT_00=256'h" in line and b"rom_bank" not in line and b"/csr/" not in line,
                     lambda line: line.replace(b"INIT_00=256'h0", b"INIT_00=256'h1", 1)),
     "8x8 bram: 16 INIT bit(s) differ"),
    ("a measured harness image swapped for the head's", "harness/1x1/none/measured.elf", "swap",
     "harness/1x1/none/measured.elf: equals the image rebuilt at bench head 8c5e2b4f"),
    ("one more data byte in a harness image", "harness/8x8-1if/answering-ports/head.elf", None,
     "8x8-1if/answering-ports: 7 loaded bytes differ"),
    ("a group's CPU cycles changed (a digit prefixed)", "groups/1x1/none/control.head.json",
     lambda d: d.replace(b'"cpu_cycles": ', b'"cpu_cycles": 1', 1), "1x1/none/control: 325 leaves"),
    ("a raw log digit changed other than the version's", "groups/1x1/none/aecp-held.head.log.gz",
     first_line_edit(lambda line: line.startswith(b"PASS ") and b"5" in line,
                     lambda line: line.replace(b"5", b"6", 1)), "1x1/none/aecp-held: raw log"),
    ("R879-2-S2: a '2' -> '3' digit outside the firmware_version string", "groups/1x1/none/control.head.log.gz",
     first_line_edit(lambda line: line.startswith(b"PASS ") and b"2" in line,
                     lambda line: line.replace(b"2", b"3", 1)), "1x1/none/control: raw log"),
    ("R879-2-S3: an operand the claims need, removed", "groups/1x1/none/aecp.head.log.gz", "remove",
     "operand groups/1x1/none/aecp.head.log is absent"),
]

if not grader_self_check():
    sys.exit(3)
control = replay(copy())
held = control.returncode == 0 and control.stdout.rstrip().endswith(RESULT_OK)
print(f"== control: the unplanted packet, exactly as given: replay exit {control.returncode}, "
      f"{'ALL CLAIMS HOLD' if held else 'DOES NOT HOLD: no plant is graded'}")
if not held:
    print("\n".join(line for line in control.stdout.splitlines() if line.startswith("  FAIL"))[:4000])
    sys.exit(2)
caught = 0
for label, rel, plant, marker in PLANTS:
    root = copy()
    target = root / rel
    if plant == "swap":
        rewrite(target, (root / rel.replace("measured.elf", "head.elf")).read_bytes())
    elif plant == "remove":
        target.unlink()
    elif plant is None:
        text_plant(target, flip_bit(elf_text_byte(target)))
    else:
        text_plant(target, plant)
    seal(root)
    run = replay(root)
    ok = graded(run.returncode, run.stdout, marker)
    caught += ok
    hits = [line for line in run.stdout.splitlines() if line.startswith("  FAIL") and marker in line]
    others = [line for line in run.stdout.splitlines() if line.startswith("  FAIL") and marker not in line]
    print(f"== {label} ({rel})\n   replay exit {run.returncode}, RESULT reached: {'== RESULT: ' in run.stdout}: "
          f"{'CAUGHT' if ok else 'MISSED'} (marker: {marker!r})")
    for line in (hits or others)[:2]:
        print(f"   {line.strip()[:260]}")
shutil.rmtree(WORK / "packet", ignore_errors=True)
print(f"plants caught: {caught} of {len(PLANTS)} (by their named markers only)")
sys.exit(0 if caught == len(PLANTS) else 1)
