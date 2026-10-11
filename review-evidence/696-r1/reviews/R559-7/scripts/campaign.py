#!/usr/bin/env python3
"""Reviewer-side parallel replay of tb/verilator/maap/mutants.py plus extra probes.

Usage: python3 -I campaign.py <repo> <workdir> <jobs> [--only-probes]

Reads MUTANTS / DATAPATH_MUTANTS from the repository's own mutants.py (by
import from its directory), applies each anchor exactly once to a scratch copy
of KL_maap.sv (or milan_datapath.sv for wiring probes), builds through the
suite's own Makefile targets and applies the suite's kill rule: build rc 0,
harness rc 1 and "[FAIL] <named check>" in its output. A probe whose expected
check is None is reported as CAUGHT (any failure, rc 1) or ESCAPED (rc 0).
No checkout file is written; all outputs land under <workdir>.
"""
import importlib.util
import os
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3])
only_probes = "--only-probes" in sys.argv
suite = repo / "tb/verilator/maap"
spec = importlib.util.spec_from_file_location("maap_mutants", suite / "mutants.py")
mm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mm)
rtl_src = (repo / "hdl/ieee1722/maap/KL_maap.sv").read_text()
dp_path = repo / "hdl/milan/milan_datapath.sv"
dp_src = dp_path.read_text()
work.mkdir(parents=True, exist_ok=True)
dp_gate = threading.Semaphore(3)          # datapath builds are heavy
env = dict(os.environ, MAKEFLAGS="")

# Reviewer probes: (name, target file 'rtl'|'dp', harness 'unit'|'int', anchor,
# replacement, expected named check or None for "any failure")
PROBES = (
    ("p_dp_link_tied_high", "dp", "int", ".port_operational_i (eff_link_w),",
     ".port_operational_i (1'b1),", "M5 datapath: link return starts four fresh PROBEs"),
    ("p_dp_clock_zero", "dp", "int", ".realtime_ns_i     (ptp_now_w[31:0]),",
     ".realtime_ns_i     (32'd0),", "M3 datapath: real-time clock changes probe intervals"),
    ("p_dp_clock_high_word", "dp", "int", ".realtime_ns_i     (ptp_now_w[31:0]),",
     ".realtime_ns_i     (ptp_now_w[63:32]),", None),
    ("p_m8_keep5_one_byte", "rtl", "unit", "(rbeat_r == 3'd5) ? 8'h03 : 8'h00",
     "(rbeat_r == 3'd5) ? 8'h01 : 8'h00", None),
    ("p_m8_no_frame_rearm", "rtl", "unit", "((rbeat_r == '0) || rx_bytes_valid_r)",
     "(1'b1)", None),
    ("p_m8_last_beat_unchecked", "rtl", "unit", "&& rx_bytes_valid_r && rx_beat_complete_w;",
     "&& rx_bytes_valid_r;", None),
    ("p_m6_cancel_no_disable", "rtl", "unit", "if (!enable_i || restart_w || port_operational_p)",
     "if (restart_w || port_operational_p)", "M6 pending response cancelled with allocation"),
    ("p_m6_cancel_no_restart", "rtl", "unit", "if (!enable_i || restart_w || port_operational_p)",
     "if (!enable_i || port_operational_p)", "M6 pending response cancelled with allocation"),
    ("p_m6_cancel_no_link", "rtl", "unit", "if (!enable_i || restart_w || port_operational_p)",
     "if (!enable_i || restart_w)", "M6 pending response cancelled with allocation"),
    ("p_m6_conf_start_not_saved", "rtl", "unit", "tx_conf_start_r <= conf_start_w;",
     "tx_conf_start_r <= offset_r;", None),
    ("p_m6_conf_cnt_not_saved", "rtl", "unit", "tx_conf_cnt_r   <= conf_cnt_w;",
     "tx_conf_cnt_r   <= 16'(count_i);", None),
    ("p_m2_count_low_byte", "rtl", "unit", "tx_cnt_r        <= rx_cnt_r;",
     "tx_cnt_r        <= {8'd0, rx_cnt_r[7:0]};", "M2 B.3.6.6 requested count echoes all 16 bits"),
    ("p_m2_own_count_live", "rtl", "unit", "{8'd0, tx_own_cnt_r}", "{8'd0, count_i}", None),
    ("p_m1_defend_probe_compare", "rtl", "unit", "((state_r != ANNOUNCE_S) || !mac_lower_w)",
     "!mac_lower_w", None),
    ("p_m1_probe_compare_le", "rtl", "unit",
     "wire mac_lower_w = octet_rev(station_mac_i) < octet_rev(rx_src_r);",
     "wire mac_lower_w = octet_rev(station_mac_i) <= octet_rev(rx_src_r);", None),
    ("p_m7_count0_offset_bound", "rtl", "unit", "(seed_offset_i < POOL_SIZE_C)\n", "1'b1\n", None),
    ("p_m5_link_keeps_offset", "rtl", "unit",
     "offset_r     <= rand_offset(lfsr_r[15:0], count_i);",
     "offset_r     <= port_operational_p && !restart_w ? offset_r : rand_offset(lfsr_r[15:0], count_i);",
     None),
    ("p_m5_link_counts_conflict", "rtl", "unit", "            if (restart_w)\n              conflicts_o",
     "            if (1'b1)\n              conflicts_o", None),
    ("p_m4_rebegin_reuses_first_fold", "rtl", "unit", "rand_offset(rng_seeded_r ? lfsr_next_w[15:0]",
     "rand_offset(1'b0 ? lfsr_next_w[15:0]", None),
    ("p_m4_seed_after_mac_ignored_high", "rtl", "unit", "station_mac_i[31:0] + realtime_ns_i",
     "{station_mac_i[31:16], 16'd0} + realtime_ns_i", None),
    ("p_m3_announce_from_fold", "rtl", "unit", "{6'd0, lfsr_r[9:0]}", "{6'd0, 4'd0, probe_fold(lfsr_next_w)}", None),
)

