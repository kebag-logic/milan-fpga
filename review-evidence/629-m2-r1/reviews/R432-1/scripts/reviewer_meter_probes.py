#!/usr/bin/env python3
"""Reviewer-own meter mutants: does ANY meter check fail under each?

Each probe is a set of exact replacements (each anchor exactly once) applied
to a scratch copy of hdl/ieee1722/crf/KL_aaf_clock_meter.sv. The suite's own
Makefile builds Vmeter_sim against the copy, and ALL fourteen meter cases run.
A probe is CAUGHT when the harness exits nonzero with a [FAIL] line; it
ESCAPES when every check passes. The failing check names are printed.

usage: reviewer_meter_probes.py <tree>/tb/verilator/aaf_clock_meter --work DIR
       [--jobs 8] [--only NAME ...]
env:   VERILATOR (the pinned 5.050 wrapper)
"""
import argparse
import os
import subprocess
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

PROBES = {
    # Round 4's rule, which the design's round 5 replaced (Lost PDUs, rule 1):
    # the deviation verdict is taken only at a group's PDU 15, so a group that
    # loses a later PDU is never checked.
    "deviation_verdict_deferred_to_pdu15": (
        ("  logic        pdu_restart_r;\n",
         "  logic        pdu_restart_r;\n  logic        dev_bad_r;\n"),
        ("      pdu_restart_r <= 1'b0;\n      max_dev_r <= '0;",
         "      pdu_restart_r <= 1'b0; dev_bad_r <= 1'b0;\n      max_dev_r <= '0;"),
        ("          grp_id_r  <= s2_gid_w;\n        end else",
         "          grp_id_r  <= s2_gid_w; dev_bad_r <= 1'b0;\n        end else"),
        ("          if (!s2_in_bound_w) begin\n"
         "            grp_act_r     <= 1'b0;\n"
         "            pdu_restart_r <= 1'b1;\n"
         "          end else if (s2_pos_w == 4'd15) begin",
         "          if (s2_pos_w == 4'd15 && (dev_bad_r || !s2_in_bound_w)) begin\n"
         "            grp_act_r     <= 1'b0;\n"
         "            pdu_restart_r <= 1'b1;\n"
         "          end else if (s2_pos_w == 4'd15) begin"),
        ("          end else begin\n            grp_sum_r <= grp_sum_r + 20'(s2_dev_r);",
         "          end else begin\n            if (!s2_in_bound_w) dev_bad_r <= 1'b1;\n"
         "            grp_sum_r <= grp_sum_r + 20'(s2_dev_r);"),
    ),
    # a sequence gap no longer breaks the settle run before lock
    "gap_does_not_break_settle": (
        ("        if (s2_gap_r)                              settle_r <= '0;\n"
         "        else if (settle_r",
         "        if (settle_r"),
    ),
    # a change of the followed listener keeps a held lock
    "listener_change_keeps_lock": (
        ("wire lock_clr_w  = en_rise_w || en_fall_w || idx_chg_w || !en_w;",
         "wire lock_clr_w  = en_rise_w || en_fall_w || !en_w;"),
    ),
    # the bind edge also clears a held lock (the design says it clears none)
    "bind_edge_clears_lock": (
        ("wire lock_clr_w  = en_rise_w || en_fall_w || idx_chg_w || !en_w;",
         "wire lock_clr_w  = en_rise_w || en_fall_w || idx_chg_w || !en_w || bind_rise_w;"),
    ),
    # channels_per_frame == 0 accepted
    "cpf_zero_accepted": (
        ("               && !f_sp_w && (f_cpf_w != 10'd0)",
         "               && !f_sp_w"),
    ),
    # nsr not checked
    "nsr_unchecked": (
        ("(f_nsr_w == AAF_NSR_48K_C)", "1'b1"),
    ),
    # format not checked
    "format_unchecked": (
        ("(f_format_w == AAF_FMT_INT32_C)", "1'b1"),
    ),
    # sp not checked
    "sp_unchecked": (
        ("               && !f_sp_w && (f_cpf_w != 10'd0)",
         "               && (f_cpf_w != 10'd0)"),
    ),
    # tv not checked
    "tv_unchecked": (
        ("(subtype_i == 8'(AAF)) && tv_i", "(subtype_i == 8'(AAF))"),
    ),
    # a STOPPED input is consumed
    "stopped_ignored": (
        ("(match_idx_i == follow_idx_i) && !stopped_w", "(match_idx_i == follow_idx_i)"),
    ),
    # the group mean divides by 8 (wrong pick arithmetic)
    "mean_divides_by_8": (
        ("g_pick_r <= pc_ts0_r + 32'(pc_sum_r >>> GRP_LOG2_C);",
         "g_pick_r <= pc_ts0_r + 32'(pc_sum_r >>> 3);"),
    ),
    # the history count steps by 1 across a voided group (grid slips a group)
    "k2_counts_one_interval": (
        ("hist_cnt_r <= (g_k_r == 4'd2) ? g3_c2_w : g3_c1_w;", "hist_cnt_r <= g3_c1_w;"),
    ),
    # max deviation status not saturated / not tracked
    "max_dev_not_tracked": (
        ("          else if (16'(s2_abs_w) > max_dev_r)  max_dev_r <= 16'(s2_abs_w);\n", "\n"),
    ),
    # restart count not incremented on a spacing restart
    "spacing_restart_not_counted": (
        ("          if (!g_first_r) restart_cnt_r <= restart_cnt_r + 8'd1;\n", "\n"),
    ),
    # lock after 7 PDUs instead of 8 (settle compare off by one)
    "settle_off_by_one": (
        ("else if (settle_r != 3'(SETTLE_C - 1))", "else if (settle_r != 3'(SETTLE_C - 2))"),
    ),
}


def mutate(src, edits):
    for a, r in edits:
        if src.count(a) != 1:
            return None
        src = src.replace(a, r)
    return src


def one(args):
    suite, work, name = args
    meter = Path(suite) / "../../../hdl/ieee1722/crf/KL_aaf_clock_meter.sv"
    src = mutate(meter.read_text(), PROBES[name])
    if src is None:
        return name, "ANCHOR-ERROR", ""
    with tempfile.TemporaryDirectory(dir=work, prefix=f"{name}-") as d:
        p = Path(d) / f"{name}.sv"
        p.write_text(src)
        b = subprocess.run(["make", "-s", "-C", suite, "build", f"METER_RTL={p}",
                            f"MDIR={d}/obj", f"VERILATOR={os.environ['VERILATOR']}",
                            "VERILATOR_JOBS=1"], capture_output=True, text=True)
        if b.returncode:
            return name, "BUILD-FAILED", (b.stdout + b.stderr)[-1500:]
        r = subprocess.run([f"{d}/obj/Vmeter_sim"], capture_output=True, text=True)
        out = r.stdout + r.stderr
        fails = [ln for ln in out.splitlines() if "[FAIL]" in ln]
        tally = [ln for ln in out.splitlines() if "checks:" in ln]
        verdict = "CAUGHT" if (r.returncode != 0 and fails) else "ESCAPED"
        return name, verdict, "\n".join(tally + fails[:12])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("suite")
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    suite = str(Path(a.suite).resolve())
    names = [n for n in PROBES if not a.only or n in a.only]
    with ProcessPoolExecutor(a.jobs) as ex:
        res = list(ex.map(one, [(suite, a.work, n) for n in names]))
    for n, v, detail in res:
        print(f"===== {n}: {v}")
        if detail:
            print(detail)
    print("SUMMARY: " + ", ".join(f"{n}={v}" for n, v, _ in res))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
