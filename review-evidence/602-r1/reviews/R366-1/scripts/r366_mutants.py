#!/usr/bin/env python3
"""Reviewer-owned mutation probes for PR #603 (issue #602), round R366-1.

Each probe writes a mutated COPY of one RTL file under WORK, builds the named
leg through tb/verilator/milan_dp's own Makefile recipe (DP_SRC / MCR_SRC and
GMSTEP_MDIR / OPTOFF_MDIR overridden) and runs it. Tracked files are never
edited. A probe is CAUGHT when the leg exits non-zero with at least one
"[FAIL]" line naming the expected check; SURVIVED when the leg passes.

Usage: r366_mutants.py <repo> <work> [probe-name ...]
Environment: VERILATOR (pinned 5.050 wrapper), JOBS (parallel builds, default 4).
"""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
ONLY = set(sys.argv[3:])
TB = REPO / "tb/verilator/milan_dp"
DP = REPO / "hdl/milan/milan_datapath.sv"
MCR = REPO / "hdl/ieee1722/avtp/KL_media_clock_restart.sv"
BASE = "6d5ebd7357c1e468e446f18a61527c5be6118a04"

HEAD_EXPR = ("  wire mcr_restart_p_w = crf_clk_selected_r\n"
             "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w);\n")
BASE_EXPR = ("  wire mcr_restart_p_w = (crf_clk_selected_r\n"
             "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w))\n"
             "                       | media_rebase_p_w;\n")
GM_BLOCK_END = "  end : g_gm_recentre\n"


def base_file(rel):
    return subprocess.run(["git", "-C", str(REPO), "show", f"{BASE}:{rel}"],
                          capture_output=True, text=True, check=True).stdout


# name: (file-key, [(anchor, replacement)], legs, {leg: expected-failing-check or None})
# None = informational: the leg is expected to PASS (probe bounds the test reach).
PROBES = {
    "P1_restore_rebase_term_verbatim_base_expr": (
        "dp", [(HEAD_EXPR, BASE_EXPR)], ["gmstep", "optoff"],
        {"gmstep": "restart: a PHC-only step leaves outgoing mr unchanged",
         "optoff": "CLKV: PHC-only steps leave INTERNAL mr unchanged (#602)"}),
    "P2_restore_rebase_term_gated_by_crf_selection": (
        "dp", [(HEAD_EXPR,
                "  wire mcr_restart_p_w = crf_clk_selected_r\n"
                "                          & ((tkd_crflk_q_r & ~crf_locked_w) | crf_mr_toggle_p_w"
                " | media_rebase_p_w);\n")],
        ["gmstep", "optoff"],
        {"gmstep": "restart: a PHC-only step leaves outgoing mr unchanged", "optoff": None}),
    "P3_gm_identity_change_requests_restart": (
        "dp", [(HEAD_EXPR,
                "  wire gm_rst_probe_w;\n" + HEAD_EXPR.replace(
                    "crf_mr_toggle_p_w);", "crf_mr_toggle_p_w) | gm_rst_probe_w;")),
               (GM_BLOCK_END, GM_BLOCK_END + "  assign gm_rst_probe_w = gm_recentre_p_r;\n")],
        ["gmstep"],
        {"gmstep": "restart: a PHC-only step leaves outgoing mr unchanged"}),
    "P4_phc_step_suppresses_genuine_restart": (
        "dp", [(HEAD_EXPR, HEAD_EXPR.replace(
            "crf_mr_toggle_p_w);", "crf_mr_toggle_p_w) & ~media_rebase_p_w;"))],
        ["gmstep"], {"gmstep": None}),
    "P5_settime_only_restored_graded_on_gmstep": (
        "dp", [(HEAD_EXPR, HEAD_EXPR.replace(
            "  wire mcr_restart_p_w = crf_clk_selected_r\n", "  wire mcr_restart_p_w = (crf_clk_selected_r\n").replace(
            "crf_mr_toggle_p_w);", "crf_mr_toggle_p_w)) | cfg_ptp_cmd_load;"))],
        ["gmstep", "optoff"],
        {"gmstep": None, "optoff": "CLKV: the settime leaves mr unchanged (#602)"}),
    "P6_source_change_detector_never_updates": (
        "mcr", [("src_change_w = (clk_src_q_r != clk_src_i);",
                 "src_change_w = 1'b0 & (clk_src_q_r != clk_src_i);")],
        ["gmstep"], {"gmstep": "source control: a real source change toggles mr once"}),
    "P7_crf_disruption_term_removed": (
        "dp", [(HEAD_EXPR,
                "  wire mcr_restart_p_w = crf_clk_selected_r\n"
                "                          & (crf_mr_toggle_p_w | 1'b0);\n")],
        ["gmstep"], {"gmstep": None}),
    "P8_crf_mr_echo_removed": (
        "dp", [(HEAD_EXPR,
                "  wire mcr_restart_p_w = crf_clk_selected_r\n"
                "                          & (tkd_crflk_q_r & ~crf_locked_w);\n")],
        ["gmstep"], {"gmstep": "CRF control: selected CRF mr propagates exactly once"}),
    "P9_whole_base_datapath_under_head_tests": (
        "dp_base", [], ["gmstep", "optoff"],
        {"gmstep": "restart: a PHC-only step leaves outgoing mr unchanged",
         "optoff": "CLKV: the settime leaves mr unchanged (#602)"}),
    "P10_render_rebase_dropped_restart_intact": (
        "dp", [("       media_rebase_p_w\n       | src_recentre_p_r;",
                "       1'b0\n       | src_recentre_p_r;")],
        ["gmstep"], {"gmstep": "render: the GM change is one counted re-base event"}),
}

