#!/usr/bin/env python3
"""Plant extra PHY-init defects into a copy of the firmware and report what the pin-level peer does.

Usage: phy_probe.py <clone> <work-dir> [name-regex]. Nothing is written to the clone. Each probe is
(name, firmware replacements, phy_host.c replacements). CAUGHT names the first failed assertion.
"""
import re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(clone / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm
import test_phy_firmware as phy

source = nvm.FIRMWARE.read_text()
driver = (clone / "sw/firmware/nvm_hosttest/phy_host.c").read_text()
R4, R9K, GUARD = phy.REGISTER_4_VALUE, phy.REGISTER_9_KEEP, phy.READ_GUARD
R0 = ("((unsigned int)control | PHY_BMCR_AN_ENABLE |\n\t\t\t   PHY_BMCR_AN_RESTART) &\n"
      "\t\t       ~(PHY_BMCR_RESET | PHY_BMCR_ISOLATE)")
probes = {}

def add(name, fw=(), host=()):
    probes[name] = (fw, host)

add("baseline")
for bit in (15, 13, 12):
    mask = f"0x{1 << bit:04x}u"
    add(f"force-bit-4.{bit}", [(R4, f"{mask} | ({R4})")])
    add(f"drop-bit-4.{bit}", [(R4, R4.replace("~(", f"~({mask} | "))])
for bit in (14, 13, 11, 8, 7, 6):
    mask = f"0x{1 << bit:04x}u"
    add(f"force-bit-0.{bit}", [(R0, f"{mask} | ({R0})")])
    add(f"drop-bit-0.{bit}", [(R0, f"~{mask} & ({R0})")])
# whole-field shapes a single-bit table does not name
add("selector-constant-802.3", [(R4, f"(({R4}) & ~0x001fu) | 0x0001u")])
add("pause-swapped", [(R4, f"(({R4}) & ~0x0c00u) | ((({R4}) & 0x0400u) << 1) | ((({R4}) & 0x0800u) >> 1)")])
add("master-slave-constant-auto", [(R9K, "0x0000u |")])
add("master-slave-inverted", [(R9K, "((~(unsigned int)gigabit) & PHY_GBCR_MASTER_SLAVE) |")])
# refused reads: no retry, and a guard moved between the writes
add("guard-no-retry", [(GUARD, GUARD.replace("return 0;", "return 1;"))])
add("reg4-guard-after-reg9-write",
    [(GUARD, GUARD.replace("advertisement < 0 || ", "")),
     ("\tphy_mdio_write(4, (unsigned int)advertisement &", "\tif (advertisement < 0)\n\t\treturn 0;\n\tphy_mdio_write(4, (unsigned int)advertisement &")])
add("reg0-guard-after-reg4-write",
    [(GUARD, GUARD.replace(" || control < 0", "")),
     ("\tphy_mdio_write(0, ((unsigned int)control | PHY_BMCR_AN_ENABLE |", "\tif (control < 0)\n\t\treturn 0;\n\tphy_mdio_write(0, ((unsigned int)control | PHY_BMCR_AN_ENABLE |")])
# the fix's own necessity: each table mutant against a peer with one arm's opposite state removed
ARM1 = [("registers[4] = 0x4be1;", "registers[4] = 0x47fe;"), ("registers[9] = 0xf5ff;", "registers[9] = 0xe9ff;")]
ARM2 = [("registers[4] = 0x47fe;", "registers[4] = 0x4be1;"), ("registers[9] = 0xe9ff;", "registers[9] = 0xf5ff;")]
OLD = [("registers[4] = 0x4be1;", "registers[4] = 0x4fe1;"), ("registers[9] = 0xf5ff;", "registers[9] = 0xfdff;"),
       ("registers[4] = 0x47fe;", "registers[4] = 0x4fe1;"), ("registers[9] = 0xe9ff;", "registers[9] = 0xfdff;")]
kept = {k: v for k, v in phy.ADVERTISEMENT_MUTANTS.items()
        if v[2] in ("selector_kept", "pause_bits_kept", "master_slave_kept")}
for label, host in (("arm1-as-arm2", ARM1), ("arm2-as-arm1", ARM2), ("prior-start-values", OLD)):
    for name, (old, new, _) in kept.items():
        add(f"{label}:{name}", [(old, new)], host)

# the round 2 probes, rerun at this head
add("r2-nak-reg9-unguarded", [(GUARD, GUARD.replace("gigabit < 0 || ", ""))])
add("r2-nak-reg4-unguarded", [(GUARD, GUARD.replace("advertisement < 0 || ", ""))])
add("r2-nak-reg0-unguarded", [(GUARD, GUARD.replace(" || control < 0", ""))])
add("r2-bmsr-unacked-still-inits", [("\tif (!phy_advertised && bmsr >= 0)\n", "\tif (!phy_advertised)\n")])
add("r2-write-frame-no-release", [("\t\tphy_mdio_bit(1, (frame >> (31u - i)) & 1u);\n\tmilan_mac_phy_mdio_w_write(0);\n",
                                   "\t\tphy_mdio_bit(1, (frame >> (31u - i)) & 1u);\n")])
if len(sys.argv) > 3:
    probes = {k: v for k, v in probes.items() if re.search(sys.argv[3], k)}

def run(item):
    name, (fw, host) = item
    d = work / re.sub(r"[^A-Za-z0-9_.-]", "_", name)
    d.mkdir(parents=True, exist_ok=True)
    nvm.make_bench(nvm.ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", d, source)
    phy.phy_csr(d)
    text = nvm.FENCE_RE.sub("(void)0;", source)
    for old, new in fw:
        if text.count(old) < 1:
            return name, "ANCHOR-MISSING " + old[:40]
        text = text.replace(old, new)
    host_text = driver
    for old, new in host:
        if host_text.count(old) != 1:
            return name, "HOST-ANCHOR-MISSING " + old
        host_text = host_text.replace(old, new)
    (d / "milan_baremetal.c").write_text(text)
    (d / "phy_host.c").write_text(host_text)
    (d / "phy_peer.h").write_text((clone / "sw/firmware/nvm_hosttest/phy_peer.h").read_text())
    cmd = ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Werror", "-Wno-format", "-ffunction-sections",
           "-fdata-sections", "-Wl,--gc-sections", f"-I{d}", f"-I{nvm.STUBS}", str(d / "phy_host.c"), "-o", str(d / "phy")]
    built = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if built.returncode:
        return name, "BUILD-FAILED " + built.stderr[:200]
    got = subprocess.run([str(d / "phy")], capture_output=True, text=True, timeout=120)
    if got.returncode == 0:
        return name, "ESCAPED (all assertions pass)"
    m = re.search(r"Assertion `(.+?)' failed", got.stderr)
    return name, "CAUGHT by " + (m.group(1) if m else got.stderr[:120])

with ThreadPoolExecutor(12) as pool:
    for name, verdict in pool.map(run, probes.items()):
        print(f"{name}: {verdict}", flush=True)
