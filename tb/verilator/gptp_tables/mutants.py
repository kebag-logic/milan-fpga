#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The defect controls the gPTP table lockstep owns.

WHY THIS EXISTS. A lockstep that cannot go red proves nothing. Issue #640
lane M7 moved six of the fabric gPTP plane's tables into another storage
form; for each one this driver plants three defects of the kinds a storage
conversion can introduce - a wrong depth, a wrong read latency and an index
alias - one at a time, and requires the table's OWN named lockstep check to
fail. A control that leaves that check green is a finding about the bench.

Every control edits private copies of exactly the files the build reads
(`make print-inputs`), verified against their committed bytes and pinned
submodule blobs by the slice suite's input copier; caller sources are never
modified.

Usage:
    python3 mutants.py            # every control
    python3 mutants.py --list     # name them and change nothing

Exit 0 = every control was caught by its own check and private work was
cleaned; 1 = a control was not caught; 2 = input or cleanup refusal;
130/143 = handled INT/TERM.
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(HERE.parent / "gptp_shadow"))
from owned_process import Cancelled, OwnedProcesses  # noqa: E402
from private_inputs import InputRefused, copy_inputs  # noqa: E402

PLANE = REPO / "hdl" / "ieee8021as" / "gptp_plane"
SHADOW = PLANE / "KL_gptp_shadow.sv"
RET = PLANE / "KL_gptp_txret.sv"
ENGINE = REPO / "gptp-processor" / "hdl" / "top" / "KL_gptp_engine.sv"
TIMER = REPO / "gptp-processor" / "hdl" / "common" / "KL_gptp_timer.sv"

RX = "rx_fifo lockstep"
TX = "tx_fifo lockstep"
BANK = "bank lockstep"
LED = "ledger lockstep"
RES = "results lockstep"
TMR = "timer lockstep"

