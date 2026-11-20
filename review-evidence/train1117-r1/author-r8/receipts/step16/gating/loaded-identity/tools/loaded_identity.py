#!/usr/bin/env python3
"""loaded_identity.py: one gating bench image's firmware against the product image the ledger links at the same point
(#665; R866-4-F1), two-sided and by every loaded byte.

    loaded_identity.py --repo REPO --point NAME --gating-elf ELF --product-elf ELF --build BUILD --artifacts LIST
                       [--gating-objects DIR --product-objects DIR]

REPO is a checkout of the head (its sw/litex modules are imported: ctrl_memory, check_image_identity,
qspi_owner_transition). BUILD is the gating build's milan_soc.py output directory, LIST the chain's artifacts.sha256.
The objects, when given, are the two links' inputs, compared section by section to say why the whole files differ.

Each check prints CHECK <name>: PASS|FAIL and its evidence:
  elf-header    class, data, machine, type, entry and flags equal
  segments      every program header equal, and every PT_LOAD's file bytes equal (sha256 of each side)
  loaded        every SHF_ALLOC section: name, type, flags, VMA, LMA, size and its bytes' sha256 on each side, equal
  not-loaded    every other section listed on each side; the whole files' differing bytes all inside them
  symtab        the symbol tables hold the same entries; an entry moved only past another at its own address
  rom-words     the repository's rom words (ctrl_memory.rom_words) of each ELF equal the rom banks' init files the
                bitstream was built from (check_image_identity.facts)
  manifest      image_manifest.json's sha256 is LIST's; it binds the gating ELF (sha256, bytes) and the bitstream
                (bitstream_binding: payload sha256 and part, recomputed from the .bit); every file LIST names has the
                sha256 LIST gives
  identity-gate check_image_identity.findings(BUILD, firmware=gating ELF, bitstream) is empty
  objects       (with the objects) no SHF_ALLOC section of any input object differs; the differing kinds counted,
                and each tree's compiler identification (.comment)
Exit 0 when every check passes, 1 otherwise, 2 when an input cannot be read. Standard library only."""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import struct
import sys
from pathlib import Path

SHF_ALLOC, SHT_NOBITS, SHT_SYMTAB, PT_LOAD = 0x2, 8, 2, 1
TYPES = {0: 'NULL', 1: 'PROGBITS', 2: 'SYMTAB', 3: 'STRTAB', 4: 'RELA', 8: 'NOBITS', 9: 'REL', 14: 'INIT_ARRAY',
         15: 'FINI_ARRAY', 0x70000003: 'RISCV_ATTRIBUTES'}
