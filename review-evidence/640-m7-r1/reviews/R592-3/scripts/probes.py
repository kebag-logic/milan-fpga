#!/usr/bin/env python3
"""Reviewer fault probes for PR #713 (issue #640 lane M7), independent of the
author's mutants.py. Each probe plants one defect in the CHANGED RTL of a
private hard-link copy of an exact-head extraction (the mutated file is
unlinked first, so the base tree is never written), then runs `make run` of
the named suites and records the tally and the failed check names.

usage: probes.py <base-tree> <work-dir> <out-dir> <parallel> <verilator-jobs>
"""
import concurrent.futures as cf
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
T, S = "gptp_tables", "gptp_shadow"

# (name, file, old, new, suites)
PROBES = [
    ("rx_lowest_lane", SHADOW,
     "      if (rx_tkeep_i[i]) fw_top_w = LANE_W_C'(i);",
     "      if (rx_tkeep_i[KEEP_W_C-1-i]) fw_top_w = LANE_W_C'(KEEP_W_C-1-i);",
     [T, S]),
    ("rx_bad_mask_all_bits", SHADOW,
     "    .USER_BAD_FRAME_MASK ((LANE_W_C + 1)'(1)),",
     "    .USER_BAD_FRAME_MASK ('1),",
     [T, S]),
    ("tx_decode_le", SHADOW,
     "      txf_keep_w[i] = (CNT_W_C'(i) < txf_cnt_w);",
     "      txf_keep_w[i] = (CNT_W_C'(i) <= txf_cnt_w);",
     [T, S]),
    ("tx_count_no_plus1", SHADOW,
     "          st_cnt_r   <= CNT_W_C'(gb_idx_r) + CNT_W_C'(1);",
     "          st_cnt_r   <= CNT_W_C'(gb_idx_r);",
     [T, S]),
    ("tx_decode_count0_allones", SHADOW,
     "      txf_keep_w[i] = (CNT_W_C'(i) < txf_cnt_w);",
     "      txf_keep_w[i] = (CNT_W_C'(i) < txf_cnt_w) || (txf_cnt_w == '0);",
     [T, S]),
    ("ledger_type_written_at_head", RET,
     "      led_type_r[led_tail_w] <= alloc_type_i;",
     "      led_type_r[led_head_r] <= alloc_type_i;",
     [T, S]),
    ("result_seq_from_ledger_tail", RET,
     "      res_seq_r [res_tail_w] <= led_head_seq_w;",
     "      res_seq_r [res_tail_w] <= led_seq_r[led_tail_w];",
     [T, S]),
    ("ledger_write_ungated_when_full", RET,
     "  assign led_we_w = alloc_i && (n_led_r != OCC_W_C'(TXTS_CAP_N_P));",
     "  assign led_we_w = alloc_i;",
     [T, S]),
    ("timer_written_at_sweep_slot", TIMER,
     "      deadline_r[arm_slot_i] <= ms_now_r + arm_delta_ms_i;",
     "      deadline_r[sweep_r] <= ms_now_r + arm_delta_ms_i;",
     [T, S]),
    ("timer_deadline_drops_delta_msb", TIMER,
     "      deadline_r[arm_slot_i] <= ms_now_r + arm_delta_ms_i;",
     "      deadline_r[arm_slot_i] <= ms_now_r + {1'b0, arm_delta_ms_i[30:0]};",
     [T, S]),
    ("result_gen_stuck_1", RET,
     "      res_gen_r [res_tail_w] <= gen_r;",
     "      res_gen_r [res_tail_w] <= TXTS_GEN_W_P'(1);",
     [T, S]),
    ("result_ok_stuck_1", RET,
     "      res_ok_r  [res_tail_w] <= res_ok_w;",
     "      res_ok_r  [res_tail_w] <= 1'b1;",
     [T, S]),
    ("ledger_tag_stuck_1", RET,
     "      led_tag_r [led_tail_w] <= alloc_tagged_i;",
     "      led_tag_r [led_tail_w] <= 1'b1;",
     [T, S]),
    ("result_ns_low_bit_stuck", RET,
     "      res_ns_r  [res_tail_w] <= res_ns_w;",
     "      res_ns_r  [res_tail_w] <= {res_ns_w[63:1], 1'b0};",
     [T, S]),
]

TALLY = re.compile(r"== (\S+): checks: (\d+) +failures: (\d+) ==")


def run_probe(base: Path, work: Path, probe, vjobs: int) -> dict:
    name, rel, old, new, suites = probe
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    subprocess.run(["cp", "-al", str(base), str(tree)], check=True)
    target = tree / rel
    text = target.read_text(encoding="utf-8")
    rec = {"probe": name, "file": rel, "old": old, "new": new, "suites": {}}
    if text.count(old) != 1:
        rec["anchor"] = f"found {text.count(old)} times"
        return rec
    target.unlink()  # break the hard link before writing
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    env = dict(os.environ, VERILATOR_JOBS=str(vjobs))
    for suite in suites:
        cwd = tree / "tb" / "verilator" / suite
        args = ["make", "-s", "run"]
        if suite == T:
            args.insert(1, "gptp_ucode.hex")
        p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
        out = p.stdout + p.stderr
        (work / f"{name}.{suite}.log").write_text(out, encoding="utf-8")
        m = TALLY.search(out)
        fails = sorted({l.strip()[7:].split("  got=")[0].strip()
                        for l in out.splitlines() if l.strip().startswith("[FAIL] ")})
        rec["suites"][suite] = {
            "rc": p.returncode,
            "tally": m.group(0) if m else None,
            "failed_checks": fails,
        }
    shutil.rmtree(tree)
    return rec


def main() -> int:
    base, work, out = (Path(a).resolve() for a in sys.argv[1:4])
    par, vjobs = int(sys.argv[4]), int(sys.argv[5])
    probes = PROBES
    if len(sys.argv) > 6:  # optional: a JSON list of [name, file, old, new, suites]
        probes = [tuple(p) for p in json.loads(Path(sys.argv[6]).read_text())]
    work.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    results = []
    with cf.ThreadPoolExecutor(max_workers=par) as ex:
        futs = [ex.submit(run_probe, base, work, p, vjobs) for p in probes]
        for f in cf.as_completed(futs):
            r = f.result()
            results.append(r)
            print(json.dumps({"probe": r["probe"],
                              "suites": {k: (v["tally"], v["failed_checks"][:4])
                                         for k, v in r["suites"].items()},
                              "anchor": r.get("anchor")}), flush=True)
    results.sort(key=lambda r: r["probe"])
    (out / "probes.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
