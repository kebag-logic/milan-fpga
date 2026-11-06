#!/usr/bin/env python3
"""Disposable falsification probes for the PHY peer at a given clone.

usage: phy_probe.py <repo> <workdir> [jobs]
Compiles phy_host.c against planted copies of the firmware, in <workdir> only,
and reports for every (driver variant, firmware mutant) pair the first failed
assertion, or ESCAPED when the driver still exits 0.
"""
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 12
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm      # noqa: E402
import test_phy_firmware as phy      # noqa: E402

work.mkdir(parents=True, exist_ok=True)
source = nvm.FENCE_RE.sub("(void)0;", nvm.FIRMWARE.read_text())
nvm.make_bench(nvm.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "base", nvm.FIRMWARE.read_text())
phy.phy_csr(work / "base")
driver_src = (repo / "sw/firmware/nvm_hosttest/phy_host.c").read_text()
peer_src = repo / "sw/firmware/nvm_hosttest/phy_peer.h"

R4 = phy.REGISTER_4_VALUE
R9 = phy.REGISTER_9_KEEP
R0_CLEAR = "~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE));"
R0_SET = "((unsigned int)control | PHY_BMCR_AN_ENABLE |\n"
GUARD = phy.READ_GUARD

extra = {}
# bits the code keeps as read but which no tabled field names
for bit in (15, 13, 12):
    m = f"0x{1 << bit:04x}u"
    extra[f"x-force-4.{bit}"] = (R4, f"{m} | ({R4})")
    extra[f"x-drop-4.{bit}"] = (R4, R4.replace("~(", f"~({m} | "))
for bit in (14, 13, 11, 8, 7, 6, 5, 0):
    m = f"0x{1 << bit:04x}u"
    extra[f"x-force-0.{bit}"] = (R0_SET, f"((unsigned int)control | {m} | PHY_BMCR_AN_ENABLE |\n")
    extra[f"x-drop-0.{bit}"] = (R0_CLEAR, f"~({m} | PHY_BMCR_RESET | PHY_BMCR_ISOLATE));")
# refusal arms not tabled
extra["x-nak-reg9-not-checked"] = (GUARD, GUARD.replace(" || gigabit < 0", ""))
extra["x-nak-gives-up"] = (GUARD, GUARD.replace("return 0;", "return 1;"))
extra["x-reg4-check-after-reg9-write"] = (
    GUARD + "\tphy_mdio_write(9, ((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);\n",
    "\tif (gigabit < 0 || control < 0)\n\t\treturn 0;\n"
    "\tphy_mdio_write(9, ((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);\n"
    "\tif (advertisement < 0)\n\t\treturn 0;\n")
extra["x-reg0-check-after-reg9-write"] = (
    GUARD + "\tphy_mdio_write(9, ((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);\n",
    "\tif (advertisement < 0 || gigabit < 0)\n\t\treturn 0;\n"
    "\tphy_mdio_write(9, ((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);\n"
    "\tif (control < 0)\n\t\treturn 0;\n")
# field-shaped defects
extra["x-selector-constant"] = (R4, f"0x0001u | ({R4} & ~0x001fu)")
extra["x-selector-low-bit-only"] = (R4, f"({R4}) & ~0x001eu")
extra["x-pause-swapped"] = (R4, f"(({R4}) & ~0x0c00u) | ((((unsigned int)advertisement >> 1) & 0x0400u) | (((unsigned int)advertisement << 1) & 0x0800u))")
extra["x-ms-constant-101"] = (R9, "0x1400u |")
extra["x-ms-constant-010"] = (R9, "0x0800u |")
extra["x-ms-inverted"] = (R9, "(~(unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |")
extra["x-wrong-read-reg5-for-reg4"] = ("advertisement = phy_mdio_read(4);", "advertisement = phy_mdio_read(5);")
extra["x-wrong-read-reg10-for-reg9"] = ("gigabit = phy_mdio_read(9);", "gigabit = phy_mdio_read(10);")
# kept only while auto-negotiation is off/on: correlated with the arm that holds the bit
extra["x-drop-pause10-when-an-on"] = (R4, f"({R4}) & (((unsigned int)control & PHY_BMCR_AN_ENABLE) ? ~0x0400u : ~0u)")
extra["x-force-pause10-when-an-off"] = (R4, f"({R4}) | (((unsigned int)control & PHY_BMCR_AN_ENABLE) ? 0u : 0x0800u)")

