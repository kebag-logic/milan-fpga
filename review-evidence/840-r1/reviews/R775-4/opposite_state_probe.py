#!/usr/bin/env python3
"""Fault probe for the round's two kept register 0 bits.

Run from a disposable export of the head: argv[1] is the tree. Each scenario
edits a copy of phy_host.c, each mutant comes from the table the test ships,
and the row records whether the mutant was caught, by which assertion, and how
many gigabit arms had passed before the abort.
"""
import re, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm
import test_phy_firmware as phy

HOST = (tree / "sw/firmware/nvm_hosttest/phy_host.c").read_text()
ARM1 = "registers[0] = 0x9c00;"
ARM2 = "registers[0] = 0x6100;"
ASSERT_PD = "\tassert(power_down_kept);\n"
ASSERT_LB = "\tassert(loopback_kept);\n"
for anchor in (ARM1, ARM2, ASSERT_PD, ASSERT_LB):
    assert HOST.count(anchor) == 1, anchor
BITS = ("force-bit-0.11", "drop-bit-0.11", "force-bit-0.14", "drop-bit-0.14")
SCENARIOS = (
    ("head", HOST, {m: True for m in BITS}),
    ("arm1-power-down-clear-0x9400", HOST.replace(ARM1, "registers[0] = 0x9400;"),
     {"force-bit-0.11": True, "drop-bit-0.11": False}),
    ("arm2-power-down-set-0x6900", HOST.replace(ARM2, "registers[0] = 0x6900;"),
     {"force-bit-0.11": False, "drop-bit-0.11": True}),
    ("arm1-loopback-set-0xdc00", HOST.replace(ARM1, "registers[0] = 0xdc00;"),
     {"force-bit-0.14": False, "drop-bit-0.14": True}),
    ("arm2-loopback-clear-0x2100", HOST.replace(ARM2, "registers[0] = 0x2100;"),
     {"force-bit-0.14": True, "drop-bit-0.14": False}),
    ("power-down-assert-removed", HOST.replace(ASSERT_PD, ""),
     {"force-bit-0.11": False, "drop-bit-0.11": False}),
    ("loopback-assert-removed", HOST.replace(ASSERT_LB, ""),
     {"force-bit-0.14": False, "drop-bit-0.14": False}),
)
#: firmware defects the table does not spell, graded by the head's assertions
EXTRA = {
    "rebuild-register-0-from-constants":
        (phy.REGISTER_0_VALUE, "(0u * (unsigned int)control) | PHY_BMCR_AN_ENABLE | PHY_BMCR_AN_RESTART",
         "power_down_kept"),
    "clear-power-down-and-loopback-together":
        (phy.REGISTER_0_VALUE, phy.REGISTER_0_VALUE.replace("~(", "~(0x4800u | "), "power_down_kept"),
    "force-power-down-and-loopback-together":
        (phy.REGISTER_0_VALUE, f"0x4800u | ({phy.REGISTER_0_VALUE})", "loopback_kept"),
}

source = nvm.FIRMWARE.read_text()
bad = 0
with tempfile.TemporaryDirectory(prefix="r775-phy-", dir=sys.argv[2]) as temporary:
    work = Path(temporary)
    nvm.make_bench(nvm.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work, source)
    phy.phy_csr(work)

    def run(host, name, plant):
        text = nvm.FENCE_RE.sub("(void)0;", source)
        if plant:
            assert text.count(plant[0]) == 1, name
            text = text.replace(plant[0], plant[1])
        (work / "milan_baremetal.c").write_text(text)
        driver = work / "phy_host.c"
        driver.write_text(host)
        (work / "phy_peer.h").write_text((tree / "sw/firmware/nvm_hosttest/phy_peer.h").read_text())
        subprocess.run(["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Wno-format",
                        "-Wno-unused-variable", "-ffunction-sections", "-fdata-sections",
                        "-Wl,--gc-sections", f"-I{work}", f"-I{nvm.STUBS}", str(driver),
                        "-o", str(work / "phy")], check=True, timeout=120)
        got = subprocess.run(["stdbuf", "-oL", str(work / "phy")], capture_output=True,
                             text=True, timeout=120)
        named = re.search(r"Assertion `([^']+)' failed", got.stderr)
        return got.returncode, named[1] if named else "-", got.stdout.count("PHY_ADVERTISEMENT")

    for label, host, expected in SCENARIOS:
        rc, named, arms = run(host, "none", None)
        print(f"{label} unmutated rc={rc} assertion={named} arms_passed={arms}")
        if rc:
            bad += 1
        for mutant, caught in expected.items():
            anchor, plant, wanted = phy.ADVERTISEMENT_MUTANTS[mutant]
            rc, named, arms = run(host, mutant, (anchor, plant))
            ok = (rc != 0 and named == wanted) if caught else rc == 0
            bad += not ok
            print(f"{label} {mutant} rc={rc} assertion={named} arms_passed={arms} "
                  f"expected={'caught' if caught else 'escape'} {'AS-PREDICTED' if ok else 'UNEXPECTED'}")
    for name, (anchor, plant, wanted) in EXTRA.items():
        rc, named, arms = run(HOST, name, (anchor, plant))
        ok = rc != 0 and named == wanted
        bad += not ok
        print(f"extra {name} rc={rc} assertion={named} arms_passed={arms} {'AS-PREDICTED' if ok else 'UNEXPECTED'}")
print("UNEXPECTED_ROWS", bad)
sys.exit(1 if bad else 0)
