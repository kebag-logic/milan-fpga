#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-planted mutants for processor issue #128 (KL_acmp_talker).

Usage: reviewer_mutants.py SRC_CLONE SCRATCH VERILATOR OUT [--jobs N] [--suite S]
                           [--only NAME ...] [--base-rtl REV]

Exports the exact HEAD of SRC_CLONE with `git archive` into one disposable
tree per mutant under SCRATCH, applies one textual mutation to
hdl/acmp/KL_acmp_talker.sv (each anchor must match exactly once), builds and
runs tb/<suite> with the given Verilator, and records the tally and the FAIL
lines. SRC_CLONE is never written. A mutant counts as KILLED only when the
simulation printed a tally and it has a nonzero FAIL count or nonzero exit;
a missing tally (build error) is reported as NO-TALLY, never as a kill.
"""
import argparse
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

RTL = "hdl/acmp/KL_acmp_talker.sv"

MUTANTS = {
    # retry-lifetime restarts
    "no_conflict_wait_clear": [("|| !en_q_r[i] || set_conflict_w[i])", "|| !en_q_r[i])")],
    "no_reenable_wait_clear": [("if (!cfg_src_en_i[i] || !en_q_r[i] || set_conflict_w[i])",
                                "if (!cfg_src_en_i[i] || set_conflict_w[i])")],
    "wait_on_release": [("ev_to_maap_w && !ev_maap_rel_w)\n        retry_wait_r",
                         "ev_to_maap_w)\n        retry_wait_r")],
    "tick_no_rearm": [("      if (retry_tick_w) begin\n        retry_t0_r   <= now_ms_i;\n",
                       "      if (retry_tick_w) begin\n")],
    "no_rotate_advance": [("          retry_next_r <= (disp_src_w == SRC_W_C'(N_STREAM_OUT_P - 1))\n"
                           "                          ? '0 : disp_src_w + SRC_W_C'(1);",
                           "          retry_next_r <= retry_next_r;")],
    # obsolete-grant cancellation
    "no_sticky_gp_window": [("(maap_busy_r || gp_valid_r) && maap_kill_w", "maap_busy_r && maap_kill_w")],
    "grant_kill_reg_only": [("if (maap_kill_r || maap_kill_w)", "if (maap_kill_r)")],
    "accept_kill_zero": [("        maap_kill_r <= !cfg_src_en_i[mreq_src_r] || pe_off_r[mreq_src_r]\n"
                          "                       || pe_conflict_r[mreq_src_r]\n"
                          "                       || (maap_conflict_valid_i\n"
                          "                           && maap_conflict_src_i == mreq_src_r);",
                          "        maap_kill_r <= 1'b0;")],
    "kill_no_pending_conflict": [("  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]\n"
                                  "                       || pe_conflict_r[maap_src_r]\n",
                                  "  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]\n")],
    "kill_no_live_conflict": [("                       || pe_conflict_r[maap_src_r]\n"
                               "                       || (maap_conflict_valid_i\n"
                               "                           && maap_conflict_src_i == maap_src_r);",
                               "                       || pe_conflict_r[maap_src_r];")],
    "kill_no_disable": [("  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]",
                         "  assign maap_kill_w = pe_off_r[maap_src_r]")],
    # command/event arbitration
    "init_elig_no_avail": [("|| (maap_avail_w && |init_ready_w));", "|| |init_ready_w);")],
    "no_turn_restore": [("        txn_turn_r <= 1'b1;\n        if (disp_code_w == EVC_INIT)",
                         "        if (disp_code_w == EVC_INIT)")],
    "elig_drop_rel": [("|| |pe_tmr_r || |pe_lsn_r || |pe_rel_r", "|| |pe_tmr_r || |pe_lsn_r")],
    "elig_drop_off": [("!(|pe_off_r || |pe_conflict_r", "!(|pe_conflict_r")],
    "ready_ignores_turn": [("assign txn_ready_o = (state_r == S_IDLE) && !gp_valid_r && txn_eligible_w;",
                            "assign txn_ready_o = (state_r == S_IDLE) && !gp_valid_r;")],
    # EVC_INIT guards
    "init_ignores_off_conflict": [("(rec_w.gstate == GS_NO_DA_C) && cfg_src_en_i[ev_src_r]\n"
                                   "            && !pe_off_r[ev_src_r] && !pe_conflict_r[ev_src_r]",
                                   "(rec_w.gstate == GS_NO_DA_C) && cfg_src_en_i[ev_src_r]")],
    "retry_period_200": [("DA_RETRY_MS_C = 32'd100", "DA_RETRY_MS_C = 32'd200")],
    "tick_ge_to_gt": [("(now_ms_i - retry_t0_r) >= DA_RETRY_MS_C", "(now_ms_i - retry_t0_r) > DA_RETRY_MS_C")],
    # whole-cause removals (the single-term kill mutants above are mutually redundant)
    "kill_no_conflict_at_all": [
        ("                       || pe_conflict_r[maap_src_r]\n"
         "                       || (maap_conflict_valid_i\n"
         "                           && maap_conflict_src_i == maap_src_r);",
         "                       ;"),
        ("        maap_kill_r <= !cfg_src_en_i[mreq_src_r] || pe_off_r[mreq_src_r]\n"
         "                       || pe_conflict_r[mreq_src_r]\n"
         "                       || (maap_conflict_valid_i\n"
         "                           && maap_conflict_src_i == mreq_src_r);",
         "        maap_kill_r <= !cfg_src_en_i[mreq_src_r] || pe_off_r[mreq_src_r];")],
    "kill_no_disable_at_all": [
        ("  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]\n"
         "                       || pe_conflict_r[maap_src_r]",
         "  assign maap_kill_w = pe_conflict_r[maap_src_r]"),
        ("        maap_kill_r <= !cfg_src_en_i[mreq_src_r] || pe_off_r[mreq_src_r]\n"
         "                       || pe_conflict_r[mreq_src_r]",
         "        maap_kill_r <= pe_conflict_r[mreq_src_r]")],
    "kill_sticky_off": [("      if (!maap_accept_w && (maap_busy_r || gp_valid_r) && maap_kill_w)\n"
                         "        maap_kill_r <= 1'b1;\n", "")],
    # demand-driven attempt paths that the paced rounds could mask
    "no_probe_initset": [("    if ((state_r == S_TXN_ACT) && txn_initset_w) set_init_w[tsrc_w]   = 1'b1;\n", "")],
    "no_lsn_initset": [("          ev_initset_w = 1'b1;    // a listener appeared: retry allocation", "")],
    "no_conflict_daok_initset": [("          ev_rec2_w.gstate = GS_NO_DA_C;   // nothing declared: no backoff\n"
                                  "          ev_initset_w     = 1'b1;",
                                  "          ev_rec2_w.gstate = GS_NO_DA_C;   // nothing declared: no backoff")],
    "no_backoff_exit_initset": [("            ev_initset_w     = 1'b1;   // re-allocate, then re-declare", "")],

}


def export(src: Path, dest: Path, rev: str = "HEAD") -> None:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    arc = subprocess.run(["git", "-C", str(src), "archive", rev], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=arc, check=True)


def run(name: str, args, edits=None, base_rtl=None) -> str:
    tree = args.scratch / name
    export(args.src, tree)
    rtl = tree / RTL
    if base_rtl is not None:
        rtl.write_bytes(subprocess.run(["git", "-C", str(args.src), "show", f"{base_rtl}:{RTL}"],
                                       check=True, capture_output=True).stdout)
    for old, new in edits or []:
        text = rtl.read_text()
        n = text.count(old)
        if n != 1:
            return f"{name} ANCHOR-COUNT={n}"
        rtl.write_text(text.replace(old, new))
    res = subprocess.run(["make", "-C", str(tree / "tb" / args.suite), f"VERILATOR={args.verilator}"],
                         capture_output=True, text=True, timeout=3000)
    out = res.stdout + res.stderr
    (args.out / f"{args.suite}-{name}.log").write_text(out)
    tallies = re.findall(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", out)
    if not tallies:
        verdict = "NO-TALLY"
    else:
        fails = int(tallies[-1][2])
        verdict = "KILLED" if (fails or res.returncode) else "SURVIVED"
    fl = [l for l in out.splitlines() if l.startswith("FAIL")]
    shutil.rmtree(tree, ignore_errors=True)
    t = " ".join("/".join(x) for x in tallies[-1:])
    return f"{name} rc={res.returncode} tally={t or '-'} fails={len(fl)} {verdict}" + \
        "".join(f"\n    {l}" for l in fl[:6])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path)
    ap.add_argument("scratch", type=Path)
    ap.add_argument("verilator")
    ap.add_argument("out", type=Path)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--suite", default="acmp_talker")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--base-rtl", help="also run the talker RTL from this revision under the head tests")
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    args.out.mkdir(parents=True, exist_ok=True)
    head = subprocess.check_output(["git", "-C", str(args.src), "rev-parse", "HEAD"], text=True).strip()
    jobs = [("baseline", None, None)]
    if args.base_rtl:
        jobs.append((f"base_rtl_{args.base_rtl[:8]}", None, args.base_rtl))
    for n in (args.only if args.only is not None else MUTANTS):
        jobs.append((n, MUTANTS[n], None))
    lines = [f"head {head}", f"suite {args.suite}",
             "verilator " + subprocess.check_output([args.verilator, "--version"], text=True).strip()]
    with cf.ThreadPoolExecutor(max_workers=min(args.jobs, 8)) as ex:
        futs = {ex.submit(run, n, args, e, b): n for n, e, b in jobs}
        results = {futs[f]: f.result() for f in cf.as_completed(futs)}
    for n, _, _ in jobs:
        lines.append(results[n])
    text = "\n".join(lines) + "\n"
    (args.out / f"summary-{args.suite}.txt").write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
