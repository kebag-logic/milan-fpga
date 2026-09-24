#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probes for PR #540 round R277-2 (issue #387 gmstep leg).

Run from <tree>/tb/verilator/milan_dp of a disposable copy of the exact head.
Every build goes through the Makefile's own `gmstep-build` recipe with
DP_SRC / CLKV_SRC / RSP_SRC / GMSTEP_MDIR overridden; nothing in the tree is
edited (planted copies live in --scratch).

  --sweep A-B      clean leg on --datapath at every feed delay A..B
  --probes D,..    every probe below at every listed feed delay
  --head D,..      the unedited head datapath at every listed feed delay

A probe with `expect` must FAIL with every named check among its failures
(a build failure, a crash or a missing summary is NOT a catch). A probe with
expect == [] is a boundary control that must PASS; expect == "INFO" is
recorded only (it must still produce the leg's summary). Builds run one at a time
(VERILATOR_JOBS from the environment); legs run at most --jobs (<= 8) at once.
Writes one JSON line per run to --out/<campaign>.jsonl and each run's stdout
to --out/raw/. Exit 0 only when every run is as required.
"""

import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path.cwd()
CLKV = HERE / "../../../hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv"
STAGE = HERE / "../../../hdl/ieee1722/aaf/KL_render_setpoint.sv"
HEAD_DP = HERE / "../../../hdl/milan/milan_datapath.sv"

RENDER_LINE = "       media_rebase_p_w | src_recentre_p_r;"
REBASE_LINE = "  wire media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load;"
MCR_TAIL = "                       | media_rebase_p_w;"
RENDER_DECL = "  wire render_recentre_p_w /* verilator public_flat_rd */ ="
EN_ASSIGN = "assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;\n"
EN_PORT = "    .stream_en_i (aaf_stream_en_w),\n"


def delayed(name: str, source: str, cycles: int) -> str:
    """SV block: `name` pulses `cycles` cycles after `source` pulses."""
    return (f"  logic [15:0] {name}_cnt_r;\n"
            f"  logic        {name};\n"
            f"  always_ff @(posedge axis_clk) begin : {name}_b\n"
            f"    if (!axis_resetn) begin\n"
            f"      {name}_cnt_r <= 16'd0;\n"
            f"      {name}       <= 1'b0;\n"
            f"    end else begin\n"
            f"      {name} <= ({name}_cnt_r == 16'd1);\n"
            f"      if ({source}) {name}_cnt_r <= 16'd{cycles};\n"
            f"      else if ({name}_cnt_r != 16'd0) {name}_cnt_r <= {name}_cnt_r - 16'd1;\n"
            f"    end\n"
            f"  end : {name}_b\n")


def talker_dies(after_cycles: int) -> list[tuple[str, str]]:
    """Silence the AAF packetizer for good `after_cycles` after the SECOND
    plane step pulse (the first is the link-up step); the gate CSR still
    reads open because only the packetizer's enable is cut."""
    block = (EN_ASSIGN +
             "  logic [1:0]  probe_steps_r;\n"
             "  logic [19:0] probe_cnt_r;\n"
             "  logic        probe_dead_r;\n"
             "  always_ff @(posedge axis_clk) begin : probe_dies\n"
             "    if (!axis_resetn) begin\n"
             "      probe_steps_r <= 2'd0;\n"
             "      probe_cnt_r   <= 20'd0;\n"
             "      probe_dead_r  <= 1'b0;\n"
             "    end else begin\n"
             "      if (gptp_step_we_w && probe_steps_r != 2'd3) probe_steps_r <= probe_steps_r + 2'd1;\n"
             "      if (probe_steps_r == 2'd2 && !probe_dead_r) begin\n"
             f"        if (probe_cnt_r >= 20'd{after_cycles}) probe_dead_r <= 1'b1;\n"
             "        else probe_cnt_r <= probe_cnt_r + 20'd1;\n"
             "      end\n"
             "    end\n"
             "  end : probe_dies\n")
    return [(EN_ASSIGN, block),
            (EN_PORT, "    .stream_en_i (aaf_stream_en_w & ~{N_STREAMS{probe_dead_r}}),\n")]


TU_FALL = ("  logic probe_tuq_r;\n"
           "  always_ff @(posedge axis_clk) begin : probe_tuq\n"
           "    if (!axis_resetn) probe_tuq_r <= 1'b1;\n"
           "    else probe_tuq_r <= clkv_tu_w;\n"
           "  end : probe_tuq\n"
           "  wire probe_tu_fall_p_w = probe_tuq_r & ~clkv_tu_w;\n")

W_RENDER = "render: every counted re-base lands at a PDU end right after the step"
C_RENDER = "render: the GM change is one counted re-base event"
LAW = "render: every PDU push leaves the target fill across the event"
W_MR = "restart: every mr toggle is first sent right after the step"
MID_MR = "restart: MEDIA_RESET does not move between the commit and the step"
ONE_MR = "restart: the outgoing mr toggles exactly once"
ONE_CNT = "restart: the talker's MEDIA_RESET counts exactly one"
PAUSE = "licence: the talker never pauses beyond four of its intervals"
RATE = "licence: the talker keeps its baseline rate within 1%"
AFTER = "tu: talker PDUs graded after tu clears"
TU_FIRST = "tu: set in the first cycle the bank names GM B"

#: (id, what, file key, [(anchor, replacement)], checks that must fail)
PROBES = [
    ("P1", "render re-base keyed to the GM identity only (restart still on the step)", "dp",
     [(RENDER_LINE, "       gm_recentre_p_r | cfg_ptp_cmd_load | src_recentre_p_r;")],
     [W_RENDER]),
    ("P2", "mr restart keyed to the GM identity only (render still on the step)", "dp",
     [(MCR_TAIL, "                       | gm_recentre_p_r;")],
     [W_MR, MID_MR]),
    ("P3", "mr restart 3000 cycles (~4.7 talker intervals) after the step", "dp",
     [(REBASE_LINE, REBASE_LINE + "\n" + delayed("probe_mr_dly_p", "media_rebase_p_w", 3000)),
      (MCR_TAIL, "                       | probe_mr_dly_p;")],
     [W_MR]),
    ("P4", "render re-base 600 cycles after the step (beyond the 500-cycle window)", "dp",
     [(RENDER_DECL, delayed("probe_rr_dly_p", "media_rebase_p_w", 600) + RENDER_DECL),
      (RENDER_LINE, "       probe_rr_dly_p | src_recentre_p_r;")],
     [W_RENDER]),
    ("P5", "BOUNDARY: render re-base 150 cycles after the step (must still pass)", "dp",
     [(RENDER_DECL, delayed("probe_rr_dly_p", "media_rebase_p_w", 150) + RENDER_DECL),
      (RENDER_LINE, "       probe_rr_dly_p | src_recentre_p_r;")],
     []),
    ("P6", "talker silenced for good at the step", "dp", talker_dies(0),
     [PAUSE, RATE, AFTER]),
    ("P7", "talker silenced for good 640000 cycles after the step (tu long clear)", "dp",
     talker_dies(640000),
     [PAUSE, RATE]),
    ("P8", "recentre snaps one event LOW (fill 13 after the push)", "stage",
     [("                rptr_r[s]    <= snap_rptr_w;\n                prefill_r[s] <= 1'b0;\n",
       "                rptr_r[s]    <= prefill_r[s] ? snap_rptr_w : snap_rptr_w + 1'b1;\n"
       "                prefill_r[s] <= 1'b0;\n")],
     [LAW]),
    ("P9", "recentre snaps one event HIGH (fill 15 after the push)", "stage",
     [("                rptr_r[s]    <= snap_rptr_w;\n                prefill_r[s] <= 1'b0;\n",
       "                rptr_r[s]    <= prefill_r[s] ? snap_rptr_w : snap_rptr_w - 1'b1;\n"
       "                prefill_r[s] <= 1'b0;\n")],
     [LAW]),
    ("P10", "mr restart on the step AND the identity (two toggles)", "dp",
     [(MCR_TAIL, "                       | media_rebase_p_w | gm_recentre_p_r;")],
     [ONE_MR, W_MR, MID_MR]),
    ("P11", "re-base (render and restart) keyed to tu falling, not the step", "dp",
     [(REBASE_LINE, TU_FALL + "  wire media_rebase_p_w = probe_tu_fall_p_w | cfg_ptp_cmd_load;")],
     [W_RENDER, W_MR]),
    ("P12", "INFO: tu reaches the talkers ONE cycle late (the bank copy lags the "
     "discontinuity pulse by one cycle, so this may sit inside the contract)", "clkv",
     [("  assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w;\n",
       "  logic tu_late1_r;\n"
       "  always_ff @(posedge clk_i) begin : p_tu_late1\n"
       "    tu_late1_r <= (~sync_ok_w) | hold_w | disc_p_w;\n"
       "  end : p_tu_late1\n"
       "  assign ts_uncertain_o = tu_late1_r;\n")],
     "INFO"),
    ("P13", "tu reaches the talkers TWO cycles late", "clkv",
     [("  assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w;\n",
       "  logic [1:0] tu_late2_r;\n"
       "  always_ff @(posedge clk_i) begin : p_tu_late2\n"
       "    tu_late2_r <= {tu_late2_r[0], (~sync_ok_w) | hold_w | disc_p_w};\n"
       "  end : p_tu_late2\n"
       "  assign ts_uncertain_o = tu_late2_r[1];\n")],
     [TU_FIRST]),
    ("P14", "Stream Input GET_COUNTERS answer an empty mask (vacuous listener arms)", "dp",
     [("  wire ctr_sin_w = (ctrq_type_r == DESC_STREAM_INPUT_C)\n"
       "                && (ctrq_index_r < 16'(N_STREAMS));",
       "  wire ctr_sin_w = 1'b0;")],
     ["licence: both Stream Input answers carry MEDIA_UNLOCKED and FRAMES_RX",
      "licence: FRAMES_RX advances by the PDUs the listener accepted"]),
]


def build(dp: Path, clkv: Path, stage: Path, mdir: str, logs: Path, tag: str) -> bool:
    cmd = ["make", "gmstep-build", f"GMSTEP_MDIR={mdir}", f"DP_SRC={dp}",
           f"CLKV_SRC={clkv}", f"RSP_SRC={stage}"]
    for name in ("VERILATOR", "VERILATOR_JOBS"):
        if name in os.environ:
            cmd.append(f"{name}={os.environ[name]}")
    done = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, check=False)
    (logs / f"build-{tag}.log").write_text(done.stdout + done.stderr, encoding="utf-8")
    return done.returncode == 0 and (HERE / mdir / "Vmilan_dp_gmstep").exists()


