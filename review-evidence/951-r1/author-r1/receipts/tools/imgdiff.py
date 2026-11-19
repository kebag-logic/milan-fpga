#!/usr/bin/env python3
"""imgdiff.py BASE_IMAGE_DIR HEAD_IMAGE_DIR: what differs between two linked split images of the same point.

1. Objects: the sha256 of every object the link map loads (each LOAD line, archives included), by name; the names
   that differ.
2. Each differing object, normalised: `objdump -dr --no-show-raw-insn` with every address, encoded branch offset and
   relocation offset removed, so only instructions, operands that are not addresses, relocation types and their
   symbols remain; plus every section's bytes (`objdump -s`) other than code; the unified diff of each.
3. The link map: every input section's size, by (object, section), and its placement shift (head address less base
   address); the sections whose size differs, and the shifts as runs over the map's order.
4. The image: each output section's address and size, and the sha256 of its loadable bytes (objcopy -O binary).
Prints a report; exit 0 always (the report is the evidence, the reader judges it)."""
import difflib
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = '<sdk>/host/bin/riscv32-buildroot-linux-gnu-'
base, head = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()


def sh(*a: str) -> str:
    return subprocess.run(a, check=True, capture_output=True, text=True).stdout


def loads(d: Path) -> list[Path]:
    return [Path(l.split(None, 1)[1].strip()) for l in (d / 'ctrl_app.map').read_text().splitlines()
            if l.startswith('LOAD ') and not l.startswith('LOAD linker stubs')]


def digest(p: Path) -> str:
    """An object's sha256, or an archive's members' (each member's sha256 by name, so `ar` headers' dates and the
    build's path do not count)."""
    if p.suffix != '.a':
        return hashlib.sha256(p.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([TOOL + 'ar', 'x', str(p)], cwd=d, check=True)
        members = sorted(Path(d).iterdir())
        return hashlib.sha256(''.join(f'{m.name} {hashlib.sha256(m.read_bytes()).hexdigest()}\n'
                                      for m in members).encode()).hexdigest()


def discarded(d: Path) -> set[tuple[str, str]]:
    """(object, section) of every input section the link map lists as discarded."""
    lines = (d / 'ctrl_app.map').read_text().splitlines()
    a = next(i for i, l in enumerate(lines) if l.startswith('Discarded input sections'))
    b = next(i for i, l in enumerate(lines) if l.startswith('Memory Configuration'))
    out, pending = set(), None
    for l in lines[a:b]:
        m = re.match(r'^ (\.\S+)\s*$', l)
        if m:
            pending = m.group(1)
            continue
        m = re.match(r'^ (\.\S+)\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+(\S+)$', l)
        if m:
            out.add((Path(m.group(2)).name, m.group(1)))
            continue
        m = re.match(r'^\s+0x[0-9a-f]+\s+0x[0-9a-f]+\s+(\S+)$', l)
        if m and pending:
            out.add((Path(m.group(1)).name, pending))
        pending = None
    return out


ADDR = re.compile(r'^\s*[0-9a-f]+:\s*')
TARGET = re.compile(r'\b[0-9a-f]+ (<[^>]+>)')
LABEL = re.compile(r'^[0-9a-f]{8} (<[^>]+>):$')
COMMENT = re.compile(r'\s+# [0-9a-f]+( <[^>]+>)?$')


def code(obj: Path) -> list[str]:
    out = []
    for line in sh(TOOL + 'objdump', '-dr', '--no-show-raw-insn', str(obj)).splitlines()[2:]:
        if not line.strip():
            continue
        m = LABEL.match(line)
        if m:
            out.append(m.group(1) + ':')
            continue
        line = COMMENT.sub('', ADDR.sub('', line))
        out.append('\t' + TARGET.sub(r'\1', line).strip())
    return out


def data(obj: Path, dropped: set[tuple[str, str]]) -> list[str]:
    secs = [l.split()[1] for l in sh(TOOL + 'objdump', '-h', str(obj)).splitlines()
            if re.match(r'^\s+\d+ ', l)]
    out = []
    for s in secs:
        if s.startswith('.text') or s.startswith('.rela'):
            continue
        tag = ' (discarded by the link)' if (obj.name, s) in dropped else ''
        dump = sh(TOOL + 'objdump', '-s', '-j', s, str(obj)).splitlines()[3:]
        out += [f'{s}{tag}: ' + ' '.join(l.split()[1:5]) for l in dump if l.strip()]
    return out


SEC = re.compile(r'^ (\.\S+)\s*$|^ (\.\S+)\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\S+)$')
CONT = re.compile(r'^\s+0x([0-9a-f]+)\s+0x([0-9a-f]+)\s+(\S+)$')


def placements(d: Path) -> list[tuple[str, str, int, int]]:
    """(object, input section, address, size) for every input section the map places, in map order."""
    rows, pending = [], None
    lines = (d / 'ctrl_app.map').read_text().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith('Linker script and memory map'))
    for l in lines[start:]:
        m = SEC.match(l)
        if m and m.group(1):
            pending = m.group(1)
            continue
        if m and m.group(2):
            rows.append((Path(m.group(5)).name, m.group(2), int(m.group(3), 16), int(m.group(4), 16)))
            pending = None
            continue
        c = CONT.match(l)
        if c and pending:
            rows.append((Path(c.group(3)).name, pending, int(c.group(1), 16), int(c.group(2), 16)))
        pending = None
    return [r for r in rows if r[3] > 0]


