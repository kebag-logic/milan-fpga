#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The planted defects the KL_reboot_ctrl harness must catch (issue #787).

A harness that cannot go red proves nothing. Each control below plants one
defect in a private copy of hdl/milan/KL_reboot_ctrl.sv, builds the harness
against that copy through this directory's Makefile (CTRL_SRC, MDIR), and
requires the run to fail on the control's OWN named check. The first control
is the one the issue names: a reset controller that ignores the request.

The committed module is built first as the golden run and must pass. A
mutated copy that fails to build is not caught by a check, so it fails this
driver. Mutant logs stay in the private directory: their failing lines would
otherwise read as failures of this suite.

Usage:
    python3 mutants.py            # the golden run, then every control
    python3 mutants.py --list     # name the controls and build nothing

Exit 0 = the golden run passed and every control was caught by its check;
1 = otherwise.
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[2] / "hdl" / "milan" / "KL_reboot_ctrl.sv"

REQ = "U1 no writer, nothing in the MAC: from the request the PHY hold rises more than one tick later"
DIRTY = "U3 dirty work with a live writer: no PHY hold and no IPROG for 4,000 ms"
PEND = "U4 pending work with a live writer: no PHY hold for 1,500 ms"
LOST = "U6 the writer is lost: from that clock ...and at most two ticks and the crossing later"
LATE = "U5 ...and at most one tick more"
EARLY = ("U5 a writer that never commits: the PHY hold more than 10,000 ms and two ticks "
         "after the request")
SHORT = "U1 the hold is longer than 3,500 ms"
LONG = "U1 the hold is at most one tick longer than 3,500 ms"
WORDS = ("U1 eight consecutive clocks carry dummy, sync, NOOP, WBSTAR, 0, CMD, IPROG, "
         "NOOP, bits reversed per byte")
CSIB = "U1 CSIB is high again after the eighth word"
HELD = "U1 the PHY hold stays up through the IPROG words"
LATCH = "U7 a one-clock request: the PHY hold still rises"
RESET = "U9 a reset during the hold: back to idle, and no IPROG afterwards"
# the egress wait (issue #787: no PHY hold before the frames in the MAC reach its PHY)
IN_MAC = "U12 frames in the MAC at the request: no PHY hold 20 ms later with three frames still in the MAC"
TWO_LEFT = "U12 two frames still in the MAC: no PHY hold"
QUIET = "U12 the last frame reaches the PHY: from its end the PHY hold rises more than one tick later"
COINCIDE = "U12 coincide: the second frame is still in the MAC: no PHY hold"
IN_PROGRESS = "U13 a frame still being taken 3 ms into the wait: no PHY hold"
NO_BOUND = "U14 a MAC that never finishes: the PHY hold still rises"
BOUND_SHORT = "U14 ...after more than the derived egress bound"
BOUND_LONG = "U14 ...and at most one tick more"
FLUSH = "U15 a flush in the wait: from the flush ...and at most two ticks and the crossing later"
WRAP = "U16 it reaches the PHY: from its end ...and at most two ticks and the crossing later"
QUIET_GAP = "U18 ...no PHY hold at the next tick"

