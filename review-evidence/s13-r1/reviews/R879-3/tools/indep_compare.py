#!/usr/bin/env python3
"""Reviewer-owned comparison of the #665 flip identity operands, written without the packet's tools.

Usage: python3 -I indep_compare.py <identity-dir>

1. Routed dumps, both shapes: cells (name, REF_NAME, LOC, BEL, every property), nets (every ROUTE), 8x8 block RAM.
   Every differing property must be an INIT/INITP word; the differing bits are counted per cell.
2. The 13 re-measured groups: every JSON leaf (no exclusion) and every raw-log line. Each differing log line is
   reduced to its differing character runs, and those runs are printed and classified.
Exit 0 only if every difference is one the flip names (a ROM/CSR-defaults INIT bit; a firmware_version
'2' -> '3' at the string's major digit, as text or as its hex/word encoding).
"""
import gzip, json, lzma, re, sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(sys.argv[1])
BAD = []


def say(text):
    print(text, flush=True)


def lines_xz(path):
    return lzma.decompress(path.read_bytes()).decode().splitlines()


def cell_map(lines):
    out = {}
    for line in lines:
        toks = line.split(" ")
        name = toks[0]
        props = {}
        fixed = []
        for t in toks[1:]:
            if "=" in t and re.match(r"^[A-Z_0-9]+=", t):
                k, v = t.split("=", 1)
                props[k] = v
            else:
                fixed.append(t)
        if name in out:
            BAD.append(f"duplicate cell {name}")
        out[name] = (tuple(fixed), props)
    return out


def hexbits(v):
    m = re.match(r"^(\d+)'h([0-9A-Fa-f]+)$", v)
    return (int(m.group(1)), int(m.group(2), 16)) if m else None


def dumps(shape):
    d = ROOT / "shipping" / shape / "dump"
    say(f"== {shape}: routed dumps")
    a, b = cell_map(lines_xz(d / "bench.cells.xz")), cell_map(lines_xz(d / "flip.cells.xz"))
    say(f"   cells: bench {len(a)}, flip {len(b)}; names equal: {set(a) == set(b)}")
    if set(a) != set(b):
        BAD.append(f"{shape} cell name sets differ")
    fixed_diff = [n for n in a if n in b and a[n][0] != b[n][0]]
    say(f"   cells whose REF_NAME/LOC/BEL differ: {len(fixed_diff)}")
    BAD.extend(f"{shape} cell {n} placement/type differs" for n in fixed_diff)
    bits_total, cells_init = 0, []
    for n in sorted(a):
        if n not in b:
            continue
        pa, pb = a[n][1], b[n][1]
        if set(pa) != set(pb):
            BAD.append(f"{shape} cell {n} property names differ")
            continue
        nbits = 0
        for k in pa:
            if pa[k] == pb[k]:
                continue
            if not k.startswith("INIT"):
                BAD.append(f"{shape} cell {n} property {k} differs: {pa[k]} -> {pb[k]}")
                continue
            ha, hb = hexbits(pa[k]), hexbits(pb[k])
            if not ha or not hb or ha[0] != hb[0]:
                BAD.append(f"{shape} cell {n} {k} unparsable difference")
                continue
            nbits += bin(ha[1] ^ hb[1]).count("1")
        if nbits:
            bits_total += nbits
            cells_init.append((n, a[n][0][0], nbits))
    for n, ref, nb in cells_init:
        rom = n.startswith("rom_bank") or n == "milan_datapath/csr/sweep_cnt_reg_rep"
        say(f"     {n} {ref}: {nb} bit(s){'' if rom else '  <-- NOT a ROM bank / CSR defaults ROM'}")
        if not rom:
            BAD.append(f"{shape} INIT difference outside a ROM: {n}")
    say(f"   INIT bits differing: {bits_total} in {len(cells_init)} cell(s)")
    na, nb_ = lines_xz(d / "bench.nets.xz"), lines_xz(d / "flip.nets.xz")
    eq = na == nb_
    say(f"   nets: bench {len(na)} lines, flip {len(nb_)} lines; every line byte-identical: {eq}")
    if not eq:
        BAD.append(f"{shape} nets differ")
    if (d / "bench.bram.xz").exists():
        ba, bb = cell_map(lines_xz(d / "bench.bram.xz")), cell_map(lines_xz(d / "flip.bram.xz"))
        bits, cells = 0, 0
        for n in ba:
            if n not in bb or ba[n][0] != bb[n][0]:
                BAD.append(f"{shape} bram {n} name/placement differs")
                continue
            c = 0
            for k in ba[n][1]:
                if ba[n][1][k] != bb[n][1].get(k):
                    ha, hb = hexbits(ba[n][1][k]), hexbits(bb[n][1][k])
                    c += bin(ha[1] ^ hb[1]).count("1")
            if c:
                cells += 1
                bits += c
        say(f"   block RAM dump: {len(ba)} RAMs, names equal {set(ba) == set(bb)}; {bits} INIT bit(s) in {cells} RAM(s)")
    return bits_total


