#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Execute the SHIPPED SERVO / SRTO / BECOME words of a generated ROM image
on an independent model of the gPTP uCPU (semantics read from
hdl/ucpu/KL_gptp_ucpu.sv at the reviewed head) and grade every write against
an independent reference of the #68 owner policy and of the parent's
PHC_ADJ_MAX_C expression (KL_gptp_txret.sv), written out here.

The image is generated from the generator at the head under review, for each
clock given, and the leg bases are read from the generator's own report line.
Only the hex words are executed; nothing of the generator's Python is.

Usage: servo_rom_emulator.py <generator.py> <scratch-dir> <clk_hz>...
Exit 0 when every case matches; 1 otherwise.
"""

from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

M64 = (1 << 64) - 1

# encoding, gptp_ucpu_pkg.sv: op[47:43] rd[42:39] ra[38:35] rb[34:31]
# fmt[30:28] cnd[27:24] imm[23:0]
OP_BR, OP_BRS, OP_END, OP_MOVE, OP_CMP = 1, 2, 3, 4, 5
OP_RDST, OP_WRST, OP_COMMIT, OP_ALU, OP_MD = 8, 9, 21, 29, 30

RG_SCR, RG_PUB, RG_PHC, RG_TMR = 0x20000, 0x30000, 0x40000, 0x50000
S_SYNCTS, S_INTG, S_CID, S_MYPV, S_LOCK = 0, 15, 25, 10, 43
S_BESTPV, S_BESTID, S_BESTSRC = 2, 3, 20


def s64(v: int) -> int:
    v &= M64
    return v - (1 << 64) if v >> 63 else v


def s32(v: int) -> int:
    v &= 0xFFFFFFFF
    return v - (1 << 32) if v >> 31 else v


def parent_adj_max(clk_hz: int, ppm: int = 200) -> int:
    """KL_gptp_txret.sv PHC_ADJ_MAX_C, as its SystemVerilog reads."""
    return (ppm * (1 << 24) * 1000 + clk_hz // 2) // clk_hz


def decode(word: int) -> dict:
    return {
        "op": (word >> 43) & 0x1F, "rd": (word >> 39) & 0xF,
        "ra": (word >> 35) & 0xF, "rb": (word >> 31) & 0xF,
        "fmt": (word >> 28) & 0x7, "cnd": (word >> 24) & 0xF,
        "imm": word & 0xFFFFFF,
    }


class Cpu:
    """Only the opcodes the three legs use; anything else is refused."""

    def __init__(self, rom: list[int], scratch: dict, pub: dict):
        self.rom = rom
        self.rf = [0] * 16
        self.z = self.lt = False
        self.scratch = scratch
        self.pub = pub
        self.writes: list[tuple[int, int]] = []

    def rd_state(self, addr: int) -> int:
        region, off = addr & 0xF0000, addr & 0xFFFF
        if region == RG_SCR:
            return self.scratch.get(off & 0x3F, 0) & M64
        if region == RG_PUB:
            return self.pub.get(off & 0xF, 0) & M64
        raise AssertionError(f"read of region {region:#x}")

    def wr_state(self, addr: int, val: int) -> None:
        val &= M64
        self.writes.append((addr, val))
        region, off = addr & 0xF0000, addr & 0xFFFF
        if region == RG_SCR:
            self.scratch[off & 0x3F] = val
        elif region == RG_PUB:
            self.pub[off & 0xF] = val

    def run(self, pc: int, limit: int = 400) -> None:
        for _ in range(limit):
            i = decode(self.rom[pc])
            op, rd, ra, rb, fmt, cnd, imm = (i[k] for k in (
                "op", "rd", "ra", "rb", "fmt", "cnd", "imm"))
            opa = self.rf[ra]
            b = self.rf[rb] if rb != 0 else imm
            nxt = pc + 1
            if op == OP_END:
                return
            if op == OP_BR:
                nxt = imm & 0x3FF
            elif op == OP_BRS:
                flag = {2: self.z, 3: self.lt}.get(cnd)
                if flag is None:
                    raise AssertionError(f"BRS cnd {cnd} at {pc}")
                if flag:
                    nxt = imm & 0x3FF
            elif op == OP_MOVE:
                if ra != 0:
                    raise AssertionError(f"MOVE from a register at {pc}")
                self.set(rd, imm)
            elif op == OP_CMP:
                a = {0: opa & 0xFF, 1: opa & 0xFFFF,
                     2: opa & 0xFFFFFFFF}.get(fmt, opa)
                sub = (a & 0xFFFFFFFF) - (b & 0xFFFFFFFF)
                self.z = (opa == b) if fmt == 3 else ((sub & 0xFFFFFFFF) == 0)
                self.lt = sub < 0
            elif op == OP_ALU:
                c = cnd & 7
                if c == 0:
                    v = opa + b
                elif c == 1:
                    v = opa - b
                elif c == 2:
                    v = opa & b
                elif c == 3:
                    v = opa | b
                elif c == 4:
                    v = opa ^ b
                elif c == 5:
                    v = opa << (b & 63)
                elif c == 6:
                    v = opa >> (b & 63)
                else:
                    v = s64(opa) >> (b & 63)
                self.set(rd, v)
            elif op == OP_MD:
                if cnd & 1:  # DIVU 64 / 32 -> 64, divisor reg[31:0] or imm
                    d = (self.rf[rb] & 0xFFFFFFFF) if rb != 0 else imm
                    if d == 0:
                        raise AssertionError(f"divide by zero at {pc}")
                    self.set(rd, opa // d)
                else:        # MULS signed 32 x 32 -> 64, register b only
                    self.set(rd, s32(opa) * s32(self.rf[rb]))
            elif op == OP_RDST:
                self.set(rd, self.rd_state(imm))
            elif op == OP_WRST:
                self.wr_state(imm, opa)
            elif op == OP_COMMIT:
                self.writes.append(("COMMIT", 0))
            else:
                raise AssertionError(f"opcode {op} at {pc} not modelled")
            pc = nxt
        raise AssertionError("leg did not END")

    def set(self, rd: int, v: int) -> None:
        self.rf[rd] = v & M64


def reference(off: int, lock: int, intg: int, lim: int, gain_m: int):
    """The owner policy of 2026-09-23 plus the #68 PI as documented:
    returns (step_value or None, addend, new_intg)."""
    thr = 20000 + lock
    clamp = lambda v: max(-lim, min(lim, v))  # noqa: E731
    if abs(off) > thr:
        return (-off) & M64, (-clamp(intg)) & 0xFFFFFFFF, intg
    t = (off * gain_m) >> 6
    ni = clamp(intg + (t >> 2))
    trim = clamp((t - (t >> 2)) + ni)
    return None, (-trim) & 0xFFFFFFFF, ni


def generate(gen: Path, scratch: Path, clk: int) -> tuple[list[int], dict]:
    img = scratch / f"emu_{clk}.hex"
    out = subprocess.run([sys.executable, str(gen), "--clk-hz", str(clk),
                          "-o", str(img)], capture_output=True, text=True,
                         check=True).stdout
    legs = {}
    for tok in out.split():
        if "@" in tok:
            n, a = tok.split("@")
            legs[n] = int(a)
    rom = [int(x, 16) for x in img.read_text().split()]
    return rom, legs


def main() -> int:
    gen, scratch = Path(sys.argv[1]), Path(sys.argv[2])
    clks = [int(c) for c in sys.argv[3:]]
    rng = random.Random(0x68259)
    bad = 0
    for clk in clks:
        rom, legs = generate(gen, scratch, clk)
        lim = parent_adj_max(clk)
        gain_m = round((1 << 24) * 64 * 8 / clk)
        # the immediates the ROM carries for the two clamps
        servo = legs["SERVO"]
        imms = [decode(rom[a]) for a in range(servo, servo + 60)]
        div_imms = [d["imm"] for d in imms
                    if d["op"] == OP_MD and d["cnd"] & 1 and d["rb"] == 0]
        clamp_ok = div_imms == [2 * lim + 1, 2 * lim + 1]
        print(f"clk {clk}: parent PHC_ADJ_MAX_C {lim}, ROM DIVU clamp "
              f"divisors {div_imms} -> {'OK' if clamp_ok else 'MISMATCH'}; "
              f"SERVO@{servo} SRTO@{legs['SRTO']} BECOME@{legs['BECOME']}")
        bad += 0 if clamp_ok else 1
        stats = {"cases": 0, "steps": 0, "slews": 0, "rail": 0,
                 "clamped_pi": 0, "max_abs_addend": 0}
        for lock in (0, 80000):
            thr = 20000 + lock
            offs = [0, 1, -1, thr - 1, -(thr - 1), thr, -thr, thr + 1,
                    -(thr + 1), 2 * thr, -2 * thr, 2 * thr + 1,
                    -(2 * thr + 1), 20000, -20000, 20001, -20001, 100000,
                    -100000, 100001, -100001, 10**6, -10**6, 11 * 10**8,
                    -11 * 10**8, 2**31 - 1, -2**31, 2**32, -2**32, 2**62,
                    -2**62, 2**63 - 1, -2**63, -2**63 + 1, 2**63 - 1 - thr,
                    2**63 - thr, 2**63 - 1 - 2 * thr]
            offs += [rng.randint(-2 * thr, 2 * thr) for _ in range(1500)]
            offs += [rng.randint(-2**63, 2**63 - 1) for _ in range(200)]
            intgs = [0, lim, -lim, lim - 1, -(lim - 1)]
            intgs += [rng.randint(-lim, lim) for _ in range(6)]
            for off in offs:
                for intg in intgs:
                    scratch_m = {S_LOCK: lock, S_INTG: intg & M64,
                                 S_SYNCTS: 12345}
                    pub = {2: 0x7 | 0}
                    cpu = Cpu(rom, scratch_m, pub)
                    cpu.rf[1] = off & M64                    # RA = offset
                    cpu.run(servo)
                    stepv, addend, ni = reference(off, lock, intg, lim,
                                                  gain_m)
                    want = []
                    if stepv is not None:
                        want.append((RG_PHC | 1, stepv))
                    else:
                        want.append((RG_SCR | S_INTG, ni & M64))
                    got_phc = [(a, v) for a, v in cpu.writes
                               if a != "COMMIT" and (a & 0xF0000) == RG_PHC]
                    got_intg = [(a, v) for a, v in cpu.writes
                                if a == RG_SCR | S_INTG]
                    tail = [w for w in cpu.writes
                            if w[0] == "COMMIT" or (w[0] & 0xF0000) != RG_PHC
                            and w[0] != RG_SCR | S_INTG]
                    ok = True
                    if stepv is not None:
                        ok &= got_phc[:1] == [(RG_PHC | 1, stepv)]
                        ok &= len(got_phc) == 2 and got_intg == []
                    else:
                        ok &= len(got_phc) == 1
                        ok &= got_intg == [(RG_SCR | S_INTG, ni & M64)]
                    ok &= (got_phc[-1][0] == RG_PHC | 0 and
                           got_phc[-1][1] & 0xFFFFFFFF == addend)
                    a32 = s32(got_phc[-1][1])
                    ok &= -lim <= a32 <= lim
                    ok &= tail == [(RG_SCR | S_SYNCTS, 0), (RG_TMR | 4, 375),
                                   (RG_TMR | 5, 0), (RG_SCR | S_LOCK, 80000),
                                   (RG_PUB | 2, 0x7 | 8), ("COMMIT", 0)]
                    stats["cases"] += 1
                    stats["steps" if stepv is not None else "slews"] += 1
                    stats["rail"] += abs(a32) == lim
                    if stepv is None:
                        t = (off * gain_m) >> 6
                        raw = (t - (t >> 2)) + ni
                        stats["clamped_pi"] += abs(raw) > lim
                    stats["max_abs_addend"] = max(stats["max_abs_addend"],
                                                  abs(a32))
                    if not ok:
                        bad += 1
                        if bad <= 10:
                            print(f"  MISMATCH clk {clk} lock {lock} off "
                                  f"{off} intg {intg}: {cpu.writes}")
        print(f"  SERVO: {stats['cases']} cases, {stats['steps']} step, "
              f"{stats['slews']} slew, {stats['clamped_pi']} slews whose "
              f"P+I exceeded the envelope before the clamp, "
              f"{stats['rail']} addends exactly on it, max |addend| "
              f"{stats['max_abs_addend']} (limit {lim})")
        # SRTO and BECOME: each writes S_LOCK = 0 and nothing reads it
        for leg, flags_in in (("SRTO", 0xF), ("BECOME", 0xD)):
            cpu = Cpu(rom, {S_LOCK: 80000, S_CID: 0x1234, S_MYPV: 0x55},
                      {2: flags_in})
            cpu.run(legs[leg])
            lockw = [v for a, v in cpu.writes if a == RG_SCR | S_LOCK]
            flagw = [v for a, v in cpu.writes if a == RG_PUB | 2]
            phcw = [a for a, _ in cpu.writes
                    if a != "COMMIT" and (a & 0xF0000) == RG_PHC]
            want_flags = {"SRTO": 0x7, "BECOME": 0x7}[leg]
            ok = lockw == [0] and flagw == [want_flags] and phcw == []
            print(f"  {leg}: S_LOCK writes {lockw}, flags {flags_in:#x} -> "
                  f"{[hex(f) for f in flagw]}, PHC writes {len(phcw)} -> "
                  f"{'OK' if ok else 'MISMATCH'}")
            bad += 0 if ok else 1
    # the generator's envelope helper against the parent's expression
    sys.path.insert(0, str(gen.parent))
    import importlib.util
    spec = importlib.util.spec_from_file_location("gen_head", gen)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sweep = list(range(1_000_000, 400_000_001, 999_983))
    sweep += [2_000_000, 25_000_000, 50_000_000, 62_500_000, 100_000_000,
              125_000_000, 156_250_000, 2**31, 2**31 * 5, 2**31 * 25,
              3 * 5**5 * 2**20]
    diff = [c for c in sweep
            if mod.ppm_addend(200, c) != parent_adj_max(c)]
    ties = [c for c in (2**31, 2**31 * 5, 2**31 * 25)
            if (200 * (1 << 24) * 1000) % c == c // 2]
    print(f"ppm_addend vs parent expression: {len(sweep)} clocks, "
          f"{len(diff)} differ; exact-tie clocks exercised: {ties}")
    bad += len(diff)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'} ({bad} mismatches)")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
