#!/usr/bin/env python3
"""replay.py [DIR]: re-derive the #665 flip's image-identity claims from the operands in DIR (default: this file's
parent's parent, the identity/ directory). Python 3.9+, standard library only; nothing is fetched or built.

Each check prints `ok` or `FAIL` and the figures it found. Exit 0 only when every check holds.

  1. manifest   every file is listed in MANIFEST.sha256 with its hash, and every listed file hashes as listed; every
                compressed operand's content hashes as MANIFEST.content.sha256 lists it (the content is what the
                claims read; the compressed bytes are one encoding of it, binding.json `reencoded`);
  2. binding    each operand's sha256 against the identity published for it (binding.json: the bench re-check's
                images, the round-1 flip images, the measured CPU-budget images and their rebuilds);
  3. shipping   per shape (1x1/1if, 8x8/1if), bench image against flip image:
                a. the .bit: the same header layout and packet structure; every differing byte named: header text
                   (the design name's SW_CRC/SW_HDR_SHA256, the date, the time), the configuration CRC register
                   write, and FDRI frame bits (frame, word, bit count); nothing else;
                b. the platform image (ctrl_app.elf): the same loaded layout; the only loaded bytes that differ are
                   one lui/addi pair whose value is crc32 of the image's own aecp_entity_image, and that image's
                   firmware-version byte '2' -> '3'; aecp_entity_image is byte for byte the export's aem_desc.bin;
                c. the ROM: the rom_bank*.init files concatenated are exactly the ELF's load segments, zero beyond;
                d. the export's other files: every differing line named (the AEM CRC, the manifest's VERSION and
                   hashes);
                e. the routed checkpoints' dumps: block RAM INIT bits (both shapes), and where the full dump is here
                   every cell's name, type, LOC and BEL and every net's route; the INIT bits that differ sum to the
                   frame bits of (a), and each differing cell is the CSR defaults ROM or a platform ROM bank;
  4. harness    the 16 CPU-budget arm images (8 arms x 2 points), measured against this head's: the same layout,
                only the lui/addi pair and the version byte differ, as (3b); each arm's group partition
                (parts.json) is equal;
  5. groups     the 13 re-measured groups that read the ENTITY descriptor, measured against this head's: every
                leaf of the result JSON equal, none excluded; and the raw simulation logs: the same lines, each
                differing line only inside the ENTITY's firmware_version string, the one the arm's two images
                differ in (section 4): a WIRE line's payload bytes, or a PASS line's mailbox words (W, laid out as
                little-endian bytes in their order), differ only within an occurrence of the measured string that
                reads as the head's string at the same offset; each difference is printed in its context.

An operand the manifest names but the directory does not hold is refused by name, and the run still ends with its
RESULT line.
"""
import binascii
import gzip
import hashlib
import json
import lzma
import struct
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
FAILS = []


def check(ok, text):
    print(("  ok    " if ok else "  FAIL  ") + text)
    if not ok:
        FAILS.append(text)
    return ok


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    """A file's bytes, through xz or gzip when its name says so."""
    data = path.read_bytes()
    if path.suffix == ".xz":
        return lzma.decompress(data)
    if path.suffix == ".gz":
        return gzip.decompress(data)
    return data


def find(base, name):
    """base/name, or its .xz/.gz form."""
    for suffix in ("", ".xz", ".gz"):
        path = base / (name + suffix)
        if path.is_file():
            return path
    return None


class Absent(Exception):
    """A required operand is not in the directory; its claims are refused, by name, and the run goes on."""


def operand(base, name):
    """base/name (or its .xz/.gz form), which the claims need; raises Absent naming it."""
    path = find(base, name)
    if path is None:
        raise Absent(str((base / name).relative_to(ROOT)))
    return path


def refused(scope, absent):
    check(False, f"{scope}: operand {absent} is absent; the claims that read it are refused")


