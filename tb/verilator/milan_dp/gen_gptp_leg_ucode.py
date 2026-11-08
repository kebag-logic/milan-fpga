# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate a gPTP leg's engine image from a config, through the builder.

usage: gen_gptp_leg_ucode.py <config.yaml> -o <image.hex>

The image takes the generator options the builder resolves for the config
(`endstation_builder.gptp_ucode_args`), so priority1 and clockAccuracy are
that config's, as the shipping image's are (#843, 802.1AS-2011 8.6.2.3).
Three options are this leg's own and replace the builder's:

  --clk-hz 2000000   the leg's compressed fabric clock (the Makefile's
                     MILAN_CLK_FREQ_HZ), not the board's
  --cease-ms 3000    the leg's cease delay, which its link-loss phases time
  --mac              the generator's default MAC, whose clockIdentity the
                     leg's pathTrace checks name (sim_gptp.cpp THIS_CLOCK)

Build-time artifact, like gptp_ucode.hex was: never tracked, made per make.
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "sw" / "builder"))

import endstation_builder as eb  # noqa: E402

#: The options this leg sets itself, and the values it sets them to.
LEG_OPTIONS = {"--clk-hz": "2000000", "--cease-ms": "3000",
               "--mac": "0x02A1B2C3D4E5"}
#: Every option the builder passes. A new one must be decided here, not
#: dropped or overridden by accident.
BUILDER_OPTIONS = ("--mac", "--p1", "--clk-hz", "--clock-accuracy")


def leg_options(config: Path) -> list[str]:
    """The generator options for `config`'s image in this leg."""
    built = eb.gptp_ucode_args(eb.load_config(str(config)))
    options = dict(zip(built[::2], built[1::2]))
    if tuple(options) != BUILDER_OPTIONS or len(built) != 2 * len(options):
        raise SystemExit(f"gen_gptp_leg_ucode: the builder passes {built}, "
                         f"this leg expects the options {BUILDER_OPTIONS}")
    options.update(LEG_OPTIONS)
    return [part for item in options.items() for part in item]


def main() -> None:
    """Write the leg's image and print the options it was made with."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("config", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    args = ap.parse_args()
    options = leg_options(args.config)
    print(f"{args.out.name}: {args.config.name}: {' '.join(options)}")
    subprocess.run([sys.executable, str(eb.GPTP_UCODE_GENERATOR),
                    "-o", str(args.out), *options], check=True)


if __name__ == "__main__":
    main()
