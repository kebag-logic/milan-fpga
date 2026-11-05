#!/usr/bin/env python3
"""Reviewer fault probes for PR #213 (issue #212).

Usage: probe.py HEAD_TREE OUT_DIR SUITE NAME [NAME ...]
Copies HEAD_TREE/hdl and the suite into OUT_DIR/<NAME>/, applies one exact
single-occurrence text edit to hdl/srp/KL_srp_listener_fsm.sv, builds and
runs the suite with `make` (VERILATOR from the environment), and writes
OUT_DIR/<NAME>.log plus a one-line verdict with the FAIL: tags.
"""
import os, shutil, subprocess, sys
from pathlib import Path

RTL = "hdl/srp/KL_srp_listener_fsm.sv"
PROBES = {
    # the port registrar keeps the type of its allocation (no Advertise<->Failed follow)
    "pt-type-on-alloc-only": (
        "        pt_type_r[e] <= rx_is_failed_w;\n",
        "        if (pt_alloc_w[e]) pt_type_r[e] <= rx_is_failed_w;\n"),
    # the port registrar keeps the FailureInformation of its first Talker Failed
    "pt-fcode-first-only": (
        "        if (rx_is_failed_w) begin\n          pt_fcode_r[e] <= evt_failure_code_i;\n          pt_fsys_r[e]  <= evt_failure_system_id_i;\n",
        "        if (rx_is_failed_w && (pt_alloc_w[e] || !pt_type_r[e])) begin\n          pt_fcode_r[e] <= evt_failure_code_i;\n          pt_fsys_r[e]  <= evt_failure_system_id_i;\n"),
    # the port registrar keeps the latency of its allocation (no refresh)
    "pt-lat-on-alloc-only": (
        "        pt_lat_r[e]  <= evt_acc_latency_i;\n",
        "        if (pt_alloc_w[e]) pt_lat_r[e]  <= evt_acc_latency_i;\n"),
    # an unheld value is allocated IN on any Talker event (rLv, rIn, rMt too)
    "pt-alloc-any-event": (
        "      pt_alloc_w[e] = pt_rx_w && rx_registering_w && (pt_hit_w == '0)\n",
        "      pt_alloc_w[e] = pt_rx_w && (pt_hit_w == '0)\n"),
    # an A8 teardown seeds the registrar as a settle does
    "seed-on-teardown": (
        "    seed_v_w = ctl_valid_i && !evt_valid_i && ctl_settle_i\n",
        "    seed_v_w = ctl_valid_i && !evt_valid_i\n"),
    # rLv on an LV port registrar ends it at once (Table 10-4 says -x-)
    "pt-rlv-on-lv-ends": (
        "        if (pt_reg_r[e] == R_IN_C) pt_nreg_w[e] = R_MT_C;   // Δ13; LV: -x-\n",
        "        pt_nreg_w[e] = R_MT_C;\n"),
    # the whole pre-settle path removed: no seed and no one-walk declaration
    "presettle-removed": None,
    # the seed ignores the port registrar's type for the declaration (always Ready)
    "seed-declares-ready-only": (
        "            decl_fp_r[ctl_sink_i]   <= seed_type_w ? 2'(SRP_DECL_ASKING_FAILED)\n",
        "            decl_fp_r[ctl_sink_i]   <= 1'b0 ? 2'(SRP_DECL_ASKING_FAILED)\n"),
}
REMOVED = [
    ("    seed_v_w = ctl_valid_i && !evt_valid_i && ctl_settle_i\n",
     "    seed_v_w = 1'b0 && ctl_valid_i && !evt_valid_i && ctl_settle_i\n"),
    ("          if (pk_decl_w) begin\n", "          if (1'b0 && pk_decl_w) begin\n"),
]

def main():
    head, out, suite, names = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4:]
    out.mkdir(parents=True, exist_ok=True)
    for name in names:
        tree = out / ("tree-" + name + "-" + suite)
        if tree.exists():
            shutil.rmtree(tree)
        shutil.copytree(head / "hdl", tree / "hdl")
        tbdir = "pp_top" if suite.startswith("pp_top") else suite
        extra = ("srp_encoder", "srp_admission", "srp_stream_fsms") if suite == "srp_top" else ()
        for d in ("common", tbdir) + extra:
            shutil.copytree(head / "tb" / d, tree / "tb" / d,
                            ignore=shutil.ignore_patterns("obj*", "__pycache__"))
        edits = REMOVED if PROBES[name] is None else [PROBES[name]]
        src = (tree / RTL).read_text()
        for old, new in edits:
            assert src.count(old) == 1, (name, old)
            src = src.replace(old, new)
        (tree / RTL).write_text(src)
        log = out / (name + "@" + suite + ".log")
        with log.open("w") as f:
            if suite.startswith("pp_top"):
                # pp_top: as tb/pp_top/acmp_mutants.py grades its PP_TOP arms
                # (--acmp-only); pp_top_all: the default build, every section
                rc = subprocess.run(["make", "-C", str(tree / "tb" / "pp_top"), "gsi-build"],
                                    stdout=f, stderr=subprocess.STDOUT).returncode
                if rc == 0:
                    args = ["./obj_dir/Vpp_top_sim"] + (["--acmp-only"] if suite == "pp_top" else [])
                    rc = subprocess.run(args, cwd=tree / "tb" / "pp_top", stdout=f,
                                        stderr=subprocess.STDOUT).returncode
            else:
                rc = subprocess.run(["make", "-C", str(tree / "tb" / suite)], stdout=f,
                                    stderr=subprocess.STDOUT).returncode
        text = log.read_text(errors="replace")
        fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
        tally = [l for l in text.splitlines() if (" checks: " in l and "PASS" in l) or (" checks, " in l and "failures" in l)]
        tags = sorted({l.split(":", 2)[1].strip().split(" ")[0] for l in fails})
        print(f"{name}@{suite}: rc={rc} tally={tally[-1] if tally else 'NONE'} "
              f"fails={len(fails)} tags={','.join(tags)}", flush=True)
        shutil.rmtree(tree)

if __name__ == "__main__":
    main()
