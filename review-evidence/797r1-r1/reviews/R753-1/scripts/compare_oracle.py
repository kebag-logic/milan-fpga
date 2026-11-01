#!/usr/bin/env python3
"""Compare REGISTER_MAP.md field tables with the oracle's observations.
Usage: compare_oracle.py <page> <oracle_raw>. The page is parsed as text, without the generator."""
import re, sys
page, raw = sys.argv[1], sys.argv[2]
obs = {}
for ln in open(raw):
    m = re.match(r"([0-9a-f]{3}) r0=(\w+) r1=(\w+) base=(\w+) w1=(\w+) w0=(\w+) gbase=(\w+) g1=(\w+)", ln)
    if m:
        obs[int(m.group(1), 16)] = [int(x, 16) for x in m.groups()[1:]]
    else:
        print("ORACLE-NOTE", ln.strip())
regs = []
text = open(page, encoding="utf-8").read()
for m in re.finditer(r"^### (\S+) registers? \(offset (0x[0-9A-F]+)(?: to (0x[0-9A-F]+), stride (0x[0-9A-F]+))?\) \[reset = ([^\]]+)\]\n(.*?)(?=^#{2,3} )", text, re.M | re.S):
    name, lo, hi, stride, reset, body = m.groups()
    fields = []
    for r in re.finditer(r"^\| (\d+)(?::(\d+))? \| `([^`]+)` \| ([^`|\s]+) \| ([^|]*?) \|", body, re.M):
        h = int(r.group(1)); l = int(r.group(2)) if r.group(2) else h
        fields.append((h, l, r.group(3), r.group(4), r.group(5).strip()))
    lo = int(lo, 16); s = int(stride, 16) if stride else 4; hi2 = int(hi, 16) if hi else lo
    regs.append((name, lo, hi2, s, reset, fields))
print("registers parsed:", len(regs), "fields:", sum(len(r[5]) for r in regs))
covered = set()
problems = 0
def bit(v, n): return (v >> n) & 1
for name, lo, hi, s, reset, fields in regs:
    for a in range(lo, hi + 1, s):
        covered.add(a)
        o = obs[a]
        r0, r1, base, w1, w0, gb, g1 = o
        seen = {}
        for h, l, fname, acc, rst in fields:
            for n in range(l, h + 1):
                seen[n] = 1
        if len(seen) != 32:
            print(f"BITS {name}: table covers {len(seen)} bits")
        issues = []
        for h, l, fname, acc, rst in fields:
            # expected reset bits
            vals = None
            if rst not in ("X", "see table"):
                hexd = rst[:-1] if rst.endswith("h") else rst
                try:
                    vals = int(hexd.replace("X", "0"), 16)
                    xmask = int("".join("F" if c == "X" else "0" for c in hexd), 16)
                except ValueError:
                    vals, xmask = None, 0
            else:
                xmask = 0
            dep = 0; rv = 0; a1 = 0; a0 = 0
            width = h - l + 1
            field = lambda v: (v >> l) & ((1 << width) - 1)
            f0, f1, fw1, fw0, fg1 = field(r0), field(r1), field(w1), field(w0), field(g1)
            if rst == "X":
                if f0 == f1:
                    issues.append(f"[{h}:{l}] {fname} page reset X, but no input moves it: reads {f0:#x} from reset")
            elif rst == "see table":
                pass
            elif vals is not None:
                nonx = ~xmask & ((1 << width) - 1)
                if (f0 & nonx) != (vals & nonx):
                    issues.append(f"[{h}:{l}] {fname} page reset {rst}, RTL reads {f0:#x} with inputs low")
                if (f1 & nonx) != (vals & nonx):
                    issues.append(f"[{h}:{l}] {fname} page reset {rst}, RTL reads {f1:#x} with inputs high (page says not input-driven)")
            full = (1 << width) - 1
            if acc == "R/W":
                if not (fw1 == full and fw0 == 0):
                    issues.append(f"[{h}:{l}] {fname} page R/W: w1={fw1:#x} w0={fw0:#x}")
            elif acc in ("R",):
                if fw1 != field(base) or fw0 != field(base):
                    issues.append(f"[{h}:{l}] {fname} page R: base={field(base):#x} w1={fw1:#x} w0={fw0:#x}")
            elif acc in ("W", "W1S", "W1C"):
                if fw1 != 0 or fw0 != 0:
                    issues.append(f"[{h}:{l}] {fname} page {acc} (reads 0): w1={fw1:#x} w0={fw0:#x}")
        if issues:
            problems += len(issues)
            print(f"{a:#05x} {name}:")
            for i in issues:
                print("    " + i)
print("field findings:", problems)
holes = []
for a, o in sorted(obs.items()):
    if a in covered:
        continue
    if any(o[k] != 0 for k in range(7)):
        holes.append(f"{a:#05x} r0={o[0]:08x} r1={o[1]:08x} base={o[2]:08x} w1={o[3]:08x} w0={o[4]:08x} g1={o[6]:08x}")
print("undocumented addresses with a nonzero observation:", len(holes))
for h in holes:
    print("   ", h)