table = {k: (v[0], v[1]) for k, v in phy.ADVERTISEMENT_MUTANTS.items()}
names = {k: v[2] for k, v in phy.ADVERTISEMENT_MUTANTS.items()}


def variant_drivers():
    """Driver variants: the head, each arm start reverted, each refusal arm removed."""
    head = driver_src
    out = {"head": head}
    # both arms at the previous all-one start of the kept pause and MASTER-SLAVE bits
    v = head.replace("registers[4] = 0x4be1;", "registers[4] = 0x4fe1;").replace("registers[9] = 0xf5ff;", "registers[9] = 0xfdff;")
    v = v.replace("registers[4] = 0x47fe;", "registers[4] = 0x4fe1;").replace("registers[9] = 0xe9ff;", "registers[9] = 0xfdff;")
    out["prior-starts"] = v
    # second arm collapsed onto the first
    out["arm2-equals-arm1"] = head.replace("registers[4] = 0x47fe;", "registers[4] = 0x4be1;").replace("registers[9] = 0xe9ff;", "registers[9] = 0xf5ff;")
    # refusal arms removed
    v = re.sub(r"\tnak_register = 4;\n.*?\tnak_register = 0;\n", "\tnak_register = 0;\n", head, flags=re.S)
    assert v != head
    out["no-reg4-arm"] = v
    v = re.sub(r"\tnak_register = 0;\n.*?\tnak_register = 32;\n", "\tnak_register = 32;\n", head, count=1, flags=re.S)
    assert v != head
    out["no-reg0-arm"] = v
    return out


def one(variant, text, name, anchor, plant):
    d = work / "runs" / variant / name
    d.mkdir(parents=True, exist_ok=True)
    fw = source
    if anchor is not None:
        if fw.count(anchor) != 1:
            return variant, name, "ANCHOR-ERROR"
        fw = fw.replace(anchor, plant)
    (d / "milan_baremetal.c").write_text(fw)
    (d / "phy_host.c").write_text(text)
    shutil.copy(peer_src, d / "phy_peer.h")
    cmd = ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Wno-format", "-ffunction-sections",
           "-fdata-sections", "-Wl,--gc-sections", f"-I{d}", f"-I{work / 'base'}", f"-I{nvm.STUBS}",
           str(d / "phy_host.c"), "-o", str(d / "phy")]
    c = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if c.returncode:
        return variant, name, "COMPILE-ERROR " + c.stderr[-300:].replace("\n", " ")
    r = subprocess.run([str(d / "phy")], capture_output=True, text=True, timeout=120)
    m = re.search(r"Assertion `(.+?)' failed", r.stderr)
    shutil.rmtree(d)
    if r.returncode == 0:
        return variant, name, "ESCAPED"
    return variant, name, m.group(1) if m else f"rc={r.returncode}"


tasks = []
variants = variant_drivers()
tasks.append(("head", variants["head"], "none", None, None))
for k, (a, p) in {**table, **extra}.items():
    tasks.append(("head", variants["head"], k, a, p))
for var in ("prior-starts", "arm2-equals-arm1"):
    tasks.append((var, variants[var], "none", None, None))
    for k, (a, p) in table.items():
        if k.startswith(("force-", "drop-bit", "clear-pause", "drop-master")):
            tasks.append((var, variants[var], k, a, p))
for var, k in (("no-reg4-arm", "nak-reg4-not-checked"), ("no-reg0-arm", "nak-reg0-not-checked")):
    tasks.append((var, variants[var], "none", None, None))
    tasks.append((var, variants[var], k, *table[k]))

with cf.ThreadPoolExecutor(jobs) as ex:
    results = list(ex.map(lambda t: one(*t), tasks))
for var, name, res in results:
    want = names.get(name, "-")
    verdict = "" if want == "-" else ("named" if res == want else "NOT-NAMED")
    print(f"{var}\t{name}\t{res}\t{want}\t{verdict}")
