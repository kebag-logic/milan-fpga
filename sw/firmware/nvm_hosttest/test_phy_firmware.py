#!/usr/bin/env python3
# SPDX-License-Identifier: (GPL-2.0 OR MIT)
"""Drive the firmware's bit-bang transactions and kill a missing publisher."""
from pathlib import Path
import subprocess
import tempfile

import test_nvm_firmware as nvm


def main() -> None:
    """Compile the product translation with a pin-level peer and unchanged policy."""
    source = nvm.FIRMWARE.read_text()
    with tempfile.TemporaryDirectory(prefix="milan-phy-") as temporary:
        work = Path(temporary)
        nvm.make_bench(nvm.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work, source)
        (work / "generated/csr.h").write_text(
            f'#include "{nvm.STUBS / "generated/csr.h"}"\n'
            '#define CSR_MILAN_MAC_PHY_MDIO_W_ADDR 1\n')
        driver = Path(__file__).with_name("phy_host.c")
        command = ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", "-Wno-format",
                   "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
                   f"-I{work}", f"-I{nvm.STUBS}", str(driver), "-o", str(work / "phy")]
        for mutant in ("none", "no-publish", "defer-recovery", "late-sample"):
            text = nvm.FENCE_RE.sub("(void)0;", source)
            if mutant == "no-publish":
                anchor = "\tmilan_mac_link_status_write(status);"
                if text.count(anchor) != 1:
                    raise RuntimeError("publisher mutation anchor is not unique")
                text = text.replace(anchor, "\t(void)status;")
                text = text.replace("milan_mac_link_status_write(0);", "(void)0;")
            elif mutant == "late-sample":
                anchor = ("\tvalue = milan_mac_phy_mdio_r_read() & 1u;\n"
                          "\tmilan_mac_phy_mdio_w_write(pins | PHY_MDC);\n\tcdelay(32);")
                if text.count(anchor) != 1:
                    raise RuntimeError("phase mutation anchor is not unique")
                text = text.replace(anchor,
                                    "\tmilan_mac_phy_mdio_w_write(pins | PHY_MDC);\n"
                                    "\tcdelay(32);\n\tvalue = milan_mac_phy_mdio_r_read() & 1u;")
            elif mutant == "defer-recovery":
                anchor = ("\tif (bmsr >= 0 && !(bmsr & PHY_BMSR_LINK) && (phy_published & 1u)) {\n"
                          "\t\tmilan_mac_link_status_write(0);\n"
                          "\t\tphy_published = 0;\n\t}\n")
                if text.count(anchor) != 1:
                    raise RuntimeError("recovery mutation anchor is not unique")
                text = text.replace(anchor, "")
            (work / "milan_baremetal.c").write_text(text)
            subprocess.run(command, check=True, timeout=120)
            result = subprocess.run([str(work / "phy")], capture_output=True, text=True, timeout=120)
            if mutant == "none":
                if result.returncode or "PHY_OK" not in result.stdout:
                    raise RuntimeError(result.stdout + result.stderr)
                print(result.stdout, end="")
            else:
                expected = "publishes > before" if mutant == "no-publish" else "status_word == expected"
                if result.returncode == 0 or expected not in result.stderr:
                    raise RuntimeError(mutant + " escaped its named assertion")
                print("PHY_MUTANT " + mutant + ": caught")


if __name__ == "__main__":
    main()