LEG = {
    "gmstep": ("gmstep-build", "GMSTEP_MDIR", "Vmilan_dp_gmstep", True),
    "optoff": ("option-off-build", "OPTOFF_MDIR", "Vmilan_dp_sim", False),
}


def plant(name, spec):
    key, edits, _, _ = spec
    if key == "dp_base":
        text, target = base_file("hdl/milan/milan_datapath.sv"), DP
    else:
        target = DP if key == "dp" else MCR
        text = target.read_text()
    for anchor, repl in edits:
        n = text.count(anchor)
        if n != 1:
            raise SystemExit(f"{name}: anchor found {n} times")
        text = text.replace(anchor, repl)
    out = WORK / name / target.name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    return ("MCR_SRC" if target == MCR else "DP_SRC"), out


def build_and_run(name, spec, leg):
    var, path = plant(name, spec)
    target, mvar, exe, aem = LEG[leg]
    mdir = WORK / name / f"obj_{leg}"
    t0 = time.time()
    b = subprocess.run(["make", "-s", "-C", str(TB), target, f"{mvar}={mdir}", f"{var}={path}",
                        "VERILATOR_JOBS=2"], capture_output=True, text=True)
    (WORK / name / f"build_{leg}.log").write_text(b.stdout + b.stderr)
    if b.returncode != 0 or not (mdir / exe).is_file():
        return dict(probe=name, leg=leg, verdict="BUILD-FAILED", build_rc=b.returncode)
    cmd = [str(mdir / exe)] + ([str(mdir / "aemi.bin")] if aem else [])
    r = subprocess.run(cmd, cwd=str(TB), capture_output=True, text=True)
    log = r.stdout + r.stderr
    (WORK / name / f"run_{leg}.log").write_text(log)
    fails = [l.strip() for l in log.splitlines() if l.strip().startswith("[FAIL]")]
    expect = spec[3][leg]
    if r.returncode == 0 and not fails:
        verdict = "SURVIVED(pass)"
    elif fails:
        verdict = "CAUGHT" if (expect is None or any(expect in f for f in fails)) else "FAILED-OTHER"
    else:
        verdict = f"NO-VERDICT rc={r.returncode}"
    ok = (verdict == "SURVIVED(pass)") if expect is None else (verdict == "CAUGHT")
    return dict(probe=name, leg=leg, expected=("pass (informational)" if expect is None else f"fail: {expect}"),
                verdict=verdict, as_expected=ok, run_rc=r.returncode, failed_checks=fails,
                tally=[l for l in log.splitlines() if "checks" in l and ("failures" in l or "FAIL" in l)][-1:],
                seconds=round(time.time() - t0, 1), mutated_sha256=subprocess.run(
                    ["sha256sum", str(path)], capture_output=True, text=True).stdout.split()[0])


def main():
    jobs = [(n, s, leg) for n, s in PROBES.items() if not ONLY or n in ONLY for leg in s[2]]
    with ThreadPoolExecutor(int(os.environ.get("JOBS", "4"))) as ex:
        results = list(ex.map(lambda j: build_and_run(*j), jobs))
    for r in results:
        print(f"{r['probe']:<48} {r['leg']:<7} {r['verdict']:<16} as_expected={r.get('as_expected')} "
              f"{r.get('expected', '')}")
        for f in r.get("failed_checks", [])[:6]:
            print(f"      {f[:150]}")
    (WORK / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    return 0 if all(r.get("as_expected") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
