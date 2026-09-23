#!/usr/bin/env python3
"""The head servo's largest sustained rate trim against the parent
KL_gptp_txret addend envelope, per clock. The trim is computed with the
generator's own set_servo_gains and the SERVO leg's integer arithmetic
(input saturated at SLEW_NS_C, kp = t - t>>2, integrator on its ILIM rail);
the envelope is PHC_ADJ_MAX_C = (RECON_REL_PPM_P * 2^24 * 1000 + clk/2) / clk
with the parent default RECON_REL_PPM_P = 200 (KL_gptp_txret.sv). The
generator is imported from the donor tree given as the only argument.
Usage: envelope_table.py <donor-head-tree>"""
import importlib.util
import sys
from pathlib import Path


def main() -> int:
    """Print one row per clock; exit 1 if any sustained trim is refused."""
    spec = importlib.util.spec_from_file_location(
        "gen", Path(sys.argv[1]) / "hdl/ucode/gen_gptp_ucode.py")
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    refused = 0
    for clk in (2_000_000, 25_000_000, 50_000_000, 100_000_000, 125_000_000):
        gen.set_servo_gains(clk)
        m, ilim = gen.RUNTIME["gain_m"], gen.RUNTIME["ilim"]
        t = (gen.SLEW_NS_C * m) >> gen.GAIN_S_C
        trim = (t - (t >> 2)) + ilim
        env = (200 * (1 << 24) * 1000 + clk // 2) // clk
        unit_ppm = 1e6 / ((1 << 24) * 1e9 / clk)   # ppm per addend unit
        over = trim > env
        refused += over
        print(f"clk {clk:>11} Hz: gain_m {m} ilim {ilim} sustained trim {trim} "
              f"({trim * unit_ppm:.1f} ppm) envelope {env} ({env * unit_ppm:.1f} ppm) "
              f"{'REFUSED' if over else 'inside'}")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
