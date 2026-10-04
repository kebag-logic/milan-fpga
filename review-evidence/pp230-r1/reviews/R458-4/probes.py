#!/usr/bin/env python3
"""R458-4 independent probes of the #230 storage paths.

Each probe is one exact text edit of one HDL file at the reviewed head. For
every probe the driver copies hdl/ and the SRP suites to a scratch tree of its
own, applies the edit (refusing it unless the old text occurs exactly once),
runs the full default `make` of every suite that builds the edited file, and
records each suite's rc and its FAIL lines. A probe is CAUGHT when at least one
suite exits non-zero with a tally line ("checks:") and at least one FAIL line;
a build failure or a missing tally is BUILD-ERROR, never a catch.

Usage: probes.py --root <checkout at the head> --out <dir> [--jobs N] [--only a,b]
The caller exports VERILATOR (the pinned simulator) and TMPDIR.
"""
import argparse
import concurrent.futures as cf
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

TK = "hdl/srp/KL_srp_talker_fsm.sv"
LS = "hdl/srp/KL_srp_listener_fsm.sv"
TOP = "hdl/srp/KL_srp_top.sv"
ADM = "hdl/srp/KL_srp_admission.sv"
FSM_SUITES = ["srp_stream_fsms", "srp_top"]
TOP_SUITES = ["srp_top"]
ADM_SUITES = ["srp_admission", "srp_top"]

# name, file, old text, new text, suites
PROBES = [
    ("q-wtsp-read-neighbour", TK,
     "  assign wtsp_w = wtsp_r[wsrc_r];",
     "  assign wtsp_w = wtsp_r[(wsrc_r == 0) ? SRC_W_C'(N_SOURCES_P - 1) : wsrc_r - SRC_W_C'(1)];",
     FSM_SUITES),
    ("q-wtsp-written-at-walk-source", TK,
     "      wtsp_r[gate_src_i] <= {gate_max_frame_i,",
     "      wtsp_r[wsrc_r] <= {gate_max_frame_i,",
     FSM_SUITES),
    ("q-wid-ram-write-ignores-ready", TK,
     "      if (gate_open_acc_w) begin\n        wid_r[gate_src_i]",
     "      if (rst_n && gate_valid_i && gate_open_i) begin\n        wid_r[gate_src_i]",
     FSM_SUITES),
    ("q-wid-ram-written-on-close", TK,
     "      if (gate_open_acc_w) begin\n        wid_r[gate_src_i]",
     "      if (rst_n && gate_acc_w) begin\n        wid_r[gate_src_i]",
     FSM_SUITES),
    ("q-wid-ram-vid-dropped", TK,
     "        wid_r[gate_src_i] <= {gate_stream_id_i, gate_da_i, gate_vid_i};",
     "        wid_r[gate_src_i] <= {gate_stream_id_i, gate_da_i, 12'd0};",
     FSM_SUITES),
    ("q-wtsp-mif-from-mfs", TK,
     "      wtsp_r[gate_src_i] <= {gate_max_frame_i, gate_max_interval_i,",
     "      wtsp_r[gate_src_i] <= {gate_max_frame_i, gate_max_frame_i,",
     FSM_SUITES),
    ("q-wtsp-write-no-reset-gate-equivalent", TK,
     "  assign gate_open_acc_w = rst_n && gate_acc_w && gate_open_i;",
     "  assign gate_open_acc_w = gate_acc_w && gate_open_i;",
     FSM_SUITES),
    ("q-wsid-ram-read-neighbour", LS,
     "    assign wsid_w = wsid_r[wsrc_r];",
     "    assign wsid_w = wsid_r[(wsrc_r == 0) ? SNK_W_C'(N_SINKS_P - 1) : wsrc_r - SNK_W_C'(1)];",
     FSM_SUITES),
    ("q-wsid-ram-from-da", LS,
     "        wsid_r[ctl_sink_i] <= ctl_stream_id_i;",
     "        wsid_r[ctl_sink_i] <= {16'd0, ctl_da_i};",
     FSM_SUITES),
    ("q-wsid-ram-write-at-walk-sink", LS,
     "        wsid_r[ctl_sink_i] <= ctl_stream_id_i;",
     "        wsid_r[wsrc_r] <= ctl_stream_id_i;",
     FSM_SUITES),
    ("q-tf-ls-head-read-ahead", TOP,
     "    tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1]];",
     "    tf_q_r[1] <= tf_ls_ram_r[tf_rptr_r[1] + 5'd1];",
     TOP_SUITES),
    ("q-tf-ls-write-at-rptr", TOP,
     "      tf_ls_ram_r[tf_wptr_r[1]]",
     "      tf_ls_ram_r[tf_rptr_r[1]]",
     TOP_SUITES),
    ("q-tf-tk-cancel-dropped", TOP,
     "        <= {tk_arm_cancel_w, tk_arm_slot_w, tk_arm_owner_w, tk_arm_dl_w};",
     "        <= {1'b0, tk_arm_slot_w, tk_arm_owner_w, tk_arm_dl_w};",
     TOP_SUITES),
    ("q-tf-ls-cancel-dropped", TOP,
     "        <= {ls_arm_cancel_w, ls_arm_slot_w, ls_arm_owner_w, ls_arm_dl_w};",
     "        <= {1'b0, ls_arm_slot_w, ls_arm_owner_w, ls_arm_dl_w};",
     TOP_SUITES),
    ("q-tf-ls-full-of-tk-count", TOP,
     "  assign tf_push_w[1] = ls_arm_v_w && (tf_cnt_r[1] != 6'(TFD_C));",
     "  assign tf_push_w[1] = ls_arm_v_w && (tf_cnt_r[0] != 6'(TFD_C));",
     TOP_SUITES),
    ("q-tf-ls-deadline-low-bit", TOP,
     "        <= {ls_arm_cancel_w, ls_arm_slot_w, ls_arm_owner_w, ls_arm_dl_w};",
     "        <= {ls_arm_cancel_w, ls_arm_slot_w, ls_arm_owner_w, ls_arm_dl_w[31:1], 1'b0};",
     TOP_SUITES),
    ("q-slope-read-neighbour", ADM,
     "  assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[aidx_r]};",
     "  assign cand_w   = {1'b0, acc_r} + {1'b0, slope_q_r[(32'(aidx_r) == 0) ? SRC_W_C'(N_SOURCES_P - 1) : aidx_r - SRC_W_C'(1)]};",
     ADM_SUITES),
    ("q-slope-grant-reads-neighbour", ADM,
     "    wgslope_now_w[aidx_r]  = fit_w ? slope_q_r[aidx_r] : 32'd0;",
     "    wgslope_now_w[aidx_r]  = fit_w ? slope_q_r[(32'(aidx_r) == 0) ? SRC_W_C'(N_SOURCES_P - 1) : aidx_r - SRC_W_C'(1)] : 32'd0;",
     ADM_SUITES),
]


