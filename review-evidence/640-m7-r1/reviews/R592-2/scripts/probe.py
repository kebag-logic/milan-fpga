#!/usr/bin/env python3
"""Reviewer fault probes for tb/verilator/gptp_tables (issue #640, lane M7).

Each probe copies a pristine source tree (an extraction of the exact head
with its pinned submodules) into its own scratch directory, replaces one
anchor that must occur exactly once, runs `make -s run` of the gptp_tables
suite with the given simulator, and records the tally and the failed check
names. Caller trees are never modified.

Usage:
    probe.py PRISTINE_TREE SCRATCH_DIR LOG_DIR VERILATOR_BIN NAME [NAME ...]
    probe.py --list
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SHADOW = "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
RET = "hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv"
TIMER = "gptp-processor/hdl/common/KL_gptp_timer.sv"

#: name -> (file, old, new, the check family this should break or None)
PROBES = {
    "tx_count_off_by_one": (SHADOW,
        "st_cnt_r   <= CNT_W_C'(gb_idx_r) + CNT_W_C'(1);",
        "st_cnt_r   <= CNT_W_C'(gb_idx_r);",
        "tx_fifo lockstep"),
    "rx_lowest_lane": (SHADOW,
        "      if (rx_tkeep_i[i]) fw_top_w = LANE_W_C'(i);",
        "      if (rx_tkeep_i[i] && (fw_top_w == '0)) fw_top_w = LANE_W_C'(i);",
        "rx_fifo lockstep"),
    "rx_bad_bit_moved": (SHADOW,
        "    .USER_BAD_FRAME_MASK ((LANE_W_C + 1)'(1)),",
        "    .USER_BAD_FRAME_MASK ((LANE_W_C + 1)'(8)),",
        "rx_fifo lockstep"),
    "tx_decode_le": (SHADOW,
        "      txf_keep_w[i] = (CNT_W_C'(i) < txf_cnt_w);",
        "      txf_keep_w[i] = (CNT_W_C'(i) <= txf_cnt_w);",
        "tx_fifo decode"),
    "ledger_tag_stuck0": (RET,
        "      led_tag_r [led_tail_w] <= alloc_tagged_i;",
        "      led_tag_r [led_tail_w] <= 1'b0;",
        "ledger lockstep"),
    "results_seq_from_tail": (RET,
        "      res_seq_r [res_tail_w] <= led_head_seq_w;",
        "      res_seq_r [res_tail_w] <= led_seq_r[led_tail_w];",
        "results lockstep"),
    "ledger_ram_write_when_full": (RET,
        "    if (rst_n && led_we_w) begin",
        "    if (rst_n && alloc_i) begin",
        None),
    "timer_write_slot_alias": (TIMER,
        "      deadline_r[arm_slot_i] <= ms_now_r + arm_delta_ms_i;",
        "      deadline_r[arm_slot_i ^ 3'd1] <= ms_now_r + arm_delta_ms_i;",
        "timer lockstep"),
}

TALLY_RE = re.compile(r"^== gptp_tables: checks: (\d+) +failures: (\d+) ==", re.M)


def run_probe(pristine: Path, scratch: Path, logs: Path, vbin: str, name: str) -> dict:
    rel, old, new, expect = PROBES[name]
    tree = scratch / f"probe-{name}"
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(pristine, tree, symlinks=True)
    path = tree / rel
    text = path.read_text(encoding="utf-8")
    result = {"name": name, "file": rel, "expect": expect}
    if text.count(old) != 1:
        result["verdict"] = "ANCHOR-MISSING"
        return result
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    env = dict(os.environ)
    env["PATH"] = str(Path(vbin).parent) + os.pathsep + env.get("PATH", "")
    env["VERILATOR"] = vbin
    proc = subprocess.run(["make", "-s", "run"], cwd=tree / "tb/verilator/gptp_tables",
                          env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, check=False)
    (logs / f"probe_{name}.log").write_text(proc.stdout, encoding="utf-8")
    tally = TALLY_RE.search(proc.stdout)
    failed = sorted({line.strip()[7:].split("  got=")[0].strip()
                     for line in proc.stdout.splitlines()
                     if line.strip().startswith("[FAIL] ")})
    result.update({"make_rc": proc.returncode,
                   "checks": int(tally.group(1)) if tally else None,
                   "failures": int(tally.group(2)) if tally else None,
                   "failed_checks": failed})
    if tally is None:
        result["verdict"] = "NO-TALLY"
    elif int(tally.group(2)) == 0:
        result["verdict"] = "GREEN"
    elif expect and any(f.startswith(expect) for f in failed):
        result["verdict"] = "CAUGHT-BY-EXPECTED"
    else:
        result["verdict"] = "CAUGHT-OTHER"
    shutil.rmtree(tree / "tb/verilator/gptp_tables/obj_dir", ignore_errors=True)
    return result


def main() -> int:
    if sys.argv[1:] == ["--list"]:
        for name, (rel, _o, _n, expect) in PROBES.items():
            print(f"{name:28s} {rel} -> {expect}")
        return 0
    pristine, scratch, logs, vbin = (Path(sys.argv[1]), Path(sys.argv[2]),
                                     Path(sys.argv[3]), sys.argv[4])
    for name in sys.argv[5:]:
        res = run_probe(pristine, scratch, logs, vbin, name)
        (logs / f"probe_{name}.json").write_text(json.dumps(res, indent=1) + "\n",
                                                 encoding="utf-8")
        print(json.dumps(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
