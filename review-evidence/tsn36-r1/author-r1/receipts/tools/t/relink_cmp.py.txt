#!/usr/bin/env python3
"""relink_cmp.py BASE_CLONE BASE_IMAGE_DIR HEAD_CLONE HEAD_IMAGE_DIR OUT: the two images compared with every address
field named by its relocation.

Each image is linked again from its own inputs, in its link map's LOAD order, with its tree's plat/ctrl_split.ld and the
same flags ctrl_srp_image.link passes, plus -Wl,-q (--emit-relocs), which keeps the relocations in the output and
changes no placement. The relink's loadable bytes (objcopy -O binary) must equal the built image's, so it is the same
link. Then each image is listed canonically:
  - code: `objdump -d -M no-aliases --no-show-raw-insn`, each instruction without its address; an instruction that carries a
    relocation loses its numeric operands (the address the linker wrote) and keeps the relocation's type and target;
  - data (.rodata, .data): each 4-byte word, or, at a relocation's offset, the relocation's type and target;
  - a target is the symbol that holds the relocated address in that image (function or object, else section) plus the
    offset into it, so a symbol placed elsewhere names the same target in both.
The diff of the two listings is what differs other than placement. Prints the report and writes both listings to OUT."""
import bisect
import difflib
import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = '<sdk>/host/bin/riscv32-buildroot-linux-gnu-'


def sh(*a: str) -> str:
    return subprocess.run(a, check=True, capture_output=True, text=True).stdout


def relink(clone: Path, image: Path, out: Path) -> Path:
    loads = [l.split(None, 1)[1].strip() for l in (image / 'ctrl_app.map').read_text().splitlines()
             if l.startswith('LOAD ') and not l.startswith('LOAD linker stubs')]
    objs = [p for p in loads if not p.endswith('.a')]
    libs = [p for p in loads if p.endswith('.a')]
    elf = out / 'relinked.elf'
    subprocess.run([TOOL + 'gcc', '-march=rv32im', '-mabi=ilp32', '-nostdlib', '-static', '-no-pie',
                    '-Wl,--gc-sections,--build-id=none', '-Wl,-q', f'-Wl,-Map,{out / "relinked.map"}',
                    '-T', str(clone / 'sw/firmware/ctrl/plat/ctrl_split.ld'), f'-L{image}', *objs,
                    '-Wl,--start-group', *libs, '-Wl,--end-group', '-o', str(elf)], check=True)
    return elf


def loadable(elf: Path) -> str:
    with tempfile.NamedTemporaryFile(suffix='.bin') as f:
        subprocess.run([TOOL + 'objcopy', '-O', 'binary', str(elf), f.name], check=True)
        return hashlib.sha256(Path(f.name).read_bytes()).hexdigest()


class Symbols:
    """An image's symbols (functions, objects and labels, the assembler's local labels included) and its sections, to
    name an address as the nearest symbol at or before it in its own section, plus the offset."""

    RANK = {'FUNC': 0, 'OBJECT': 1, 'NOTYPE': 2}

    def __init__(self, elf: Path):
        self.secs = []
        for l in sh(TOOL + 'readelf', '-SW', str(elf)).splitlines():
            m = re.match(r'^\s+\[\s*\d+\]\s+(\S+)\s+(PROGBITS|NOBITS)\s+([0-9a-f]+)\s+[0-9a-f]+\s+([0-9a-f]+)', l)
            if m:
                self.secs.append((int(m.group(3), 16), int(m.group(4), 16), m.group(1)))
        rows = []
        for l in sh(TOOL + 'readelf', '-sW', str(elf)).splitlines():
            f = l.split()
            if len(f) == 8 and f[0].endswith(':') and f[3] in self.RANK and f[6] not in ('UND',):
                rows.append((int(f[1], 16), self.RANK[f[3]], f[7]))
        rows.sort()
        self.rows = rows
        self.starts = [r[0] for r in rows]

    def section(self, addr: int):
        return next(((a, s, n) for a, s, n in self.secs if a <= addr < a + s), None)

    def name(self, addr: int) -> str:
        sec = self.section(addr)
        if sec is None:
            exact = [r for r in self.rows if r[0] == addr]
            if exact:
                return f'{min(exact, key=lambda r: (r[1], r[2]))[2]}+0x0'
            ends = [n for a, s, n in self.secs if addr == a + s]
            return f'[{ends[0]}]+end' if ends else f'{addr:#x}'
        i = bisect.bisect_right(self.starts, addr) - 1
        while i >= 0 and self.rows[i][0] >= sec[0]:
            at = self.rows[i][0]
            same = [r for r in self.rows[bisect.bisect_left(self.starts, at):bisect.bisect_right(self.starts, at)]]
            r = min(same, key=lambda r: (r[1], r[2]))
            return f'{r[2]}+{addr - at:#x}'
        return f'[{sec[2]}]+{addr - sec[0]:#x}'


