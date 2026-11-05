#!/usr/bin/env python3
"""Reviewer probe: plant extra PHY-init mutants into a temporary copy of the
firmware translation and report whether the pin-level peer (phy_host.c) fails.

Usage: python3 -B phy_extra_mutants.py <repo-root>
Nothing in <repo-root> is written; every build lives in a temporary directory.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402
import test_phy_firmware as phy  # noqa: E402

MUTANTS = {
    # register 4 loses its pause bits 10 and 11, which the init claims to keep
    "drop-pause": ("#define PHY_ANAR_BELOW_GIGABIT 0x03e0u",
                   "#define PHY_ANAR_BELOW_GIGABIT 0x0fe0u"),
    # register 4 reserved bit 14 no longer cleared
    "keep-reserved-4.14": ("~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));",
                           "~(PHY_ANAR_BELOW_GIGABIT));"),
    # register 9 MASTER-SLAVE bits 12 to 10 dropped instead of kept
    "drop-master-slave": ("((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |",
                          "((unsigned int)gigabit & 0u) |"),
    # register 9 test-mode bits 15 to 13 kept instead of zeroed
    "keep-test-mode": ("#define PHY_GBCR_MASTER_SLAVE 0x1c00u",
                       "#define PHY_GBCR_MASTER_SLAVE 0xfc00u"),
    # restart leaves ISOLATE as read
    "restart-keeps-isolate": ("~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE));",
                              "~(PHY_BMCR_RESET));"),
    # restart asserts RESET (control check must catch)
    "restart-sets-reset": ("PHY_BMCR_AN_RESTART) &\n\t\t       ~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE));",
                           "PHY_BMCR_AN_RESTART | PHY_BMCR_RESET) &\n\t\t       ~(PHY_BMCR_ISOLATE));"),
    # ability gate on 1000BASE-T half duplex (15.12) instead of full (15.13)
    "gate-on-half-duplex": ("#define PHY_ESTATUS_1000_FULL 0x2000u",
                            "#define PHY_ESTATUS_1000_FULL 0x1000u"),
    # register 4 never written
    "no-register-4-write": ("\tphy_mdio_write(4, (unsigned int)advertisement &\n"
                            "\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));\n",
                            "\t(void)advertisement;\n"),
}


def main() -> int:
    source = nvm.FIRMWARE.read_text()
    rows = []
    with tempfile.TemporaryDirectory(prefix="r775-phy-") as temporary:
        work = Path(temporary)
        nvm.make_bench(ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work, source)
        phy.phy_csr(work)
        driver = ROOT / "sw/firmware/nvm_hosttest/phy_host.c"
        command = ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", "-Wno-format",
                   "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
                   f"-I{work}", f"-I{nvm.STUBS}", str(driver), "-o", str(work / "phy")]
        for name, (anchor, plant) in [("none", (None, None)), *MUTANTS.items()]:
            text = nvm.FENCE_RE.sub("(void)0;", source)
            if anchor is not None:
                if text.count(anchor) != 1:
                    rows.append((name, "ANCHOR-NOT-UNIQUE", ""))
                    continue
                text = text.replace(anchor, plant)
            (work / "milan_baremetal.c").write_text(text)
            subprocess.run(command, check=True, timeout=120)
            r = subprocess.run([str(work / "phy")], capture_output=True, text=True, timeout=120)
            assertion = next((l for l in r.stderr.splitlines() if "Assertion" in l), "")
            verdict = "PASS" if r.returncode == 0 else "FAIL"
            if name != "none":
                verdict = "ESCAPED" if r.returncode == 0 else "CAUGHT"
            adv = next((l for l in r.stdout.splitlines() if l.startswith("PHY_ADVERTISEMENT")), "")
            rows.append((name, verdict, assertion.split("Assertion")[-1].strip() or adv))
    for row in rows:
        print("R775_PHY_PROBE %-24s %-8s %s" % row)
    return 0


if __name__ == "__main__":
    sys.exit(main())