def sections(elf: Path) -> list[str]:
    out = []
    for l in sh(TOOL + 'readelf', '-SW', str(elf)).splitlines():
        m = re.match(r'^\s+\[\s*\d+\]\s+(\S+)\s+(\S+)\s+([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)', l)
        if m and m.group(2) in ('PROGBITS', 'NOBITS'):
            out.append(f'{m.group(1)} {m.group(2)} addr 0x{m.group(3)} size 0x{m.group(4)}')
    return out


def loadable(elf: Path) -> str:
    with tempfile.NamedTemporaryFile(suffix='.bin') as f:
        subprocess.run([TOOL + 'objcopy', '-O', 'binary', str(elf), f.name], check=True)
        return hashlib.sha256(Path(f.name).read_bytes()).hexdigest()


def rel(p: Path, d: Path) -> str:
    try:
        return str(p.relative_to(d))
    except ValueError:
        return p.name


print(f'# image diff: base {base.parent.name}/{base.name} against head (same point)')
bl, hl = loads(base), loads(head)
bn, hn = [rel(p, base) for p in bl], [rel(p, head) for p in hl]
print(f'## 1. linked inputs: {len(bl)} base, {len(hl)} head, same names in the same order: {bn == hn}')
differ = []
for b, h, name in zip(bl, hl, bn):
    if digest(b) != digest(h):
        differ.append((b, h, name))
print(f'inputs that differ by sha256: {len(differ)} of {len(bl)}: {", ".join(n for _, _, n in differ) or "none"}')
for b, h, name in differ:
    if not name.endswith('.o'):
        continue
    dc = list(difflib.unified_diff(code(b), code(h), 'base/' + name, 'head/' + name, n=2, lineterm=''))
    dd = list(difflib.unified_diff(data(b, discarded(base)), data(h, discarded(head)), 'base/' + name,
                                   'head/' + name, n=0, lineterm=''))
    kept = [l for l in dd if l[:1] in '+-' and l[:3] not in ('+++', '---') and 'discarded by the link' not in l]
    print(f'## 2. {name}, normalised code: {sum(1 for l in dc if l[:1] in "+-" and l[:3] not in ("+++", "---"))} '
          f'line(s) differ; other sections\' bytes: {"equal" if not dd else "differ only in sections the link discards" if not kept else "DIFFER"}')
    print('\n'.join(dc))
    print('\n'.join(dd))
bp, hp = placements(base), placements(head)
print(f'## 3. link map: {len(bp)} placed input sections base, {len(hp)} head; '
      f'same (object, section) order: {[r[:2] for r in bp] == [r[:2] for r in hp]}')
if [r[:2] for r in bp] == [r[:2] for r in hp]:
    sized = [(b[0], b[1], b[3], h[3]) for b, h in zip(bp, hp) if b[3] != h[3]]
    print('input sections whose size differs: ' +
          ('; '.join(f'{o} {s} {x} -> {y} bytes' for o, s, x, y in sized) or 'none'))
    runs, prev = [], None
    for b, h in zip(bp, hp):
        shift = h[2] - b[2]
        if prev is None or shift != prev[0]:
            prev = [shift, b, b, 0]
            runs.append(prev)
        prev[2] = b
        prev[3] += 1
    for shift, first, last, n in runs:
        print(f'  shift {shift:+d} B over {n} section(s): {first[0]} {first[1]} @0x{first[2]:x} .. '
              f'{last[0]} {last[1]} @0x{last[2]:x}')
be, he = base / 'ctrl_app.elf', head / 'ctrl_app.elf'
print('## 4. output sections (base | head)')
for x, y in zip(sections(be), sections(he)):
    print(f'  {x} | {y}' + ('' if x == y else '   <-'))
print(f'loadable bytes sha256: base {loadable(be)[:16]} head {loadable(he)[:16]}; '
      f'whole ELF base {digest(be)[:16]} head {digest(he)[:16]}')