def relocs(elf: Path) -> dict[str, dict[int, tuple[str, int]]]:
    """Per relocated section, offset -> (type, target address)."""
    out, sec = {}, None
    for l in sh(TOOL + 'readelf', '-rW', str(elf)).splitlines():
        m = re.match(r"^Relocation section '\.rela(\S+)'", l)
        if m:
            sec = m.group(1)
            out[sec] = {}
            continue
        m = re.match(r'^([0-9a-f]+)\s+[0-9a-f]+\s+(R_RISCV_\S+)\s+([0-9a-f]+)\s+(\S+)?\s*([+-]\s*[0-9a-f]+)?', l)
        if m and sec:
            value = int(m.group(3), 16)
            addend = int(m.group(5).replace(' ', ''), 16) if m.group(5) else 0
            out[sec].setdefault(int(m.group(1), 16), (m.group(2), value + addend))
    return out


INSN = re.compile(r'^\s*([0-9a-f]+):\s+(.*)$')
LABEL = re.compile(r'^([0-9a-f]{8}) <([^>]+)>:$')


def listing(elf: Path) -> list[str]:
    s, rel = Symbols(elf), relocs(elf)
    text = rel.get('.text', {})
    out = []
    for line in sh(TOOL + 'objdump', '-d', '-M', 'no-aliases', '--no-show-raw-insn', str(elf)).splitlines():
        m = LABEL.match(line)
        if m:
            out.append(f'<{m.group(2)}>:')
            continue
        m = INSN.match(line)
        if not m:
            continue
        addr, body = int(m.group(1), 16), m.group(2).split(' # ')[0].strip()
        if addr in text:
            kind, target = text[addr]
            op = body.split(None, 1)
            regs = [x for x in (op[1].split(',') if len(op) > 1 else [])
                    if re.fullmatch(r'[a-z][a-z0-9]+(\([a-z0-9]+\))?', x.strip()) and not
                    re.fullmatch(r'0x[0-9a-f]+|[0-9a-f]+', x.strip())]
            out.append(f'\t{op[0]} {",".join(r.strip() for r in regs)}  {kind} {s.name(target)}')
        else:
            body = re.sub(r'\b[0-9a-f]+ <([^>]+)>', lambda x: f'<{s.name(int(x.group(0).split()[0], 16))}>', body)
            out.append('\t' + body)
    for sec in ('.rodata', '.data'):
        dump = sh(TOOL + 'objdump', '-s', '-j', sec, str(elf)).splitlines()
        words = []
        for l in dump:
            f = l.split()
            if len(f) >= 2 and re.fullmatch(r'[0-9a-f]{4,8}', f[0]):
                base = int(f[0], 16)
                for k, w in enumerate(f[1:5]):
                    if re.fullmatch(r'[0-9a-f]{2,8}', w):
                        words.append((base + 4 * k, w))
        r = rel.get(sec, {})
        sec_start = next(a for a, _, n in s.secs if n == sec)
        for a, w in words:
            if a in r:
                out.append(f'{sec}+{a - sec_start:#x} {r[a][0]} {s.name(r[a][1])}')
            else:
                out.append(f'{sec}+{a - sec_start:#x} {w}')
    return out


bc, bi, hc, hi, outdir = map(lambda x: Path(x).resolve(), sys.argv[1:6])
outdir.mkdir(parents=True, exist_ok=True)
rows = {}
for tag, clone, image in (('base', bc, bi), ('head', hc, hi)):
    d = outdir / tag
    d.mkdir(exist_ok=True)
    elf = relink(clone, image, d)
    same = loadable(elf) == loadable(image / 'ctrl_app.elf')
    print(f'{tag}: relinked with -Wl,-q, loadable bytes {"EQUAL to" if same else "DIFFERENT from"} the built image '
          f'({loadable(image / "ctrl_app.elf")[:16]})')
    assert same, tag
    rows[tag] = listing(elf)
    (d / 'listing.txt').write_text('\n'.join(rows[tag]) + '\n')
diff = list(difflib.unified_diff(rows['base'], rows['head'], 'base', 'head', n=3, lineterm=''))
changed = [l for l in diff if l[:1] in '+-' and l[:3] not in ('+++', '---')]
print(f'canonical listings: {len(rows["base"])} base lines, {len(rows["head"])} head lines, {len(changed)} differ')
print('\n'.join(diff))
