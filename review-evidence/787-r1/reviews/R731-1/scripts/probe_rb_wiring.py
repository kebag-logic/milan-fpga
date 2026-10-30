#!/usr/bin/env python3
"""Reviewer probes of milan_datapath's KL_reboot_ctrl wiring under pp_shadow [RB].

Each probe plants one change into a private copy of hdl/milan/milan_datapath.sv,
builds pp_shadow's base leg into a private directory with the datapath source
list read as the suite's Makefile reads it (as reboot_mutant.py does), and runs
section [RB] alone. Tracked bytes are never written.

usage: probe_rb_wiring.py <clone> <workdir>
"""
import os
import subprocess
import sys
from pathlib import Path

PROBES = [
    # the port's beat term replaced by the frame term: a half-taken frame is invisible
    ("beat-wired-to-frame-end",
     "      .mac_tx_beat_i   (tx_mac_beat_w),\n",
     "      .mac_tx_beat_i   (tx_mac_good_w),\n"),
    # every accepted beat counted as a frame: the account over-counts
    ("frame-wired-to-beat",
     "      .mac_tx_frame_i  (tx_mac_good_w),\n",
     "      .mac_tx_frame_i  (tx_mac_beat_w),\n"),
    # the link guard's flush unwired
    ("flush-unwired",
     "      .mac_flush_i     (linkg_reinit_w & linkg_eth_rst_w),\n",
     "      .mac_flush_i     (1'b0),\n"),
]


def main() -> int:
    clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    here = clone / "tb/verilator/pp_shadow"
    dp = (clone / "hdl/milan/milan_datapath.sv").resolve()
    original = dp.read_text()
    quiet = {k: v for k, v in os.environ.items() if k not in ("MAKEFLAGS", "MFLAGS")}
    listing = subprocess.run(["make", "-s", "--no-print-directory", "-C", "../milan_dp",
                              "print-srcs"], cwd=here, check=True, capture_output=True,
                             text=True, env=quiet).stdout.split()
    sources = [(here / p).resolve() for p in listing]
    assert sources.count(dp) == 1, "datapath not exactly once in the source list"
    for name, old, new in PROBES:
        if original.count(old) != 1:
            print(f"{name}: REFUSED, anchor count {original.count(old)}")
            continue
        d = work / name
        (d / "hdl/milan").mkdir(parents=True, exist_ok=True)
        planted = d / "hdl/milan/milan_datapath.sv"
        planted.write_text(original.replace(old, new))
        srcs = [planted if p == dp else p for p in sources]
        log = d / "rb.log"
        with log.open("w") as fh:
            made = subprocess.run(["make", "--no-print-directory", "build-base",
                                   f"BUILD_DIR={d / 'obj'}", "DP_SRCS=" + " ".join(map(str, srcs))],
                                  cwd=here, stdout=fh, stderr=subprocess.STDOUT).returncode
            rc = made if made else subprocess.run([str(d / "obj/Vpp_shadow_sim"), "--reboot-only"],
                                                  cwd=here, stdout=fh,
                                                  stderr=subprocess.STDOUT).returncode
        text = log.read_text()
        fails = [l.strip() for l in text.splitlines() if l.strip().startswith("[FAIL]")]
        verdict = "BUILD-FAILED" if made else ("KILLED" if rc != 0 and fails else "SURVIVED")
        print(f"{name}: {verdict} (exit {rc}, failing checks {len(fails)})")
        for line in fails[:4]:
            print(f"    {line}")
        for line in text.splitlines():
            if "[i]    RB" in line and ("PHY hold" in line):
                print(f"    {line.strip()}")
    if dp.read_text() != original:
        print("FAIL: the tracked source changed")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
