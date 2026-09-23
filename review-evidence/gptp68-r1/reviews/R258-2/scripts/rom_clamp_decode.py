#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Decode the SERVO leg of a generated ROM image and compare its clamp and
threshold immediates with the parent's envelope expression.

The parent (KL_gptp_txret.sv) refuses egress timestamps while
|adj| > PHC_ADJ_MAX_C = (RECON_REL_PPM_P * 2^24 * 1000 + PHC_CLK_HZ_P / 2)
/ PHC_CLK_HZ_P, with RECON_REL_PPM_P = 200, in 64-bit unsigned integer
arithmetic. Written out here independently of both repositories.

Usage: rom_clamp_decode.py <gen.py> <clk_hz> [<clk_hz> ...]
Generates each image into a temp dir with the given generator.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

OPS = {0: "NOP", 1: "BR", 2: "BRS", 3: "END", 4: "MOVE", 5: "CMP", 8: "RDST",
       9: "WRST", 21: "COMMIT", 29: "ALU", 30: "MD"}
ALU = ["ADD", "SUB", "AND", "OR", "XOR", "SHL", "SHR", "SAR"]


def parent_env(clk):
    return (200 * (1 << 24) * 1000 + clk // 2) // clk


def decode(w):
    op = (w >> 43) & 0x1F
    rd, ra, rb = (w >> 39) & 0xF, (w >> 35) & 0xF, (w >> 31) & 0xF
    fmt, cnd, imm = (w >> 28) & 0x7, (w >> 24) & 0xF, w & 0xFFFFFF
    return OPS.get(op, f"op{op}"), rd, ra, rb, fmt, cnd, imm


def main():
    gen = sys.argv[1]
    for clk in map(int, sys.argv[2:]):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "img.hex"
            log = subprocess.run([sys.executable, "-B", gen, "--clk-hz",
                                  str(clk), "-o", str(out)],
                                 capture_output=True, text=True, check=True)
            legs = dict(x.split("@") for x in
                        log.stdout.split("legs:")[1].split())
            words = [int(x, 16) for x in out.read_text().split()]
        servo = int(legs["SERVO"])
        # SERVO runs up to the first END after its base
        seq = []
        a = servo
        while True:
            d = decode(words[a])
            seq.append((a, d))
            if d[0] == "END":
                break
            a += 1
        env = parent_env(clk)
        adds = [d[6] for _, d in seq
                if d[0] == "ALU" and d[5] == 0 and d[3] == 0 and d[6] > 1000]
        divs = [d[6] for _, d in seq if d[0] == "MD" and d[5] == 1 and d[3] == 0]
        regdiv = [a for a, d in seq if d[0] == "MD" and d[5] == 1 and d[3] != 0]
        movs = [d[6] for _, d in seq if d[0] == "MOVE" and d[2] == 0]
        sat_lims = [x for x in adds if 2 * x + 1 in divs]
        print(f"clk {clk:>10d}: SERVO@{servo} {len(seq)} words; parent "
              f"PHC_ADJ_MAX_C={env}; e_sat limits in ROM={sat_lims}; "
              f"e_sat divisors={divs}; register-divisor DIVU at {regdiv}; "
              f"ALU-ADD imms={adds}; MOVE imms={movs}; "
              f"{'MATCH' if sat_lims == [env, env] else 'MISMATCH'}")


if __name__ == "__main__":
    main()
