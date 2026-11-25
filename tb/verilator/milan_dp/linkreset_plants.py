# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""linkreset_plants.py - the linkreset leg's planted premature qualification (#972).

The plant is made at the word's cause: a copy of sw/litex/mac_link_status.py,
which milan_soc.py's MilanMAC resets milan_mac_link_status from, whose
link_up_reset gives link up whatever owns the PHY (the reset before #972). The
leg's published arm runs at each shape with the copy's reset, and must fail
with the finding that a frame crossed the MAC boundary before the firmware's
publication. The models are the ones `make linkreset` built: the word is the
bench's input, so the plant needs no rebuild.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
HELPER = HERE.parents[2] / "sw/litex/mac_link_status.py"
#: The helper's statement the plant rewrites, and what it writes.
ANCHOR = "    return 0 if fw_link_owner else 1\n"
PLANTED = "    return 1\n"
#: The finding the published arm must give under the plant.
FINDING = "no frame crosses the MAC boundary before the firmware's publication"
SHAPES = ("1x1", "8x8")


def word(helper: Path) -> int:
    """The split's word reset as `helper` gives it."""
    out = subprocess.run([sys.executable, "-B", str(helper), "gmii", "1"], check=True, capture_output=True, text=True)
    return int(out.stdout.split()[1])


def main() -> int:
    """Plant the helper's copy, run the published arm at each shape under it, and require each to fail."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--publish-ms", default="1500", help="the publication, as the Makefile's LINKRESET_PUBLISH_MS")
    ap.add_argument("--window-ms", default="1600", help="the window, as the Makefile's LINKRESET_WINDOW_MS")
    args = ap.parse_args()
    work = HERE / "obj_linkreset_plants"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()
    text = HELPER.read_text()
    if text.count(ANCHOR) != 1:
        print(f"PLANT REFUSED: the anchor occurs {text.count(ANCHOR)} times in {HELPER.name}")
        return 2
    planted = work / HELPER.name
    planted.write_text(text.replace(ANCHOR, PLANTED))
    head, bad = word(HELPER), word(planted)
    print(f"linkreset plant premature-qualification: the word resets to {bad} (the head's {head})")
    if bad == head or (bad & 1) == 0:
        print("PLANT REFUSED: the planted reset does not qualify the link")
        return 2
    caught = 0
    for shape in SHAPES:
        model = HERE / f"obj_linkreset_{shape}" / "Vmilan_dp_linkreset"
        run = subprocess.run([str(model), "--word-reset", str(bad), "--publish-ms", args.publish_ms,
                              "--window-ms", args.window_ms], capture_output=True, text=True)
        log = run.stdout + run.stderr
        (work / f"{shape}.log").write_text(log)
        found = any("[FAIL]" in line and FINDING in line for line in log.splitlines())
        ok = run.returncode == 1 and found
        caught += ok
        print(f"[{'ok' if ok else 'ESCAPED'}] premature-qualification at {shape}/1if: rc {run.returncode}, "
              f"finding {'given' if found else 'absent'}")
        for line in log.splitlines():
            if line.startswith(("FRAME 0", "FRAMES", "  [FAIL]")):
                print(f"    {line.strip()}")
    print(f"linkreset plants: {caught} of {len(SHAPES)} caught")
    return 0 if caught == len(SHAPES) else 1


if __name__ == "__main__":
    sys.exit(main())
