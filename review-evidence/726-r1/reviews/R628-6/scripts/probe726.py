#!/usr/bin/env python3
"""R628-6 reviewer probe for the #726 parent counter fixture.

Usage: probe726.py <repo> <plant> <shape> <work> [frames-only|uncertain] [OMIT_GROUP]

Imports the head's tb/verilator/milan_dp/stream_counters.py unchanged and wraps
only its plant() so one disposable source replacement is staged under <work>
(never in <repo>). Runs the fixture once (detection), and, when OMIT_GROUP is
given, re-runs the same binary with COUNTERS_OMIT_CHECK=OMIT_GROUP (omission
control). Prints the failing [726 <group>] counts for each run.
"""
import os
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
probe, shape, work = sys.argv[2], int(sys.argv[3]), Path(sys.argv[4]).resolve()
condition = sys.argv[5] if len(sys.argv) > 5 else "uncertain"
omit = sys.argv[6] if len(sys.argv) > 6 else None
sys.path.insert(0, str(repo / "tb/verilator/milan_dp"))
import stream_counters as sc  # noqa: E402

AAF = "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
CRF = "hdl/ieee1722/crf/KL_crf_rx.sv"
TX = "hdl/ieee1722/avtp/KL_talker_diag_ctx.sv"
NOTIFY = "protocol-processor/hdl/aecp/KL_aecp_notify.sv"

PLANTS = {
    "none": [],
    # AAF FRAMES_RX publishes +1 per interval instead of the packet batch
    "aaf-rx-interval": [(AAF, "? 32'(frx_add_r) : 32'd1);", "? 32'd1 : 32'd1);")],
    # restore the base healthy-path guards in the AAF engine (both sites)
    "aaf-guard": [(AAF, "if (iv_seen_r[iv_s_w] != '0)",
                   "if ((iv_seen_r[iv_s_w] & ~(12'b1 << C_FRX_C)) != '0)"),
                  (AAF, "            dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r <= monst_next_w;",
                   "            if (!cur_w.tv || lock_now_w ||\n"
                   "                (seq_mm_w && lost_w >= 8'(INTERRUPT_MIN_LOST_C)))\n"
                   "              dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r <= monst_next_w;")],
    # restore the base healthy FRAMES_RX exclusion in the CRF engine
    "crf-guard": [(CRF, "        pdu_count_o <= pdu_count_o + 32'd1;\n        dirty_p_o <= 1'b1;",
                   "        pdu_count_o <= pdu_count_o + 32'd1;")],
    # CRF FRAMES_RX keeps counting past a 16-bit boundary only by saturating
    "crf-rx-16": [(CRF, "        pdu_count_o <= pdu_count_o + 32'd1;\n        dirty_p_o <= 1'b1;",
                   "        if (pdu_count_o != 32'h0000FFFF) pdu_count_o <= pdu_count_o + 32'd1;\n"
                   "        dirty_p_o <= 1'b1;")],
    # FRAMES_TX saturates instead of wrapping at 32 bits
    "tx-saturate": [(TX, "ftx_r[c] <= ftx_r[c] + 32'd1;",
                     "if (ftx_r[c] != 32'hFFFFFFFF) ftx_r[c] <= ftx_r[c] + 32'd1;")],
    # only the AAF per-PDU dirty is removed; the interval-commit dirty remains
    "aaf-pdu-dirty-only": [(AAF, "            dirty_p_o[ev_s_r] <= 1'b1;\n            monst_r <= monst_next_w;",
                            "            monst_r <= monst_next_w;")],
    # processor scheduler spacing loosened to 900 ms (rate limit broken)
    "sched-900": [(NOTIFY, "((now_ms_i - ctr_last_r[c]) >= 32'd1000)",
                   "((now_ms_i - ctr_last_r[c]) >= 32'd900)")],
    # processor scheduler spacing 1030 ms (just over the fixed 1025 ms bound)
    "sched-1030": [(NOTIFY, "((now_ms_i - ctr_last_r[c]) >= 32'd1000)",
                    "((now_ms_i - ctr_last_r[c]) >= 32'd1030)")],
    # processor scheduler spacing 1020 ms (inside the fixed 1025 ms bound)
    "sched-1020": [(NOTIFY, "((now_ms_i - ctr_last_r[c]) >= 32'd1000)",
                    "((now_ms_i - ctr_last_r[c]) >= 32'd1020)")],
}

orig_plant = sc.plant


def plant(variant, w, output_condition):
    paths = orig_plant("clean", w, output_condition)
    for rel, old, new in PLANTS[probe]:
        src = Path(paths.get(str(repo / rel), str(repo / rel)))
        text = src.read_text()
        if text.count(old) != 1:
            raise SystemExit(f"anchor count {text.count(old)} for {probe}: {old!r}")
        dest = w / ("probe_" + Path(rel).name)
        dest.write_text(text.replace(old, new))
        paths[str(repo / rel)] = str(dest)
    return paths


def groups_of(log: Path) -> dict:
    out = {}
    if log.exists():
        for line in log.read_text(errors="replace").splitlines():
            if "[FAIL]" in line:
                tag = line.split("[726 ")[1].split("]")[0] if "[726 " in line else "other"
                out[tag] = out.get(tag, 0) + 1
    return out


sc.plant = plant
try:
    sc.run(shape, "clean", work, os.environ.get("VERILATOR", "verilator"), condition)
    verdict = "ESCAPED (clean-run contract passed)"
except RuntimeError as exc:
    verdict = f"DETECTED: {str(exc)[:240]}"
print(f"PROBE {probe} shape={shape} condition={condition}: {verdict}")
print(f"PROBE {probe} failing groups: {groups_of(work / 'run.log')}")
if omit:
    env = dict(os.environ, COUNTERS_OMIT_CHECK=omit)
    runtime = work / "tb/verilator/milan_dp"
    with (work / "omit.log").open("w") as log:
        rc = subprocess.run([str(work / "obj/stream_counters")], cwd=runtime, env=env,
                            stdout=log, stderr=subprocess.STDOUT, check=False).returncode
    text = (work / "omit.log").read_text(errors="replace")
    ok = rc == 0 and "RESULT: PASS" in text and "[FAIL]" not in text
    print(f"PROBE {probe} omit={omit}: rc={rc} {'ESCAPES (passes with group omitted)' if ok else 'STILL FAILS'} "
          f"groups={groups_of(work / 'omit.log')}")
