#!/usr/bin/env python3
"""Execute the SERVO leg of the real ROM images, base and new, and compare.

The images are the generator's own output (hex words), decoded field by
field as gptp_ucpu_pkg / KL_gptp_ucpu.sv define them, and executed from the
SERVO leg's base with RA = offset, a chosen integrator and a chosen sync-ok
flag. Every state write (PHC, scratch, timers, flags) and COMMIT is recorded
in order. Registers other than R0 and RA start as random garbage, and any
state read the model does not provide aborts the run, so a leg that depends
on anything unlisted is caught rather than silently fed zero.

Claims checked, per clock configuration:
  A. in band (|offset| <= 20 us), first or synchronized, any integrator in
     [-ILIM, ILIM]: base and new images write the SAME sequence;
  B. the new image equals the #68 policy formula for random offsets over
     +-2^40 ns plus the edges (1 s, 1 s + 1 ns, 20 us, 20 us + 1 ns ...);
  C. the base image equals the pre-#68 formula (validates this emulator).

Usage: python3 rom_servo_differential.py [--base SHA] [--n 20000]
"""
from __future__ import annotations

import argparse
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(os.environ.get("A188_LANE", "$LANES/gptp68-step-policy"))
M64 = (1 << 64) - 1
OPS = {"NOP": 0, "BR": 1, "BRS": 2, "END": 3, "MOVE": 4, "CMP": 5, "RDST": 8,
       "WRST": 9, "COMMIT": 21, "ALU": 29, "MD": 30}
NAME = {v: k for k, v in OPS.items()}
FMT_B, FMT_W, FMT_D, FMT_Q = 0, 1, 2, 3
RG_SCR, RG_PUB, RG_PHC, RG_TMR = 0x20000, 0x30000, 0x40000, 0x50000
S_INTG, S_1E9 = 15, 26
FL = 0x1 | 0x4                      # PRESENT | ASCAP: the servo's own gate
SYNCOK = 0x8


def s64(x: int) -> int:
    x &= M64
    return x - (1 << 64) if x >> 63 else x


def s32(x: int) -> int:
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x >> 31 else x


def fmt_a(v: int, fmt: int) -> int:
    return {FMT_B: v & 0xFF, FMT_W: v & 0xFFFF, FMT_D: v & 0xFFFFFFFF}.get(fmt, v)


