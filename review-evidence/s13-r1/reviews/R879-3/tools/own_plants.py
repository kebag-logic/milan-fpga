#!/usr/bin/env python3
"""Reviewer-owned plants against the identity replay (not from the packet's rmutants list).

Usage: python3 -I own_plants.py <identity-dir> <work-dir>
Each plant: a fresh copy, one change, manifests resealed (unless the plant says not to), then the packet's
tools/replay.py. A plant is caught only with a non-zero exit, the RESULT line reached, and a FAIL line naming the
expected group or operand.
"""
import gzip, hashlib, shutil, subprocess, sys, lzma
from pathlib import Path

SRC, WORK = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()


def content(p):
    d = p.read_bytes()
    return lzma.decompress(d) if p.suffix == ".xz" else gzip.decompress(d)


def seal(root):
    files = [p for p in sorted(root.rglob("*")) if p.is_file() and not p.name.startswith("MANIFEST.")]
    packed = [f"{hashlib.sha256(content(p)).hexdigest()}  {p.relative_to(root)}" for p in files
              if p.suffix in (".xz", ".gz")]
    (root / "MANIFEST.content.sha256").write_text("\n".join(packed) + "\n")
    rows = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root)}" for p in files]
    rows.append(f"{hashlib.sha256((root / 'MANIFEST.content.sha256').read_bytes()).hexdigest()}  MANIFEST.content.sha256")
    (root / "MANIFEST.sha256").write_text("\n".join(sorted(rows, key=lambda r: r.split(None, 1)[1])) + "\n")


def gz_line_edit(path, lineno, edit):
    lines = gzip.decompress(path.read_bytes()).split(b"\n")
    new = edit(lines[lineno - 1])
    assert new != lines[lineno - 1], "plant changed nothing"
    lines[lineno - 1] = new
    path.write_bytes(gzip.compress(b"\n".join(lines), mtime=0))


def nth_replace(old, new, skip):
    def edit(line):
        at = -1
        for _ in range(skip + 1):
            at = line.index(old, at + 1)
        return line[:at] + new + line[at + len(old):]
    return edit


def wire_other_digit(line):
    """A '2' -> '3' in the WIRE payload outside the firmware_version string's bytes."""
    fw = line.index(b"332e39362e30")
    at = line.rindex(b"2", 0, fw)  # the byte 0x02 just before the string: adjacent, but not inside it
    return line[:at] + b"3" + line[at + 1:]


PLANTS = [
    # (label, file, editor or action, expected FAIL marker, reseal)
    ("WIRE line: the payload byte 0x02 just before the version string -> 0x03",
     "groups/1x1/none/aecp.head.log.gz", ("gz", 84238, wire_other_digit), "1x1/none/aecp: raw log", True),
    ("PASS line: the mailbox word just before the version's, 0x02000000 -> 0x03000000",
     "groups/1x1/none/aecp.head.log.gz", ("gz", 84254, nth_replace(b":a35:2000000", b":a35:3000000", 0)), "1x1/none/aecp: raw log", True),
    ("8x8 block RAM dump removed, manifests left naming it", "shipping/8x8/dump/flip.bram.xz", "remove",
     "flip.bram", False),
    ("1x1 bench ELF removed and resealed", "shipping/1x1/bench/ctrl_app.elf", "remove", "ctrl_app.elf", True),
    ("8x8 nets: one route line dropped", "shipping/8x8/dump/flip.nets.xz", "xzdrop", "8x8 nets", True),
    ("binding.json: a bench hash's published prefix altered", "binding.json", "binding", "c7189218", True),
]


def run(label, rel, action, marker, reseal):
    root = WORK / "packet"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(SRC, root)
    target = root / rel
    if action == "remove":
        target.unlink()
    elif action == "xzdrop":
        lines = lzma.decompress(target.read_bytes()).split(b"\n")
        del lines[len(lines) // 2]
        target.write_bytes(lzma.compress(b"\n".join(lines), preset=1))
    elif action == "binding":
        target.write_text(target.read_text().replace("c7189218", "c7189219", 1))
    elif action[0] == "gz":
        gz_line_edit(target, action[1], action[2])
    if reseal:
        seal(root)
    r = subprocess.run([sys.executable, "-I", str(root / "tools/replay.py"), str(root)], capture_output=True, text=True)
    fails = [l for l in r.stdout.splitlines() if l.startswith("  FAIL")]
    reached = "== RESULT: " in r.stdout
    caught = r.returncode != 0 and reached and any(marker in l for l in fails)
    print(f"== {label} ({rel}; resealed {reseal})")
    print(f"   exit {r.returncode}, RESULT reached {reached}, traceback {'Traceback' in r.stderr}: "
          f"{'CAUGHT' if caught else 'MISSED'} (marker {marker!r})")
    for l in (fails or r.stderr.splitlines()[-3:])[:3]:
        print(f"   {l.strip()[:300]}")
    return caught


WORK.mkdir(parents=True, exist_ok=True)
n = sum(run(*p) for p in PLANTS)
shutil.rmtree(WORK / "packet", ignore_errors=True)
print(f"reviewer plants caught: {n} of {len(PLANTS)}")
sys.exit(0 if n == len(PLANTS) else 1)
