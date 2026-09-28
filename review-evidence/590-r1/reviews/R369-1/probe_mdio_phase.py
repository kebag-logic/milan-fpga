#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Reviewer probe: firmware MDIO sampling phase against an IEEE-timed peer.

Usage: probe_mdio_phase.py <repo-root> <work-dir>
Builds the unchanged firmware translation unit exactly as
sw/firmware/nvm_hosttest/test_phy_firmware.py does, with probe_mdio_phase.c
as the driver, once per peer phase, and prints what each reader decodes.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
source = nvm.FIRMWARE.read_text()
nvm.make_bench(root / "configs/endstation_ax7101_1x1_tdm8.yaml", work, source)
(work / "generated/csr.h").write_text(
    f'#include "{nvm.STUBS / "generated/csr.h"}"\n'
    '#define CSR_MILAN_MAC_PHY_MDIO_W_ADDR 1\n')
(work / "milan_baremetal.c").write_text(nvm.FENCE_RE.sub("(void)0;", source))
driver = Path(__file__).with_name("probe_mdio_phase.c")
for phase in (0, 1):
    exe = work / f"phase{phase}"
    subprocess.run(["gcc", "-std=gnu11", "-O1", "-Wall", "-Wno-format",
                    "-Wno-unused-function", f"-DPEER_PHASE={phase}",
                    "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
                    f"-I{work}", f"-I{nvm.STUBS}", str(driver), "-o", str(exe)],
                   check=True, timeout=120)
    out = subprocess.run([str(exe)], capture_output=True, text=True, timeout=120, check=True)
    print(out.stdout, end="")
