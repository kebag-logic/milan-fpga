#!/usr/bin/env python3
"""Reviewer check for #665 F3 round 5: execute the arithmetic helpers AS COMPILED FOR RV32I (from a linked ELF) on a
minimal RV32I interpreter that faults on any non-RV32I word, and compare every result with exact C semantics.
Usage: rv32i_exec.py ELF TOOLPREFIX [random_pairs]"""
import multiprocessing, random, struct, subprocess, sys

M32 = (1 << 32) - 1
M64 = (1 << 64) - 1
SENT = 0xFFFFFFF0


def load(elf):
    data = open(elf, "rb").read()
    assert data[:6] == b"\x7fELF\x01\x01"
    phoff = struct.unpack_from("<I", data, 28)[0]
    phentsize, phnum = struct.unpack_from("<HH", data, 42)
    mem = {}
    for i in range(phnum):
        p_type, off, vaddr, _, filesz, memsz, _, _ = struct.unpack_from("<8I", data, phoff + i * phentsize)
        if p_type == 1:
            for k in range(memsz):
                mem[vaddr + k] = data[off + k] if k < filesz else 0
    return mem


def sx(v, bits):
    v &= (1 << bits) - 1
    return v - (1 << bits) if v >> (bits - 1) else v


class Cpu:
    def __init__(self, mem):
        self.code = mem
        self.data = {}

    def rd(self, a, n):
        return sum(self.byte(a + i) << (8 * i) for i in range(n))

    def byte(self, a):
        if a in self.data:
            return self.data[a]
        return self.code.get(a, 0)

    def wr(self, a, v, n):
        for i in range(n):
            self.data[a + i] = (v >> (8 * i)) & 0xFF

    def call(self, pc, args, limit=200000):
        x = [0] * 32
        x[1] = SENT
        x[2] = 0x7FFF0000
        for i, a in enumerate(args):
            x[10 + i] = a & M32
        self.data = {}
        steps = 0
        while pc != SENT:
            steps += 1
            if steps > limit:
                raise RuntimeError("step limit")
            w = self.rd(pc, 4)
            op, rd, f3, rs1, rs2, f7 = w & 0x7F, (w >> 7) & 31, (w >> 12) & 7, (w >> 15) & 31, (w >> 20) & 31, w >> 25
            a, b = x[rs1], x[rs2]
            immi = sx(w >> 20, 12)
            npc = (pc + 4) & M32
            v = None
            if op == 0x37:
                v = w & 0xFFFFF000
            elif op == 0x17:
                v = (pc + (w & 0xFFFFF000)) & M32
            elif op == 0x6F:
                imm = sx(((w >> 31) << 20) | (((w >> 12) & 0xFF) << 12) | (((w >> 20) & 1) << 11) | (((w >> 21) & 0x3FF) << 1), 21)
                v = npc; npc = (pc + imm) & M32
            elif op == 0x67 and f3 == 0:
                v = npc; npc = (a + immi) & ~1 & M32
            elif op == 0x63:
                imm = sx(((w >> 31) << 12) | (((w >> 7) & 1) << 11) | (((w >> 25) & 0x3F) << 5) | (((w >> 8) & 0xF) << 1), 13)
                t = {0: a == b, 1: a != b, 4: sx(a, 32) < sx(b, 32), 5: sx(a, 32) >= sx(b, 32), 6: a < b, 7: a >= b}[f3]
                if t:
                    npc = (pc + imm) & M32
            elif op == 0x03:
                ad = (a + immi) & M32
                v = {0: lambda: sx(self.rd(ad, 1), 8) & M32, 1: lambda: sx(self.rd(ad, 2), 16) & M32,
                     2: lambda: self.rd(ad, 4), 4: lambda: self.rd(ad, 1), 5: lambda: self.rd(ad, 2)}[f3]()
            elif op == 0x23 and f3 in (0, 1, 2):
                ad = (a + sx((f7 << 5) | rd, 12)) & M32
                self.wr(ad, b, 1 << f3)
            elif op == 0x13:
                sh = rs2
                if f3 == 0: v = (a + immi) & M32
                elif f3 == 2: v = int(sx(a, 32) < immi)
                elif f3 == 3: v = int(a < (immi & M32))
                elif f3 == 4: v = (a ^ immi) & M32
                elif f3 == 6: v = (a | immi) & M32
                elif f3 == 7: v = (a & immi) & M32
                elif f3 == 1 and f7 == 0: v = (a << sh) & M32
                elif f3 == 5 and f7 == 0: v = a >> sh
                elif f3 == 5 and f7 == 0x20: v = (sx(a, 32) >> sh) & M32
                else: raise RuntimeError(f"non-RV32I OP-IMM {w:#010x} at {pc:#x}")
            elif op == 0x33 and f7 in (0, 0x20):
                s = b & 31
                key = (f3, f7)
                if key == (0, 0): v = (a + b) & M32
                elif key == (0, 0x20): v = (a - b) & M32
                elif key == (1, 0): v = (a << s) & M32
                elif key == (2, 0): v = int(sx(a, 32) < sx(b, 32))
                elif key == (3, 0): v = int(a < b)
                elif key == (4, 0): v = a ^ b
                elif key == (5, 0): v = a >> s
                elif key == (5, 0x20): v = (sx(a, 32) >> s) & M32
                elif key == (6, 0): v = a | b
                elif key == (7, 0): v = a & b
                else: raise RuntimeError(f"non-RV32I OP {w:#010x} at {pc:#x}")
            else:
                raise RuntimeError(f"non-RV32I or unexpected word {w:#010x} at {pc:#x}")
            if v is not None and rd:
                x[rd] = v & M32
            pc = npc
        return x[10], x[11], steps