#: (name, old text, new text, the named check this must break)
MUTATIONS = [
    ("request-ignored",
     "if (reboot_req_i) state_r <= S_DRAIN;",
     "if (reboot_req_i & 1'b0) state_r <= S_DRAIN;", REQ),
    ("drain-ignores-dirty",
     "assign drained_w    = ~nvm_backed_i | (~nvm_dirty_i & ~nvm_pend_i);",
     "assign drained_w    = ~nvm_backed_i | (~(nvm_dirty_i & 1'b0) & ~nvm_pend_i);", DIRTY),
    ("drain-ignores-pend",
     "assign drained_w    = ~nvm_backed_i | (~nvm_dirty_i & ~nvm_pend_i);",
     "assign drained_w    = ~nvm_backed_i | (~nvm_dirty_i & ~(nvm_pend_i & 1'b0));", PEND),
    ("drain-ignores-a-lost-writer",
     "assign drained_w    = ~nvm_backed_i | (~nvm_dirty_i & ~nvm_pend_i);",
     "assign drained_w    = ~(nvm_backed_i | 1'b1) | (~nvm_dirty_i & ~nvm_pend_i);", LOST),
    ("no-drain-deadline",
     "assign drain_exp_w  = ms_tick_i & (ms_r == MS_W_C'(T_DRAIN_MS_P));",
     "assign drain_exp_w  = ms_tick_i & (ms_r == MS_W_C'(T_DRAIN_MS_P)) & 1'b0;", LATE),
    ("drain-deadline-a-tick-early",
     "assign drain_exp_w  = ms_tick_i & (ms_r == MS_W_C'(T_DRAIN_MS_P));",
     "assign drain_exp_w  = ms_tick_i & (ms_r == MS_W_C'(T_DRAIN_MS_P - 1));", EARLY),
    ("hold-skipped",
     "assign hold_exp_w   = ms_tick_i & (ms_r == MS_W_C'(T_HOLD_MS_P));",
     "assign hold_exp_w   = 1'b1 | (ms_tick_i & (ms_r == MS_W_C'(T_HOLD_MS_P)));", SHORT),
    ("hold-a-tick-short",
     "assign hold_exp_w   = ms_tick_i & (ms_r == MS_W_C'(T_HOLD_MS_P));",
     "assign hold_exp_w   = ms_tick_i & (ms_r == MS_W_C'(T_HOLD_MS_P - 1));", SHORT),
    ("hold-a-tick-long",
     "assign hold_exp_w   = ms_tick_i & (ms_r == MS_W_C'(T_HOLD_MS_P));",
     "assign hold_exp_w   = ms_tick_i & (ms_r == MS_W_C'(T_HOLD_MS_P + 1));", LONG),
    ("bits-not-reversed",
     "assign icap_i_o      = byte_swap_bits_f(iprog_word_f(idx_r));",
     "assign icap_i_o      = iprog_word_f(idx_r) | (byte_swap_bits_f(32'd0) & 32'd0);", WORDS),
    ("wbstar-write-dropped",
     "3'd3:    iprog_word_f = 32'h3002_0001;",
     "3'd3:    iprog_word_f = 32'h2000_0000;", WORDS),
    ("desync-for-iprog",
     "3'd6:    iprog_word_f = 32'h0000_000F;",
     "3'd6:    iprog_word_f = 32'h0000_000D;", WORDS),
    ("words-repeat-without-a-hold",
     "if (idx_r == 3'd7) state_r <= S_HOLD;",
     "if (idx_r == 3'd7) state_r <= S_IPROG;", CSIB),
    ("phy-hold-released-for-iprog",
     "            state_r <= S_IPROG;\n            ms_r    <= '0;",
     "            state_r <= S_IPROG;\n            hold_r  <= 1'b0;\n            ms_r    <= '0;", HELD),
    ("request-not-latched",
     "          if (drained_w || drain_exp_w) begin",
     "          if (!reboot_req_i) begin\n            state_r <= S_IDLE;\n"
     "          end else if (drained_w || drain_exp_w) begin", LATCH),
    ("hold-survives-reset",
     "      hold_r  <= 1'b0;\n      quiet_r <= 1'b0;",
     "      quiet_r <= 1'b0;", RESET),
    # the [A10] arms of issuecomment-6518083444: today's PHY hold on the
    # request alone, a drain that ignores the MAC FIFO, a drain with no bound
    ("hold-on-the-request-alone",
     "            state_r <= S_EGRESS;\n            ms_r    <= '0;\n            quiet_r <= 1'b0;",
     "            state_r <= S_HOLD;\n            ms_r    <= '0;\n            hold_r  <= 1'b1;",
     IN_MAC),
    ("egress-ignores-the-mac-fifo",
     "assign idle_w       = ~in_frame_r & (fly_r == '0);",
     "assign idle_w       = ~in_frame_r & ((fly_r == '0) | 1'b1);", IN_MAC),
    ("egress-without-a-bound",
     "assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C));",
     "assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C)) & 1'b0;", NO_BOUND),
    ("egress-bound-a-tick-short",
     "assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C));",
     "assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C - 1));", BOUND_SHORT),
    ("egress-bound-a-tick-long",
     "assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C));",
     "assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C + 1));", BOUND_LONG),
    ("egress-bound-rounded-down",
     "localparam int unsigned T_SEND_MS_C    = (MAC_TX_OCTETS_P * 8 + BITS_PER_MS_C - 1)",
     "localparam int unsigned T_SEND_MS_C    = (MAC_TX_OCTETS_P * 8 + 0 * BITS_PER_MS_C)",
     BOUND_SHORT),
    ("egress-without-the-quiet-tick",
     "          if ((ms_tick_i && quiet_r && idle_w) || egress_exp_w) begin",
     "          if ((ms_tick_i && (quiet_r | 1'b1) && idle_w) || egress_exp_w) begin", QUIET),
    ("egress-ignores-the-frame-at-the-port",
     "assign idle_w       = ~in_frame_r & (fly_r == '0);",
     "assign idle_w       = ~(in_frame_r & 1'b0) & (fly_r == '0);", IN_PROGRESS),
    ("frames-taken-not-counted",
     "assign took_w       = mac_tx_beat_i & mac_tx_frame_i;",
     "assign took_w       = mac_tx_beat_i & mac_tx_frame_i & 1'b0;", IN_MAC),
    ("end-read-as-a-level",
     "assign txend_w      = txend_sync_r[2] ^ txend_sync_r[1];",
     "assign txend_w      = txend_sync_r[2] | (txend_sync_r[1] & 1'b0);", TWO_LEFT),
    ("end-wins-over-a-take",
     "      else if (txend_w && !took_w && fly_r != '0)",
     "      else if (txend_w && fly_r != '0)", COINCIDE),
    ("count-wraps-below-zero",
     "      else if (txend_w && !took_w && fly_r != '0)",
     "      else if (txend_w && !took_w)", WRAP),
    ("flush-ignored",
     "      if (mac_flush_i)\n        fly_r <= '0;\n      else if",
     "      if (mac_flush_i & 1'b0)\n        fly_r <= '0;\n      else if", FLUSH),
    ("egress-quiet-sampled-only-at-ticks",
     "          end else if (!idle_w) begin\n            quiet_r <= 1'b0;\n          end",
     "          end", QUIET_GAP),
]


