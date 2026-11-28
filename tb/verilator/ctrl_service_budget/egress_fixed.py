# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Measure the 100 Mb/s egress row's fixed path on the converted MII chain, and hold egress_mii.MII_FIXED_NS to it.

egress_fixed_main.cpp sends one frame at a time through tb/verilator/gptp_txts/generated/mac_tx_chain_mii.v, the
shipping MAC transmit chain on the board's MII stages as sw/litex/gen_mac_tx_model.py converts it, and prints for
each length and each of 8 x 8 clock phases the chain's latency from its boundary's last beat to the last nibble at
its pads, less the frame's wire time. The stated figure is the largest, rounded up to 10 ns; the run exits 1 unless
MII_FIXED_NS is exactly that.

usage: python3 -I egress_fixed.py BUILD_DIR
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import egress_mii

HERE = Path(__file__).resolve().parent
CHAIN = HERE.parents[1] / 'verilator/gptp_txts/generated/mac_tx_chain_mii.v'
#: The least frame, one under it the padding covers, the SR stream's, gPTP's longest, an odd length, the largest.
LENGTHS = (14, 60, 64, 90, 127, 512, 1514)


def build(build_dir: Path) -> Path:
    """Verilate the converted chain with the bench; the executable."""
    build_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(['verilator', '--cc', '--exe', '--build', '-O3', '-Wno-fatal', '--top-module', 'mac_tx_chain_mii',
                    '--Mdir', str(build_dir), '-CFLAGS', '-O2 -std=c++17', str(CHAIN),
                    str(HERE / 'egress_fixed_main.cpp'), '-o', 'Vmac_tx_chain_mii'],
                   check=True, stdout=subprocess.DEVNULL)
    return build_dir / 'Vmac_tx_chain_mii'


def measured(binary: Path) -> dict[int, int]:
    """The largest fixed path at each length, ps."""
    out: dict[int, int] = {}
    text = subprocess.run([str(binary), *map(str, LENGTHS)], check=True, capture_output=True, text=True).stdout
    for line in text.splitlines():
        _, length, _, _, ps = line.split()
        out[int(length)] = max(out.get(int(length), 0), int(ps))
    return out


def main(argv: list[str]) -> int:
    """Build, measure and compare with the stated figure."""
    if len(argv) != 1:
        print(__doc__)
        return 2
    worst = measured(build(Path(argv[0])))
    for length, ps in sorted(worst.items()):
        print(f'length {length}: fixed path at most {ps / 1000:.1f} ns over 64 clock phases')
    stated = -(-max(worst.values()) // 10_000) * 10
    ok = stated == egress_mii.MII_FIXED_NS
    print(f'{"PASS" if ok else "FAIL"}: the most is {max(worst.values()) / 1000:.1f} ns, stated {stated} ns; '
          f'egress_mii.MII_FIXED_NS is {egress_mii.MII_FIXED_NS} ns')
    return int(not ok)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
