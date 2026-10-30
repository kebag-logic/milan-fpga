"""The lane's two new host checks against dev 1e80128f's firmware: both must fail by name.

usage: python3 -B dev_firmware_controls.py REPO
Reads the dev firmware with `git show`, never edits the checkout."""
import subprocess
import sys
import tempfile
from pathlib import Path

repo = Path(sys.argv[1])
sys.path.insert(0, str(repo / "sw/firmware/nvm_hosttest"))
import test_nvm_firmware as nvm  # noqa: E402
import test_boot_walk as bw  # noqa: E402
import test_phy_firmware as phy  # noqa: E402

dev = subprocess.run(["git", "-C", str(repo), "show",
                      "1e80128f0a467b58bf884b7d9bf62e013a2fb141:sw/firmware/milan_baremetal/milan_baremetal.c"],
                     check=True, capture_output=True, text=True).stdout
cfg = repo / "configs/endstation_ax7101_1x1_tdm8.yaml"
ok = True
with tempfile.TemporaryDirectory(prefix="a704-devctl.") as t:
    work = Path(t)
    bench = nvm.make_bench(cfg, work / "bw", dev)
    got = bw.grade(cfg, work / "bw-grade", dev, bench)
    for item in got:
        print("BOOT-WALK FINDING:", item)
    want = ("boot walk, cold boot, CLOSED restore: the console claims the entity enabled",
            "boot walk, cold boot, stalled restore: the timeout did not report")
    for w in want:
        hit = any(i.startswith(w) for i in got)
        print(("CAUGHT " if hit else "MISSED ") + w)
        ok &= hit
    got = phy.boot_path_findings(cfg, work / "phy", dev)
    for item in got:
        print("PHY FINDING:", item)
    w = "PHY boot path persistence disabled: the link-status CSR holds 0"
    hit = any(i.startswith(w) for i in got)
    print(("CAUGHT " if hit else "MISSED ") + w)
    ok &= hit
print("DEV CONTROLS:", "every named check fails on dev's firmware" if ok else "NOT AS REQUIRED")
sys.exit(0 if ok else 1)
