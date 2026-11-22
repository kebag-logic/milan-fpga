#!/usr/bin/env python3
"""Reviewer-owned, independent re-derivation of the #665 flip image-identity carry.

Written without reusing the author's replay driver. Standard library only. Usage:

    python3 -I r879_identity.py <identity-packet-dir>

It reads the published operands (shipping .bit pairs, platform ELFs, ROM bank inits, export files, routed-checkpoint
dumps, the 16 harness image pairs, the 13 groups' results and raw logs) and prints every difference it finds, then a
verdict line per claim.  Exit 0 only if every claim holds on the operands present; operands listed in the packet's
MANIFEST.sha256 but absent are reported as NOT REPLAYABLE (exit 3), never silently skipped.
"""
import gzip
import hashlib
import json
import lzma
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
FAILS, ABSENT = [], []


def say(ok, text):
    print(("  ok    " if ok else "  FAIL  ") + text)
    if not ok:
        FAILS.append(text)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------- manifest
print("== manifest")
listed = {}
for line in (ROOT / "MANIFEST.sha256").read_text().splitlines():
    digest, name = line.split(None, 1)
    listed[name.lstrip("*").lstrip("./")] = digest
present = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()} - {"MANIFEST.sha256"}
ABSENT = sorted(n for n in listed if n not in present)
bad = sorted(n for n in listed if n in present and sha(ROOT / n) != listed[n])
unlisted = sorted(n for n in present if n not in listed)
print(f"     listed {len(listed)}, present {len(present)}, absent {len(ABSENT)}, mismatched {len(bad)}, "
      f"unlisted {len(unlisted)}")
for n in ABSENT:
    print(f"     ABSENT (listed, not published): {n}")
say(not bad, f"every present listed file hashes as listed {bad}")

# ---------------------------------------------------------------- published identities
print("== published identities (bench re-check comment and round-1 REVIEW READY)")
PUBLISHED = {"shipping/1x1/bench/alinx_ax7101.bit": "c7189218", "shipping/1x1/bench/ctrl_app.elf": "c873a0aa",
             "shipping/8x8/bench/alinx_ax7101.bit": "7d903412", "shipping/8x8/bench/ctrl_app.elf": "d67fd049",
             "shipping/1x1/flip/alinx_ax7101.bit": "68e5308b", "shipping/8x8/flip/alinx_ax7101.bit": "6a1ff1ef"}
for name, prefix in PUBLISHED.items():
    say(sha(ROOT / name).startswith(prefix), f"{name} sha256 starts {prefix}")


# ---------------------------------------------------------------- .bit
def bit_parse(data):
    """Xilinx .bit: <u16 len><9 B><u16 1> then keyed fields a..d (u16 len), e (u32 len) payload."""
    pos = 2 + struct.unpack(">H", data[:2])[0]
    pos += 2  # the 0x0001 that precedes 'a'
    fields = {}
    while True:
        key = chr(data[pos]); pos += 1
        if key == "e":
            n = struct.unpack(">I", data[pos:pos + 4])[0]; pos += 4
            fields["e"] = (pos, pos + n)
            assert pos + n == len(data), "payload length does not end the file"
            return fields
        n = struct.unpack(">H", data[pos:pos + 2])[0]; pos += 2
        fields[key] = (pos, pos + n)
        pos += n


