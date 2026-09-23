#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probes for the #387 gmstep leg (round R276-1).

Each probe copies one RTL source into a scratch directory, plants one
change by exact anchor replacement (the anchor must occur exactly once),
and rebuilds the SAME leg through the Makefile's own recipe
(`make gmstep` with DP_SRC / CLKV_SRC and GMSTEP_MDIR overridden). The
tracked tree is never edited.

Usage (from anywhere):
  python3 gmstep_probes.py --repo <clone> --scratch <dir> \
      --edited-datapath <head datapath with the proposed #387 patch applied> \
      [--only NAME ...]
VERILATOR and VERILATOR_JOBS pass through from the environment.
Prints one summary line per probe: checks, failures and the failed names.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

IDENTITY_KEYED_REBASE = (
    "  logic [63:0] probe_gm_q_r;\n"
    "  logic        probe_gm_p_r;\n"
    "  always_ff @(posedge axis_clk) begin : probe_gm\n"
    "    if (!axis_resetn) begin\n"
    "      probe_gm_q_r <= '0;\n"
    "      probe_gm_p_r <= 1'b0;\n"
    "    end else begin\n"
    "      probe_gm_q_r <= cfg_adp_gptp_gm;\n"
    "      probe_gm_p_r <= (cfg_adp_gptp_gm != probe_gm_q_r) &&\n"
    "                      (probe_gm_q_r != 64'd0);\n"
    "    end\n"
    "  end : probe_gm\n"
    "  wire media_rebase_p_w = probe_gm_p_r | cfg_ptp_cmd_load;\n")

#: the AAF talker falls silent for good once tu clears after the GM change
#: (the second tu fall since reset); the gate register still reads open
TALKER_DIES_AFTER_EVENT = (
    "assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;\n",
    "assign aaf_stream_en_w = aaf_stream_en_raw_w & ~amap_edit_out_resv_r;\n"
    "  logic       probe_tu_q_r;\n"
    "  logic [1:0] probe_falls_r;\n"
    "  logic       probe_dead_r;\n"
    "  always_ff @(posedge axis_clk) begin : probe_dead\n"
    "    if (!axis_resetn) begin\n"
    "      probe_tu_q_r  <= 1'b1;\n"
    "      probe_falls_r <= 2'd0;\n"
    "      probe_dead_r  <= 1'b0;\n"
    "    end else begin\n"
    "      probe_tu_q_r <= clkv_tu_w;\n"
    "      if (probe_tu_q_r && !clkv_tu_w && probe_falls_r != 2'd3)\n"
    "        probe_falls_r <= probe_falls_r + 2'd1;\n"
    "      if (probe_falls_r == 2'd2) probe_dead_r <= 1'b1;\n"
    "    end\n"
    "  end : probe_dead\n")

#: name -> (base: "head" | "edit", source: "datapath" | "clkv", anchor, replacement)
#: a replacement may also be a list of (anchor, replacement) pairs
PROBES = {
    "edit-step-recentre-removed": (
        "edit", "datapath",
        "       media_rebase_p_w | src_recentre_p_r;\n",
        "       src_recentre_p_r;\n"),
    "edit-talker-silent-after-event": (
        "edit", "datapath", None,
        [TALKER_DIES_AFTER_EVENT,
         ("    .stream_en_i (aaf_stream_en_w),\n",
          "    .stream_en_i (aaf_stream_en_w & ~{N_STREAMS{probe_dead_r}}),\n")]),
    "edit-clean": ("edit", "datapath", None, None),
    "edit-identity-keyed-rebase": (
        "edit", "datapath",
        "  wire media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load;\n",
        IDENTITY_KEYED_REBASE),
    "head-step-recentre-removed": (
        "head", "datapath",
        "       gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load\n",
        "       gm_recentre_p_r | cfg_ptp_cmd_load\n"),
    "head-tu-four-cycles-late": (
        "head", "clkv",
        "  assign ts_uncertain_o = (~sync_ok_w) | hold_w | disc_p_w;\n",
        "  logic [3:0] tu_late_r;\n"
        "  always_ff @(posedge clk_i) begin : p_tu_late\n"
        "    tu_late_r <= {tu_late_r[2:0], (~sync_ok_w) | hold_w | disc_p_w};\n"
        "  end : p_tu_late\n"
        "  assign ts_uncertain_o = tu_late_r[3];\n"),
    "head-step-does-not-rearm-holdover": (
        "head", "datapath",
        "                   ? gptp_step_we_w : cfg_ptp_cmd_adjust),",
        "                   ? 1'b0 : cfg_ptp_cmd_adjust),"),
}


def plant(base: Path, dest: Path, anchor, replacement) -> None:
    """Copy base to dest, replacing the single occurrence of anchor."""
    text = base.read_text(encoding="utf-8")
    pairs = replacement if isinstance(replacement, list) else [(anchor, replacement)]
    for one_anchor, one_replacement in pairs:
        if one_anchor is None:
            continue
        count = text.count(one_anchor)
        if count != 1:
            raise SystemExit(f"anchor occurs {count} times in {base}")
        text = text.replace(one_anchor, one_replacement, 1)
    dest.write_text(text, encoding="utf-8")


def run(repo: Path, scratch: Path, edited: Path, name: str) -> str:
    """Build and run one probe; return its summary line."""
    base_kind, source, anchor, replacement = PROBES[name]
    head_dp = repo / "hdl/milan/milan_datapath.sv"
    clkv = repo / "hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv"
    sources = {"datapath": head_dp if base_kind == "head" else edited, "clkv": clkv}
    planted = scratch / f"{name}_{sources[source].name}"
    plant(sources[source], planted, anchor, replacement)
    sources[source] = planted
    mdir = f"obj_gmstep_probe_{name}"
    cmd = ["make", "gmstep", f"GMSTEP_MDIR={mdir}",
           f"DP_SRC={sources['datapath']}", f"CLKV_SRC={sources['clkv']}"]
    for var in ("VERILATOR", "VERILATOR_JOBS"):
        if var in os.environ:
            cmd.append(f"{var}={os.environ[var]}")
    tb = repo / "tb/verilator/milan_dp"
    done = subprocess.run(cmd, cwd=tb, capture_output=True, text=True, check=False)
    log = done.stdout + done.stderr
    (scratch / f"{name}.log").write_text(log, encoding="utf-8")
    shutil.rmtree(tb / mdir, ignore_errors=True)
    summary = [ln for ln in log.splitlines() if ln.startswith("== gmstep: checks:")]
    failed = [ln.split("[FAIL]", 1)[1].split(" got=")[0].strip()
              for ln in log.splitlines() if "[FAIL]" in ln]
    info = [ln for ln in log.splitlines()
            if ln.startswith(("RENDER:", "EVENT:", "TU:", "TALKER:"))]
    return (f"{name}: make exit {done.returncode}; "
            f"{summary[0] if summary else 'NO VERDICT'}; failed {failed}; "
            f"{' | '.join(info)}")


def main() -> int:
    """Run the selected probes in order."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--edited-datapath", type=Path, required=True)
    ap.add_argument("--only", nargs="*", default=list(PROBES))
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    for name in args.only:
        print(run(args.repo.resolve(), args.scratch.resolve(),
                  args.edited_datapath.resolve(), name), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
