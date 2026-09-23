#!/usr/bin/env python3
"""ROM-level evidence for the #68 correction round, on the real images.

The images are the generators' own output, decoded field by field as
gptp_ucpu_pkg / KL_gptp_ucpu.sv define them and executed by a small
emulator (adapted from the prior lane's public differential). Registers
other than those a leg is entered with start as random garbage, and a state
read the model does not provide aborts the run, so a leg that depends on
anything unlisted is caught rather than silently fed zero.

Claims, at 2, 25, 50, 100 and 125 MHz:
  A. SERVO, |offset| <= 20 us, either lock state, integrator anywhere in
     [-ILIM, ILIM] with both rails: the new image writes what the base
     image (c1b6174) writes, apart from the new S_LOCK write, and apart from
     the rate trim wherever the base trim left +-ILIM, where the new one is
     exactly that trim clamped to +-ILIM. Counted separately.
  B. SERVO: the new image equals the documented #68 rule, written out below
     as plain arithmetic, for random offsets over +-2^40 ns, dense ones over
     +-200 us, and the edges, in both lock states.
  C. SERVO: the base image equals the pre-#68 rule (validates the emulator).
  D. PDPAIR, the only asCapable setter: for random scratch and flags, the
     new image writes exactly what the base writes, in the same order (the
     hoisted S_PDGOT write moved only ahead of compares), plus one
     S_LOCK = 0 exactly when asCapable rises.
  E. Every other program: the base generator's code, emitted at the new
     leg bases, is word-for-word the new image. Only SERVO, PDPAIR, SRTO
     and BECOME change content; the rest only moved.
Also prints ILIM against the parent's PHC_ADJ_MAX_C expression.

Usage: python3 rom_differential.py [--n 20000]
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(os.environ.get("A199_LANE", "$LANES/gptp68-step-policy"))
BASE = "c1b617435824929a790739ea8585c3fe1a328cc0"
M64 = (1 << 64) - 1
OPS = {"NOP": 0, "BR": 1, "BRS": 2, "END": 3, "MOVE": 4, "CMP": 5, "RDST": 8,
       "WRST": 9, "COMMIT": 21, "ALU": 29, "MD": 30}
NAME = {v: k for k, v in OPS.items()}
FMT_B, FMT_W, FMT_D, FMT_Q = 0, 1, 2, 3
RG_SCR, RG_PUB, RG_PHC, RG_TMR = 0x20000, 0x30000, 0x40000, 0x50000
S_INTG, S_LOCK = 15, 43
S_PDOK, S_PDLOST, S_PDGOT = 7, 8, 11
S_NR3, S_NR4, S_NRR, S_T1, S_T4, S_T2, S_PDELAY = 12, 13, 14, 16, 17, 5, 4
PRESENT, AMGM, ASCAP, SYNCOK = 1, 2, 4, 8
LOCKX = 80000


def s64(x: int) -> int:
    x &= M64
    return x - (1 << 64) if x >> 63 else x


def s32(x: int) -> int:
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x >> 31 else x


def fmt_a(v: int, fmt: int) -> int:
    return {FMT_B: v & 0xFF, FMT_W: v & 0xFFFF, FMT_D: v & 0xFFFFFFFF}.get(fmt, v)


def execute(rom, pc, regs, mem, rng):
    rf = [rng.getrandbits(64) for _ in range(16)]
    rf[0] = 0
    for r, v in regs.items():
        rf[r] = v & M64
    mem = dict(mem)
    writes = []
    z = lt = False
    for _ in range(4096):
        w = rom[pc]
        op, rd, ra, rb = w >> 43, (w >> 39) & 15, (w >> 35) & 15, (w >> 31) & 15
        fmt, cnd, imm = (w >> 28) & 7, (w >> 24) & 15, w & 0xFFFFFF
        name = NAME.get(op)
        opa, opb = rf[ra], rf[rb]
        bi = opb if rb != 0 else imm
        pc += 1
        if name == "END":
            return writes
        if name == "MOVE":
            rf[rd] = imm if ra == 0 else fmt_a(opa, fmt)
        elif name == "ALU":
            c, sh = cnd & 7, bi & 63
            r = {0: opa + bi, 1: opa - bi, 2: opa & bi, 3: opa | bi,
                 4: opa ^ bi, 5: opa << sh, 6: opa >> sh, 7: s64(opa) >> sh}[c]
            rf[rd] = r & M64
        elif name == "MD":
            if cnd & 1:                                  # DIVU 64 / 32
                d = (opb & 0xFFFFFFFF) if rb != 0 else imm
                assert d != 0, "divide by zero"
                rf[rd] = (opa // d) & M64
            else:                                        # MULS 32 x 32
                rf[rd] = (s32(opa) * s32(opb)) & M64
        elif name == "CMP":
            a = fmt_a(opa, fmt)
            sub = (a & 0xFFFFFFFF) - (bi & 0xFFFFFFFF)
            lt = sub < 0
            z = (opa == bi) if fmt == FMT_Q else (sub & 0xFFFFFFFF) == 0
        elif name == "BRS":
            if cnd not in (2, 3):
                raise AssertionError(f"unmodelled BRS condition {cnd}")
            if (cnd == 2 and z) or (cnd == 3 and lt):
                pc = imm
        elif name == "BR":
            pc = imm
        elif name == "RDST":
            if imm not in mem:
                raise AssertionError(f"unmodelled state read {imm:#x}")
            rf[rd] = mem[imm]
        elif name == "WRST":
            mem[imm] = opa
            writes.append((imm, opa))
        elif name == "COMMIT":
            writes.append(("COMMIT",))
        else:
            raise AssertionError(f"unmodelled opcode {op} at {pc - 1}")
    raise AssertionError("leg did not END")


def ppm_addend(ppm, clk):
    """The parent's PHC_ADJ_MAX_C expression (KL_gptp_txret.sv)."""
    return (ppm * (1 << 24) * 1000 + clk // 2) // clk


def servo_rule(off, intg, locked, gain_m, lim):
    """The documented #68 rule as an ordered write list."""
    thr = 100000 if locked else 20000
    cl = lambda v: max(-lim, min(lim, v))          # noqa: E731
    tail = [(RG_SCR | 0, 0), (RG_TMR | 4, 375), (RG_TMR | 5, 0),
            (RG_SCR | S_LOCK, LOCKX), (RG_PUB | 2, PRESENT | ASCAP | SYNCOK),
            ("COMMIT",)]
    if abs(off) > thr:
        return [(RG_PHC | 1, (-off) & M64),
                (RG_PHC | 0, (-cl(intg)) & M64)] + tail
    t = (off * gain_m) >> 6
    i2 = cl(intg + (t >> 2))
    return [(RG_SCR | S_INTG, i2 & M64),
            (RG_PHC | 0, (-cl((t - (t >> 2)) + i2)) & M64)] + tail


def base_rule(off, intg, gain_m, lim):
    """The pre-#68 rule: 20 us on every pair, no whole-trim clamp."""
    tail = [(RG_SCR | 0, 0), (RG_TMR | 4, 375), (RG_TMR | 5, 0),
            (RG_PUB | 2, PRESENT | ASCAP | SYNCOK), ("COMMIT",)]
    if abs(off) > 20000:
        return [(RG_PHC | 1, (-off) & M64), (RG_PHC | 0, (-intg) & M64)] + tail
    t = (off * gain_m) >> 6
    i2 = max(-lim, min(lim, intg + (t >> 2)))
    return [(RG_SCR | S_INTG, i2 & M64),
            (RG_PHC | 0, (-((t - (t >> 2)) + i2)) & M64)] + tail


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def image(gen: Path, clk: int, tmp: Path, tag: str):
    out = tmp / f"{tag}.hex"
    r = subprocess.run([sys.executable, str(gen), "--clk-hz", str(clk),
                        "-o", str(out)], capture_output=True, text=True,
                       check=True).stdout
    legs = {m.group(1): int(m.group(2)) for m in re.finditer(r"(\w+)@(\d+)", r)}
    return [int(x, 16) for x in out.read_text().split()], legs


def servo_claims(old, ob, new, nb, clk, gain_m, lim, n, rng):
    edges = [0, 1, -1, 19999, -19999, 20000, -20000, 20001, -20001,
             99999, -99999, 100000, -100000, 100001, -100001, 90000, -90000,
             110000, -110000, 5_000_000, -5_000_000, (1 << 31), -(1 << 31),
             (1 << 40), -(1 << 40)]
    ident = clamped = cb = cc = 0
    bad = 0
    for k in range(n + 4 * len(edges)):
        if k < 4 * len(edges):
            off = edges[k // 4]
            locked = bool(k & 1)
            intg = (lim, -lim)[(k >> 1) & 1]
        else:
            locked = rng.random() < 0.5
            intg = rng.randint(-lim, lim)
            off = rng.choice((rng.randint(-20000, 20000),
                              rng.randint(-200000, 200000),
                              rng.randint(-(1 << 40), 1 << 40)))
        flags = PRESENT | ASCAP | (SYNCOK if locked else 0)
        mem_new = {RG_PUB | 2: flags, RG_SCR | S_INTG: intg & M64,
                   RG_SCR | S_LOCK: LOCKX if locked else 0}
        mem_old = {RG_PUB | 2: flags, RG_SCR | S_INTG: intg & M64}
        wn = execute(new, nb, {1: off}, mem_new, rng)
        wo = execute(old, ob, {1: off}, mem_old, rng)
        if wn != servo_rule(off, intg, locked, gain_m, lim):
            bad += 1
            print(f"  B FAIL clk {clk} off {off} intg {intg} locked {locked}: {wn}")
        cb += 1
        if wo != base_rule(off, intg, gain_m, lim):
            bad += 1
            print(f"  C FAIL clk {clk} off {off} intg {intg}: {wo}")
        cc += 1
        if abs(off) <= 20000:
            wn2 = [w for w in wn if w[:1] != (RG_SCR | S_LOCK,)]
            if wn2 == wo:
                ident += 1
                continue
            # the only allowed difference: the trim, clamped
            diff = [(a, b) for a, b in zip(wn2, wo) if a != b]
            ok = (len(wn2) == len(wo) and len(diff) == 1
                  and diff[0][0][0] == RG_PHC | 0
                  and abs(s64(diff[0][1][1])) > lim
                  and s64(diff[0][0][1]) == max(-lim, min(lim, s64(diff[0][1][1]))))
            if ok:
                clamped += 1
            else:
                bad += 1
                print(f"  A FAIL clk {clk} off {off} intg {intg} locked {locked}")
    print(f"  SERVO: A in band {ident} identical + {clamped} clamped only; "
          f"B new == #68 rule {cb}; C base == pre-#68 rule {cc}")
    return bad


def pdpair_claims(old, ob, new, nb, clk, n, rng):
    bad = seen_rise = seen_good = 0
    for _ in range(n):
        # aim the delay at the verdict: good (-80..800) most of the time,
        # with the Milan floor and threshold edges, else far outside
        d = rng.choice((rng.randint(-80, 800), -80, -81, 800, 801,
                        rng.randint(-100000, 100000)))
        t1 = rng.getrandbits(40)
        t2 = rng.getrandbits(40)
        turn = rng.randint(250000, 300000)
        resid = turn - 2 * d
        # t4 - t1 = turn; t3 - t2 = resid; an exact or stale ratio keeps the
        # aimed delay, a near-unity one moves it by a few ns
        t4 = t1 + turn
        t3 = t2 + resid
        nr3 = rng.choice((0, rng.getrandbits(40)))
        nr4 = rng.getrandbits(40)
        nrr = rng.choice((0, 1 << 30, rng.randint((1 << 30) - 3000, (1 << 30) + 3000)))
        pdok = rng.randint(0, 5)
        flags = rng.choice((0, PRESENT, PRESENT | AMGM, ASCAP, PRESENT | ASCAP,
                            PRESENT | ASCAP | SYNCOK, PRESENT | AMGM | ASCAP))
        mem = {RG_SCR | S_T4: t4, RG_SCR | S_NR3: nr3, RG_SCR | S_NR4: nr4,
               RG_SCR | S_NRR: nrr, RG_SCR | S_T1: t1, RG_SCR | S_T2: t2,
               RG_SCR | S_PDOK: pdok, RG_PUB | 2: flags}
        wo = execute(old, ob, {3: t3}, mem, rng)
        wn = execute(new, nb, {3: t3}, mem, rng)
        rise = [w for w in wn if w[:1] == (RG_SCR | S_LOCK,)]
        wn2 = [w for w in wn if w[:1] != (RG_SCR | S_LOCK,)]
        # S_PDGOT is written first in the verdict now, but only compares,
        # which write nothing, used to precede it: the write order is equal
        ok = wn2 == wo and wo.count((RG_SCR | S_PDGOT, 1)) == 1
        # the S_LOCK write exactly when asCapable rises
        pub = [w[1] for w in wo if w[:1] == (RG_PUB | 2,)]
        rose = bool(pub) and not (flags & ASCAP) and bool(pub[-1] & ASCAP)
        ok = ok and rise == ([(RG_SCR | S_LOCK, 0)] if rose else [])
        seen_rise += rose
        seen_good += (RG_SCR | S_PDLOST, 0) in wo
        if not ok:
            bad += 1
            print(f"  D FAIL clk {clk}: old {wo}\n         new {wn}")
    print(f"  PDPAIR: D {n} cases, {seen_rise} of them an asCapable rise, "
          f"{seen_good} a good verdict")
    return bad


def leg_claims(clk, tmp, new_rom, legs):
    base_src = subprocess.run(["git", "-C", str(LANE), "show",
                               f"{BASE}:hdl/ucode/gen_gptp_ucode.py"],
                              capture_output=True, text=True, check=True).stdout
    (tmp / "gen_base_mod.py").write_text(base_src)
    g = load(tmp / "gen_base_mod.py", f"gb{clk}")
    g.set_servo_gains(clk)
    for name in legs:
        g.LB[name] = legs[name]
    mac = 0x02A1B2C3D4E5
    fixed = [(16, g.prog_rx_sync), (64, g.prog_rx_followup),
             (128, g.prog_rx_announce), (192, g.prog_rx_pdreq),
             (256, g.prog_rx_pdresp), (320, g.prog_rx_pdrfu),
             (384, g.prog_rx_signal), (448, g.prog_tx_ts),
             (512, lambda b: g.prog_tmr(b, mac, 0, 0)),
             (704, g.prog_tb_battery)]
    progs = [(f"fixed@{b}", b, fn) for b, fn in fixed] + \
            [(name, legs[name], fn) for name, fn in g.LEG_FNS]
    changed = []
    for label, b, fn in progs:
        words = fn(b).words()
        if new_rom[b:b + len(words)] != words:
            changed.append(label)
    print(f"  programs whose content changed: {', '.join(changed)}")
    return 0 if sorted(changed) == ["BECOME", "PDPAIR", "SERVO", "SRTO"] else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=20000)
    a = ap.parse_args()
    rng = random.Random(68199)
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        old_gen = tmp / "gen_base.py"
        old_gen.write_text(subprocess.run(
            ["git", "-C", str(LANE), "show", f"{BASE}:hdl/ucode/gen_gptp_ucode.py"],
            capture_output=True, text=True, check=True).stdout)
        new_gen = LANE / "hdl/ucode/gen_gptp_ucode.py"
        for clk in (2_000_000, 25_000_000, 50_000_000, 100_000_000, 125_000_000):
            old, ol = image(old_gen, clk, tmp, "old")
            new, nl = image(new_gen, clk, tmp, "new")
            gain_m = round((1 << 24) * 64 * 8 / clk)
            lim = ppm_addend(200, clk)
            assert lim == round(200 * (1 << 24) * 1000 / clk)
            print(f"clk {clk}: ILIM = parent PHC_ADJ_MAX_C = {lim}; "
                  f"SERVO {ol['SERVO']} -> {nl['SERVO']}, "
                  f"PDPAIR {ol['PDPAIR']} -> {nl['PDPAIR']}")
            bad += servo_claims(old, ol["SERVO"], new, nl["SERVO"], clk,
                                gain_m, lim, a.n, rng)
            bad += pdpair_claims(old, ol["PDPAIR"], new, nl["PDPAIR"], clk,
                                 a.n // 4, rng)
            bad += leg_claims(clk, tmp, new, nl)
    print("RESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
