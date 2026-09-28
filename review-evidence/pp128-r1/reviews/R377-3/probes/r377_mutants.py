#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (R377-2, extended for R377-3): plant single edits in scratch copies of the
processor tree and (a) run the committed KL_acmp_talker suite, or (b) run a
randomized observational lockstep of the edited module against the original.

Never writes to the source tree. Usage:
  r377_mutants.py suite    --src TREE --work DIR --out DIR [--only NAME ...]
  r377_mutants.py lockstep --src TREE --work DIR --out DIR --seeds N --cycles C
Environment: VERILATOR names the simulator (default: verilator on PATH).
"""

import argparse
import concurrent.futures as cf
import os
import re
import shutil
import subprocess
from pathlib import Path

RTL = "hdl/acmp/KL_acmp_talker.sv"
HERE = Path(__file__).resolve().parent

# name: (list of (anchor, replacement), expectation note)
MUTANTS = {
    # control: identity edit, must pass the suite and never diverge
    "identity": ([("localparam logic [31:0] DA_RETRY_MS_C = 32'd100;",
                   "localparam logic [31:0] DA_RETRY_MS_C = 32'd100;")], "control"),
    # control: a mutant the committed campaign kills; lockstep must diverge
    "ctl_kill_no_live_conflict": ([(
        "                       || pe_conflict_r[maap_src_r]\n"
        "                       || (maap_conflict_valid_i\n"
        "                           && maap_conflict_src_i == maap_src_r);",
        "                       || pe_conflict_r[maap_src_r];")], "control"),
    # the four terms the campaign records as equivalent
    "eq_no_sticky_gp_window": ([("(maap_busy_r || gp_valid_r) && maap_kill_w",
                                 "maap_busy_r && maap_kill_w")], "claimed equivalent"),
    "eq_accept_kill_zero": ([(
        "        maap_kill_r <= !cfg_src_en_i[mreq_src_r] || pe_off_r[mreq_src_r]\n"
        "                       || pe_conflict_r[mreq_src_r]\n"
        "                       || (maap_conflict_valid_i\n"
        "                           && maap_conflict_src_i == mreq_src_r);",
        "        maap_kill_r <= 1'b0;")], "claimed equivalent"),
    "eq_accept_kill_no_disable": ([(
        "maap_kill_r <= !cfg_src_en_i[mreq_src_r] || pe_off_r[mreq_src_r]",
        "maap_kill_r <= 1'b0 && pe_off_r[mreq_src_r]")], "claimed equivalent"),
    "eq_kill_no_pending_conflict": ([(
        "  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]\n"
        "                       || pe_conflict_r[maap_src_r]\n",
        "  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]\n")],
        "claimed equivalent"),
    # the removed term, re-inserted: must be equivalent to the head
    "readd_en_q_clear": ([("if (!cfg_src_en_i[i] || set_conflict_w[i])",
                           "if (!cfg_src_en_i[i] || !en_q_r[i] || set_conflict_w[i])")],
                         "removed-as-equivalent term"),
    # reviewer-derived single-term mutants
    "elig_drop_conflict": ([("!(|pe_off_r || |pe_conflict_r || |pe_pcp_r",
                             "!(|pe_off_r || |pe_pcp_r")], "reviewer"),
    "elig_drop_pcp": ([("!(|pe_off_r || |pe_conflict_r || |pe_pcp_r",
                        "!(|pe_off_r || |pe_conflict_r")], "reviewer"),
    "elig_drop_tmr": ([("|| |pe_tmr_r || |pe_lsn_r || |pe_rel_r",
                        "|| |pe_lsn_r || |pe_rel_r")], "reviewer"),
    "elig_drop_lsn": ([("|| |pe_tmr_r || |pe_lsn_r || |pe_rel_r",
                        "|| |pe_tmr_r || |pe_rel_r")], "reviewer"),
    "elig_unmasked_init": ([("|| (maap_avail_w && |init_ready_w));",
                             "|| (maap_avail_w && |pe_init_r));")], "reviewer"),
    "init_busy_else_removed": ([(
        "            ev_initset_w = 1'b1;  // maap busy: keep the request pending", "")],
        "reviewer: suspected dead branch"),
    "kill_w_no_off": ([(
        "  assign maap_kill_w = !cfg_src_en_i[maap_src_r] || pe_off_r[maap_src_r]\n",
        "  assign maap_kill_w = !cfg_src_en_i[maap_src_r]\n")], "reviewer"),
    "accept_kill_no_pending_conflict": ([(
        "                       || pe_conflict_r[mreq_src_r]\n", "")], "reviewer"),
    "accept_kill_no_live_conflict": ([(
        "                       || (maap_conflict_valid_i\n"
        "                           && maap_conflict_src_i == mreq_src_r);", ";")], "reviewer"),
    "rotate_from_pointer": ([(
        "          retry_next_r <= (disp_src_w == SRC_W_C'(N_STREAM_OUT_P - 1))\n"
        "                          ? '0 : disp_src_w + SRC_W_C'(1);",
        "          retry_next_r <= retry_next_r + SRC_W_C'(1);")], "reviewer"),
    "turn_not_on_grant": ([(
        "        txn_turn_r <= 1'b1;\n        if (disp_code_w == EVC_INIT)",
        "        if (disp_code_w != EVC_GRANT) txn_turn_r <= 1'b1;\n"
        "        if (disp_code_w == EVC_INIT)")], "reviewer"),
    "tick_sets_all": ([("retry_tick_w ? cfg_src_en_i : '0", "retry_tick_w ? '1 : '0")],
                      "reviewer: expected equivalent"),
    "init_ready_no_en": ([("pe_init_r & cfg_src_en_i & ~retry_wait_r",
                           "pe_init_r & ~retry_wait_r")], "reviewer"),
    "disp_init_no_avail": ([("end else if (maap_avail_w && |init_ready_w) begin",
                             "end else if (|init_ready_w) begin")], "reviewer"),
    "wait_on_visit": ([(
        "      if ((state_r == S_EV_ACT) && ev_to_maap_w && !ev_maap_rel_w)\n"
        "        retry_wait_r[ev_src_r] <= 1'b1;",
        "      if ((state_r == S_IDLE) && disp_kind_w == DK_EV && disp_code_w == EVC_INIT)\n"
        "        retry_wait_r[disp_src_w] <= 1'b1;")], "reviewer"),
    "turn_clear_on_dispatch": ([(
        "      if (state_r == S_TXN_ACT) txn_turn_r <= 1'b0;",
        "      if ((state_r == S_IDLE) && disp_kind_w == DK_TXN) txn_turn_r <= 1'b0;")],
        "reviewer: expected equivalent"),
    # R377-3 additions: the round-3 stated equivalent m29 and the offer-pacing mutant
    "eq_sticky_kill_ignores_accept": ([(
        "if (!maap_accept_w && (maap_busy_r || gp_valid_r) && maap_kill_w)",
        "if ((maap_busy_r || gp_valid_r) && maap_kill_w)")], "claimed equivalent (m29)"),
    "wait_only_on_accept": ([(
        "if ((state_r == S_EV_ACT) && ev_to_maap_w && !ev_maap_rel_w)\n"
        "        retry_wait_r[ev_src_r] <= 1'b1;",
        "if (maap_accept_w && !mreq_rel_r)\n"
        "        retry_wait_r[mreq_src_r] <= 1'b1;")], "reviewer (R376-2 m27)"),
    "t0_reset_zero": ([("      retry_t0_r   <= now_ms_i;\n      retry_wait_r <= '0;\n"
                        "      retry_next_r <= '0;",
                        "      retry_t0_r   <= '0;\n      retry_wait_r <= '0;\n"
                        "      retry_next_r <= '0;")], "reviewer"),
}


def mutate(src: str, edits) -> str:
    for old, new in edits:
        if src.count(old) != 1:
            raise RuntimeError(f"anchor not unique ({src.count(old)}): {old[:60]!r}")
        src = src.replace(old, new)
    return src


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    for sub in ("hdl", "tb/acmp_talker", "tb/common"):
        if (src / sub).exists():
            shutil.copytree(src / sub, dst / sub,
                            ignore=shutil.ignore_patterns("obj_dir", "__pycache__"))


def run_suite(name: str, src: Path, work: Path, out: Path, verilator: str) -> str:
    tree = work / name
    copy_tree(src, tree)
    rtl = tree / RTL
    rtl.write_text(mutate(rtl.read_text(), MUTANTS[name][0]))
    res = subprocess.run(["make", "-C", str(tree / "tb/acmp_talker"), f"VERILATOR={verilator}"],
                         capture_output=True, text=True, check=False)
    text = res.stdout + res.stderr
    tally = re.search(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", text)
    fails = [ln for ln in text.splitlines() if ln.startswith("FAIL:")]
    verdict = ("NO-TALLY" if tally is None else
               ("SURVIVED" if res.returncode == 0 and not fails else "KILLED"))
    (out / f"suite-{name}.txt").write_text(
        f"mutant: {name}\nnote: {MUTANTS[name][1]}\nrc: {res.returncode}\n"
        f"tally: {tally.group() if tally else 'none'}\nverdict: {verdict}\n"
        + "\n".join(fails[:40]) + ("\n" if fails else "")
        + ("" if tally else text[-3000:]))
    shutil.rmtree(tree, ignore_errors=True)
    first = fails[0] if fails else ""
    return f"{name:34s} {verdict:9s} {tally.group() if tally else '-':34s} {first}"


def run_lockstep(name: str, src: Path, work: Path, out: Path, verilator: str,
                 seeds: int, cycles: int) -> str:
    tree = work / f"ls-{name}"
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir(parents=True)
    ref = (src / RTL).read_text()
    mut = mutate(ref, MUTANTS[name][0])
    mut = mut.replace("module KL_acmp_talker\n", "module KL_acmp_talker_mut\n", 1)
    mut = mut.replace("endmodule : KL_acmp_talker", "endmodule : KL_acmp_talker_mut", 1)
    (tree / "mut.sv").write_text(mut)
    cmd = [verilator, "--cc", "--exe", "--build", "-j", "2", "--top-module", "lockstep",
           "-Wno-fatal", "-Wno-WIDTH", "-Wno-DECLFILENAME", "-Wno-UNUSED", "-Wno-MULTITOP",
           "-CFLAGS", "-std=c++17 -O2", "-Mdir", str(tree / "obj"),
           str(src / "hdl/common/pp_pkg.sv"), str(src / "hdl/srp/srp_pkg.sv"),
           str(src / RTL), str(tree / "mut.sv"), str(HERE / "lockstep/lockstep.sv"),
           str(HERE / "lockstep/lockstep_main.cpp"), "-o", "Vls"]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode:
        (out / f"lockstep-{name}.txt").write_text("BUILD FAILED\n" + res.stderr[-4000:])
        return f"{name:34s} BUILD-FAILED"
    lines = []
    diverged = None
    for seed in range(1, seeds + 1):
        r = subprocess.run([str(tree / "obj/Vls"), str(seed), str(cycles)],
                           capture_output=True, text=True, check=False)
        line = (r.stdout.strip().splitlines() or [f"rc={r.returncode} no output"])[-1]
        lines.append(line)
        if r.returncode == 3 and diverged is None:
            diverged = line
    (out / f"lockstep-{name}.txt").write_text(
        f"mutant: {name}\nnote: {MUTANTS[name][1]}\nseeds: {seeds} cycles/seed: {cycles}\n"
        + "\n".join(lines) + "\n")
    shutil.rmtree(tree, ignore_errors=True)
    ndiff = sum(1 for ln in lines if ln.startswith("DIVERGE"))
    return f"{name:34s} {'DIVERGED' if ndiff else 'NO-DIFF':9s} {ndiff}/{seeds} seeds  first: {diverged or '-'}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("suite", "lockstep"))
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", nargs="+", choices=sorted(MUTANTS))
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--cycles", type=int, default=2_000_000)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    a.work.mkdir(parents=True, exist_ok=True)
    verilator = os.environ.get("VERILATOR", "verilator")
    names = a.only or list(MUTANTS)
    jobs = max(1, min(a.jobs, 8))
    with cf.ThreadPoolExecutor(max_workers=jobs) as pool:
        if a.mode == "suite":
            futs = [pool.submit(run_suite, n, a.src, a.work, a.out, verilator) for n in names]
        else:
            futs = [pool.submit(run_lockstep, n, a.src, a.work, a.out, verilator,
                                a.seeds, a.cycles) for n in names]
        rows = [f.result() for f in futs]
    summary = "\n".join(rows) + "\n"
    (a.out / f"{a.mode}-summary.txt").write_text(summary)
    print(summary, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