PTYPES = {0: 'NULL', 1: 'LOAD', 4: 'NOTE', 0x6474e551: 'GNU_STACK', 0x70000003: 'RISCV_ATTRIBUTES'}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Elf:
    """An ELF32 little-endian file: its header, sections and program headers."""

    def __init__(self, path: Path):
        self.path, self.data = path, path.read_bytes()
        b = self.data
        if b[:4] != b'\x7fELF' or b[4] != 1 or b[5] != 1:
            raise ValueError(f'{path}: not an ELF32 little-endian file')
        (self.type, self.machine, self.version, self.entry, phoff, shoff, self.flags, _, phentsize, phnum, shentsize,
         shnum, shstrndx) = struct.unpack_from('<HHIIIIIHHHHHH', b, 16)
        self.ident = b[:16]
        raw = [struct.unpack_from('<IIIIIIIIII', b, shoff + k * shentsize) for k in range(shnum)]
        names = raw[shstrndx]
        strtab = b[names[4]:names[4] + names[5]]
        self.sections = [dict(index=k, name=strtab[s[0]:strtab.index(b'\0', s[0])].decode(), type=s[1], flags=s[2],
                              addr=s[3], offset=s[4], size=s[5], link=s[6], info=s[7], align=s[8], entsize=s[9])
                         for k, s in enumerate(raw)]
        self.segments = [dict(zip(('type', 'offset', 'vaddr', 'paddr', 'filesz', 'memsz', 'flags', 'align'),
                                  struct.unpack_from('<IIIIIIII', b, phoff + k * phentsize))) for k in range(phnum)]

    def bytes_of(self, s: dict) -> bytes:
        return b'' if s['type'] == SHT_NOBITS else self.data[s['offset']:s['offset'] + s['size']]

    def lma(self, s: dict) -> int | None:
        """The load address: the PT_LOAD that holds the section's bytes (or, for NOBITS, its addresses)."""
        for p in self.segments:
            if p['type'] != PT_LOAD:
                continue
            if s['type'] != SHT_NOBITS and s['size'] and p['offset'] <= s['offset'] and \
                    s['offset'] + s['size'] <= p['offset'] + p['filesz']:
                return p['paddr'] + s['offset'] - p['offset']
            if s['type'] == SHT_NOBITS and p['vaddr'] <= s['addr'] < p['vaddr'] + p['memsz']:
                return p['paddr'] + s['addr'] - p['vaddr']
        return None

    def symbols(self) -> list[tuple]:
        sym = next(s for s in self.sections if s['type'] == SHT_SYMTAB)
        strs = self.bytes_of(self.sections[sym['link']])
        out = []
        for k in range(sym['size'] // 16):
            name, value, size, info, other, shndx = struct.unpack_from('<IIIBBH', self.data, sym['offset'] + 16 * k)
            out.append((strs[name:strs.index(b'\0', name)].decode(), value, size, info, other, shndx))
        return out


def check(name: str, ok: bool, lines: list[str], results: dict) -> None:
    results[name] = ok
    print(f'CHECK {name}: {"PASS" if ok else "FAIL"}')
    for line in lines:
        print(f'  {line}')


def hexa(v: int | None) -> str:
    return '-' if v is None else f'0x{v:08x}'


def section_rows(g: Elf, p: Elf, alloc: bool) -> tuple[list[str], bool, set[str]]:
    """The table of one class of sections, both sides by name, and whether every row agrees."""
    gs = {s['name']: s for s in g.sections if bool(s['flags'] & SHF_ALLOC) == alloc and s['type']}
    ps = {s['name']: s for s in p.sections if bool(s['flags'] & SHF_ALLOC) == alloc and s['type']}
    rows, ok, differ = ['| section | type | flags | VMA | LMA | bytes | sha256 gating | sha256 product | equal |',
                        '|---|---|---|---|---|---:|---|---|---|'], True, set()
    for name in sorted(set(gs) | set(ps), key=lambda n: (gs.get(n) or ps[n])['index']):
        a, b = gs.get(name), ps.get(name)
        if a is None or b is None:
            rows.append(f'| {name} | only {"product" if a is None else "gating"} | | | | | | | NO |')
            ok = False
            differ.add(name)
            continue
        da, db = g.bytes_of(a), p.bytes_of(b)
        head = (a['type'], a['flags'], a['addr'], g.lma(a), a['size']) == (b['type'], b['flags'], b['addr'], p.lma(b),
                                                                            b['size'])
        same = head and da == db
        ok &= same
        if not same:
            differ.add(name)
        ha, hb = ('(NOBITS: no file bytes)',) * 2 if a['type'] == SHT_NOBITS else (sha(da), sha(db))
        rows.append(f'| {name} | {TYPES.get(a["type"], hex(a["type"]))} | 0x{a["flags"]:x} | {hexa(a["addr"])} | '
                    f'{hexa(g.lma(a))} | {a["size"]} | {ha} | {hb} | {"yes" if same else "NO"} |')
    return rows, ok, differ


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    for arg in ('--repo', '--point', '--gating-elf', '--product-elf', '--build', '--artifacts'):
        ap.add_argument(arg, required=True)
    ap.add_argument('--gating-objects')
    ap.add_argument('--product-objects')
    a = ap.parse_args()
    repo, build = Path(a.repo), Path(a.build)
    sys.path.insert(0, str(repo / 'sw/litex'))
    try:
        g, p = Elf(Path(a.gating_elf)), Elf(Path(a.product_elf))
        listed = {}
        for line in Path(a.artifacts).read_text().splitlines():
            digest, name = line.split(None, 1)
            listed[name.strip()] = digest
        import check_image_identity as cii
        import ctrl_memory
        from qspi_owner_transition import bitstream_binding
    except (OSError, ValueError, ImportError) as exc:
        print(f'UNREADABLE: {exc}')
        return 2
    results: dict[str, bool] = {}
    print(f'# {a.point}: the gating bench image\'s firmware against the ledger\'s product image')
    print(f'gating  ELF {sha(g.data)} {len(g.data)} bytes')
    print(f'product ELF {sha(p.data)} {len(p.data)} bytes')
    print()

    keys = ('type', 'machine', 'version', 'entry', 'flags', 'ident')
    check('elf-header', all(getattr(g, k) == getattr(p, k) for k in keys),
          [f'{k}: {getattr(g, k)!r} / {getattr(p, k)!r}' if k == 'ident' else
           f'{k}: 0x{getattr(g, k):x} / 0x{getattr(p, k):x}' for k in keys], results)

    rows, ok = ['| # | type | offset | vaddr | paddr | filesz | memsz | flags | sha256 of the file bytes, gating | '
                'product | equal |', '|---:|---|---:|---|---|---:|---:|---|---|---|---|'], len(g.segments) == len(p.segments)
    for k, (x, y) in enumerate(zip(g.segments, p.segments)):
        bx, by = g.data[x['offset']:x['offset'] + x['filesz']], p.data[y['offset']:y['offset'] + y['filesz']]
        same = x == y and bx == by
        ok &= same
        rows.append(f'| {k} | {PTYPES.get(x["type"], hex(x["type"]))} | {x["offset"]} | {hexa(x["vaddr"])} | '
                    f'{hexa(x["paddr"])} | {x["filesz"]} | {x["memsz"]} | 0x{x["flags"]:x} | {sha(bx)} | {sha(by)} | '
                    f'{"yes" if same else "NO"} |')
    check('segments', ok, rows, results)

    rows, ok, _ = section_rows(g, p, alloc=True)
    check('loaded', ok, rows, results)

    rows, _, differ = section_rows(g, p, alloc=False)
    diff = [k for k in range(min(len(g.data), len(p.data))) if g.data[k] != p.data[k]]
    owner = collections.Counter()
    for k in diff:
        hit = next((s['name'] for s in g.sections if s['type'] and s['type'] != SHT_NOBITS and
                    s['offset'] <= k < s['offset'] + s['size']), '(no section: ELF or section headers)')
        owner[hit] += 1
    inside = len(g.data) == len(p.data) and set(owner) <= differ and \
        not any(s['flags'] & SHF_ALLOC for s in g.sections if s['name'] in owner)
    rows += ['', f'whole files: {len(diff)} differing bytes of {len(g.data)}, by section: {dict(owner)}',
             'section header tables: ' + ('equal' if [(s['name'], s['type'], s['flags'], s['addr'], s['offset'],
                                                       s['size']) for s in g.sections] ==
                                          [(s['name'], s['type'], s['flags'], s['addr'], s['offset'], s['size'])
                                           for s in p.sections] else 'DIFFER')]
    check('not-loaded', inside, rows, results)

    gy, py = g.symbols(), p.symbols()
    moved = [k for k in range(len(gy)) if gy[k] != py[k]]
    same_addr = all(gy[k][1] == py[k][1] for k in moved)
    check('symtab', collections.Counter(gy) == collections.Counter(py) and same_addr,
          [f'entries: {len(gy)} / {len(py)}; the same entries on both sides: {collections.Counter(gy) == collections.Counter(py)}',
           f'positions holding another entry: {len(moved)}, from {moved[0] if moved else "-"} to '
           f'{moved[-1] if moved else "-"}; each at the address of the entry it replaces: {same_addr}',
           *[f'#{k}: gating {gy[k][0]!r} @ 0x{gy[k][1]:x} / product {py[k][0]!r} @ 0x{py[k][1]:x}' for k in moved[:6]]],
          results)

    facts = cii.facts(build)
    words = {side: ctrl_memory.rom_words(ctrl_memory.read_elf(e.path)) for side, e in (('gating', g), ('product', p))}
    pack = lambda w: struct.pack(f'<{len(w)}I', *w)
    check('rom-words', words['gating'] == words['product'] == facts['rom_words'],
          [f'{side} ELF: {len(w)} rom words, sha256 {sha(pack(w))}' for side, w in words.items()] +
          [f'rom bank init files of the build: {len(facts["rom_words"])} words, sha256 {sha(pack(facts["rom_words"]))}'],
          results)

    man_path = build / 'image_manifest.json'
    man = json.loads(man_path.read_text())
    bit = build / 'gateware/alinx_ax7101.bit'
    rebound = bitstream_binding(bit)
    lines, ok = [], True
    for name, digest in listed.items():
        path = Path(name) if Path(name).is_absolute() else build / name
        have = sha(path.read_bytes()) if path.is_file() else 'missing'
        same = have == digest
        ok &= same
        lines.append(f'{Path(name).name}: listed {digest}, file {have}: {"equal" if same else "DIFFERS"}')
    fw = man['ctrl_firmware']
    ok &= fw['sha256'] == sha(g.data) and fw['bytes'] == len(g.data) and man['bitstream'] == rebound
    lines += [f'manifest binds the firmware {fw["path"]}: sha256 {fw["sha256"]} ({"the gating ELF" if fw["sha256"] == sha(g.data) else "NOT the gating ELF"}), '
              f'{fw["bytes"]} bytes',
              f'manifest binds the bitstream: {man["bitstream"]}',
              f'recomputed from the .bit (sha256 {sha(bit.read_bytes())}): {rebound}: '
              f'{"equal" if man["bitstream"] == rebound else "DIFFERS"}']
    check('manifest', ok, lines, results)

    found = cii.findings(build, firmware=g.path, bitstream=bit)
    check('identity-gate', not found, [f'findings: {found or "none"}'], results)

    if a.gating_objects and a.product_objects:
        kinds, alloc, comments, n = collections.Counter(), [], collections.defaultdict(set), 0
        for po in sorted(Path(a.product_objects).glob('*.o')):
            go = Path(a.gating_objects) / po.name
            x, y = Elf(go), Elf(po)
            n += 1
            sx, sy = {s['name']: s for s in x.sections}, {s['name']: s for s in y.sections}
            if set(sx) != set(sy):
                kinds['the section set'] += 1
            for name, s in sx.items():
                t = sy.get(name)
                for side, e, sec in (('gating', x, s), ('product', y, t)):
                    if name == '.comment' and sec is not None:
                        comments[side] |= {c.decode() for c in e.bytes_of(sec).split(b'\0') if c}
                if t is None or s['type'] in (0, SHT_NOBITS) or x.bytes_of(s) == y.bytes_of(t):
                    continue
                if s['flags'] & SHF_ALLOC:
                    alloc.append(f'{po.name} {name}')
                kinds['.rela.*' if name.startswith('.rela') else name] += 1
        check('objects', not alloc,
              [f'{n} input objects compared; SHF_ALLOC sections differing: {alloc or "none"}',
               f'differing sections, by kind (objects): {dict(kinds)}',
               *[f'{side} compiler identification (.comment): {sorted(c)}' for side, c in comments.items()]], results)

    verdict = all(results.values())
    print()
    print(f'RESULT {a.point}: {"PASS" if verdict else "FAIL"}: ' + ', '.join(f'{k} {"pass" if v else "FAIL"}'
                                                                        for k, v in results.items()))
    return 0 if verdict else 1


if __name__ == '__main__':
    sys.exit(main())