def execute(rom: list[int], base: int, off: int, intg: int, synced: bool,
            rng: random.Random) -> list[tuple]:
    rf = [rng.getrandbits(64) for _ in range(16)]
    rf[0] = 0
    rf[1] = off & M64                                   # RA
    mem = {RG_PUB | 2: FL | (SYNCOK if synced else 0),
           RG_SCR | S_INTG: intg & M64, RG_SCR | S_1E9: 1_000_000_000}
    writes: list[tuple] = []
    z = lt = False
    pc = base
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
                 4: opa ^ bi, 5: opa << sh, 6: opa >> sh,
                 7: s64(opa) >> sh}[c]
            rf[rd] = r & M64
        elif name == "MD":
            if cnd & 1:                                  # DIVU 64 / 32
                d = (opb & 0xFFFFFFFF) if rb != 0 else imm
                assert d != 0, "divide by zero in the servo leg"
                rf[rd] = (opa // d) & M64
            else:                                        # MULS 32 x 32
                rf[rd] = (s32(opa) * s32(opb)) & M64
        elif name == "CMP":
            a = fmt_a(opa, fmt)
            sub = (a & 0xFFFFFFFF) - (bi & 0xFFFFFFFF)
            lt = sub < 0
            z = (opa == bi) if fmt == FMT_Q else (sub & 0xFFFFFFFF) == 0
        elif name == "BRS":
            if (cnd == 2 and z) or (cnd == 3 and lt):
                pc = imm
            elif cnd not in (2, 3):
                raise AssertionError(f"unmodelled BRS condition {cnd}")
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


def tail(intg_bits: int | None, flags_after: int) -> list[tuple]:
    t = [] if intg_bits is None else []
    return t + [(RG_SCR | 0, 0), (RG_TMR | 4, 375), (RG_TMR | 5, 0),
                (RG_PUB | 2, flags_after), ("COMMIT",)]


def model(off: int, intg: int, synced: bool, gain_m: int, ilim: int,
          policy: str) -> list[tuple]:
    """The documented rule in plain arithmetic, as an ordered write list."""
    if policy == "new":
        step = (not synced) and abs(off) > 1_000_000_000
        s = max(-20000, min(20000, off))
    else:                                             # pre-#68
        step = abs(off) > 20000
        s = off
    flags_after = FL | SYNCOK
    if step:
        return [(RG_PHC | 1, (-off) & M64), (RG_PHC | 0, (-intg) & M64)] + \
            tail(None, flags_after)
    t = (s * gain_m) >> 6
    i2 = max(-ilim, min(ilim, intg + (t >> 2)))
    out = -((t - (t >> 2)) + i2)
    return [(RG_SCR | S_INTG, i2 & M64), (RG_PHC | 0, out & M64)] + \
        tail(None, flags_after)


def image(gen: Path, args: list[str], tmp: Path) -> tuple[list[int], int]:
    out = tmp / "img.hex"
    r = subprocess.run([sys.executable, str(gen), *args, "-o", str(out)],
                       capture_output=True, text=True, check=True).stdout
    base = int(re.search(r"SERVO@(\d+)", r).group(1))
    words = [int(x, 16) for x in out.read_text().split()]
    return words, base


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="c1b617435824929a790739ea8585c3fe1a328cc0")
    ap.add_argument("--n", type=int, default=20000)
    a = ap.parse_args()
    rng = random.Random(68)
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        old_gen = tmp / "gen_base.py"
        old_gen.write_text(subprocess.run(
            ["git", "-C", str(LANE), "show", f"{a.base}:hdl/ucode/gen_gptp_ucode.py"],
            capture_output=True, text=True, check=True).stdout)
        new_gen = LANE / "hdl/ucode/gen_gptp_ucode.py"
        for clk in (100_000_000, 2_000_000, 25_000_000, 125_000_000):
            args = ["--clk-hz", str(clk)]
            old, ob = image(old_gen, args, tmp)
            new, nb = image(new_gen, args, tmp)
            gain_m = round((1 << 24) * 64 * 8 / clk)
            ilim = round(200 * (1 << 24) * 1000 / clk)
            edges = [0, 1, -1, 20000, -20000, 20001, -20001, 999_999_999,
                     1_000_000_000, -1_000_000_000, 1_000_000_001,
                     -1_000_000_001, 900_000_000, -900_000_000,
                     1_100_000_000, -1_100_000_000, (1 << 31), -(1 << 31),
                     (1 << 40), -(1 << 40)]
            ia = ib = ic = 0
            for k in range(a.n + 4 * len(edges)):
                if k < 4 * len(edges):
                    off = edges[k // 4]
                    synced = bool(k & 1)
                    intg = (ilim, -ilim)[(k >> 1) & 1]
                else:
                    synced = rng.random() < 0.5
                    intg = rng.randint(-ilim, ilim)
                    off = rng.choice((rng.randint(-20000, 20000),
                                      rng.randint(-(1 << 40), 1 << 40),
                                      rng.randint(-1_100_000_000, 1_100_000_000)))
                wn = execute(new, nb, off, intg, synced, rng)
                wo = execute(old, ob, off, intg, synced, rng)
                if abs(off) <= 20000:
                    ia += 1
                    if wn != wo:
                        bad += 1
                        print(f"A FAIL clk {clk} off {off} intg {intg} synced {synced}")
                ib += 1
                if wn != model(off, intg, synced, gain_m, ilim, "new"):
                    bad += 1
                    print(f"B FAIL clk {clk} off {off} intg {intg} synced {synced}: {wn}")
                ic += 1
                if wo != model(off, intg, synced, gain_m, ilim, "old"):
                    bad += 1
                    print(f"C FAIL clk {clk} off {off} intg {intg} synced {synced}: {wo}")
            print(f"clk {clk}: SERVO base {ob} -> {nb}; "
                  f"A in-band identical {ia}, B new==policy {ib}, "
                  f"C base==pre-#68 {ic} cases")
    print("RESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