def run_leg(mdir: str, delay: int) -> tuple[int, str]:
    done = subprocess.run([f"./{mdir}/Vmilan_dp_gmstep", f"{mdir}/aemi.bin", str(delay)],
                          cwd=HERE, capture_output=True, text=True, check=False)
    return done.returncode, done.stdout + done.stderr


def failed(log: str) -> list[str]:
    return [line.split("[FAIL]", 1)[1].split(" got=")[0].strip()
            for line in log.splitlines() if "[FAIL]" in line]


def summary(log: str) -> str:
    lines = [line for line in log.splitlines() if line.startswith("== gmstep: checks:")]
    return lines[0] if lines else "NO SUMMARY"


def grep(log: str, prefix: str) -> list[str]:
    return [line for line in log.splitlines() if line.startswith(prefix)]


def execute(jobs: list, out: Path, name: str,
            width: int) -> int:
    """jobs: (probe id, mdir, delay, expect or None for must-pass)."""
    bad = 0
    raw = out / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=width) as pool:
        results = list(pool.map(lambda j: (j, *run_leg(j[1], j[2])), jobs))
    with open(out / f"{name}.jsonl", "a", encoding="utf-8") as sink:
        for (pid, _mdir, delay, expect), status, log in results:
            (raw / f"{name}-{pid}-d{delay}.log").write_text(log, encoding="utf-8")
            broke = failed(log)
            has_summary = "== gmstep: checks:" in log
            if expect == "INFO":
                ok = has_summary
                verdict = "INFO " + ("PASSED" if status == 0 and not broke else "FAILED")
                missing = []
            elif expect is None or expect == []:
                ok = status == 0 and "RESULT: PASS" in log and not broke
                verdict = "PASS as required" if ok else "UNEXPECTED FAIL"
                missing = []
            else:
                missing = [c for c in expect if c not in broke]
                ok = status != 0 and has_summary and not missing
                verdict = "CAUGHT" if ok else "ESCAPED"
            bad += 0 if ok else 1
            record = {"campaign": name, "probe": pid, "delay": delay, "exit": status,
                      "summary": summary(log), "failed": broke, "expected": expect,
                      "missing": missing, "verdict": verdict,
                      "render_fill": grep(log, "RENDER: fill after"),
                      "recentres": grep(log, "RENDER: counted recentre"),
                      "mr": grep(log, "RESTART:"), "talker": grep(log, "TALKER:"),
                      "event": grep(log, "EVENT: identity"), "tu": grep(log, "TU:")}
            sink.write(json.dumps(record) + "\n")
            print(f"[{verdict}] {name} {pid} delay {delay}: {summary(log)} failed={broke}",
                  flush=True)
    return bad