def leaves(obj, path=""):
    if isinstance(obj, dict):
        for k in sorted(obj):
            yield from leaves(obj[k], f"{path}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, f"{path}[{i}]")
    else:
        yield path, obj


VERSION_RUNS = {("2", "3")}


def classify(ra, rb):
    """Allowed: a bare '2' -> '3', or a hex digit/byte change whose decoding is '2' (0x32) -> '3' (0x33)."""
    if (ra, rb) in VERSION_RUNS:
        return "text 2->3"
    return None


def groups():
    gdir = ROOT / "groups"
    groups = sorted(p.parent / p.name[: -len(".head.json")] for p in gdir.glob("*/*/*.head.json"))
    say(f"== groups: {len(groups)}")
    if len(groups) != 13:
        BAD.append(f"{len(groups)} groups, not 13")
    for g in groups:
        ja = json.loads(Path(f"{g}.measured.json").read_text())
        jb = json.loads(Path(f"{g}.head.json").read_text())
        la, lb = list(leaves(ja)), list(leaves(jb))
        dl = [(p, v, w) for (p, v), (q, w) in zip(la, lb) if p != q or v != w]
        rel = g.relative_to(gdir)
        say(f"   {rel}: JSON {len(la)}/{len(lb)} leaves, {len(dl)} differ")
        for p, v, w in dl[:5]:
            say(f"       {p}: {v!r} -> {w!r}")
        if dl or len(la) != len(lb):
            BAD.append(f"{rel} JSON differs")
        a = gzip.decompress(Path(f"{g}.measured.log.gz").read_bytes()).decode(errors="replace").splitlines()
        b = gzip.decompress(Path(f"{g}.head.log.gz").read_bytes()).decode(errors="replace").splitlines()
        if len(a) != len(b):
            BAD.append(f"{rel} log line counts differ {len(a)} {len(b)}")
        diffs = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        say(f"   {rel}: log {len(a)}/{len(b)} lines, {len(diffs)} differ")
        for i, x, y in diffs:
            sm = SequenceMatcher(None, x, y, autojunk=False)
            runs = [(x[i1:i2], y[j1:j2], i1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
            kinds = []
            for ra, rb, at in runs:
                kind = classify(ra, rb)
                ctx = x[max(0, at - 24): at + 24]
                kinds.append(f"{ra!r}->{rb!r} @{at} [{kind or 'UNCLASSIFIED'}] ctx {ctx!r}")
                if not kind:
                    BAD.append(f"{rel} line {i + 1}: unclassified run {ra!r}->{rb!r}")
            say(f"       line {i + 1} ({x.split(':', 1)[0][:24]}): " + "; ".join(kinds))
        # The text-level classification above accepts any '2'->'3'; anchor it: the measured line must hold the
        # measured firmware_version at that offset, as text or as the hex bytes of its text.
        for i, x, y in diffs:
            ok = False
            for old, new in (("2.96.0", "3.96.0"), ("322e39362e30", "332e39362e30"), ("2e320000", "2e330000")):
                if old in x and x.replace(old, new) == y:
                    ok = True
            if not ok:
                hexa = x.lower()
                ok = hexa.replace("322e39362e30", "332e39362e30") == y.lower()
            say(f"       line {i + 1}: whole-line substitution of the firmware_version encoding reproduces head: {ok}")
            if not ok:
                BAD.append(f"{rel} line {i + 1}: not a firmware_version-only substitution")


def main():
    bits = {s: dumps(s) for s in ("1x1", "8x8")}
    groups()
    say("== RESULT: " + ("ALL DIFFERENCES NAMED" if not BAD else f"{len(BAD)} UNNAMED DIFFERENCE(S)"))
    for b in BAD:
        say(f"   BAD {b}")
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
