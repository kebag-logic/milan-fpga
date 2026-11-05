#!/usr/bin/env python3
"""Reviewer probe: the #100 scaledLastGmFreqChange datapath at its extremes.

Lifts, verbatim, the TLV frequency declarations and assignments from
hdl/top/KL_gptp_engine.sv (refusing to run if any lifted line is absent),
wraps them in a probe module, and drives it under Verilator at several clock
rates with the trim pairs at the rate envelope's corners (the generator's
ilim = ppm_addend(RATE_PPM_C, clk)) plus a random sweep inside it.

For each vector it checks, against exact integer arithmetic:
  * RTL == floor(dlt * TLV_K_C / 2^16)            (the documented formula)
  * |RTL - floor(dlt * clk * 2^17 / 1e9)| <= 1    (11.4.4.3.9 exact value)
  * sign(RTL) == sign(dlt) and RTL fits Integer32 (no overflow / sign defect)
where dlt = addend - word3 and the gate (slew active or no rate since reset)
forces zero.

Usage: tlv_mul_probe.py REPO WORKDIR VERILATOR [CLK_HZ ...]
"""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

LIFT = [
    "  localparam longint unsigned TLV_K_C =\n"
    "      ((64'(CLK_HZ_P) << 33) + 64'd500_000_000) / 64'd1_000_000_000;\n",
    "  logic signed [24:0] tlv_dlt_r;\n",
    "  logic signed [31:0] tlv_freq_r;\n",
    "  wire signed [63:0] tlv_prod_w = 64'(tlv_dlt_r) *\n"
    "                                  $signed({1'b0, TLV_K_C[31:0]});\n",
    "        tlv_dlt_r <= (phc_slew_active_o || !phc_rate_seen_r) ? 25'sd0\n"
    "                   : 25'(phc_addend_o - st_wdata_w[31:0]);\n",
    "      if (tlv_mul_r) tlv_freq_r <= 32'(tlv_prod_w >>> 16);\n",
]

CPP = r"""
#include "Vtlv_probe.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
int main(int argc, char **argv) {
  Verilated::commandArgs(argc, argv);
  Vtlv_probe *d = new Vtlv_probe;
  FILE *in = fopen(argv[1], "r");
  unsigned long long a, w; int slew, seen;
  d->clk_i = 0; d->eval();
  while (fscanf(in, "%llx %llx %d %d", &a, &w, &slew, &seen) == 4) {
    d->phc_addend_o = (uint32_t)a; d->st_wdata_w = w;
    d->phc_slew_active_o = slew; d->phc_rate_seen_r = seen;
    d->tlv_become_w = 1;
    d->clk_i = 1; d->eval(); d->clk_i = 0; d->eval();
    d->tlv_become_w = 0;
    d->clk_i = 1; d->eval(); d->clk_i = 0; d->eval();
    printf("%08x\n", (uint32_t)d->freq_o);
  }
  delete d;
  return 0;
}
"""


def module(lifted: list[str], clk: int) -> str:
    k, dlt, freq, prod, dlt_asg, freq_asg = lifted
    return (
        "module tlv_probe #(parameter int unsigned CLK_HZ_P = %d) (\n"
        "  input wire clk_i, input wire tlv_become_w,\n"
        "  input wire phc_slew_active_o, input wire phc_rate_seen_r,\n"
        "  input wire [31:0] phc_addend_o, input wire [63:0] st_wdata_w,\n"
        "  output logic [31:0] freq_o);\n" % clk
        + k + dlt + freq + prod +
        "  logic tlv_mul_r = 1'b0;\n"
        "  always_ff @(posedge clk_i) begin\n"
        "    tlv_mul_r <= tlv_become_w;\n"
        "    if (tlv_become_w)\n" + dlt_asg + freq_asg +
        "  end\n"
        "  assign freq_o = tlv_freq_r;\n"
        "endmodule\n")


