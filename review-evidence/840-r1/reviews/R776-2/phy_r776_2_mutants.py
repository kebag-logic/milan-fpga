#!/usr/bin/env python3
"""Independent PHY init mutants and a pin-level wire comparison.

usage: phy_r776_2_mutants.py <repo> <work-dir> [<old-firmware-rev> ...]
Every plant is applied to a temporary copy; the repository is only read.
Prints one line per mutant: CAUGHT <assertion> or SURVIVED, and for each
named revision the SHA-256 of the MDIO pin stream and the cdelay total.
"""
import hashlib, re, shutil, subprocess, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); root = Path(sys.argv[2]).resolve(); revs = sys.argv[3:]
sys.path.insert(0, str(repo / 'sw/firmware/nvm_hosttest'))
import test_nvm_firmware as nvm
import test_phy_firmware as phy

GUARD = "\tif (advertisement < 0 || gigabit < 0 || control < 0)\n\t\treturn 0;\n"
M = {
 "nak-reg4-unguarded": (GUARD, "\tif (gigabit < 0 || control < 0)\n\t\treturn 0;\n"),
 "nak-reg0-unguarded": (GUARD, "\tif (advertisement < 0 || gigabit < 0)\n\t\treturn 0;\n"),
 "nak-reg9-unguarded": (GUARD, "\tif (advertisement < 0 || control < 0)\n\t\treturn 0;\n"),
 "bmsr-unacked-still-inits": ("\tif (!phy_advertised && bmsr >= 0)\n", "\tif (!phy_advertised)\n"),
 "no-retry-after-nak": ("\t\tphy_advertised = phy_advertise_gigabit_only((unsigned int)bmsr);\n",
                        "\t\t{ (void)phy_advertise_gigabit_only((unsigned int)bmsr); phy_advertised = 1; }\n"),
 "gate-on-either-1000-ability": ("#define PHY_ESTATUS_1000_FULL 0x2000u", "#define PHY_ESTATUS_1000_FULL 0x3000u"),
 "master-slave-partial": ("#define PHY_GBCR_MASTER_SLAVE 0x1c00u", "#define PHY_GBCR_MASTER_SLAVE 0x0c00u"),
 "pause-partial": ("#define PHY_ANAR_BELOW_GIGABIT 0x03e0u", "#define PHY_ANAR_BELOW_GIGABIT 0x07e0u"),
 "selector-cleared": ("~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));", "~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED | 0x001fu));"),
 "register-9-after-restart": (phy.ADVERTISEMENT_WRITES + phy.RESTART_WRITE,
    "\tphy_mdio_write(4, (unsigned int)advertisement &\n\t\t       ~(PHY_ANAR_BELOW_GIGABIT | PHY_ANAR_RESERVED));\n" + phy.RESTART_WRITE +
    "\tphy_mdio_write(9, ((unsigned int)gigabit & PHY_GBCR_MASTER_SLAVE) |\n\t\t       PHY_GBCR_1000_FULL);\n"),
 "restart-written-twice": (phy.RESTART_WRITE, phy.RESTART_WRITE + phy.RESTART_WRITE),
 "write-frame-no-release": ("\t\tphy_mdio_bit(1, (frame >> (31u - i)) & 1u);\n\tmilan_mac_phy_mdio_w_write(0);\n}\n",
                            "\t\tphy_mdio_bit(1, (frame >> (31u - i)) & 1u);\n}\n"),
 "write-no-preamble": ("\tfor (i = 0; i < 32u; ++i)\n\t\tphy_mdio_bit(1, 1);\n\tfor (i = 0; i < 32u; ++i)\n\t\tphy_mdio_bit(1, (frame",
                       "\tfor (i = 0; i < 32u; ++i)\n\t\tphy_mdio_bit(1, (frame"),
 "write-bad-turnaround": ("(2u << 16) | (value & 0xffffu);", "(3u << 16) | (value & 0xffffu);"),
 "init-before-found": ("\tbmsr = phy_mdio_read(1);\n\tif (!phy_advertised",
                       "\tbmsr = phy_mdio_read(1);\n\tif (phy_published != 0xffu && !phy_advertised && (phy_address & 1u)"),
}

def bench(work: Path):
    nvm.make_bench(repo / 'configs/endstation_ax7101_1x1_tdm8.yaml', work, nvm.FIRMWARE.read_text())
    phy.phy_csr(work)

def cmd(work, driver):
    return ["gcc", "-std=gnu11", "-O1", "-Wall", "-Wextra", "-Wno-format", "-ffunction-sections",
            "-fdata-sections", "-Wl,--gc-sections", f"-I{work}", f"-I{nvm.STUBS}", str(driver), "-o", str(work / "phy")]

if root.exists(): shutil.rmtree(root)
root.mkdir(parents=True)
src = nvm.FENCE_RE.sub("(void)0;", nvm.FIRMWARE.read_text())
driver = repo / 'sw/firmware/nvm_hosttest/phy_host.c'
for name, (old, new) in M.items():
    work = root / name; work.mkdir(); bench(work)
    if src.count(old) != 1:
        print(f"MUTANT {name}: ANCHOR-MISSING count={src.count(old)}"); continue
    (work / 'milan_baremetal.c').write_text(src.replace(old, new))
    c = subprocess.run(cmd(work, driver), capture_output=True, text=True, timeout=180)
    if c.returncode:
        print(f"MUTANT {name}: BUILD-FAILED {c.stderr[:200]}"); continue
    r = subprocess.run([str(work / 'phy')], capture_output=True, text=True, timeout=120)
    a = re.search(r"Assertion `(.*?)' failed", r.stderr)
    print(f"MUTANT {name}: " + (f"CAUGHT {a[1]}" if r.returncode and a else f"CAUGHT rc={r.returncode}" if r.returncode else "SURVIVED"), flush=True)

# Wire comparison: the same peer and driver, logging every pin write.
peer = (repo / 'sw/firmware/nvm_hosttest/phy_peer.h').read_text()
hook = 'void milan_mac_phy_mdio_w_write(uint32_t value)\n{\n'
assert peer.count(hook) == 1
for rev in ['HEAD', *revs]:
    work = root / ('wire-' + rev[:12]); work.mkdir(); bench(work)
    text = subprocess.check_output(['git', '-C', str(repo), 'show', rev + ':sw/firmware/milan_baremetal/milan_baremetal.c'], text=True)
    (work / 'milan_baremetal.c').write_text(nvm.FENCE_RE.sub("(void)0;", text))
    (work / 'phy_peer.h').write_text(peer.replace(hook, hook + '\tfprintf(stderr, "%x\\n", (unsigned)value);\n'))
    shutil.copy(driver, work / 'phy_host.c')
    subprocess.run(cmd(work, work / 'phy_host.c'), check=True, capture_output=True, timeout=180)
    r = subprocess.run([str(work / 'phy')], capture_output=True, text=True, timeout=180)
    ok = re.search(r'PHY_OK transfers=(\d+) delay_cycles=(\d+)', r.stdout)
    print(f"WIRE {rev[:12]}: rc={r.returncode} pins={r.stderr.count(chr(10))} sha256={hashlib.sha256(r.stderr.encode()).hexdigest()} {ok[0] if ok else 'no PHY_OK'}", flush=True)