def tdiv(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def tmod(a, b):
    return a - tdiv(a, b) * b


def expected(name, x, y):
    a, b = x & M32, y & M32
    sa, sb, s64x, s64y = sx(a, 32), sx(b, 32), sx(x, 64), sx(y, 64)
    s = y & 63
    if name == "__mulsi3": return (a * b) & M32
    if name == "__udivsi3": return None if b == 0 else a // b
    if name == "__umodsi3": return None if b == 0 else a % b
    if name == "__divsi3": return None if b == 0 or (sa == -2**31 and sb == -1) else tdiv(sa, sb) & M32
    if name == "__modsi3": return None if b == 0 or (sa == -2**31 and sb == -1) else tmod(sa, sb) & M32
    if name == "__muldi3": return (x * y) & M64
    if name == "__udivdi3": return None if y == 0 else x // y
    if name == "__umoddi3": return None if y == 0 else x % y
    if name == "__divdi3": return None if y == 0 or (s64x == -2**63 and s64y == -1) else tdiv(s64x, s64y) & M64
    if name == "__moddi3": return None if y == 0 or (s64x == -2**63 and s64y == -1) else tmod(s64x, s64y) & M64
    if name == "__lshrdi3": return x >> s
    if name == "__ashldi3": return (x << s) & M64
    if name == "__ashrdi3": return (s64x >> s) & M64
    raise KeyError(name)


SI = {"__mulsi3", "__udivsi3", "__umodsi3", "__divsi3", "__modsi3"}
SHIFT = {"__lshrdi3", "__ashldi3", "__ashrdi3"}
EDGE = [0, 1, 2, 3, 7, 0x7F, 0x80, 0xFF, 0x7FFFFFFF, 0x80000000, 0x80000001, 0xFFFFFFFE, 0xFFFFFFFF, 1 << 32,
        (1 << 32) + 1, (1 << 33) - 1, (1 << 63) - 1, 1 << 63, (1 << 63) + 1, 0xFFFFFFFF00000000, 0xFFFFFFFF80000000,
        M64 - 1, M64, 0x0123456789ABCDEF]


def run_one(job):
    elf, addr, name, npairs = job
    cpu = Cpu(load(elf))
    rng = random.Random(sum(map(ord, name)) * 665)
    pairs = [(x, y) for x in EDGE for y in EDGE] + [(x, s) for x in EDGE for s in range(64)]
    for _ in range(npairs):
        pairs.append((rng.getrandbits(64) >> rng.randrange(64), rng.getrandbits(64) >> rng.randrange(64)))
    bad, done, maxsteps = [], 0, 0
    for x, y in pairs:
        if name in SHIFT:
            y &= 63
        want = expected(name, x, y)
        if want is None:
            continue
        if name in SI:
            args = [x & M32, y & M32]
        elif name in SHIFT:
            args = [x & M32, x >> 32, y]
        else:
            args = [x & M32, x >> 32, y & M32, y >> 32]
        lo, hi, steps = cpu.call(addr, args)
        maxsteps = max(maxsteps, steps)
        got = lo if name in SI else lo | (hi << 32)
        done += 1
        if got != want and len(bad) < 5:
            bad.append(f"{name}({x:#x}, {y:#x}) = {got:#x}, want {want:#x}")
    return name, done, bad, maxsteps


def main():
    elf, tool = sys.argv[1], sys.argv[2]
    npairs = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
    syms = {}
    for line in subprocess.run([tool + "nm", elf], capture_output=True, text=True, check=True).stdout.splitlines():
        parts = line.split()
        if len(parts) == 3:
            syms[parts[2]] = int(parts[0], 16)
    names = sorted(n for n in syms if n.startswith("__") and (n.endswith("si3") or n.endswith("di3")))
    with multiprocessing.Pool(min(13, len(names))) as pool:
        results = pool.map(run_one, [(elf, syms[n], n, npairs) for n in names])
    fail = 0
    for name, done, bad, maxsteps in results:
        print(f"{'OK ' if not bad else 'BAD'} {name}: {done} cases executed on RV32I, max {maxsteps} instructions"
              + ("" if not bad else "; " + "; ".join(bad)))
        fail += bool(bad)
    print(f"{len(results)} helpers, {fail} failing")
    return 1 if fail or not results else 0


if __name__ == "__main__":
    sys.exit(main())