# ------------------------------------------------------------------ 1. manifest
def manifest():
    print("== 1. manifest")
    rows = [line.split(None, 1) for line in (ROOT / "MANIFEST.sha256").read_text().splitlines() if line.strip()]
    listed = {name.strip(): digest for digest, name in rows}
    present = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and p.name != "MANIFEST.sha256"}
    bad = sorted(n for n, d in listed.items() if not (ROOT / n).is_file() or sha(ROOT / n) != d)
    check(not bad, f"{len(listed)} listed files hash as listed" + (f"; mismatched {bad}" if bad else ""))
    check(set(listed) == present, f"no file unlisted ({sorted(present - set(listed))[:5]}) or missing "
                                  f"({sorted(set(listed) - present)[:5]})")
    content = ROOT / "MANIFEST.content.sha256"
    rows = [line.split(None, 1) for line in content.read_text().splitlines() if line.strip()]
    compressed = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and p.suffix in (".xz", ".gz")}
    wrong = sorted(n.strip() for d, n in rows
                   if not (ROOT / n.strip()).is_file() or hashlib.sha256(read(ROOT / n.strip())).hexdigest() != d)
    check(not wrong and {n.strip() for _d, n in rows} == compressed,
          f"{len(rows)} compressed operands' content hashes as MANIFEST.content.sha256 lists it, every compressed "
          f"file listed" + (f"; mismatched or absent {wrong[:5]}" if wrong else "")
          + (f"; unlisted {sorted(compressed - {n.strip() for _d, n in rows})[:5]}"
             if compressed - {n.strip() for _d, n in rows} else ""))


# ------------------------------------------------------------------- 2. binding
def binding():
    print("== 2. binding to the published identities (binding.json)")
    table = json.loads((ROOT / "binding.json").read_text())
    for row in table["operands"]:
        path = find(ROOT, row["path"])
        got = sha(path) if path else "absent"
        check(got.startswith(row["sha256"]), f"{row['path']}: {got[:16]} is {row['sha256'][:16]} ({row['source']})")
    for row in table.get("rebuilds", []):
        operand = find(ROOT, row["operand"])
        got = sha(operand) if operand else "absent"
        check(got == row["sha256"], f"{row['operand']}: equals the image rebuilt at {row['head']} ({row['why']})")


# ------------------------------------------------------------------ 3a. bitstream
REGS = {0: "CRC", 1: "FAR", 2: "FDRI", 3: "FDRO", 4: "CMD", 5: "CTL0", 6: "MASK", 7: "STAT", 8: "LOUT", 9: "COR0",
        10: "MFWR", 11: "CBC", 12: "IDCODE", 13: "AXSS", 14: "COR1", 16: "WBSTAR", 17: "TIMER", 22: "BOOTSTS",
        24: "CTL1", 31: "BSPI"}
FRAME_WORDS = 101
NUL = bytes(1)
NAMES = {"a": "design name", "b": "part", "c": "date", "d": "time", "e": "payload length"}


def bit_header(data):
    """[(key, value offset, value)] of the .bit header, the payload offset and length."""
    pos = 2 + int.from_bytes(data[0:2], "big") + 2  # the 9-byte magic, then a length 1 that counts the key 'a'
    fields = []
    while chr(data[pos]) != "e":
        n = int.from_bytes(data[pos + 1:pos + 3], "big")
        fields.append((chr(data[pos]), pos + 3, data[pos + 3:pos + 3 + n]))
        pos += 3 + n
    fields.append(("e", pos + 1, data[pos + 1:pos + 5]))
    return fields, pos + 5, int.from_bytes(data[pos + 1:pos + 5], "big")


def bit_packets(data):
    """[(start, end, kind, register)] of the configuration packet stream after the sync word."""
    i = data.find(b"\xaa\x99\x55\x66") + 4
    regions, last = [], None
    while i + 4 <= len(data):
        w, = struct.unpack_from(">I", data, i)
        typ = w >> 29
        if typ == 1:
            reg, cnt = (w >> 13) & 0x3FFF, w & 0x7FF
            regions.append((i, i + 4, "packet header", REGS.get(reg, str(reg))))
            last = reg
            if cnt:
                regions.append((i + 4, i + 4 + 4 * cnt, "fdri" if reg == 2 else "register", REGS.get(reg, str(reg))))
            i += 4 + 4 * cnt
        elif typ == 2:
            cnt = w & 0x7FFFFFF
            regions.append((i, i + 4, "packet header", REGS.get(last, str(last))))
            regions.append((i + 4, i + 4 + 4 * cnt, "fdri" if last == 2 else "register", REGS.get(last, str(last))))
            i += 4 + 4 * cnt
        else:
            regions.append((i, i + 4, "word", f"0x{w:08x}"))
            i += 4
    return regions


