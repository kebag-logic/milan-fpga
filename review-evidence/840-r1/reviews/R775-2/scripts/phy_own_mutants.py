#!/usr/bin/env python3
"""Reviewer's disposable PHY-init mutants, planted in a temporary copy.

Usage: phy_own_mutants.py <repo>. Each mutant is compiled against the head's
phy_host.c and pin-level peer; the report names the failing assertion or says
the mutant escaped. Nothing in the repository is modified.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

repo = pathlib.Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / 'sw/firmware/nvm_hosttest'))
sys.dont_write_bytecode = True
import test_nvm_firmware as nvm  # noqa: E402
import test_phy_firmware as phy  # noqa: E402

COND = "\tif (advertisement < 0 || gigabit < 0 || control < 0)\n\t\treturn 0;\n"
MUTANTS = {
    # the documented retry on an unacknowledged read of each register
    "nak-reg4-not-checked": (COND, "\tif (gigabit < 0 || control < 0)\n\t\treturn 0;\n"),
    "nak-reg9-not-checked": (COND, "\tif (advertisement < 0 || control < 0)\n\t\treturn 0;\n"),
    "nak-reg0-not-checked": (COND, "\tif (advertisement < 0 || gigabit < 0)\n\t\treturn 0;\n"),
    "nak-retry-given-up": (COND, "\tif (advertisement < 0 || gigabit < 0 || control < 0)\n\t\treturn 1;\n"),
    "nak-ability-given-up": ("\tif (extended < 0)\n\t\treturn 0;\n", "\tif (extended < 0)\n\t\treturn 1;\n"),
    # the poll's status read failing, with the init run all the same
    "init-on-failed-bmsr": ("\tif (!phy_advertised && bmsr >= 0)\n", "\tif (!phy_advertised)\n"),
    # register 4 bits the page does not name as kept
    "clear-next-page": ("#define PHY_ANAR_RESERVED 0x4000u", "#define PHY_ANAR_RESERVED 0xc000u"),
    "clear-remote-fault": ("#define PHY_ANAR_RESERVED 0x4000u", "#define PHY_ANAR_RESERVED 0x6000u"),
    "clear-selector": ("#define PHY_ANAR_RESERVED 0x4000u", "#define PHY_ANAR_RESERVED 0x401fu"),
    # register 0 rewritten from constants, not from the read
    "reg0-from-constant": ("(unsigned int)control | PHY_BMCR_AN_ENABLE |", "0u * (unsigned int)control | PHY_BMCR_AN_ENABLE |"),
    # register 9 written before its partner, order swapped (no contract on this order)
    "write-4-before-9": (phy.ADVERTISEMENT_WRITES,
                         "\tphy_mdio_write(4, (unsigned int)advertisement &\n"
                         "\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));\n"
                         "\tphy_mdio_write(9, ((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |\n"
                         "\t\t       PHY_GBCR_1000_FULL);\n"),
    # a "kept" field forced to ones: the peer only ever starts these bits at one
    "force-pause-on": ("phy_mdio_write(4, (unsigned int)advertisement &\n\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));",
                       "phy_mdio_write(4, 0x0c00u | ((unsigned int)advertisement &\n\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED)));"),
    "force-manual-master": ("PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);",
                            "PHY_GBCR_MASTER_SLAVE) | 0x1c00u |\n\t\t       PHY_GBCR_1000_FULL);"),
    "force-manual-config-only": ("PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);",
                                 "PHY_GBCR_MASTER_SLAVE) | 0x1000u |\n\t\t       PHY_GBCR_1000_FULL);"),
    # frame shape: wrong turnaround, wrong start, wrong PHY address
    "write-ta-11": ("(2u << 16) | (value & 0xffffu);", "(3u << 16) | (value & 0xffffu);"),
    "write-to-phy-0": ("uint32_t frame = (5u << 28) | (phy_address << 23) | (reg << 18) |",
                       "uint32_t frame = (5u << 28) | (0u * phy_address << 23) | (reg << 18) |"),
    "write-short-preamble": ("\tfor (i = 0; i < 32u; ++i)\n\t\tphy_mdio_bit(1, 1);\n\tfor (i = 0; i < 32u; ++i)\n",
                             "\tfor (i = 0; i < 31u; ++i)\n\t\tphy_mdio_bit(1, 1);\n\tfor (i = 0; i < 32u; ++i)\n"),
    # the init marked done before the poll that found the PHY
    "advertised-from-boot": ("static int phy_advertised;", "static int phy_advertised = 1;"),
    # the gate reads the wrong register-1 bit
    "gate-on-an-done": ("\tif (!(bmsr & PHY_BMSR_EXTENDED))\n\t\treturn 1;\n", "\tif (!(bmsr & PHY_BMSR_AN_DONE))\n\t\treturn 1;\n"),
}

source = nvm.FIRMWARE.read_text()
escaped = []
with tempfile.TemporaryDirectory(prefix='r775-phy-') as tmp:
    work = pathlib.Path(tmp)
    nvm.make_bench(repo / 'configs/endstation_ax7101_1x1_tdm8.yaml', work, source)
    phy.phy_csr(work)
    driver = repo / 'sw/firmware/nvm_hosttest/phy_host.c'
    command = ['gcc', '-std=gnu11', '-O1', '-Wall', '-Wextra', '-Werror', '-Wno-format',
               '-ffunction-sections', '-fdata-sections', '-Wl,--gc-sections',
               f'-I{work}', f'-I{nvm.STUBS}', str(driver), '-o', str(work / 'phy')]
    for name, (old, new) in MUTANTS.items():
        text = nvm.FENCE_RE.sub('(void)0;', source)
        assert text.count(old) == 1, name
        (work / 'milan_baremetal.c').write_text(text.replace(old, new))
        built = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if built.returncode:
            print(f'{name}: DID NOT COMPILE {built.stderr[-200:]}')
            continue
        run = subprocess.run([str(work / 'phy')], capture_output=True, text=True, timeout=120)
        hit = re.search(r"Assertion `(.+?)' failed", run.stderr)
        if run.returncode == 0:
            escaped.append(name)
            print(f'{name}: ESCAPED (rc 0)')
        else:
            print(f'{name}: caught by {hit[1] if hit else run.stderr[-120:]}')
print('escaped:', escaped)
