#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""R445-1 reviewer probes: plant defects the D3KR cut oracle must catch,
beyond the PR's two crc controls (which delete a crc compare).

Each plant is applied to a disposable copy of the exact head (git archive),
by an exact-once text substitution; the copy is built and `--cuts-only` (or
`--cut-seed S`) is run. A plant is CAUGHT when the run exits non-zero and
reports FAIL lines. Usage:

  plants.py --repo CLONE --head SHA --work DIR --verilator V [--only NAME]...

Writes DIR/<name>/{plant.diff,build.log,build.rc,run.log,run.rc}.
"""
import argparse
import os
import subprocess
import sys

WRITER = "hdl/aecp/KL_aecp_nvm_writer.sv"
SHADOW = "hdl/acmp/KL_acmp_nvm_shadow.sv"

# Torn-write acceptance, D3 writer: the crc compare is intact, but a frame it
# refuses (a torn payload's crc) is routed on to the value rule, as a framed
# record would be, instead of keeping its default.
D3_REFUSE_OLD = (
    "            end else if (!frame_ok_w) begin\n"
    "              n_ref_r <= n_ref_r + 8'd1;      // the frame refuses it\n"
    "              ws_r    <= W_NEXT;\n")
D3_REFUSE_NEW = (
    "            end else if (!frame_ok_w) begin\n"
    "              n_ref_r <= n_ref_r + 8'd1;      // the frame refuses it\n"
    "              ws_r    <= W_RULE;              // PLANT: refused yet ruled\n")

# Torn-write acceptance, binding manager: the crc compare is intact, but a
# complete record that fails it is stored like a good one.
BIND_REFUSE_OLD = "          end else if (rs_empty_w || (rs_complete_w && !rrec_ok_w)) begin\n"
BIND_REFUSE_NEW = "          end else if (rs_empty_w) begin  // PLANT: a refused record is stored\n"
BIND_DEFAULT_OLD = (
    "      if (rs_complete_w && !rrec_ok_w && !touched_r[rs_k_r]) begin\n"
    "        valid_r[rs_k_r] <= 1'b0;                   // F07.9 per-record default\n"
    "      end\n")
BIND_DEFAULT_NEW = "      // PLANT: no per-record default for a refused record\n"

# Stale-record acceptance, D3 name stage: a blank (erased or unframed) name
# record in the apply pass writes back whatever the name buffer (a LUT RAM,
# no reset) still holds from before the cut.
D3_BLANK_OLD = (
    "            end else if (rd_blank_w) begin\n"
    "              n_blank_r <= n_blank_r + 8'd1;  // erased or unframed: the default\n"
    "              ws_r      <= W_NEXT;\n")
D3_BLANK_NEW = (
    "            end else if (rd_blank_w) begin\n"
    "              n_blank_r <= n_blank_r + 8'd1;  // erased or unframed: the default\n"
    "              ws_r      <= (rsel_w == GRP_NAME_C) ? W_NAPPLY : W_NEXT;  // PLANT\n")

# Stale-record acceptance, binding manager: the saved-binding valid bit
# survives rst_n and a blank record keeps it, so the shadow's pre-cut entry
# (its LUT RAM fields) is replayed although the device holds no record.
BIND_RST_OLD = (
    "    if (!rst_n) begin\n"
    "      valid_r   <= '0;\n"
    "      dirty_r   <= '0;\n")
BIND_RST_NEW = (
    "    if (!rst_n) begin\n"
    "      // PLANT: valid_r not reset\n"
    "      dirty_r   <= '0;\n")
BIND_BLANK_OLD = (
    "      if (rs_empty_w && !touched_r[rs_k_r]) begin\n"
    "        valid_r[rs_k_r] <= 1'b0;                   // no saved binding\n"
    "      end\n")
BIND_BLANK_NEW = "      // PLANT: a blank record keeps the stale valid bit\n"

PLANTS = {
    "torn_d3_refusal_ruled": [(WRITER, D3_REFUSE_OLD, D3_REFUSE_NEW)],
    "torn_bind_refusal_stored": [(SHADOW, BIND_REFUSE_OLD, BIND_REFUSE_NEW),
                                 (SHADOW, BIND_DEFAULT_OLD, BIND_DEFAULT_NEW)],
    "stale_d3_name_blank_applied": [(WRITER, D3_BLANK_OLD, D3_BLANK_NEW)],
    "stale_bind_blank_kept": [(SHADOW, BIND_RST_OLD, BIND_RST_NEW),
                              (SHADOW, BIND_BLANK_OLD, BIND_BLANK_NEW)],
}


def sh(cmd, cwd, log):
    with open(log, "w") as f:
        return subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT,
                              shell=isinstance(cmd, str),
                              executable="/bin/bash" if isinstance(cmd, str) else None).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--verilator", required=True)
    ap.add_argument("--only", action="append")
    ap.add_argument("--args", default="--cuts-only")
    a = ap.parse_args()
    names = a.only or list(PLANTS)
    for name in names:
        d = os.path.join(a.work, name)
        os.makedirs(d, exist_ok=True)
        tree = os.path.join(d, "tree")
        if not os.path.isdir(tree):
            os.makedirs(tree)
            subprocess.run(f"git -C {a.repo} archive {a.head} | tar -x -C {tree}",
                           shell=True, check=True)
            for path, old, new in PLANTS[name]:
                p = os.path.join(tree, path)
                src = open(p).read()
                n = src.count(old)
                if n != 1:
                    sys.exit(f"{name}: anchor in {path} found {n} times, expected 1")
                open(p, "w").write(src.replace(old, new))
        sh(f"diff -ru <(git -C {a.repo} show {a.head}:{WRITER}) {tree}/{WRITER}; "
                f"diff -ru <(git -C {a.repo} show {a.head}:{SHADOW}) {tree}/{SHADOW}; true",
                tree, os.path.join(d, "plant.diff"))
        pt = os.path.join(tree, "tb/pp_top")
        brc = sh(["make", "gsi-build", f"VERILATOR={a.verilator}"], pt,
                 os.path.join(d, "build.log"))
        open(os.path.join(d, "build.rc"), "w").write(f"{brc}\n")
        if brc != 0:
            continue
        rrc = sh(["./obj_dir/Vpp_top_sim"] + a.args.split(), pt, os.path.join(d, "run.log"))
        open(os.path.join(d, "run.rc"), "w").write(f"{rrc}\n")


if __name__ == "__main__":
    main()
