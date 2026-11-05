#!/usr/bin/env python3
"""Reviewer probe: plant extra PHY-init mutants and report whether the
pin-level peer (phy_host.c) fails on each.  Reuses the head's own bench
builder (test_nvm_firmware.make_bench) and the head's phy_host.c driver.

usage: phy_extra_mutants.py <checkout-root> <work-dir>
Never edits the checkout; every planted copy lives under <work-dir>.
"""
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work_root = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402
import test_phy_firmware as phy  # noqa: E402

MUTANTS = {
    "none": None,
    # register 4: pause bits (10, 11) cleared too; docs say they are kept
    "clear-pause-bits": ("#define PHY_ANAR_BELOW_GIGABIT 0x03e0u",
                         "#define PHY_ANAR_BELOW_GIGABIT 0x0fe0u"),
    # register 9: MASTER-SLAVE bits not kept
    "drop-master-slave": ("((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |",
                          "(0u * (unsigned int)gigabit) |"),
    # register 9: test-mode bits 15:13 kept from the read value
    "keep-test-mode": ("#define PHY_GBCR_MASTER_SLAVE 0x1c00u",
                       "#define PHY_GBCR_MASTER_SLAVE 0xfc00u"),
    # register 4: reserved bit 14 not cleared
    "keep-reserved-bit14": ("#define PHY_ANAR_RESERVED 0x4000u",
                            "#define PHY_ANAR_RESERVED 0x0000u"),
    # register 0: reset / isolate not cleared
    "keep-reset-isolate": ("~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE));",
                           "~0u);"),
    # register 0: auto-negotiation enable not forced on
    "no-an-enable": ("((unsigned int)control | PHY_BMCR_AN_ENABLE |\n",
                     "((unsigned int)control |\n"),
    # a PHY without 1000BASE-T FD ability re-read on every poll
    "no-ability-retry-forever": ("\tif (!(extended & PHY_ESTATUS_1000_FULL))\n\t\treturn 1;\n",
                                 "\tif (!(extended & PHY_ESTATUS_1000_FULL))\n\t\treturn 0;\n"),
    # register 4 never written (sanity: must be caught)
    "skip-register-4": ("\tphy_mdio_write(4, (unsigned int)advertisement &\n"
                        "\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));\n",
                        "\t(void)advertisement;\n"),
}


def main() -> int:
    source = nvm.FIRMWARE.read_text()
    work = work_root / "bench"
    work.mkdir(parents=True, exist_ok=True)
    nvm.make_bench(nvm.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work, source)
    phy.phy_csr(work)
    driver = root / "sw/firmware/nvm_hosttest/phy_host.c"
    command = ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", "-Wno-format",
               "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
               f"-I{work}", f"-I{nvm.STUBS}", str(driver), "-o", str(work / "phy")]
    for name, plant in MUTANTS.items():
        text = nvm.FENCE_RE.sub("(void)0;", source)
        if plant is not None:
            anchor, new = plant
            if text.count(anchor) != 1:
                print(f"PROBE {name}: ANCHOR-NOT-UNIQUE ({text.count(anchor)})")
                continue
            text = text.replace(anchor, new)
        (work / "milan_baremetal.c").write_text(text)
        build = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if build.returncode:
            print(f"PROBE {name}: BUILD-FAILED {build.stderr[-300:]}")
            continue
        result = subprocess.run([str(work / "phy")], capture_output=True, text=True, timeout=120)
        tail = (result.stderr.strip().splitlines() or [""])[-1]
        adv = [l for l in result.stdout.splitlines() if l.startswith("PHY_ADVERTISEMENT")]
        verdict = "CAUGHT" if result.returncode else "SURVIVED"
        print(f"PROBE {name}: {verdict} rc={result.returncode} {adv[0] if adv else ''} {tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