def trial(root: Path, probe, out: Path) -> str:
    name, path, old, new, suites = probe
    with tempfile.TemporaryDirectory(prefix="r458-4-") as tmp:
        tree = Path(tmp)
        shutil.copytree(root / "hdl", tree / "hdl")
        for s in ("common", "srp_top", "srp_stream_fsms", "srp_encoder", "srp_admission"):
            shutil.copytree(root / "tb" / s, tree / "tb" / s,
                            ignore=shutil.ignore_patterns("obj_*", "__pycache__"))
        f = tree / path
        text = f.read_text()
        if text.count(old) != 1:
            return f"{name}: EDIT-REFUSED (old text occurs {text.count(old)} times)"
        f.write_text(text.replace(old, new))
        diff = subprocess.run(["diff", "-u", str(root / path), str(f)],
                              capture_output=True, text=True).stdout
        (out / f"{name}.diff").write_text(diff)
        parts, caught, build_err = [], False, False
        for suite in suites:
            log = out / f"{name}.{suite}.log"
            with log.open("w") as stream:
                rc = subprocess.run(["make", "-C", str(tree / "tb" / suite)],
                                    stdout=stream, stderr=subprocess.STDOUT).returncode
            body = log.read_text()
            fails = [l for l in body.splitlines() if l.startswith("FAIL:")]
            tallied = "checks:" in body
            if rc != 0 and not fails:
                build_err = True
            if rc != 0 and tallied and fails:
                caught = True
            tags = sorted({l.split(":", 2)[1].strip().split()[0] for l in fails if l.count(":") >= 2})
            shapes = sorted({l.rsplit("[", 1)[1].rstrip("]") for l in fails if l.endswith("]")})
            parts.append(f"{suite} rc={rc} fails={len(fails)} tags={','.join(tags)} "
                         f"shapes={','.join(shapes)}")
        verdict = "CAUGHT" if caught else ("BUILD-ERROR" if build_err else "SURVIVED")
        return f"{name}: {verdict} | " + " | ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    sel = [p for p in PROBES if not a.only or p[0] in a.only.split(",")]
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(trial, a.root, p, a.out) for p in sel]
        lines = [f.result() for f in futs]
    for line in lines:
        print(line, flush=True)
    (a.out / "SUMMARY.txt").write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
