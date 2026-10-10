#!/usr/bin/env python3
"""Reviewer plants for KL_maap: apply each to a scratch copy, build, run, grade.

Usage: python3 -I plants.py <tree> <workdir> [--jobs N]
<tree> is a disposable copy of the exact head (only read); each plant writes
its own mutated KL_maap.sv under <workdir>/<name>/ and builds there.
A plant counts as CAUGHT only when the build succeeds, the harness exits 1 and
the expected named check prints [FAIL]. A plant marked expect=None is a probe
whose outcome is reported, not graded.
"""
import concurrent.futures
import os
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
rtl = (tree / "hdl/ieee1722/maap/KL_maap.sv").read_text()

# (name, kind, anchor, replacement, expected failing check or None, harness)
PLANTS = [
    # Re-application of four or more author plants (same defect, applied here).
    ("re_m2_own_requested_count", "author", "tx_cnt_r        <= rx_cnt_r;",
     "tx_cnt_r        <= {8'd0, count_i};", "M2 B.3.6.6 requested count echoes all 16 bits", "unit"),
    ("re_m6_drop_busy_probe", "author", "if (save_probe_w) begin", "if (1'b0) begin",
     "M6 busy PROBE gets DEFEND after wire is free", "unit"),
    ("re_m5_ignore_link_return", "author", "else if (restart_w || port_operational_p)",
     "else if (restart_w)", "M5 B.3.5.9 link return revokes and reprobes", "unit"),
    ("re_m8_missing_bytes_accepted", "author", "&& rx_bytes_valid_r && rx_beat_complete_w", "",
     "M8 B.2 truncated DEFEND-state input has no effect", "unit"),
    ("re_m7_accept_invalid_seed", "author", " && seed_in_pool_w", "",
     "M7 Table B.9 invalid supplied range refused", "unit"),
    ("re_m1_defend_no_compare", "author", "((state_r != ANNOUNCE_S) || !mac_lower_w)", "1'b1",
     "M1 rDefend/DEFEND lower MAC keeps range", "unit"),
    ("re_m4_reset_time_sampling", "author",
     "      lfsr_r       <= 32'hACE1;\n      rng_seeded_r <= 1'b0;",
     "      lfsr_r       <= enable_seed_w;\n      rng_seeded_r <= 1'b1;",
     "M4 datapath: programmed MAC changes probe intervals", "integration"),
    # Reviewer-designed plants (not in the author's campaign).
    ("new_m2_echo_low_byte_only", "reviewer", "tx_cnt_r        <= rx_cnt_r;",
     "tx_cnt_r        <= {8'd0, rx_cnt_r[7:0]};",
     "M2 B.3.6.6 requested count echoes all 16 bits", "unit"),
    ("new_m8_beat5_needs_one_byte", "reviewer", ": (rbeat_r == 3'd5) ? 8'h03 : 8'h00;",
     ": (rbeat_r == 3'd5) ? 8'h01 : 8'h00;",
     "M8 B.2 truncated", "unit"),
    ("new_m5_link_return_counts_conflict", "reviewer",
     "            if (restart_w)\n              conflicts_o",
     "            if (1'b1)\n              conflicts_o",
     "M5 B.3.5.9 link return", "unit"),
    ("new_m6_pending_survives_restart", "reviewer",
     "if (!enable_i || restart_w || port_operational_p)",
     "if (!enable_i || port_operational_p)",
     "M6 pending response cancelled with allocation", "unit"),
    ("new_m3_reseed_every_enabled_cycle", "reviewer",
     "        lfsr_r       <= enable_seed_w;\n        rng_seeded_r <= 1'b1;",
     "        lfsr_r       <= enable_seed_w;\n        rng_seeded_r <= 1'b0;",
     "M3", "unit"),
    ("new_m1_probe_cell_inverted", "reviewer", "(state_r == PROBE_S) && !mac_lower_w)",
     "(state_r == PROBE_S) && mac_lower_w)", "M1 rProbe/PROBE", "unit"),
    ("new_m5_datapath_raw_link_level_ignored", "reviewer",
     "wire port_operational_p = port_operational_i && !port_operational_r;",
     "wire port_operational_p = 1'b0;",
     "M5 datapath: link return starts four fresh PROBEs", "integration"),
]


def run(plant):
    name, kind, anchor, repl, expect, harness = plant
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    if rtl.count(anchor) != 1:
        return name, kind, "ANCHOR-NOT-UNIQUE", rtl.count(anchor), expect
    src = d / "KL_maap.sv"
    src.write_text(rtl.replace(anchor, repl))
    env = dict(os.environ)
    if harness == "unit":
        cmd = ["make", "-s", "-C", str(tree / "tb/verilator/maap"), "build",
               f"MAAP_RTL={src}", f"MDIR={d / 'obj'}", "VERILATOR_JOBS=2"]
        exe = d / "obj" / "VKL_maap_sim"
    else:
        cmd = ["make", "-s", "-C", str(tree / "tb/verilator/maap"), "integration-build",
               f"MAAP_RTL={src}", f"DP_MDIR={d / 'obj'}", "VERILATOR_JOBS=4"]
        exe = d / "obj" / "maap_integration"
    b = subprocess.run(cmd, capture_output=True, text=True, env=env)
    (d / "build.log").write_text(b.stdout + b.stderr)
    if b.returncode:
        return name, kind, "BUILD-FAILED", b.returncode, expect
    r = subprocess.run([str(exe)], cwd=d / "obj", capture_output=True, text=True, timeout=3000)
    out = r.stdout + r.stderr
    (d / "run.log").write_text(out)
    fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l]
    named = any(expect in l for l in fails)
    verdict = "CAUGHT" if (r.returncode == 1 and named) else (
        "ESCAPED" if r.returncode == 0 else "OTHER")
    return name, kind, verdict, r.returncode, expect + " | fails: " + "; ".join(fails[:6])


with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
    results = list(pool.map(run, PLANTS))
caught = 0
for name, kind, verdict, rc, info in results:
    caught += verdict == "CAUGHT"
    print(f"{verdict:18} rc={rc} [{kind}] {name}: {info}")
print(f"plants caught: {caught}/{len(results)}")
sys.exit(0 if caught == len(results) else 1)