def ilim_of(clk: int) -> int:
    return (200 * (1 << 24) * 1000 + clk // 2) // clk


def floor_div(n: int, d: int) -> int:
    return n // d  # Python floors toward minus infinity


def main() -> int:
    repo, work, verilator = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    clks = [int(c) for c in sys.argv[4:]] or [2_000_000, 100_000_000,
                                               125_000_000, 250_000_000]
    src = (repo / "hdl/top/KL_gptp_engine.sv").read_text(encoding="utf-8")
    for s in LIFT:
        if src.count(s) != 1:
            print(f"[FAIL] lifted line not found exactly once: {s!r}")
            return 2
    rng = random.Random(100)
    bad = total = 0
    for clk in clks:
        d = work / f"clk{clk}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "tlv_probe.sv").write_text(module(LIFT, clk))
        (d / "main.cpp").write_text(CPP)
        il = ilim_of(clk)
        corners = [-il, -il + 1, -1, 0, 1, il - 1, il]
        vec = [(a, -i, 0, 1) for a in corners for i in corners]
        vec += [(rng.randint(-il, il), -rng.randint(-il, il), 0, 1)
                for _ in range(4000)]
        vec += [(il, il, 1, 1), (il, -il, 0, 0), (-il, il, 1, 0)]
        (d / "vec.txt").write_text("".join(
            f"{a & 0xFFFFFFFF:x} {w & 0xFFFFFFFFFFFFFFFF:x} {s} {n}\n"
            for a, w, s, n in vec))
        b = subprocess.run([verilator, "--cc", "--exe", "--build", "-j", "2",
                            "-Wno-fatal", "-Wno-WIDTHEXPAND",
                            "-Wno-WIDTHTRUNC", "--Mdir", str(d / "obj"),
                            "--top-module", "tlv_probe",
                            str(d / "tlv_probe.sv"), str(d / "main.cpp"),
                            "-o", "probe"], capture_output=True, text=True)
        exe = d / "obj" / "probe"
        if b.returncode or not exe.is_file():
            print(b.stdout[-2000:], b.stderr[-2000:])
            return 2
        out = subprocess.run([str(exe), str(d / "vec.txt")],
                             capture_output=True, text=True).stdout.split()
        k = ((clk << 33) + 500_000_000) // 1_000_000_000
        worst = dev = 0
        # the rounding of TLV_K_C bounds the deviation from the exact value:
        # |dlt| * |K - exact K| / 2^16, plus one for the two floors
        kerr = abs(k * 1_000_000_000 - (clk << 33)) / 1_000_000_000
        tol = 1 + int(2 * il * kerr / (1 << 16)) + 1
        nbad = 0
        for (a, w, s, n), o in zip(vec, out):
            got = int(o, 16)
            got = got - (1 << 32) if got >> 31 else got
            dlt = 0 if (s or not n) else a - w
            want_k = floor_div(dlt * (k & 0xFFFFFFFF), 1 << 16)
            exact = floor_div(dlt * clk * (1 << 17), 1_000_000_000)
            sign_ok = (got > 0) == (dlt > 0) and (got < 0) == (dlt < 0)
            ok = got == want_k and abs(got - exact) <= tol and sign_ok
            worst = max(worst, abs(got))
            dev = max(dev, abs(got - exact))
            total += 1
            if not ok:
                bad += 1
                nbad += 1
                if nbad <= 5:
                    print(f"[FAIL] clk {clk} a {a} w {w} slew {s} seen {n}: "
                          f"rtl {got} k-formula {want_k} exact {exact}")
        print(f"INFO clk {clk}: ilim {il}, TLV_K_C {k}, vectors {len(vec)}, "
              f"fails {nbad}; extremes dlt +-{2 * il} -> max |rtl| {worst} "
              f"(< 2^31 = {1 << 31}); max |rtl - exact 2^41 value| {dev} LSB "
              f"(K rounding bound {tol})")
    print(f"{total} vectors: {total - bad} PASS, {bad} FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