#: (name, file, old text, new text, the named check this must break)
MUTATIONS = [
    # ---- the tap FIFO's lane field ---------------------------------------
    ("rx_fifo_wrong_depth", SHADOW,
     "    .DEPTH               (RX_FIFO_BEATS_C),",
     "    .DEPTH               (RX_FIFO_BEATS_C / 2),",
     RX),
    ("rx_fifo_wrong_read_latency", SHADOW,
     "    .DROP_WHEN_FULL      (1)\n  ) rx_fifo (",
     "    .DROP_WHEN_FULL      (1),\n    .RAM_PIPELINE        (2)\n  ) rx_fifo (",
     RX),
    ("rx_fifo_lane_alias", SHADOW,
     "      if (rx_tkeep_i[i]) fw_top_w = LANE_W_C'(i);",
     "      if (rx_tkeep_i[i]) fw_top_w = LANE_W_C'(i % 4);",
     RX),
    # ---- the transmit FIFO's lane count ----------------------------------
    #: admission bounds this FIFO to a few frames, so a depth error shows
    #: only once it is shallower than they need: 16 of its 256 beats
    ("tx_fifo_wrong_depth", SHADOW,
     "    .DEPTH               (TX_FIFO_BEATS_C),",
     "    .DEPTH               (TX_FIFO_BEATS_C / 16),",
     TX),
    ("tx_fifo_wrong_read_latency", SHADOW,
     "    .DROP_WHEN_FULL      (0)\n  ) tx_fifo (",
     "    .DROP_WHEN_FULL      (0),\n    .RAM_PIPELINE        (2)\n  ) tx_fifo (",
     TX),
    #: a three-bit count aliases eight lanes onto zero
    ("tx_fifo_count_alias", SHADOW,
     "  localparam int unsigned CNT_W_C  = 4;",
     "  localparam int unsigned CNT_W_C  = 3;",
     TX),
    # ---- the engine's message bank -----------------------------------------
    ("bank_wrong_depth", ENGINE,
     "  (* ram_style = \"block\" *) logic [31:0] bank_lo_r [0:63];\n"
     "  (* ram_style = \"block\" *) logic [31:0] bank_hi_r [0:63];",
     "  (* ram_style = \"block\" *) logic [31:0] bank_lo_r [0:31];\n"
     "  (* ram_style = \"block\" *) logic [31:0] bank_hi_r [0:31];",
     BANK),
    ("bank_wrong_read_latency", ENGINE,
     "  assign st_rdata_w = bank_q_r | st_rdata_r;",
     "  logic [63:0] bank_q2_r;\n"
     "  always_ff @(posedge clk_i) bank_q2_r <= bank_q_r;\n"
     "  assign st_rdata_w = bank_q2_r | st_rdata_r;",
     BANK),
    #: every read of message bank 1 lands in bank 0
    ("bank_index_alias", ENGINE,
     "  assign bank_raddr_w = {disp_bank_r, st_addr_w[4:0]};",
     "  assign bank_raddr_w = {1'b0, st_addr_w[4:0]};",
     BANK),
    # ---- the egress ledger's RAM fields ------------------------------------
    #: The engine's per-class claims keep a few entries outstanding, so a
    #: power-of-two short table aliases harmlessly; one entry short of the
    #: index range is lost the first time the head reaches it.
    ("ledger_wrong_depth", RET,
     "logic  [3:0] led_type_r [0:TXTS_CAP_N_P-1];\n"
     "  (* ram_style = \"distributed\" *) logic [15:0] led_seq_r  [0:TXTS_CAP_N_P-1];\n"
     "  (* ram_style = \"distributed\" *) logic        led_tag_r  [0:TXTS_CAP_N_P-1];",
     "logic  [3:0] led_type_r [0:TXTS_CAP_N_P-2];\n"
     "  (* ram_style = \"distributed\" *) logic [15:0] led_seq_r  [0:TXTS_CAP_N_P-2];\n"
     "  (* ram_style = \"distributed\" *) logic        led_tag_r  [0:TXTS_CAP_N_P-2];",
     LED),
    ("ledger_wrong_read_latency", RET,
     "  assign led_head_type_w = led_type_r[led_head_r];\n"
     "  assign led_head_seq_w  = led_seq_r [led_head_r];\n"
     "  assign led_head_tag_w  = led_tag_r [led_head_r];",
     "  always_ff @(posedge clk_i) begin\n"
     "    led_head_type_w <= led_type_r[led_head_r];\n"
     "    led_head_seq_w  <= led_seq_r [led_head_r];\n"
     "    led_head_tag_w  <= led_tag_r [led_head_r];\n"
     "  end",
     LED),
    ("ledger_index_alias", RET,
     "  assign led_head_type_w = led_type_r[led_head_r];\n"
     "  assign led_head_seq_w  = led_seq_r [led_head_r];\n"
     "  assign led_head_tag_w  = led_tag_r [led_head_r];",
     "  assign led_head_type_w = led_type_r[{1'b0, led_head_r[PTR_W_C-2:0]}];\n"
     "  assign led_head_seq_w  = led_seq_r [{1'b0, led_head_r[PTR_W_C-2:0]}];\n"
     "  assign led_head_tag_w  = led_tag_r [{1'b0, led_head_r[PTR_W_C-2:0]}];",
     LED),
    # ---- the egress result queue -------------------------------------------
    #: the queue holds a result or two at a time: one entry short, as above
    ("results_wrong_depth", RET,
     "logic [63:0] res_ns_r   [0:TXTS_CAP_N_P-1];",
     "logic [63:0] res_ns_r   [0:TXTS_CAP_N_P-2];",
     RES),
    ("results_wrong_read_latency", RET,
     "  assign txts_ns_o    = res_ns_r  [res_head_r];",
     "  logic [63:0] mut_ns_q_r;\n"
     "  always_ff @(posedge clk_i) mut_ns_q_r <= res_ns_r  [res_head_r];\n"
     "  assign txts_ns_o    = mut_ns_q_r;",
     RES),
    ("results_index_alias", RET,
     "  assign txts_ns_o    = res_ns_r  [res_head_r];",
     "  assign txts_ns_o    = res_ns_r  [{1'b0, res_head_r[PTR_W_C-2:0]}];",
     RES),
    # ---- the engine timer's deadlines --------------------------------------
    ("timer_wrong_depth", TIMER,
     "logic [31:0] deadline_r [0:SLOTS_P-1];",
     "logic [31:0] deadline_r [0:SLOTS_P/2-1];",
     TMR),
    ("timer_wrong_read_latency", TIMER,
     "  assign delta_w = $signed(deadline_r[sweep_r] - ms_now_r);",
     "  logic [31:0] mut_dl_q_r;\n"
     "  always_ff @(posedge clk_i) mut_dl_q_r <= deadline_r[sweep_r];\n"
     "  assign delta_w = $signed(mut_dl_q_r - ms_now_r);",
     TMR),
    ("timer_index_alias", TIMER,
     "  assign delta_w = $signed(deadline_r[sweep_r] - ms_now_r);",
     "  assign delta_w = $signed(deadline_r[{1'b0, sweep_r[SW_C-2:0]}] - ms_now_r);",
     TMR),
]