def bitstream(shape, a_path, b_path):
    a, b = a_path.read_bytes(), b_path.read_bytes()
    ha, sa, la = bit_header(a)
    hb, sb, lb = bit_header(b)
    for name, fields in (("bench", ha), ("flip", hb)):
        shown = [k + "=" + (str(int.from_bytes(v, "big")) if k == "e" else v.rstrip(NUL).decode(errors="replace"))
                 for k, _, v in fields]
        print(f"     {name} header: " + "; ".join(shown))
    ra, rb = bit_packets(a), bit_packets(b)
    same = (len(a) == len(b) and [(k, o, len(v)) for k, o, v in ha] == [(k, o, len(v)) for k, o, v in hb]
            and (sa, la) == (sb, lb) and [r[:3] for r in ra] == [r[:3] for r in rb])
    if not check(same, f"{shape} .bit: same length, header field layout, payload and packet structure"):
        return None
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    groups, frames = {}, {}
    fdri = [(s, e) for s, e, k, _ in ra if k == "fdri"]
    for i in diff:
        label = None
        for key, off, val in ha:
            if off <= i < off + len(val):
                label = f"header '{key}' ({NAMES[key]})"
                if key == "a":
                    label += " " + val[:i - off + 1].decode(errors="replace").split(";")[-1].split("=")[0]
        if label is None:
            hit = next((r for r in ra if r[0] <= i < r[1]), None)
            if hit and hit[2] == "fdri":
                frame, word = divmod((i - hit[0]) // 4, FRAME_WORDS)
                frames.setdefault(frame, set()).add(word)
                continue
            label = f"payload {hit[2]} {hit[3]}" if hit else "beyond the packet stream"
        groups.setdefault(label, []).append(i)
    bits = 0
    lines = []
    for frame in sorted(frames):
        base = fdri[0][0] + 4 * FRAME_WORDS * frame
        n = sum(bin(struct.unpack_from(">I", a, base + 4 * w)[0] ^ struct.unpack_from(">I", b, base + 4 * w)[0])
                .count("1") for w in frames[frame])
        bits += n
        lines.append(f"frame {frame} words {sorted(frames[frame])} {n} bit(s)")
    print(f"     differing bytes: {len(diff)}")
    for label, offs in groups.items():
        print(f"       {len(offs):3d}  {label}: offsets {offs if len(offs) <= 8 else offs[:4] + ['...'] + offs[-2:]}")
    print(f"       {sum(len(f) for f in frames.values()):3d}  FDRI frame words, {len(frames)} of "
          f"{sum((e - s) // 4 for s, e in fdri) // FRAME_WORDS} frames, {bits} bit(s): " + "; ".join(lines))
    allowed = {"header 'a' (design name) SW_CRC", "header 'a' (design name) SW_HDR_SHA256", "header 'c' (date)",
               "header 'd' (time)", "payload register CRC"}
    check(set(groups) <= allowed, f"{shape} .bit: outside the frames, only the design name's SW_CRC and "
                                  f"SW_HDR_SHA256 text, the date, the time and the CRC register write differ "
                                  f"(unexpected: {sorted(set(groups) - allowed)})")
    header = sum(len(v) for k, v in groups.items() if k.startswith("header"))
    design = sum(len(v) for k, v in groups.items() if "design" in k)
    date, time = len(groups.get("header 'c' (date)", [])), len(groups.get("header 'd' (time)", []))
    crc = len(groups.get("payload register CRC", []))
    print(f"     header bytes {header} = design name {design} + date {date} + time {time}; "
          f"CRC register bytes {crc}; frame bits {bits}")
    return bits


# ------------------------------------------------------------------- 3b. ELF
def elf(path):
    b = read(path)
    assert b[:4] == b"\x7fELF" and b[4] == 1 and b[5] == 1, f"{path}: not ELF32 LE"
    shoff, = struct.unpack_from("<I", b, 0x20)
    shentsize, shnum, shstrndx = struct.unpack_from("<HHH", b, 0x2E)
    rows = [struct.unpack_from("<IIIIIIIIII", b, shoff + i * shentsize) for i in range(shnum)]
    strtab = rows[shstrndx]
    name = lambda off: b[strtab[4] + off:b.index(b"\0", strtab[4] + off)].decode()  # noqa: E731
    secs = [dict(name=name(r[0]), type=r[1], flags=r[2], addr=r[3], off=r[4], size=r[5], link=r[6],
                 data=b[r[4]:r[4] + r[5]] if r[1] != 8 else b"") for r in rows]
    syms = {}
    for st in (s for s in secs if s["type"] == 2):
        strs = secs[st["link"]]
        for i in range(st["size"] // 16):
            nm, val, size, info, _o, _x = struct.unpack_from("<IIIBBH", b, st["off"] + 16 * i)
            if info & 0xF in (1, 2) and size:
                syms[b[strs["off"] + nm:b.index(b"\0", strs["off"] + nm)].decode()] = (val, size)
    phoff, = struct.unpack_from("<I", b, 0x1C)
    phentsize, phnum = struct.unpack_from("<HH", b, 0x2A)
    loads = []
    for i in range(phnum):
        typ, off, _va, pa, filesz, _m, _f, _al = struct.unpack_from("<8I", b, phoff + i * phentsize)
        if typ == 1 and filesz:
            loads.append((pa, b[off:off + filesz]))
    loaded = [s for s in secs if s["flags"] & 2 and s["type"] != 8 and s["size"]]
    return dict(loaded=loaded, syms=syms, loads=loads)


def symbol_bytes(image, symbol):
    val, size = image["syms"][symbol]
    sec = next(s for s in image["loaded"] if s["addr"] <= val < s["addr"] + s["size"])
    return sec["data"][val - sec["addr"]:val - sec["addr"] + size]


def lui_addi(word_hi, word_lo):
    """The value a lui/addi pair loads, or None when the two words are not lui rd and a later addi rd, rd."""
    if word_hi & 0x7F != 0x37 or word_lo & 0x707F != 0x13:
        return None
    rd = (word_hi >> 7) & 0x1F
    if (word_lo >> 7) & 0x1F != rd or (word_lo >> 15) & 0x1F != rd:
        return None
    imm = word_lo >> 20
    imm -= (imm & 0x800) << 1
    return ((word_hi & 0xFFFFF000) + imm) & 0xFFFFFFFF


def elf_pair(label, a_path, b_path, aem=None):
    """Claim (3b)/(4) for one image pair; returns (differing bytes, values) or None."""
    a, b = elf(a_path), elf(b_path)
    layout = lambda x: [(s["name"], s["addr"], s["size"]) for s in x["loaded"]]  # noqa: E731
    if not check(layout(a) == layout(b), f"{label}: the same loaded sections at the same addresses and sizes"):
        return None
    words, rodata = [], []
    total = 0
    for sa, sb in zip(a["loaded"], b["loaded"]):
        diff = [i for i in range(sa["size"]) if sa["data"][i] != sb["data"][i]]
        total += len(diff)
        if sa["flags"] & 4:  # executable: the differing aligned words
            words += sorted({sa["addr"] + i - (sa["addr"] + i) % 4 for i in diff})
        else:
            rodata += [sa["addr"] + i for i in diff]
    word = lambda x, addr: struct.unpack_from(  # noqa: E731
        "<I", next(s for s in x["loaded"] if s["addr"] <= addr < s["addr"] + s["size"])["data"],
        addr - next(s for s in x["loaded"] if s["addr"] <= addr < s["addr"] + s["size"])["addr"])[0]
    img_a, img_b = symbol_bytes(a, "aecp_entity_image"), symbol_bytes(b, "aecp_entity_image")
    base = a["syms"]["aecp_entity_image"][0]
    crc_a, crc_b = binascii.crc32(img_a), binascii.crc32(img_b)
    pair_ok = (len(words) == 2
               and lui_addi(word(a, words[0]), word(a, words[1])) == crc_a
               and lui_addi(word(b, words[0]), word(b, words[1])) == crc_b)
    off = [r - base for r in rodata]
    byte_ok = (len(rodata) == 1 and 0 <= off[0] < len(img_a) and img_a[off[0]:off[0] + 1] == b"2"
               and img_b[off[0]:off[0] + 1] == b"3")
    check(pair_ok and byte_ok,
          f"{label}: {total} loaded bytes differ: the lui/addi pair at "
          f"{', '.join(hex(w) for w in words)} loads crc32(aecp_entity_image) {crc_a:08x} -> {crc_b:08x}, and "
          f"aecp_entity_image+{', '.join(hex(o) for o in off)} reads '2' -> '3'")
    whole_a, whole_b = read(a_path), read(b_path)
    whole = sum(1 for i in range(min(len(whole_a), len(whole_b))) if whole_a[i] != whole_b[i])
    check(len(whole_a) == len(whole_b) and whole == total,
          f"{label}: the whole files ({len(whole_a)} B) differ in those {whole} bytes only (symbols, debug and "
          f"headers equal)")
    if aem is not None:
        check(img_a == read(aem[0]) and img_b == read(aem[1]),
              f"{label}: aecp_entity_image is byte for byte the export's aem_desc.bin, both sides")
    return a, b, words, rodata


# ------------------------------------------------------------------ 3c. ROM
def rom(gateware):
    data = b""
    for k in range(16):
        path = find(gateware, f"alinx_ax7101_rom_bank{k}.init")
        if path is None:
            break
        data += b"".join(struct.pack("<I", int(w, 16)) for w in read(path).split())
    return data, k


def rom_check(shape, side, gateware, image):
    data, banks = rom(gateware)
    match = all(data[pa:pa + len(seg)] == seg for pa, seg in image["loads"])
    end = max(pa + len(seg) for pa, seg in image["loads"])
    check(match and not any(data[end:]), f"{shape} {side}: the {banks} ROM bank init files ({len(data)} B) are the "
                                         f"ELF's load segments {[(hex(pa), len(s)) for pa, s in image['loads']]}, "
                                         f"zero beyond")


# ------------------------------------------------------------------ 3d. export files
def export_files(shape, bench, flip):
    for name in ("aem_desc.bin", "aem_desc.json", "aem_desc.map", "csr.csv", "csr.json", "flashboot_layout.json",
                 "image_manifest.json", "gateware/alinx_ax7101_mem.init"):
        pa, pb = find(bench, name), find(flip, name)
        if pa is None or pb is None:
            check(False, f"{shape} {name}: present on both sides")
            continue
        a, b = read(pa), read(pb)
        if a == b:
            print(f"     {name}: equal")
            continue
        if name.endswith(".bin"):
            diff = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
            check(len(a) == len(b) and len(diff) == 1 and a[diff[0]:diff[0] + 1] == b"2"
                  and b[diff[0]:diff[0] + 1] == b"3",
                  f"{shape} {name}: {len(a)} B each, {len(diff)} byte differs, at {[hex(i) for i in diff]}: '2' -> '3'")
            continue
        la, lb = a.decode().splitlines(), b.decode().splitlines()
        rows = [(x, y) for x, y in zip(la, lb) if x != y]
        print(f"     {name}: {len(rows)} line(s) differ" + (" (line counts differ)" if len(la) != len(lb) else ""))
        for x, y in rows:
            print(f"       - {x.strip()[:150]}\n       + {y.strip()[:150]}")


# ------------------------------------------------------------------ 3e. dumps
def init_bits(rows_a, rows_b):
    total, cells = 0, []
    for name in sorted(set(rows_a) & set(rows_b)):
        pa, pb = rows_a[name][2], rows_b[name][2]
        diffs = []
        for k in sorted(set(pa) | set(pb)):
            if pa.get(k) != pb.get(k):
                va, vb = int(pa[k].split("'h")[1], 16), int(pb[k].split("'h")[1], 16)
                diffs.append((k, bin(va ^ vb).count("1")))
        if diffs:
            n = sum(d[1] for d in diffs)
            total += n
            cells.append((name, rows_a[name][0], n, diffs))
    return total, cells


def dump_rows(path, with_bel):
    rows = {}
    for line in read(path).decode().splitlines():
        parts = line.split()
        if with_bel:  # name REF LOC BEL INIT...: LOC/BEL may be empty for cells with none, so find the first INIT
            k = next((i for i, p in enumerate(parts) if "=" in p), len(parts))
            rows[parts[0]] = (parts[1], tuple(parts[2:k]), dict(p.split("=", 1) for p in parts[k:]))
        else:
            rows[parts[0]] = (parts[1], (parts[2],), dict(p.split("=", 1) for p in parts[3:]))
    return rows


def dumps(shape, base, frame_bits):
    """(3e): the full cell and net dumps, required for both checkpoints, and the block RAM dump where it was made
    (the cell dump already holds every block RAM's INIT properties)."""
    for kind in ("cells", "bram"):
        pa, pb = find(base, f"bench.{kind}"), find(base, f"flip.{kind}")
        if kind == "bram" and pa is None and pb is None:
            print(f"     {shape} bram: not dumped separately (the cells dump holds every block RAM's INIT)")
            continue
        if not check(pa is not None and pb is not None, f"{shape} {kind} dump: present for both checkpoints"):
            continue
        a, b = dump_rows(pa, kind == "cells"), dump_rows(pb, kind == "cells")
        same_cells = set(a) == set(b) and all(a[n][:2] == b[n][:2] for n in a)
        check(same_cells, f"{shape} {kind}: {len(a)} cells, every name, type and placement equal")
        bits, cells = init_bits(a, b)
        for name, ref, n, diffs in cells:
            print(f"       {name} {ref}: {n} bit(s) in {', '.join(f'{k} ({c})' for k, c in diffs)}")
        roms = all(("rom_bank" in name) or ("/csr/" in name) for name, *_ in cells)
        check(bits == frame_bits and roms, f"{shape} {kind}: {bits} INIT bit(s) differ in {len(cells)} cell(s), "
                                           f"the frame bits {frame_bits}; each a ROM bank or the CSR defaults ROM")
    na, nb = find(base, "bench.nets"), find(base, "flip.nets")
    if check(na is not None and nb is not None, f"{shape} nets dump: present for both checkpoints"):
        a, b = read(na), read(nb)
        check(a == b, f"{shape} nets: {len(a.splitlines())} nets, every route byte-identical")
    for side in ("bench", "flip"):
        s = find(base, f"{side}.summary")
        if s is not None:
            lines = read(s).decode().splitlines()
            keep = [lines[0]] + [" ".join(x.replace(".", "").split()) for x in lines
                                 if "fully routed" in x or "routing errors" in x]
            print(f"     {side}.summary: " + "; ".join(keep))


def shipping():
    for shape in ("1x1", "8x8"):
        print(f"== 3. shipping {shape}/1if: bench against flip")
        base = ROOT / "shipping" / shape
        try:
            bits = bitstream(shape, operand(base, "bench/alinx_ax7101.bit"), operand(base, "flip/alinx_ax7101.bit"))
            pair = elf_pair(f"{shape} ctrl_app.elf", operand(base / "bench", "ctrl_app.elf"),
                            operand(base / "flip", "ctrl_app.elf"),
                            aem=(operand(base, "bench/aem_desc.bin"), operand(base, "flip/aem_desc.bin")))
            if pair:
                rom_check(shape, "bench", base / "bench/gateware", pair[0])
                rom_check(shape, "flip", base / "flip/gateware", pair[1])
            export_files(shape, base / "bench", base / "flip")
            if bits is not None:
                dumps(shape, base / "dump", bits)
        except Absent as absent:
            refused(f"{shape} shipping", absent)


# ------------------------------------------------------------------ 4. harness
def harness():
    print("== 4. CPU-budget harness images: measured against this head's")
    n = 0
    for arm in sorted(p for p in (ROOT / "harness").glob("*/*") if p.is_dir()):
        label = f"{arm.parent.name}/{arm.name}"
        try:
            n += bool(elf_pair(label, operand(arm, "measured.elf"), operand(arm, "head.elf")))
            check(read(operand(arm, "measured.parts.json")) == read(operand(arm, "head.parts.json")),
                  f"{label}: the same group partition (parts.json)")
        except Absent as absent:
            refused(label, absent)
    check(n == 16, f"{n} of 16 arm images compared")


# ------------------------------------------------------------------ 5. groups
def leaves(node, path=""):
    if isinstance(node, dict):
        for k in sorted(node):
            yield from leaves(node[k], f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, f"{path}[{i}]")
    else:
        yield path, node


def version_strings(point, arm):
    """(measured, head) ENTITY firmware_version strings of an arm: in its two images' aecp_entity_image, the
    NUL-delimited string holding their one differing byte; None when the images differ elsewhere too."""
    base = ROOT / "harness" / point / arm
    ia = symbol_bytes(elf(operand(base, "measured.elf")), "aecp_entity_image")
    ib = symbol_bytes(elf(operand(base, "head.elf")), "aecp_entity_image")
    diff = [i for i in range(min(len(ia), len(ib))) if ia[i] != ib[i]]
    if len(ia) != len(ib) or len(diff) != 1:
        return None
    start, end = ia.rfind(NUL, 0, diff[0]) + 1, ia.index(NUL, diff[0])
    return ia[start:end], ib[start:end]


def inside(bx, by, old, new):
    """Whether bx and by differ, and only at bytes inside an occurrence of old in bx that reads new in by."""
    if len(bx) != len(by) or len(old) != len(new):
        return False
    diff = [i for i in range(len(bx)) if bx[i] != by[i]]
    spans = [k for k in range(len(bx) - len(old) + 1) if bx[k:k + len(old)] == old and by[k:k + len(new)] == new]
    return bool(diff) and all(any(k <= d < k + len(old) for k in spans) for d in diff)


def words(tokens):
    """A PASS line's W list, (time, address, value) per word, or None when a token is not one."""
    out = []
    for token in tokens:
        parts = token.split(":")
        if len(parts) != 3:
            return None
        try:
            out.append((parts[0], parts[1], int(parts[2], 16)))
        except ValueError:
            return None
    return out


def anchored(x, y, old, new):
    """Whether one raw-log line pair differs only inside the firmware_version string (module docstring, 5)."""
    tx, ty = x.split(), y.split()
    if len(tx) != len(ty) or not tx or tx[0] != ty[0]:
        return False
    if tx[0] == "WIRE":
        try:
            return tx[:-1] == ty[:-1] and inside(bytes.fromhex(tx[-1]), bytes.fromhex(ty[-1]), old, new)
        except ValueError:
            return False
    if tx[0] == "PASS" and "W" in tx:
        k = tx.index("W")
        wx, wy = words(tx[k + 1:]), words(ty[k + 1:])
        if tx[:k + 1] != ty[:k + 1] or wx is None or wy is None or [w[:2] for w in wx] != [w[:2] for w in wy]:
            return False
        stream = lambda ws: b"".join(struct.pack("<I", v & 0xFFFFFFFF) for _t, _a, v in ws)  # noqa: E731
        return inside(stream(wx), stream(wy), old, new)
    return False


def groups():
    print("== 5. the 13 re-measured groups: measured against this head's")
    n = 0
    for result in sorted((ROOT / "groups").glob("*/*/*.measured.json")):
        label = f"{result.parent.parent.name}/{result.parent.name}/{result.name[:-len('.measured.json')]}"
        try:
            n += group(result, label)
        except Absent as absent:
            refused(label, absent)
    check(n == 13, f"{n} of 13 groups compared")


def group(result, label):
    """One group's JSON leaves and raw logs (module docstring, 5)."""
    mine = operand(result.parent, result.name.replace(".measured.json", ".head.json"))
    versions = version_strings(result.parent.parent.name, result.parent.name)
    a, b = dict(leaves(json.loads(read(result)))), dict(leaves(json.loads(read(mine))))
    diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    probes = len(json.loads(read(mine)).get("probes", []))
    check(set(a) == set(b) and not diff, f"{label}: {len(a)} leaves, {probes} probes, every leaf equal, none "
                                         f"excluded" + (f"; DIFFER {diff[:4]}" if diff else ""))
    la = read(operand(result.parent, result.name.replace(".measured.json", ".measured.log"))).decode().splitlines()
    lb = read(operand(result.parent, result.name.replace(".measured.json", ".head.log"))).decode().splitlines()
    rows = [(i, x, y) for i, (x, y) in enumerate(zip(la, lb)) if x != y]
    loose = [i for i, x, y in rows if versions is None or not anchored(x, y, *versions)]
    subs = [(i, x.split()[0] if x.split() else "", x[max(0, j - 12):j + 13], y[max(0, j - 12):j + 13])
            for i, x, y in rows for j in range(min(len(x), len(y))) if x[j] != y[j]]
    shown = "?" if versions is None else " -> ".join(v.decode(errors="replace") for v in versions)
    check(len(la) == len(lb) and not loose,
          f"{label}: raw log {len(la)} lines, {len(rows)} differ, each only inside the ENTITY firmware_version "
          f"string ({shown})" + (f"; NOT ANCHORED: lines {[i + 1 for i in loose][:5]}" if loose else "")
          + ("" if len(la) == len(lb) else f"; line counts {len(la)} and {len(lb)}"))
    for i, kind, x, y in subs[:12]:
        print(f"       line {i + 1} {kind}: ...{x}... -> ...{y}...")
    return 1


manifest()
binding()
shipping()
harness()
groups()
print(f"== RESULT: {'ALL CLAIMS HOLD' if not FAILS else f'{len(FAILS)} FAILED'}")
sys.exit(1 if FAILS else 0)