dp_srcs = subprocess.run(["make", "-s", "--no-print-directory", "-C", str(repo / "tb/verilator/milan_dp"),
                          "print-srcs"], capture_output=True, text=True, check=True, env=env).stdout.split()
dp_srcs = [str((repo / "tb/verilator/milan_dp" / s).resolve()) for s in dp_srcs]


def build_and_run(name, rtl_text, dp_text, harness):
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    rtl = d / "KL_maap.sv"
    rtl.write_text(rtl_text)
    if harness == "unit":
        cmd = ["make", "-s", "-C", str(suite), "build", f"MAAP_RTL={rtl}", f"MDIR={d / 'obj'}",
               "VERILATOR=verilator", "VERILATOR_JOBS=1"]
        exe = d / "obj" / "VKL_maap_sim"
        gate = None
    else:
        srcs = []
        for s in dp_srcs:
            if s.endswith("/hdl/ieee1722/maap/KL_maap.sv"):
                s = str(rtl)
            elif s.endswith("/hdl/milan/milan_datapath.sv") and dp_text is not None:
                p = d / "milan_datapath.sv"
                p.write_text(dp_text)
                s = str(p)
            srcs.append(s)
        cmd = ["make", "-s", "-C", str(suite), "-f", "integration.mk", "build",
               f"DP_MDIR={d / 'obj'}", f"MAAP_RTL={rtl}", "SRCS=" + " ".join(srcs),
               "VERILATOR=verilator", "VERILATOR_JOBS=2"]
        exe = d / "obj" / "maap_integration"
        gate = dp_gate
    if gate:
        gate.acquire()
    try:
        b = subprocess.run(cmd, capture_output=True, text=True, env=env)
        (d / "build.log").write_text(b.stdout + b.stderr)
        if b.returncode:
            return "BUILD_FAIL", b.returncode, ""
        r = subprocess.run([str(exe)], cwd=exe.parent, capture_output=True, text=True)
        out = r.stdout + r.stderr
        (d / "run.log").write_text(out)
        return "RAN", r.returncode, out
    finally:
        if gate:
            gate.release()


def judge(row):
    name, rtl_text, dp_text, harness, expect, mode = row
    status, rc, out = build_and_run(name, rtl_text, dp_text, harness)
    fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l]
    if status != "RAN":
        verdict = "BUILD_FAIL"
    elif mode == "clean":
        verdict = "PASS" if rc == 0 and " 0 failures" in out else "CONTROL_FAIL"
    elif expect is not None:
        verdict = "KILLED" if rc == 1 and any(f"[FAIL] {expect}" in l for l in out.splitlines()) else "ESCAPED"
    else:
        verdict = "CAUGHT" if rc == 1 and fails else ("ESCAPED" if rc == 0 else f"ABNORMAL_rc{rc}")
    return name, harness, verdict, rc, expect, fails


rows = []
rows.append(("clean_unit", rtl_src, None, "unit", None, "clean"))
rows.append(("clean_int", rtl_src, None, "int", None, "clean"))
if not only_probes:
    for name, _item, anchor, repl, failure in mm.MUTANTS:
        assert rtl_src.count(anchor) == 1, name
        rows.append((name, rtl_src.replace(anchor, repl), None, "unit", failure, "mutant"))
    for name, anchor, repl, failure in mm.DATAPATH_MUTANTS:
        assert rtl_src.count(anchor) == 1, name
        rows.append((name, rtl_src.replace(anchor, repl), None, "int", failure, "mutant"))
for name, target, harness, anchor, repl, failure in PROBES:
    src = dp_src if target == "dp" else rtl_src
    if src.count(anchor) != 1:
        print(f"ANCHOR_ERROR {name}: count={src.count(anchor)}", flush=True)
        continue
    m = src.replace(anchor, repl)
    rows.append((name, rtl_src if target == "dp" else m, m if target == "dp" else None,
                 harness, failure, "probe"))

with ThreadPoolExecutor(max_workers=jobs) as ex:
    for name, harness, verdict, rc, expect, fails in ex.map(judge, rows):
        print(f"{verdict:12s} {harness:4s} rc={rc} {name} | expect={expect!r} | fails={len(fails)}"
              + (f" first={fails[0]!r}" if fails else ""), flush=True)
