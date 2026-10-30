#!/usr/bin/env python3
"""Reviewer probes for KL_reboot_ctrl beyond the lane's own 30 arms.

Each probe plants one textual change into a private copy of
hdl/milan/KL_reboot_ctrl.sv, builds tb/verilator/reboot_ctrl through its own
Makefile with CTRL_SRC/MDIR pointing at the private copy, and records whether
the harness fails (exit != 0 and RESULT: FAIL) and which checks fail.
The checkout's tracked bytes are never written.

usage: probe_reboot_ctrl.py <clone> <workdir>
"""
import subprocess
import sys
from pathlib import Path

PROBES = [
    # the account saturates at one frame: back-to-back frames under-count
    ("sat-at-one",
     "else if (took_w && !txend_w && fly_r != FLY_W_C'(FLY_MAX_C))",
     "else if (took_w && !txend_w && fly_r != FLY_W_C'(1))"),
    # the port's half-taken flag never clears after the first beat
    ("in-frame-sticks",
     "if (mac_tx_beat_i) in_frame_r <= ~mac_tx_frame_i;",
     "if (mac_tx_beat_i) in_frame_r <= 1'b1;"),
    # the quiet exit does not re-check idle on the tick itself
    ("exit-tick-not-idle",
     "if ((ms_tick_i && quiet_r && idle_w) || egress_exp_w) begin",
     "if ((ms_tick_i && quiet_r) || egress_exp_w) begin"),
    # the tick sets quiet even when the path is busy at the tick
    ("quiet-set-when-busy",
     "quiet_r <= idle_w;",
     "quiet_r <= 1'b1;"),
    # the egress bound loses its quiet millisecond
    ("bound-without-quiet-ms",
     "localparam int unsigned T_EGRESS_MS_C  = T_SEND_MS_C + 1;",
     "localparam int unsigned T_EGRESS_MS_C  = T_SEND_MS_C;"),
]


def main() -> int:
    clone, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    src = clone / "hdl/milan/KL_reboot_ctrl.sv"
    tb = clone / "tb/verilator/reboot_ctrl"
    original = src.read_text()
    survived = 0
    for name, old, new in PROBES:
        if original.count(old) != 1:
            print(f"{name}: REFUSED, anchor count {original.count(old)}")
            survived += 1
            continue
        d = work / name
        d.mkdir(parents=True, exist_ok=True)
        planted = d / "KL_reboot_ctrl.sv"
        planted.write_text(original.replace(old, new))
        legs = []
        for leg, extra in (("default", []),
                           ("1g", ["EGRESS_MS=2", "LEG_ARGS=--egress-only",
                                   "LEG_G=-GMAC_TX_OCTETS_P=11656 -GMAC_MIN_MBPS_P=1000"])):
            log = d / f"{leg}.log"
            with log.open("w") as fh:
                rc = subprocess.run(["make", "--no-print-directory", "run",
                                     f"CTRL_SRC={planted}", f"MDIR={d / ('obj_' + leg)}", *extra],
                                    cwd=tb, stdout=fh, stderr=subprocess.STDOUT).returncode
            text = log.read_text()
            fails = [l.strip() for l in text.splitlines() if l.strip().startswith("[FAIL]")]
            legs.append((leg, rc, "RESULT: FAIL" in text, fails))
        killed = any(rc != 0 and f for _, rc, f, _ in legs)
        survived += 0 if killed else 1
        print(f"{name}: {'KILLED' if killed else 'SURVIVED'}")
        for leg, rc, f, fails in legs:
            print(f"  leg {leg}: exit {rc}, RESULT FAIL {f}, failing checks {len(fails)}")
            for line in fails[:3]:
                print(f"    {line}")
    if src.read_text() != original:
        print("FAIL: the tracked source changed")
        return 2
    print(f"== probes: {len(PROBES)}  survived: {survived} ==")
    return 0


if __name__ == "__main__":
    sys.exit(main())