def run_harness(source: Path, work: Path) -> tuple[int, str]:
    """Build and run the harness against `source`; return (status, log)."""
    command = ["make", "--no-print-directory", "run",
               f"CTRL_SRC={source}", f"MDIR={work / 'obj'}"]
    log_path = work / "run.log"
    with log_path.open("w") as log:
        result = subprocess.run(command, cwd=HERE, stdout=log,
                                stderr=subprocess.STDOUT, check=False)
    return result.returncode, log_path.read_text()


def failed_checks(text: str) -> list[str]:
    """The labels of the checks a run reports as failed."""
    labels = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[FAIL] "):
            labels.append(stripped[len("[FAIL] "):])
    return labels


def caught_by(labels: list[str], check: str) -> bool:
    """A failed check matches its label exactly or carries it before its values."""
    return any(label == check or label.startswith(check + " ") for label in labels)


def main() -> int:
    """Run the golden build, then every control; 0 when all were caught."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true", help="name the controls and stop")
    args = parser.parse_args()
    if args.list:
        for name, _old, _new, check in MUTATIONS:
            print(f"{name}: {check}")
        return 0

    original = SOURCE.read_text()
    missed = []
    with tempfile.TemporaryDirectory(prefix="reboot_ctrl_mut_") as scratch:
        root = Path(scratch)
        golden = root / "golden"
        golden.mkdir()
        status, text = run_harness(SOURCE, golden)
        golden_ok = status == 0 and "RESULT: PASS" in text
        print(f"golden: {'PASS' if golden_ok else 'NOT PASS'} (exit {status})")
        if not golden_ok:
            print("\n".join(text.splitlines()[-20:]))
            missed.append("golden")
        for name, old, new, check in MUTATIONS:
            if original.count(old) != 1:
                print(f"{name}: REFUSED, its planted text occurs {original.count(old)} times")
                missed.append(name)
                continue
            work = root / name
            work.mkdir()
            mutant = work / SOURCE.name
            mutant.write_text(original.replace(old, new))
            status, text = run_harness(mutant, work)
            labels = failed_checks(text)
            if status != 0 and caught_by(labels, check):
                print(f"{name}: KILLED by its named check, {len(labels)} failing checks")
                print(f"  named check: {check}")
            else:
                reason = ("it built nothing to grade" if status != 0 and not labels
                          else "its named check passed")
                print(f"{name}: SURVIVED, {reason} (exit {status})")
                for label in labels[:5]:
                    print(f"  failing: {label}")
                missed.append(name)
    controls = len(MUTATIONS) + 1
    print(f"== reboot_ctrl mutants: checks: {controls}   failures: {len(missed)} ==")
    if missed:
        print("RESULT: FAIL (" + ", ".join(missed) + ")")
        return 1
    print(f"RESULT: PASS (golden PASS, {len(MUTATIONS)} of {len(MUTATIONS)} controls killed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