def bit_words(data, start):
    """Classify each payload word index: ('fdri', frame) or ('reg', name) or ('other',)."""
    sync = data.index(b"\xaa\x99\x55\x66", start)
    kinds = {}
    i = sync + 4
    last_reg = None
    end = len(data)
    regs = {0: "CRC", 1: "FAR", 2: "FDRI", 4: "CMD", 5: "CTL0", 6: "MASK", 8: "LOUT", 9: "COR0", 0xC: "IDCODE",
            0xE: "COR1", 0x10: "WBSTAR", 0x18: "CTL1"}
    while i + 4 <= end:
        w = struct.unpack(">I", data[i:i + 4])[0]
        kinds[i] = ("hdr",)
        typ = w >> 29
        if typ == 1:
            op, reg, cnt = (w >> 27) & 3, (w >> 13) & 0x3FFF, w & 0x7FF
            last_reg = reg
            for k in range(cnt):
                kinds[i + 4 + 4 * k] = ("reg", regs.get(reg, hex(reg)), op)
            if reg == 2 and cnt:
                for k in range(cnt):
                    kinds[i + 4 + 4 * k] = ("fdri", k // 101)
            i += 4 + 4 * cnt
        elif typ == 2:
            cnt = w & 0x7FFFFFF
            for k in range(cnt):
                kinds[i + 4 + 4 * k] = ("fdri", k // 101) if last_reg == 2 else ("reg2", last_reg)
            i += 4 + 4 * cnt
        else:
            i += 4
    return kinds


def bit_pair(shape):
    print(f"== .bit {shape}: bench against flip")
    a = (ROOT / f"shipping/{shape}/bench/alinx_ax7101.bit").read_bytes()
    b = (ROOT / f"shipping/{shape}/flip/alinx_ax7101.bit").read_bytes()
    say(len(a) == len(b), f"{shape} same length {len(a)}")
    fa, fb = bit_parse(a), bit_parse(b)
    say({k: v[1] - v[0] for k, v in fa.items()} == {k: v[1] - v[0] for k, v in fb.items()},
        f"{shape} same header field lengths")
    for k in "abcd":
        if a[slice(*fa[k])] != b[slice(*fb[k])]:
            print(f"     header {k}: {a[slice(*fa[k])]!r}\n            -> {b[slice(*fb[k])]!r}")
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    cls = {}
    ka, kb = bit_words(a, fa["e"][0]), bit_words(b, fb["e"][0])
    say(ka == kb, f"{shape} identical packet structure ({len(ka)} words classified)")
    frames, fbits, other = {}, 0, []
    for i in diff:
        key = next((k for k, (s, e) in fa.items() if s <= i < e), "pre")
        if key in "abcd":
            # inside 'a', name the sub-field the byte belongs to
            if key == "a":
                text = a[slice(*fa["a"])].decode("ascii", "replace")
                rel = i - fa["a"][0]
                sub = next((f for f in ("SW_CRC=", "SW_HDR_SHA256=") if text.find(f) <= rel <
                            text.find(f) + len(f) + (8 if f == "SW_CRC=" else 64)), "other-a")
                tag = f"a:{sub.rstrip('=')}"
            else:
                tag = key
            cls[tag] = cls.get(tag, 0) + 1
            if tag not in ("a:SW_CRC", "a:SW_HDR_SHA256", "c", "d"):
                other.append(i)
            continue
        if key != "e":
            other.append(i); continue
        wstart = fa["e"][0] + ((i - fa["e"][0]) // 4) * 4
        sync = a.index(b"\xaa\x99\x55\x66", fa["e"][0])
        wstart = sync + ((i - sync) // 4) * 4
        kind = ka.get(wstart, ("unclassified",))
        if kind[0] == "fdri":
            frames.setdefault(kind[1], 0)
            frames[kind[1]] += bin(a[i] ^ b[i]).count("1")
            fbits += bin(a[i] ^ b[i]).count("1")
            cls["fdri-bytes"] = cls.get("fdri-bytes", 0) + 1
        elif kind[0] == "reg" and kind[1] == "CRC":
            cls["CRC-reg"] = cls.get("CRC-reg", 0) + 1
        else:
            other.append(i)
            cls[str(kind)] = cls.get(str(kind), 0) + 1
    print(f"     differing bytes {len(diff)}: {cls}")
    print(f"     frame bits {fbits} in {len(frames)} frames: {dict(sorted(frames.items()))}")
    say(not other, f"{shape} every differing byte is header a/c/d text, the CRC register write or FDRI frame data "
                   f"(other: {other[:8]})")
    return len(diff), cls, fbits


# ---------------------------------------------------------------- ELF
def elf_info(data):
    assert data[:4] == b"\x7fELF" and data[4] == 1 and data[5] == 1, "ELF32 little-endian expected"
    e_phoff, e_shoff = struct.unpack_from("<II", data, 28)
    e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx = struct.unpack_from("<HHHHH", data, 42)
    phdrs = [struct.unpack_from("<IIIIIIII", data, e_phoff + k * e_phentsize) for k in range(e_phnum)]
    shdrs = [struct.unpack_from("<IIIIIIIIII", data, e_shoff + k * e_shentsize) for k in range(e_shnum)]
    syms = {}
    for sh in shdrs:
        if sh[1] == 2:  # SYMTAB
            strtab = shdrs[sh[6]]
            for k in range(sh[5] // 16):
                name, value, size, info, other, shndx = struct.unpack_from("<IIIBBH", data, sh[4] + 16 * k)
                end = data.index(b"\0", strtab[4] + name)
                syms[data[strtab[4] + name:end].decode()] = (value, size)
    loads = [(p[1], p[2], p[4]) for p in phdrs if p[0] == 1]  # (offset, vaddr, filesz)
    return loads, syms


def off_to_addr(loads, off):
    for o, v, n in loads:
        if o <= off < o + n:
            return v + off - o
    return None


def addr_to_off(loads, addr):
    for o, v, n in loads:
        if v <= addr < v + n:
            return o + addr - v
    return None


def lui_addi_value(lui, addi):
    hi = lui & 0xFFFFF000
    imm = (addi >> 20) & 0xFFF
    imm = imm - 0x1000 if imm & 0x800 else imm
    return (hi + imm) & 0xFFFFFFFF


def elf_pair(label, pa, pb, aem_a=None, aem_b=None):
    a, b = pa.read_bytes(), pb.read_bytes()
    la, sa = elf_info(a)
    lb, sb = elf_info(b)
    say(len(a) == len(b) and la == lb, f"{label}: same size {len(a)} and load segments")
    say(set(sa) == set(sb) and all(sa[k] == sb[k] for k in sa), f"{label}: symbol tables equal ({len(sa)} symbols)")
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    img, isz = sa["aecp_entity_image"]
    ioff = addr_to_off(la, img)
    bits = sum(bin(a[i] ^ b[i]).count("1") for i in diff)
    unloaded = [i for i in diff if off_to_addr(la, i) is None]
    in_img = [i - ioff for i in diff if ioff <= i < ioff + isz]
    code = sorted({(i - (off_to_addr(la, i) % 4)) for i in diff if not (ioff <= i < ioff + isz)})
    crc_a = zlib.crc32(a[ioff:ioff + isz]); crc_b = zlib.crc32(b[ioff:ioff + isz])
    words = [(off_to_addr(la, o), struct.unpack_from("<I", a, o)[0], struct.unpack_from("<I", b, o)[0]) for o in code]
    # find the lui/addi pair: a lui (opcode 0x37) and an addi (0x13) whose combination changed
    luis = [w for w in words if w[1] & 0x7F == 0x37]
    addis = [w for w in words if w[1] & 0x7F == 0x13]
    pair_ok = len(luis) <= 1 and len(addis) <= 1 and len(words) == len(luis) + len(addis) and words
    if pair_ok:
        lu = luis[0] if luis else None
        ad = addis[0]
        # an unchanged lui is legal (only the low part changed); then find it by register
        if lu is None:
            pair_ok = False
        else:
            va, vb = lui_addi_value(lu[1], ad[1]), lui_addi_value(lu[2], ad[2])
            pair_ok = (va, vb) == (crc_a, crc_b)
    ctx_a = a[ioff + 0x180:ioff + 0x190]; ctx_b = b[ioff + 0x180:ioff + 0x190]
    say(not unloaded, f"{label}: all {len(diff)} differing bytes are loaded")
    say(in_img == [0x184] and a[ioff + 0x184:ioff + 0x185] == b"2" and b[ioff + 0x184:ioff + 0x185] == b"3",
        f"{label}: in aecp_entity_image only +0x184 '2'->'3' (context {ctx_a!r} -> {ctx_b!r})")
    say(bool(pair_ok), f"{label}: the other differing bytes are one lui/addi pair at "
        f"{[hex(w[0]) for w in words]} loading zlib.crc32(aecp_entity_image) {crc_a:08x} -> {crc_b:08x}")
    if aem_a is not None:
        say(a[ioff:ioff + isz] == aem_a.read_bytes() and b[ioff:ioff + isz] == aem_b.read_bytes(),
            f"{label}: aecp_entity_image equals the export's aem_desc.bin on both sides ({isz} B)")
    return len(diff), bits, (crc_a, crc_b)


# ---------------------------------------------------------------- ROM bank inits
def rom_bits(shape):
    tot, per = 0, {}
    ga, gb = ROOT / f"shipping/{shape}/bench/gateware", ROOT / f"shipping/{shape}/flip/gateware"
    for f in sorted(ga.glob("*rom_bank*.init")):
        wa = f.read_text().split(); wb = (gb / f.name).read_text().split()
        assert len(wa) == len(wb)
        n = sum(bin(int(x, 16) ^ int(y, 16)).count("1") for x, y in zip(wa, wb))
        if n:
            per[f.name] = n
        tot += n
    others = sorted(set(p.name for p in ga.iterdir()) ^ set(p.name for p in gb.iterdir()))
    eq_other = all((ga / p.name).read_bytes() == (gb / p.name).read_bytes() for p in ga.iterdir()
                   if "rom_bank" not in p.name)
    say(not others and eq_other, f"{shape}: the non-ROM gateware init files are equal")
    return tot, per


def export_files(shape):
    ba, fl = ROOT / f"shipping/{shape}/bench", ROOT / f"shipping/{shape}/flip"
    for f in sorted(p for p in ba.iterdir() if p.is_file() and p.suffix not in (".bit", ".elf", ".bin")):
        la, lb = f.read_text().splitlines(), (fl / f.name).read_text().splitlines()
        d = [(x, y) for x, y in zip(la, lb) if x != y]
        if len(la) != len(lb):
            d.append(("<length>", f"{len(la)} vs {len(lb)}"))
        for x, y in d:
            print(f"     {shape} {f.name}: - {x.strip()[:110]}\n     {' ' * len(shape)} {' ' * len(f.name)}  + {y.strip()[:110]}")


def dumps(shape, kind):
    pa, pb = ROOT / f"shipping/{shape}/dump/bench.{kind}.xz", ROOT / f"shipping/{shape}/dump/flip.{kind}.xz"
    if not (pa.is_file() and pb.is_file()):
        print(f"     {shape} {kind} dump: NOT REPLAYABLE (not published)")
        return None
    la = lzma.decompress(pa.read_bytes()).decode().splitlines()
    lb = lzma.decompress(pb.read_bytes()).decode().splitlines()
    if kind == "nets":
        say(la == lb, f"{shape} nets dump: {len(la)} lines, equal")
        return 0
    say(len(la) == len(lb), f"{shape} {kind} dump: {len(la)} lines each")
    bits, cells = 0, []
    for x, y in zip(la, lb):
        if x == y:
            continue
        xa, ya = x.split(), y.split()
        same_place = [t for t in xa if "=" not in t] == [t for t in ya if "=" not in t]
        props_a = dict(t.split("=", 1) for t in xa if "=" in t)
        props_b = dict(t.split("=", 1) for t in ya if "=" in t)
        only_init = same_place and set(props_a) == set(props_b) and all(
            k.startswith("INIT") for k in props_a if props_a[k] != props_b[k])
        say(only_init, f"{shape} {kind}: {xa[0]} {xa[1]} differs only in INIT* properties")
        for k in props_a:
            if props_a[k] != props_b[k]:
                va = int(props_a[k].split("h")[-1], 16); vb = int(props_b[k].split("h")[-1], 16)
                n = bin(va ^ vb).count("1")
                bits += n
                cells.append((xa[0], k, n))
    print(f"     {shape} {kind}: {bits} INIT bits in {len({c[0] for c in cells})} cells: {cells}")
    return bits


def flatten(obj, path=""):
    if isinstance(obj, dict):
        for k in sorted(obj):
            yield from flatten(obj[k], f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f"{path}[{i}]")
    else:
        yield path, obj


# ---------------------------------------------------------------- run
summary = {}
for shape in ("1x1", "8x8"):
    nbytes, cls, fbits = bit_pair(shape)
    print(f"== platform ELF {shape}")
    s = f"shipping/{shape}"
    ndiff, ebits, crcs = elf_pair(f"{shape} ctrl_app.elf", ROOT / s / "bench/ctrl_app.elf", ROOT / s / "flip/ctrl_app.elf",
                                  ROOT / s / "bench/aem_desc.bin", ROOT / s / "flip/aem_desc.bin")
    rbits, per = rom_bits(shape)
    print(f"     {shape}: ELF differing bits {ebits}; ROM bank init differing bits {rbits} {per}")
    say(rbits == ebits, f"{shape}: the ROM bank inits differ in exactly the ELF's differing bits")
    say(fbits == ebits + 1, f"{shape}: frame bits {fbits} = platform-image bits {ebits} + 1 (VERSION bit 16, "
                            "0x0002_0060 -> 0x0003_0060)")
    aem = (ROOT / s / "bench/aem_desc.bin").read_bytes(), (ROOT / s / "flip/aem_desc.bin").read_bytes()
    say((zlib.crc32(aem[0]), zlib.crc32(aem[1])) == crcs, f"{shape}: aem_desc.bin crc32 {crcs[0]:08x} -> {crcs[1]:08x}")
    export_files(shape)
    dumps(shape, "nets")
    cb = dumps(shape, "cells")
    if cb is not None:
        say(cb == fbits, f"{shape}: cells INIT bits {cb} = frame bits {fbits}")
    if (ROOT / s / "dump/bench.bram.xz").is_file():
        bb = dumps(shape, "bram")
        say(bb == fbits, f"{shape}: bram INIT bits {bb} = frame bits {fbits}")
    summary[shape] = {"bit_bytes": nbytes, "classes": cls, "frame_bits": fbits, "elf_bytes": ndiff, "elf_bits": ebits}

print("== harness: 16 measured/head image pairs")
pairs = sorted(p for p in (ROOT / "harness").glob("*/*") if p.is_dir())
for p in pairs:
    n, bits, _ = elf_pair(f"harness {p.parent.name}/{p.name}", p / "measured.elf", p / "head.elf")
    say(n == 6, f"harness {p.parent.name}/{p.name}: 6 bytes ({bits} bits)")
    say(json.loads((p / "measured.parts.json").read_text()) == json.loads((p / "head.parts.json").read_text()),
        f"harness {p.parent.name}/{p.name}: parts.json equal")
say(len(pairs) == 16, f"{len(pairs)} harness pairs")

print("== groups: measured against head")
ngroups = 0
for m in sorted((ROOT / "groups").rglob("*.measured.json")):
    h = m.with_name(m.name.replace(".measured.json", ".head.json"))
    ngroups += 1
    la, lb = list(flatten(json.loads(m.read_text()))), list(flatten(json.loads(h.read_text())))
    d = [(x, y) for x, y in zip(la, lb) if x != y]
    tag = f"{m.parent.parent.name}/{m.parent.name}/{m.name.split('.')[0]}"
    say(len(la) == len(lb) and not d, f"{tag}: {len(la)} JSON leaves equal {d[:3]}")
    lm, lh = m.with_name(m.name.replace(".json", ".log.gz")), h.with_name(h.name.replace(".json", ".log.gz"))
    if not (lm.is_file() and lh.is_file()):
        print(f"     {tag}: raw logs NOT REPLAYABLE (measured {lm.is_file()}, head {lh.is_file()})")
        continue
    xa = gzip.decompress(lm.read_bytes()).decode("utf-8", "replace").splitlines()
    xb = gzip.decompress(lh.read_bytes()).decode("utf-8", "replace").splitlines()
    dl = [(x, y) for x, y in zip(xa, xb) if x != y]
    pure = all(len(x) == len(y) and all(c == e or (c, e) == ("2", "3") for c, e in zip(x, y)) for x, y in dl)
    say(len(xa) == len(xb) and pure, f"{tag}: raw log {len(xa)} lines, {len(dl)} differ, each only by '2'->'3' digits")
    for x, y in dl[:4]:
        k = next(i for i, (c, e) in enumerate(zip(x, y)) if c != e)
        print(f"       ...{x[max(0, k - 50):k + 20]!r}\n       ...{y[max(0, k - 50):k + 20]!r}")
say(ngroups == 13, f"{ngroups} groups")

print("== summary", json.dumps(summary, sort_keys=True))
print(f"== absent listed operands: {len(ABSENT)}")
print(f"== RESULT: {'FAILS ' + str(len(FAILS)) if FAILS else 'ALL CHECKED CLAIMS HOLD'}"
      f"{'; NOT REPLAYABLE: ' + str(len(ABSENT)) + ' operand(s) absent' if ABSENT else ''}")
sys.exit(1 if FAILS else (3 if ABSENT else 0))
