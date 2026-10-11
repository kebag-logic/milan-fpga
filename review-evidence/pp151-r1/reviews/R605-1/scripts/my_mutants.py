#!/usr/bin/env python3
"""Reviewer-owned mutation probes of tb/elab_guards, independent of its mutants.py.

Each probe copies a pristine hdl/ (from --src, an exported tree of the head) into a
scratch tree of its own, applies one textual edit that must match exactly once, and
runs the head's guards.py on that tree with --only the guard named. A probe whose
`expect` is KILL is proven when guards.py exits non-zero and prints a FAIL line naming
the guard; a probe whose expect is SURVIVE is an equivalence or boundary probe whose
survival is the measured fact. Usage:
  my_mutants.py --src <head export> --out <new dir> [--jobs N] [--frontend F ...]
"""
import argparse
import concurrent.futures
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROBES = [
    # (name, file, old, new, guard, expect)
    ("R1-listener-base-form", "hdl/acmp/KL_pp_acmp_listener.sv",
     "  //! at module scope: Verilator lint and xelab never see a guard in an initial block\n"
     "  if (STRM_TIMEOUT_CYC_P == 0) begin : g_strm_tmo_check\n"
     "    $fatal(1, \"STRM_TIMEOUT_CYC_P must be greater than zero\");\n"
     "  end\n",
     "  initial begin : parameter_checks\n"
     "    if (STRM_TIMEOUT_CYC_P == 0)\n"
     "      $fatal(1, \"STRM_TIMEOUT_CYC_P must be greater than zero\");\n"
     "  end\n",
     "KL_pp_acmp_listener.g_strm_tmo_check", "KILL"),
    ("R2-encoder-info", "hdl/srp/KL_srp_encoder.sv",
     '$fatal(1, "DEPTH_P drain', '$info("DEPTH_P drain',
     "KL_srp_encoder.g_depth_check", "KILL"),
    ("R3-notify-display", "hdl/aecp/KL_aecp_notify.sv",
     '$fatal(1, "KL_aecp_notify: rows', '$display("KL_aecp_notify: rows',
     "KL_aecp_notify.g_rows_guard", "KILL"),
    ("R4-owner-initial-inside-block", "hdl/top/protocol_processor_top.sv",
     '    $fatal(1, "F08.4: owner tags OVERLAP',
     '    initial $fatal(1, "F08.4: owner tags OVERLAP',
     "protocol_processor_top.gen_g_owner_overlap", "KILL"),
    ("R5-respbuf-fatal0", "hdl/aecp/KL_aecp_resp_buf.sv",
     '$fatal(1, "RESP_BYTES_P=%0d leaves', '$fatal(0, "RESP_BYTES_P=%0d leaves',
     "KL_aecp_resp_buf.gen_g_size", "SURVIVE"),
    ("R6-shadow-rs-tmo-tightened-to-2", "hdl/acmp/KL_acmp_nvm_shadow.sv",
     "if (RS_TMO_CYC_P < 1) begin : g_rs_tmo_check",
     "if (RS_TMO_CYC_P < 2) begin : g_rs_tmo_check",
     "KL_acmp_nvm_shadow.g_rs_tmo_check", "SURVIVE"),
    ("R7-tmr-aw-error", "hdl/top/protocol_processor_top.sv",
     '$fatal(1, "F08.4: TMR_AW_C=', '$error("F08.4: TMR_AW_C=',
     "protocol_processor_top.gen_g_tmr_aw", "KILL"),
    ("R8-originator-warning", "hdl/packet_engine/KL_pp_originator.sv",
     '$fatal(1, "KL_pp_originator: INFLIGHT_P', '$warning("KL_pp_originator: INFLIGHT_P',
     "KL_pp_originator.g_inflight_check", "KILL"),
    ("R9-ucpu-label-renamed", "hdl/aecp/KL_aecp_ucpu.sv",
     "begin : gen_g_d8_cap", "begin : gen_g_d8_cap_x",
     "KL_aecp_ucpu.gen_g_d8_cap", "KILL"),
    ("R10-nvmport-lint-off", "hdl/packet_engine/KL_pp_nvm_port.sv",
     '    $fatal(1, "KL_pp_nvm_port: MEM_TIMEOUT_CYC_P',
     '    /* verilator lint_off USERFATAL */\n    $fatal(1, "KL_pp_nvm_port: MEM_TIMEOUT_CYC_P',
     "KL_pp_nvm_port.g_tmo_check", "KILL"),
]


def run_probe(args, probe):
    name, path, old, new, guard, expect = probe
    log = args.out / f"{name}.log"
    with tempfile.TemporaryDirectory(prefix="r605-mut-") as tmp:
        tree = Path(tmp)
        shutil.copytree(args.src / "hdl", tree / "hdl")
        target = tree / path
        text = target.read_text()
        if text.count(old) != 1:
            log.write_text(f"PLANT ERROR: old text found {text.count(old)} times\n")
            return name, expect, "PLANT-ERROR", -1, []
        target.write_text(text.replace(old, new))
        cmd = [sys.executable, "-B", str(args.src / "tb/elab_guards/guards.py"),
               "--root", str(tree), "--jobs", "1", "--only", guard]
        for f in args.frontend or ():
            cmd += ["--frontend", f]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, check=False)
        log.write_text(f"$ {' '.join(cmd)}\nplant {path}: {old!r} -> {new!r}\n\n" + res.stdout
                       + f"\nrc={res.returncode}\n")
    fails = [l for l in res.stdout.splitlines() if l.startswith("FAIL:") and
             (guard in l or "gen_g_d8_cap_x" in l or "parameter_checks" in l)]
    outcome = "KILLED" if res.returncode != 0 and fails else "SURVIVED"
    return name, expect, outcome, res.returncode, fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--frontend", action="append")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    bad = 0
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        for name, expect, outcome, rc, fails in pool.map(lambda p: run_probe(args, p), PROBES):
            ok = (expect == "KILL" and outcome == "KILLED") or \
                 (expect == "SURVIVE" and outcome == "SURVIVED")
            bad += not ok
            print(f"{name}: expect {expect}, {outcome} rc={rc} {'AS-EXPECTED' if ok else 'UNEXPECTED'}")
            for f in fails:
                print(f"    {f[:220]}")
    print(f"reviewer probes: {len(PROBES)} run, {bad} unexpected")
    return int(bad != 0)


if __name__ == "__main__":
    raise SystemExit(main())