def delays(text: str) -> list[int]:
    if "-" in text:
        a, b = (int(x) for x in text.split("-", 1))
        return list(range(a, b + 1))
    return [int(x) for x in text.split(",")]


def plant(base: Path, dest: Path, edits: list[tuple[str, str]]) -> None:
    text = base.read_text(encoding="utf-8")
    for anchor, repl in edits:
        if text.count(anchor) != 1:
            raise SystemExit(f"anchor not unique ({text.count(anchor)}) in {base}: {anchor!r}")
        text = text.replace(anchor, repl, 1)
    dest.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--datapath", type=Path, required=True)
    ap.add_argument("--sweep", type=delays)
    ap.add_argument("--probes", type=delays)
    ap.add_argument("--only", default="")
    ap.add_argument("--head", type=delays)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    a = ap.parse_args()
    if not 1 <= a.jobs <= 8:
        ap.error("--jobs must be 1..8")
    a.out.mkdir(parents=True, exist_ok=True)
    a.scratch.mkdir(parents=True, exist_ok=True)
    blogs = a.scratch / "build-logs"
    blogs.mkdir(exist_ok=True)
    dp, clkv, stage = a.datapath.resolve(), CLKV.resolve(), STAGE.resolve()
    bad = 0
    if a.head:
        if not build(HEAD_DP.resolve(), clkv, stage, "obj_r277_head", blogs, "head"):
            print("[BUILD FAIL] head"); return 1
        # the head is expected to fail exactly the four pending checks
        expect = [C_RENDER, W_RENDER, ONE_MR, ONE_CNT]
        bad += execute([("HEAD", "obj_r277_head", d, expect) for d in a.head], a.out, "head",
                       a.jobs)
        shutil.rmtree(HERE / "obj_r277_head", ignore_errors=True)
    if a.sweep:
        if not build(dp, clkv, stage, "obj_r277_clean", blogs, "clean"):
            print("[BUILD FAIL] clean"); return 1
        bad += execute([("CLEAN", "obj_r277_clean", d, None) for d in a.sweep], a.out, "sweep",
                       a.jobs)
        shutil.rmtree(HERE / "obj_r277_clean", ignore_errors=True)
    if a.probes:
        only = set(a.only.split(",")) if a.only else None
        jobs = []
        built = []
        for pid, what, key, edits, expect in PROBES:
            if only and pid not in only:
                continue
            src = {"dp": dp, "clkv": clkv, "stage": stage}
            planted = a.scratch / f"{pid}_{src[key].name}"
            plant(src[key], planted, edits)
            src[key] = planted
            mdir = f"obj_r277_{pid}"
            if not build(src["dp"], src["clkv"], src["stage"], mdir, blogs, pid):
                print(f"[BUILD FAIL] {pid} {what}", flush=True)
                bad += 1
                with open(a.out / "probes.jsonl", "a", encoding="utf-8") as sink:
                    sink.write(json.dumps({"campaign": "probes", "probe": pid, "what": what,
                                           "verdict": "BUILD FAIL"}) + "\n")
                continue
            print(f"[built] {pid} {what}", flush=True)
            built.append(mdir)
            jobs += [(pid, mdir, d, expect) for d in a.probes]
        bad += execute(jobs, a.out, "probes", a.jobs)
        for mdir in built:
            shutil.rmtree(HERE / mdir, ignore_errors=True)
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'} ({bad} runs not as required)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