#: the suite's tally: `== gptp_tables: checks: N   failures: M ==`
TALLY_RE = re.compile(r"^== gptp_tables: checks: \d+ +failures: (\d+) ==", re.M)


def run_suite(here: Path, owner: OwnedProcesses) -> tuple[int, str]:
    """Build in private scratch, then stop/reap all owned build descendants."""
    return owner.run(["make", "-s", "run"], cwd=here)


def suite_failed(output: str) -> bool:
    """Did the suite report a failure, rather than merely not finish?

    A build that did not compile also exits non-zero and proves nothing
    about the check a control aims at; a tally with failures is the suite
    noticing.
    """
    tally = TALLY_RE.search(output)
    return tally is not None and int(tally.group(1)) != 0


def failed_checks(output: str) -> list[str]:
    """The checks a run reported as failed, by name."""
    names = []
    for line in output.splitlines():
        text = line.strip()
        if text.startswith("[FAIL] "):
            names.append(text[len("[FAIL] "):].split("  got=")[0].strip())
    return names


def apply_control(path: Path, old: str, new: str) -> bool:
    """Plant one defect. False when its anchor is no longer in the source,
    which is a finding about this file and not a passing control."""
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def campaign(private: Path, owner: OwnedProcesses) -> int:
    """Run every control against private source bytes."""
    failures = 0
    suite = private / HERE.relative_to(REPO)
    for name, original, old, new, expect in MUTATIONS:
        owner.checkpoint()
        path = private / original.relative_to(REPO)
        pristine = path.read_bytes()
        if not apply_control(path, old, new):
            print(f"[FAIL] {name}: its anchor is not exactly once in "
                  f"{original.relative_to(REPO)}")
            failures += 1
            continue
        status, output = run_suite(suite, owner)
        path.write_bytes(pristine)
        broke = failed_checks(output)
        named = any(check.startswith(expect) for check in broke)
        if suite_failed(output) and named:
            print(f"[ ok ] {name}: caught by \"{expect}\"")
        elif suite_failed(output):
            print(f"[FAIL] {name}: caught, but not by \"{expect}\"; "
                  f"broke {sorted(set(broke))[:3]}")
            failures += 1
        else:
            reason = ("the suite stayed green" if TALLY_RE.search(output)
                      else "no completed suite tally")
            print(f"[FAIL] {name}: {reason} (make exit {status})")
            failures += 1
    return failures


def main() -> int:
    """Run every control, or list them."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true",
                        help="name the controls and change nothing")
    args = parser.parse_args()

    if args.list:
        for name, path, _old, _new, expect in MUTATIONS:
            print(f"{name:28s} {path.relative_to(REPO)}  -> {expect}")
        return 0

    try:
        with OwnedProcesses() as owner:
            with tempfile.TemporaryDirectory(prefix="gptp-tables-mutants-") as scratch:
                private = Path(scratch)
                targets = {row[1] for row in MUTATIONS}
                copy_inputs(REPO, HERE, private, owner, targets)
                failures = campaign(private, owner)
            owner.checkpoint()
        print(f"controls: {len(MUTATIONS)}   failures: {failures}")
        print(f"RESULT: {'PASS' if failures == 0 else 'FAIL'}")
        return 1 if failures else 0
    except Cancelled as exc:
        print(f"CANCELLED: signal {exc.signum}; no mutation verdict", file=sys.stderr)
        return 128 + exc.signum
    except (InputRefused, OSError, RuntimeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
