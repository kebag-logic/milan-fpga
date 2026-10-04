#!/usr/bin/env python3
"""R463-2 per-face probes of section AQ's drive (beyond the round-2 bar).

usage: aq_face_probes.py --trees DIR --work DIR --out DIR [--jobs N]

Plants a full-queue defect on ONE face only (the lowest-priority face 7, or the
middle face 3) in a copy of the head, then runs --arm-queue-only. Each must fail
AQ3: the drive must reach the full-queue path on a face other than the one that
pops most. Reuses aq_matrix.py's staging and run helpers; same environment.
"""
import argparse
import concurrent.futures
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import aq_matrix  # noqa: E402

PUSH_OK = "armq_push_ok_w[i] = armq_in_vld_w[i] && (armq_mid_w[i] != 3'd4);"
STORE = "if (armq_push_ok_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];"
WRITE = "assign wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0];"


def probes():
    out = {}
    for f in (7, 3):
        out[f"f{f}_full_pop_refuses"] = (
            PUSH_OK, f"armq_push_ok_w[i] = armq_in_vld_w[i] && "
                     f"(((i == {f}) ? armq_cnt_r[i] : armq_mid_w[i]) != 3'd4);")
        out[f"f{f}_wr_wrap_hi"] = (
            WRITE, f"assign wr_ix_w = (g == {f} && armq_cnt_r[g] >= 3'd3) ? armq_hd_r[g] + 2'd2"
                   f" : armq_hd_r[g] + armq_cnt_r[g][1:0];")
    out["f7_write_refused"] = (
        STORE, "if ((g == 7) ? armq_in_vld_w[g] : armq_push_ok_w[g]) mem_r[wr_ix_w] <= armq_in_w[g];")
    out["f7_wr_at_head"] = (
        WRITE, "assign wr_ix_w = (g == 7) ? armq_hd_r[g] : armq_hd_r[g] + armq_cnt_r[g][1:0];")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trees", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    args.r462 = None
    args.out.mkdir(parents=True, exist_ok=True)
    args.work.mkdir(parents=True, exist_ok=True)
    jobs = [{"name": n, "kind": "plant", "hdl": "head", "tb": "head", "edit": e, "expect": "fail"}
            for n, e in probes().items()]
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        results = list(pool.map(lambda j: aq_matrix.run_job(j, args), jobs))
    ok = True
    for r in results:
        r["as_expected"] = (r["rc"] != 0) == (r["expect"] == "fail")
        ok &= r["as_expected"]
        print(f"{r['name']:<24} rc={r['rc']:<5} expect={r['expect']:<4} "
              f"{'OK' if r['as_expected'] else 'UNEXPECTED'}")
    (args.out / "results.json").write_text(json.dumps(results, indent=1) + "\n")
    print("ALL AS EXPECTED" if ok else "SOME UNEXPECTED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
