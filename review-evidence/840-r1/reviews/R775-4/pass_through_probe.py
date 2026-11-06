#!/usr/bin/env python3
"""Derive the PHY init's bit partition from the firmware's own macros, compare it with the guide's named list, and force and drop every bit the guide calls ungraded.

argv[1] is the head tree, read only; argv[2] is a scratch directory.
"""
import re, subprocess, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm
import test_phy_firmware as phy

source = nvm.FIRMWARE.read_text()
macro = lambda name: int(re.search(rf"#define {name} (0x[0-9a-f]+)u", source)[1], 16)
clear4 = macro("PHY_ANAR_BELOW_GIGABIT") | macro("PHY_ANAR_RESERVED")
set0 = macro("PHY_BMCR_AN_ENABLE") | macro("PHY_BMCR_AN_RESTART")
clear0 = macro("PHY_BMCR_RESET") | macro("PHY_BMCR_ISOLATE")
pass4 = {b for b in range(16) if not clear4 >> b & 1}
pass0 = {b for b in range(16) if not (set0 | clear0) >> b & 1}
graded = {}
for register, bits, _ in phy.KEPT_FIELDS:
    graded.setdefault(register, set()).update(bits)
print("register 4 pass-through", sorted(pass4), "graded", sorted(graded[4]), "other", sorted(pass4 - graded[4]))
print("register 0 pass-through", sorted(pass0), "graded", sorted(graded[0]), "other", sorted(pass0 - graded[0]))
print("register 9 kept mask", hex(macro("PHY_GBCR_MASTER_SLAVE")), "graded", sorted(graded[9]))
print("graded total", sum(len(v) for v in graded.values()), "table size", len(phy.ADVERTISEMENT_MUTANTS))
named4, named0 = {15, 13, 12}, {13, *range(0, 9)}
partition_ok = pass4 - graded[4] == named4 and pass0 - graded[0] == named0
print("guide list equals derived list", partition_ok)
bad = 0 if partition_ok else 1
with tempfile.TemporaryDirectory(prefix="r775-pt-", dir=sys.argv[2]) as temporary:
    work = Path(temporary)
    nvm.make_bench(nvm.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work, source)
    phy.phy_csr(work)
    host = tree / "sw/firmware/nvm_hosttest/phy_host.c"
    for register, bits, value in ((4, sorted(named4), phy.REGISTER_4_VALUE), (0, sorted(named0), phy.REGISTER_0_VALUE)):
        for bit in bits:
            mask = f"0x{1 << bit:04x}u"
            for kind, plant in (("force", f"{mask} | ({value})"), ("drop", value.replace("~(", f"~({mask} | "))):
                text = nvm.FENCE_RE.sub("(void)0;", source)
                assert text.count(value) == 1
                (work / "milan_baremetal.c").write_text(text.replace(value, plant))
                subprocess.run(["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", "-Wno-format",
                                "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
                                f"-I{work}", f"-I{nvm.STUBS}", str(host), "-o", str(work / "phy")],
                               check=True, timeout=120)
                got = subprocess.run([str(work / "phy")], capture_output=True, text=True, timeout=120)
                named = re.search(r"Assertion `([^']+)' failed", got.stderr)
                state = "escaped" if got.returncode == 0 else "caught"
                bad += got.returncode != 0
                print(f"{kind}-bit-{register}.{bit} {state} rc={got.returncode} assertion={named[1] if named else '-'}")
print("rows_not_as_the_guide_says", bad)
sys.exit(1 if bad else 0)
