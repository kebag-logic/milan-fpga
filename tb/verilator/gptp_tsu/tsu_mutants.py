#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""tsu_mutants.py - planted defects of the timestamp unit (KL_gptp_tsu, #884) and of the split tap's gptp trailer
(KL_ctrl_split, #884's ruling item 2), each caught by its check.

Each defect replaces one exact text of hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv or hdl/milan/KL_ctrl_split.sv
(FILES) in a scratch copy, builds the bench on it and requires a [FAIL] line carrying the named words. A text
not found once, a build that passes, or a failure only elsewhere fails the campaign; the unplanted source must pass
first.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE.parents[2] / "hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv"

#: The two sources a defect may be planted in: the unit, and the split tap whose trailer carries its ingress stamp.
FILES = {"tsu": ("RTL", RTL), "split": ("SPLIT", HERE.parents[2] / "hdl/milan/KL_ctrl_split.sv")}

#: (name, file, old text, new text, the words its failing check must carry)
MUTANTS = (
    ("stamp-at-beat-1", "tsu",
     "      if (rx_first_r) begin\n        //! THE INGRESS STAMP POINT: the plane's, on this same edge\n"
     "        rx_ts_r   <= phc_ns_i - 64'(INGRESS_LAT_NS_P);",
     "      if (rx_second_r) rx_ts_r <= phc_ns_i - 64'(INGRESS_LAT_NS_P);\n      if (rx_first_r) begin\n"
     "        //! THE INGRESS STAMP POINT: the plane's, on this same edge",
     "I1 the trailer is the first beat's PHC less INGRESS_LAT"),
    ("ingress-latency-added", "tsu", "rx_ts_r   <= phc_ns_i - 64'(INGRESS_LAT_NS_P);",
     "rx_ts_r   <= phc_ns_i + 64'(INGRESS_LAT_NS_P);",
     "I1 the trailer is the first beat's PHC less INGRESS_LAT"),
    ("general-messages-timed", "tsu", "&& (rx_tdata_i[55:52] == 4'h1) && (rx_tdata_i[51:50] == 2'b00);",
     "&& (rx_tdata_i[55:52] == 4'h1);", "I3 general messages"),
    ("destination-ignored", "tsu", "rx_cand_r <= (da_w == DA_GPTP_C) && !rx_tlast_i;",
     "rx_cand_r <= !rx_tlast_i;", "I4 a Sync to another destination is not timed"),
    ("ethertype-ignored", "tsu", "rx_cand_r <= rx_cand_r && ({rx_tdata_i[39:32], rx_tdata_i[47:40]} == ET_GPTP_C)",
     "rx_cand_r <= rx_cand_r && 1'b1", "I4 another EtherType at the gPTP address is not timed"),
    ("sdo-ignored", "tsu", "&& (rx_tdata_i[55:52] == 4'h1) && (rx_tdata_i[51:50] == 2'b00);",
     "&& (rx_tdata_i[51:50] == 2'b00);", "I4 majorSdoId 0"),
    ("two-beat-frame-timed", "tsu", "assign rx_event_o = rx_cand_r && !rx_second_r;", "assign rx_event_o = rx_cand_r;",
     "I5 a frame of two beats carries no stamp"),
    ("trailer-lsb-first", "split", "stamp_head_w[8*(3'd7 - trl_idx_r) +: 8]", "stamp_head_w[8*trl_idx_r +: 8]",
     "I1 the trailer is the first beat's PHC less INGRESS_LAT"),
    ("trailer-dropped", "split", "        if (ser_last_r && ser_gptp_r) begin\n          trl_busy_r <= 1'b1;",
     "        if (1'b0) begin\n          trl_busy_r <= 1'b1;", "I1 a received Sync is delivered whole"),
    ("general-stamped", "split", "held_r   <= rx_event_i ? rx_stamp_i : '1;", "held_r   <= rx_stamp_i;",
     "I3 general messages"),
    ("stamp-room-unchecked", "split",
     "assign no_room_w = gptp_w && (((st_wp_r - st_rp_r) + (SW_C+1)'(held_v_r)) >= (SW_C+1)'(STAMPS_P));",
     "assign no_room_w = 1'b0;", "T2 under a flood every delivered frame carries its own stamp"),
    ("stamp-kept-for-dropped-frame", "split", "if (held_v_r && !ff_overflow_w) begin", "if (held_v_r) begin",
     "T3 a frame the frame FIFO drops takes its stamp with it"),
    ("refusal-uncounted", "split", "if ((drop_p_w | stamp_drop_p_w) & (rx_drops_o != 8'hFF))",
     "if (drop_p_w & (rx_drops_o != 8'hFF))", "T2 the stamp FIFO keeps 64"),
    ("half-tick-dropped", "tsu", "    + DP_TICK_NS_P / 2;\n  localparam longint signed TXTS_NET_NS_C",
     "    + 0;\n  localparam longint signed TXTS_NET_NS_C", "E2 GMII: the launch's PHC less 426 ns"),
    ("egress-latency-subtracted", "tsu", "longint'(TXTS_CORR_NS_C) - longint'(EGRESS_LAT_NS_P);",
     "longint'(TXTS_CORR_NS_C) + longint'(EGRESS_LAT_NS_P);", "plus EGRESS_LAT 219 ns"),
    ("mii-octet-term-dropped", "tsu", "(TXTS_DELTA_EXP_P + OBS_LAT_E_CYC_P + ETH_CYC_PER_OCTET_P - 1) * ETH_TICK_NS_P",
     "(TXTS_DELTA_EXP_P + OBS_LAT_E_CYC_P) * ETH_TICK_NS_P", "E2 MII: the launch's PHC less 3770 ns"),
    ("delta-unchecked", "tsu", "&& (cap_delta_r == TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P));", ";",
     "E3 an aborted launch and a fragmented one are losses"),
    ("abort-unchecked", "tsu", "assign tx_ok_w    = gen_ok_w && !cap_abort_r && cap_elig_r",
     "assign tx_ok_w    = gen_ok_w && cap_elig_r", "E3 an aborted launch and a fragmented one are losses"),
    ("guard-ignored", "tsu", "        cap_elig_r  <= (phc_dirty_r == GDW_C'(0));", "        cap_elig_r  <= 1'b1;",
     "G1 a launch 20 cycles after a PHC step is a loss"),
    ("envelope-ignored", "tsu", "                   && (longint'(adj_abs_w) <= PHC_ADJ_MAX_C);", "                   ;",
     "G3 an addend past the 200 ppm envelope is a loss"),
    ("unsealed-accepted", "tsu", "wire  gen_ok_w = echo_ok_r && (cap_gen_r == GEN_C);",
     "wire  gen_ok_w = (cap_gen_r == GEN_C);", "E1 before the echo a launch is a counted loss"),
    ("generation-unchecked", "tsu", "wire  gen_ok_w = echo_ok_r && (cap_gen_r == GEN_C);",
     "wire  gen_ok_w = echo_ok_r;", "S1 a record of generation 0"),
    ("no-reseal", "tsu", "      if (frame_w && cap_gen_r != GEN_C) echo_ok_r <= 1'b0;", "",
     "S1 and the unit offers its seal again"),
    ("full-overwrites", "tsu", "        if (full_w && !pop_w) begin", "        if (1'b0) begin",
     "F1 the 33rd egress record past 32 held is counted"),
)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """One command in cwd, its output captured."""
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def one(work: Path, name: str, file: str, old: str | None, new: str | None,
        needle: str | None) -> tuple[str, bool, str]:
    """One arm under work/<name>: the unplanted unit must pass; a planted one, in FILES[file], must fail with its
    needle's words. Returns the name, whether it did, and the line that says so."""
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    var, src = FILES[file]
    text = src.read_text()
    if old is not None:
        if text.count(old) != 1:
            return name, False, f"REFUSED: its text is in {src.name} {text.count(old)} times, not once"
        text = text.replace(old, new)
    (d / src.name).write_text(text)
    vl = os.environ.get("VERILATOR", "verilator")
    r = run(["make", "-s", f"VERILATOR={vl}", f"{var}={d / src.name}", f"MDIR={d / 'obj'}", "run"], HERE)
    log = r.stdout + r.stderr
    if old is None:
        return name, r.returncode == 0 and "RESULT: PASS" in log, log
    fails = [ln for ln in log.splitlines() if "[FAIL]" in ln]
    if r.returncode == 0:
        return name, False, "SURVIVED: the bench passed"
    hit = [ln for ln in fails if needle in ln]
    if not hit:
        return name, False, "MISSED: failed, not with its words:\n" + "\n".join(fails[:5]) + log[-400:]
    return name, True, "KILLED: " + hit[0].strip()


def main() -> int:
    """The baseline, then every planted defect in parallel; any survivor, miss or refusal fails the campaign."""
    work = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="tsu-mutants-"))
    name, ok, log = one(work, "baseline", "tsu", None, None, None)
    print(f"baseline: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(log[-2000:])
        return 2
    with ThreadPoolExecutor(max_workers=8) as pool:
        res = list(pool.map(lambda m: one(work, *m), MUTANTS))
    failed = 0
    for name, ok, log in res:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: {log.splitlines()[0]}")
        if not ok:
            failed += 1
            print("\n".join("      " + ln for ln in log.splitlines()[1:6]))
    print(f"== gptp timestamp unit planted defects: checks: {len(MUTANTS)}   failures: {failed} ==")
    print("RESULT: " + ("PASS" if not failed else "FAIL"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
