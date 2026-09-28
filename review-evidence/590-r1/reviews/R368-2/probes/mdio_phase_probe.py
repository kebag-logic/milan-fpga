#!/usr/bin/env python3
"""Review probe R368-2: product MDIO reader against an independent Clause-22 peer.

Usage: python3 -B mdio_phase_probe.py <repo-root> <work-dir>
The peer is the round-1 review probe mdio_peer_probe.c, unchanged:
  PEER_STD=1  IEEE 802.3 22.3.4 (value visible after rising edge k is bit k+1)
  PEER_STD=0  the pre-fix lane convention (bit k visible after edge k)
Arms: the unchanged head reader, and three planted reader phase errors.
Expected: only head/std=1 publishes 13 with BMSR 0x796d. Exit 0 iff every arm
matches its expectation. The repository is not modified.
"""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402

probe = Path(__file__).with_name("mdio_peer_probe.c")
work.mkdir(parents=True, exist_ok=True)
nvm.make_bench(root / "configs/endstation_ax7101_1x1_tdm8.yaml", work, nvm.FIRMWARE.read_text())
(work / "generated/csr.h").write_text(
    f'#include "{nvm.STUBS / "generated/csr.h"}"\n#define CSR_MILAN_MAC_PHY_MDIO_W_ADDR 1\n')
source = nvm.FENCE_RE.sub("(void)0;", nvm.FIRMWARE.read_text())


def mutate(text, old, new):
    assert text.count(old) == 1, "anchor not unique: " + old
    return text.replace(old, new)


SAMPLE = ("\tvalue = milan_mac_phy_mdio_r_read() & 1u;\n"
          "\tmilan_mac_phy_mdio_w_write(pins | PHY_MDC);\n\tcdelay(32);\n")
TA = "\tphy_mdio_bit(0, 0);\n\tack = phy_mdio_bit(0, 0);\n"
ARMS = {
    "head": source,
    # sample in the high phase after the rising edge (the round-1 defect)
    "late-sample": mutate(source, SAMPLE, "\tmilan_mac_phy_mdio_w_write(pins | PHY_MDC);\n"
                          "\tcdelay(32);\n\tvalue = milan_mac_phy_mdio_r_read() & 1u;\n"),
    # one turnaround clock only: ack taken at the released first TA bit
    "one-ta-clock": mutate(source, TA, "\tack = phy_mdio_bit(0, 0);\n"),
    # three turnaround clocks: data one bit late
    "three-ta-clocks": mutate(source, TA, "\tphy_mdio_bit(0, 0);\n" + TA),
}
# late-sample against the pre-fix convention is the round-1 reader/peer pair,
# which agreed with each other by construction.
EXPECT = {("head", 1): True, ("late-sample", 0): True}
bad = 0
for name, text in ARMS.items():
    for std in (1, 0):
        (work / "milan_baremetal.c").write_text(text)
        exe = work / f"probe-{name}-{std}"
        subprocess.run(["gcc", "-std=gnu11", "-O1", "-Wall", "-Wno-format",
                        "-Wno-unused-function", f"-DPEER_STD={std}",
                        "-ffunction-sections", "-fdata-sections", "-Wl,--gc-sections",
                        f"-I{work}", f"-I{nvm.STUBS}", str(probe), "-o", str(exe)],
                       check=True, timeout=300)
        r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=120)
        ok = r.returncode == 0
        want = EXPECT.get((name, std), False)
        verdict = "as-expected" if ok == want else "UNEXPECTED"
        bad += ok != want
        print(f"ARM reader={name} peer_std={std} publishes13={ok} expect13={want} {verdict} :: {r.stdout.strip()}")
print("MDIO PHASE PROBE:", "PASS" if not bad else f"FAIL ({bad} unexpected)")
sys.exit(1 if bad else 0)
