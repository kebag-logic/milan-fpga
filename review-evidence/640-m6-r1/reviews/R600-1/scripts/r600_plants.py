#!/usr/bin/env python3
"""Reviewer plants for the #640 M6 lockstep legs (independent of the lane's own mutants).

Usage: python3 -I r600_plants.py <repo-root> <work-dir> <suite: avtp_rxmon|chmap_capture> <receipt-dir>

Each plant replaces exactly one text in the shipping module, builds the
suite's own `make lockstep-build` recipe with the source and object directory
overridden, runs both shapes and records rc and every [FAIL] line. A plant is
CAUGHT only when a binary exits non-zero AND prints at least one [FAIL] line.
"""
import subprocess
import sys
from pathlib import Path

ROOT, WORK, SUITE, RCPT = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                           sys.argv[3], Path(sys.argv[4]).resolve())

if SUITE == "avtp_rxmon":
    RTL = ROOT / "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
    VAR, EXE = "RXMON_SRC", "Vavtp_rxmon_lockstep"
    PLANTS = [
        ("R1_cur_idx_off_by_one",
         "        cur_idx_r <= pdisp_new_w ? pq_wp_r : pq_rp_r;",
         "        cur_idx_r <= pdisp_new_w ? pq_wp_r : pq_rp_r + 2'd1;"),
        ("R2_rp_survives_reset",
         "      pq_rp_r     <= '0;\n",
         ""),
        ("R3_mirror_writes_sink0_only",
         "    if (cntw_hit_w)\n      cnt_mirror_r[",
         "    if (cntw_hit_w && ram_waddr_w[AW_C-1:5] == '0)\n      cnt_mirror_r["),
        ("R4_tv_column_serves_tnv",
         "      C_TV_C  : diag_q_o = tv_cnt_r [diag_ridx_w];",
         "      C_TV_C  : diag_q_o = tnv_cnt_r[diag_ridx_w];"),
    ]
else:
    RTL = ROOT / "hdl/ieee1722/aaf/KL_chan_map_capture.sv"
    VAR, EXE = "LS_SRC", "Vchmap_lockstep"
    PLANTS = [
        ("C1_loop_half_ignored",
         "                                            + 2 * (32'(idxh_f) * LB_PPS_C\n"
         "                                                   + 32'(idx_f))\n"
         "                                            + 32'(half_f))",
         "                                            + 2 * (32'(idxh_f) * LB_PPS_C\n"
         "                                                   + 32'(idx_f)))"),
        ("C2_bank_samples_swapped",
         "beat_bank_r[beat_wp_r] <= {cm0_l_w, lb_smp0_w, lb_smp1_w};",
         "beat_bank_r[beat_wp_r] <= {cm0_l_w, lb_smp1_w, lb_smp0_w};"),
        ("C3_second_commit_next_slot",
         "        skid_beat_r[skid_wp1_w] <= beat_wp_r;",
         "        skid_beat_r[skid_wp1_w] <= beat_wp_r + 2'd1;"),
        ("C4_i2s_rows_swapped",
         "    {cand_w[1], cand_w[2]} = i2s_hold_r;",
         "    {cand_w[2], cand_w[1]} = i2s_hold_r;"),
    ]

suite_dir = ROOT / "tb/verilator" / SUITE
src = RTL.read_text()
WORK.mkdir(parents=True, exist_ok=True)
summary = []
for name, old, new in PLANTS:
    n = src.count(old)
    if n != 1:
        summary.append(f"{name}: PATTERN COUNT {n} (not applied)")
        continue
    mpath = WORK / f"{RTL.stem}_{name}.sv"
    mpath.write_text(src.replace(old, new))
    diff = subprocess.run(["diff", "-u", str(RTL), str(mpath)], capture_output=True, text=True).stdout
    (RCPT / f"plant_{SUITE}_{name}.diff").write_text(diff.replace(str(ROOT) + "/", "").replace(str(WORK) + "/", ""))
    mdir = WORK / f"obj_{name}"
    b = subprocess.run(["make", "-s", "-C", str(suite_dir), "lockstep-build", f"{VAR}={mpath}",
                        f"LS_MDIR={mdir}"], capture_output=True, text=True)
    log = [f"# build rc {b.returncode}", b.stdout[-3000:], b.stderr[-3000:]]
    if b.returncode != 0:
        summary.append(f"{name}: BUILD FAILED rc {b.returncode}")
        (RCPT / f"plant_{SUITE}_{name}.log").write_text("\n".join(log))
        continue
    verdicts = []
    for shape in ("1", "8"):
        r = subprocess.run([str(Path(f"{mdir}{shape}") / EXE)], cwd=str(suite_dir),
                           capture_output=True, text=True)
        out = r.stdout + r.stderr
        fails = [l.strip() for l in out.splitlines() if l.strip().startswith("[FAIL]")]
        log += [f"# shape {shape} rc {r.returncode}", out]
        caught = r.returncode != 0 and bool(fails)
        verdicts.append(f"shape {shape}: rc {r.returncode}, {len(fails)} [FAIL] "
                        f"({'CAUGHT' if caught else 'not caught'})"
                        + (f"; first: {fails[0][:160]}" if fails else ""))
    (RCPT / f"plant_{SUITE}_{name}.log").write_text("\n".join(log))
    summary.append(f"{name}: " + " | ".join(verdicts))
text = "\n".join(summary) + "\n"
(RCPT / f"plants_{SUITE}_summary.txt").write_text(text)
print(text, end="")
