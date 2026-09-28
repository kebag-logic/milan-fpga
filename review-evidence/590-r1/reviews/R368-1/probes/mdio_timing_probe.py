#!/usr/bin/env python3
"""Review probe: product firmware MDIO sampling vs peer timing convention.

Usage: python3 -B mdio_timing_probe.py <repo-root> <work-dir>
Builds the unchanged product translation unit (fence stripped exactly as
test_phy_firmware.py does) against mdio_peer_probe.c twice: with the lane's
peer timing and with IEEE 802.3 22.3.4 timing. A 'fixed' arm substitutes a
read that samples the turnaround at the first TA clock (as LiteX libbase and
Linux mdio-bitbang do) to show the standard peer is decodable.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402

probe = Path(__file__).with_name("mdio_peer_probe.c")
work.mkdir(parents=True, exist_ok=True)
nvm.make_bench(root / "configs/endstation_ax7101_1x1_tdm8.yaml", work, nvm.FIRMWARE.read_text())
(work / "generated/csr.h").write_text(
    f'#include "{nvm.STUBS / "generated/csr.h"}"\n#define CSR_MILAN_MAC_PHY_MDIO_W_ADDR 1\n')
source = nvm.FENCE_RE.sub("(void)0;", nvm.FIRMWARE.read_text())
anchor = "\tphy_mdio_bit(0, 0);\n\tack = phy_mdio_bit(0, 0);\n"
assert source.count(anchor) == 1, "anchor"
fixed = source.replace(anchor, "\tack = phy_mdio_bit(0, 0);\n")
anchor2 = "\tmilan_mac_phy_mdio_w_write(0);\n\treturn ack ? -1 : (int)value;"
assert fixed.count(anchor2) == 1, "anchor2"
fixed = fixed.replace(anchor2, "\tphy_mdio_bit(0, 0);\n" + anchor2)
failures = 0
for name, text in (("product", source), ("ta-at-first-clock", fixed)):
    for std in (0, 1):
        (work / "milan_baremetal.c").write_text(text)
        exe = work / f"probe-{name}-{std}"
        subprocess.run(["gcc", "-std=gnu11", "-O1", "-Wall", "-Wno-format",
                        "-Wno-unused-function", f"-DPEER_STD={std}",
                        "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
                        f"-I{work}", f"-I{nvm.STUBS}", str(probe), "-o", str(exe)],
                       check=True, timeout=300)
        r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=120)
        print(f"ARM firmware={name} rc={r.returncode} {r.stdout.strip()}")
