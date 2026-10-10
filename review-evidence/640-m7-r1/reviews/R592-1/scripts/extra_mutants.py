#!/usr/bin/env python3
"""Reviewer-owned extra planted defects for tb/verilator/gptp_tables.

Each control copies the files the suite builds into its own work directory,
plants one defect by an exact-once text replacement, runs `make -s run` and
records which named checks failed. Controls run in parallel.

Usage: python3 -I extra_mutants.py <repo> <workdir> <jobs>
Needs `verilator` (5.050) on PATH. The repository is only read.
"""
import concurrent.futures as cf
import re
import shutil
import subprocess
import sys
from pathlib import Path

SHADOW = "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
RET = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
TIMER = "gptp-processor/hdl/common/KL_gptp_timer.sv"

# (name, file, old, new, what a correct bench should do)
CONTROLS = [
    ("results_write_at_head", RET,
     "      res_ns_r  [res_tail_w] <= res_ns_w;",
     "      res_ns_r  [res_head_r] <= res_ns_w;",
     "results lockstep fails"),
    ("ledger_write_at_head", RET,
     "      led_seq_r [led_tail_w] <= alloc_seq_i;",
     "      led_seq_r [led_head_r] <= alloc_seq_i;",
     "ledger lockstep fails"),
    ("rx_top_as_popcount", SHADOW,
     "    for (int unsigned i = 0; i < KEEP_W_C; i++) begin\n"
     "      if (rx_tkeep_i[i]) fw_top_w = LANE_W_C'(i);\n"
     "    end",
     "    for (int unsigned i = 1; i < KEEP_W_C; i++) begin\n"
     "      if (rx_tkeep_i[i]) fw_top_w = fw_top_w + LANE_W_C'(1);\n"
     "    end",
     "rx_fifo lockstep fails (equal for contiguous tkeep, differs only "
     "for a non-contiguous one)"),
    ("tx_decode_odd_counts", SHADOW,
     "      txf_keep_w[i] = (CNT_W_C'(i) < txf_cnt_w);",
     "      txf_keep_w[i] = (CNT_W_C'(i) < {txf_cnt_w[CNT_W_C-1:1], 1'b0});",
     "survives if no odd lane count ever leaves the FIFO (coverage probe)"),
    ("timer_write_alias", TIMER,
     "      deadline_r[arm_slot_i] <= ms_now_r + arm_delta_ms_i;",
     "      deadline_r[{1'b0, arm_slot_i[SW_C-2:0]}] <= ms_now_r + arm_delta_ms_i;",
     "timer lockstep fails"),
    ("results_seq_from_tail", RET,
     "      res_seq_r [res_tail_w] <= led_head_seq_w;",
     "      res_seq_r [res_tail_w] <= led_seq_r[led_tail_w];",
     "results lockstep fails"),
]

COPY = ["hdl", "gptp-processor/hdl", "third_party/verilog-axis/rtl",
        "tb/verilator/gptp_tables", "tb/verilator/gptp_shadow", "tb/common"]
TALLY = re.compile(r"^== gptp_tables: checks: (\d+) +failures: (\d+) ==", re.M)
IGNORE = shutil.ignore_patterns("obj_dir", "gptp_ucode.hex", ".git")


def run(repo: Path, work: Path, ctl) -> str:
    name, rel, old, new, expect = ctl
    root = work / name
    if root.exists():
        shutil.rmtree(root)
    for sub in COPY:
        shutil.copytree(repo / sub, root / sub, ignore=IGNORE)
    path = root / rel
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        return f"[ANCHOR] {name}: anchor count {text.count(old)}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    proc = subprocess.run(["make", "-s", "run", "VERILATOR_JOBS=2"],
                          cwd=root / "tb/verilator/gptp_tables",
                          capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    (work / f"{name}.log").write_text(out, encoding="utf-8")
    tally = TALLY.search(out)
    fails = sorted({l.strip()[7:].split("  got=")[0].strip()
                    for l in out.splitlines() if l.strip().startswith("[FAIL] ")})
    shutil.rmtree(root)
    verdict = ("NO TALLY" if tally is None else
               ("CAUGHT" if int(tally.group(2)) else "SURVIVED"))
    return (f"{name}: {verdict} (make rc {proc.returncode}); expected: {expect}; "
            f"failed checks: {fails}")


def main() -> int:
    repo, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
    work.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda c: run(repo, work, c), CONTROLS))
    for line in results:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
