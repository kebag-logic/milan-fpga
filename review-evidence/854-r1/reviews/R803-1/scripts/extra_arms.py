#!/usr/bin/env python3
"""Reviewer probe: plant extra defects in a DISPOSABLE copy of the tree and
require tb/verilator/pp_shadow section [DR] (--drops-only) to fail a named
check on each.  Usage:

    python3 -I extra_arms.py <disposable-tree-root> <work-dir> [--jobs N]

The tree root is modified in place (one arm per private copy of the file
under <work-dir>, passed through DP_SRCS as drops_mutant.py does); the
original source files are compared before and after.  Exit 0 = every arm
caught by its named check.
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
TB = ROOT / "tb" / "verilator" / "pp_shadow"
SHADOW = ROOT / "hdl" / "milan" / "KL_pp_shadow.sv"

ARMS = [
    # the refused frame's second beat counted as kept: accept_w ignored
    ("refused-at-head1",
     "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w);\n",
     "      last_kept_r <= (fw_S == FW_BODY) || (fw_S == FW_HEAD1);\n",
     "[FAIL] DR ...and are not counted: the kept frames lost equal the count"),
    # saturation one short of 255
    ("saturates-at-254",
     "      if (drop_evt_w & (rx_drops_o != 8'hFF)) rx_drops_o <= rx_drops_o + 8'd1;\n",
     "      if (drop_evt_w & (rx_drops_o != 8'hFE)) rx_drops_o <= rx_drops_o + 8'd1;\n",
     "[FAIL] DR the count saturates at 255"),
    # the FIFO halved (axis_fifo rounds depth to a power of two, so 2048 is
    # the next smaller real FIFO): the capacity check must notice
    ("fifo-2048",
     "    parameter int unsigned RX_FIFO_BYTES_P = 4096,\n",
     "    parameter int unsigned RX_FIFO_BYTES_P = 2048,\n",
     "[FAIL] DR ...and the FIFO holds 4,096 bytes of it before it loses one"),
]


def srcs() -> list:
    quiet = {k: v for k, v in os.environ.items() if k not in ("MAKEFLAGS", "MFLAGS")}
    out = subprocess.run(["make", "-s", "--no-print-directory", "-C", "../milan_dp", "print-srcs"],
                         cwd=TB, check=True, capture_output=True, text=True, env=quiet).stdout
    return [(TB / p).resolve() for p in out.split()]


def leg(name, old, new, check, sources, original):
    d = WORK / name
    (d / "hdl" / "milan").mkdir(parents=True, exist_ok=True)
    m = d / "hdl" / "milan" / SHADOW.name
    assert original.count(old) == 1, f"{name}: anchor count {original.count(old)}"
    m.write_text(original.replace(old, new))
    planted = [m if p == SHADOW.resolve() else p for p in sources]
    log = d / "run.log"
    with log.open("w") as f:
        b = subprocess.run(["make", "--no-print-directory", "build-base", f"BUILD_DIR={d / 'obj'}",
                            "DP_SRCS=" + " ".join(map(str, planted))], cwd=TB, stdout=f,
                           stderr=subprocess.STDOUT)
        rc = b.returncode
        if rc == 0:
            r = subprocess.run([str(d / "obj" / "Vpp_shadow_sim"), "--drops-only"], cwd=TB,
                               stdout=f, stderr=subprocess.STDOUT)
            rc = r.returncode
    text = log.read_text(errors="replace")
    caught = rc != 0 and "RESULT: FAIL" in text and any(
        ln.lstrip().startswith(check) for ln in text.splitlines())
    fails = [ln.strip() for ln in text.splitlines() if ln.lstrip().startswith("[FAIL]")]
    dr = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("DR ")]
    return name, rc, caught, fails, dr


def main():
    original = SHADOW.read_text()
    sources = srcs()
    assert sources.count(SHADOW.resolve()) == 1
    # generated hex files first, once, so parallel legs do not race on them
    subprocess.run(["make", "--no-print-directory", "ltn_rom.hex", "ucode.hex"], cwd=TB, check=True)
    with ThreadPoolExecutor(JOBS) as ex:
        res = list(ex.map(lambda a: leg(*a, sources, original), ARMS))
    ok = True
    for name, rc, caught, fails, dr in res:
        print(f"{name}: exit {rc} {'KILLED by its named check' if caught else 'SURVIVED'}")
        for ln in dr:
            print(f"    {ln}")
        for ln in fails:
            print(f"    {ln}")
        ok &= caught
    if SHADOW.read_text() != original:
        print("FAIL: source changed")
        return 1
    print("RESULT:", "PASS (every extra arm caught)" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
