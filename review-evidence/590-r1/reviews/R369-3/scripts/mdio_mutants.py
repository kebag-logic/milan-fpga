#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Reviewer probe: MDIO framing mutants against the committed host PHY peer.

Usage: mdio_mutants.py <repo-root> <work-dir>
Builds the committed sw/firmware/nvm_hosttest/phy_host.c exactly as
test_phy_firmware.py does and plants reviewer-chosen framing defects into a
copy of the unchanged firmware. Each defect must make phy_host abort; the
equivalent LiteX-style sample (no settle delay before the low-phase read) is
expected to pass because the peer's output is stable across the low phase.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402

TA = "\tphy_mdio_bit(0, 0);\n\tack = phy_mdio_bit(0, 0);\n"
SAMPLE = "\tmilan_mac_phy_mdio_w_write(pins);\n\tcdelay(32);\n\tvalue = milan_mac_phy_mdio_r_read() & 1u;\n"
MUTANTS = {
    "none": None,
    "one-turnaround": (TA, "\tack = phy_mdio_bit(0, 0);\n"),
    "three-turnaround": (TA, "\tphy_mdio_bit(0, 0);\n\tphy_mdio_bit(0, 0);\n\tack = phy_mdio_bit(0, 0);\n"),
    "ack-ignored": ("\treturn ack ? -1 : (int)value;", "\t(void)ack;\n\treturn (int)value;"),
    "fifteen-data": ("\tfor (i = 0; i < 16u; ++i)\n\t\tvalue = (value << 1)",
                     "\tfor (i = 0; i < 15u; ++i)\n\t\tvalue = (value << 1)"),
    "read-opcode-write": ("(6u << 10)", "(5u << 10)"),
    "sample-without-settle(equivalent)": (SAMPLE, "\tmilan_mac_phy_mdio_w_write(pins);\n"
                                          "\tvalue = milan_mac_phy_mdio_r_read() & 1u;\n\tcdelay(32);\n"),
}
work.mkdir(parents=True, exist_ok=True)
source = nvm.FIRMWARE.read_text()
nvm.make_bench(root / "configs/endstation_ax7101_1x1_tdm8.yaml", work, source)
(work / "generated/csr.h").write_text(
    f'#include "{nvm.STUBS / "generated/csr.h"}"\n#define CSR_MILAN_MAC_PHY_MDIO_W_ADDR 1\n')
driver = root / "sw/firmware/nvm_hosttest/phy_host.c"
command = ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", "-Wno-format",
           "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
           f"-I{work}", f"-I{nvm.STUBS}", str(driver), "-o", str(work / "phy")]
for label, plant in MUTANTS.items():
    text = nvm.FENCE_RE.sub("(void)0;", source)
    if plant:
        old, new = plant
        assert text.count(old) == 1, label + " anchor not unique"
        text = text.replace(old, new)
    (work / "milan_baremetal.c").write_text(text)
    subprocess.run(command, check=True, timeout=120)
    r = subprocess.run([str(work / "phy")], capture_output=True, text=True, timeout=120)
    tail = (r.stderr.strip().splitlines() or [""])[-1][-110:]
    verdict = "PASS(PHY_OK)" if r.returncode == 0 and "PHY_OK" in r.stdout else f"KILLED rc={r.returncode} {tail}"
    print(f"{label:<36} {verdict}")
