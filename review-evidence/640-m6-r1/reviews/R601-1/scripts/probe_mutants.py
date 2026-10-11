#!/usr/bin/env python3
"""R601-1 independent mutation probes for the #640 M6 lockstep legs.

Reviewer-spelled plants, distinct from the lane's own lockstep_mutants.py.
Each plant is applied to a COPY of the RTL under the disposable tree's
scratch area, built through the suite's own `make lockstep-build` recipe
(RXMON_SRC / LS_SRC and LS_MDIR overridden) at both shapes, and run.
A plant is CAUGHT when either binary prints a [FAIL] line or exits non-zero
with a harness verdict; SURVIVED when both binaries pass.

Usage: python3 -I probe_mutants.py <tree> <outdir> [--jobs N] [ids...]
The pinned Verilator must be first on PATH (run_suite.sh convention).
"""
import argparse
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

RX = "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
CM = "hdl/ieee1722/aaf/KL_chan_map_capture.sv"

# id: (suite, rtl, [(old, new), ...], intent)
PLANTS = {
    "RX-A-cap3": ("avtp_rxmon", RX,
        [("                               (pq_cnt_r != 2'd2);",
          "                               (pq_cnt_r != 2'd3);")],
        "capacity: a third waiting bundle is admitted (ring overwrites the in-service slot)"),
    "RX-B-ring2": ("avtp_rxmon", RX,
        [("    if (penq_w) pq_ring_r[pq_wp_r] <= new_evt_w;",
          "    if (penq_w) pq_ring_r[{1'b0, pq_wp_r[0]}] <= new_evt_w;"),
         ("  assign cur_w = pq_ring_r[cur_idx_r];",
          "  assign cur_w = pq_ring_r[{1'b0, cur_idx_r[0]}];")],
        "ring aliased to 2 slots: a waiting bundle overwrites the one in service"),
    "RX-C-popidx": ("avtp_rxmon", RX,
        [("        cur_idx_r <= pdisp_new_w ? pq_wp_r : pq_rp_r;",
          "        cur_idx_r <= pdisp_new_w ? pq_wp_r : pq_rp_r + 2'd1;")],
        "queued dispatch serves the second-oldest bundle"),
    "RX-D-mircol": ("avtp_rxmon", RX,
        [("      cnt_mirror_r[MIRW_C'(32'(ram_waddr_w[AW_C-1:5]) * 16 + 32'(cntw_col_w))]\n        <= ram_wdata_w;",
          "      cnt_mirror_r[MIRW_C'(32'(ram_waddr_w[AW_C-1:5]) * 16 + 32'(cntw_col_w) + 1)]\n        <= ram_wdata_w;")],
        "mirror write lands one column high"),
    "RX-E-tvswap": ("avtp_rxmon", RX,
        [("      C_TV_C  : diag_q_o = tv_cnt_r [diag_ridx_w];",
          "      C_TV_C  : diag_q_o = tnv_cnt_r[diag_ridx_w];")],
        "GET_COUNTERS TIMESTAMP_VALID column serves the TNV tally"),
    "RX-F-engonly": ("avtp_rxmon", RX,
        [("    if (cntw_hit_w)\n      cnt_mirror_r",
          "    if (cntw_hit_w && eng_we_w)\n      cnt_mirror_r")],
        "mirror ignores window (non-engine) writes"),
    "RX-G-rowstride": ("avtp_rxmon", RX,
        [("      default : diag_q_o = cnt_mirror_r[MIRW_C'(32'(diag_ridx_w) * 16\n",
          "      default : diag_q_o = cnt_mirror_r[MIRW_C'(32'(diag_ridx_w) * 8\n")],
        "read row stride 8 instead of 16 (sink aliasing)"),
    "RX-H-wpnoreset": ("avtp_rxmon", RX,
        [("      pq_wp_r     <= '0;\n", "")],
        "write pointer survives reset"),
    "RX-I-wrapzero": ("avtp_rxmon", RX,
        [("    if (cntw_hit_w)\n      cnt_mirror_r",
          "    if (cntw_hit_w && ram_wdata_w != 32'd0)\n      cnt_mirror_r")],
        "wrap: the mirror drops a write of zero (a counter wrapping to 0 keeps 0xFFFFFFFF)"),
    "RX-J-wrap31": ("avtp_rxmon", RX,
        [("        <= ram_wdata_w;\n  end : mirror_wr",
          "        <= {1'b0, ram_wdata_w[30:0]};\n  end : mirror_wr")],
        "wrap: the mirror keeps 31 bits (bit 31 of a near-2^32 value lost)"),
    "CM-A-bank2": ("chmap_capture", CM,
        [("    if (enq0_v_w) beat_bank_r[beat_wp_r] <= {cm0_l_w, lb_smp0_w, lb_smp1_w};",
          "    if (enq0_v_w) beat_bank_r[{1'b0, beat_wp_r[0]}] <= {cm0_l_w, lb_smp0_w, lb_smp1_w};"),
         ("  wire [71:0]       head_beat_w = beat_bank_r[skid_beat_r[skid_rp_r]];",
          "  wire [71:0]       head_beat_w = beat_bank_r[{1'b0, skid_beat_r[skid_rp_r][0]}];")],
        "beat bank aliased to 2 slots (overwrite only when 3+ beats are live)"),
    "CM-B-bank3": ("chmap_capture", CM,
        [("        beat_wp_r               <= beat_wp_r + 2'd1;",
          "        beat_wp_r               <= (beat_wp_r == 2'd2) ? 2'd0 : beat_wp_r + 2'd1;")],
        "beat bank cycles 3 slots (overwrite only when the skid holds 4 beats)"),
    "CM-C-enq1slot": ("chmap_capture", CM,
        [("        skid_beat_r[skid_wp1_w] <= beat_wp_r;",
          "        skid_beat_r[skid_wp1_w] <= beat_wp_r + 2'd1;")],
        "second commit of a beat names the next bank slot"),
    "CM-D-stashsmp1": ("chmap_capture", CM,
        [("      CF_STASH_SMP0_C : push_data_w = {head_beat_w[71:48], head_beat_w[47:24]};",
          "      CF_STASH_SMP0_C : push_data_w = {head_beat_w[71:48], head_beat_w[23:0]};")],
        "stash-closing commit takes smp1 instead of smp0"),
    "CM-E-loopidxh": ("chmap_capture", CM,
        [("                                            + 2 * (32'(idxh_f) * LB_PPS_C\n"
          "                                                   + 32'(idx_f))",
          "                                            + 2 * (32'(idx_f))")],
        "LOOP row ignores the stream index idxh"),
    "CM-F-i2sswap": ("chmap_capture", CM,
        [("    {cand_w[1], cand_w[2]} = i2s_hold_r;",
          "    {cand_w[2], cand_w[1]} = i2s_hold_r;")],
        "I2S L/R rows swapped"),
    "CM-G-tdmbound": ("chmap_capture", CM,
        [("        SRC_TDM_C : source_row = (32'(idx_f) < N_TDM_PAIRS_C)",
          "        SRC_TDM_C : source_row = (32'(idx_f) <= N_TDM_PAIRS_C)")],
        "TDM pair bound off by one (pair N_TDM_PAIRS reads a LOOP row)"),
}

SUITE_VAR = {"avtp_rxmon": "RXMON_SRC", "chmap_capture": "LS_SRC"}
EXE = {"avtp_rxmon": "Vavtp_rxmon_lockstep", "chmap_capture": "Vchmap_lockstep"}


def run_one(tree: Path, out: Path, pid: str) -> str:
    suite, rtl, edits, intent = PLANTS[pid]
    src = (tree / rtl).read_text()
    for old, new in edits:
        n = src.count(old)
        if n != 1:
            return f"{pid}: PATTERN-COUNT {n} (plant not applied) - {intent}"
        src = src.replace(old, new)
    work = out / "work" / pid
    work.mkdir(parents=True, exist_ok=True)
    mpath = work / Path(rtl).name
    mpath.write_text(src)
    log = out / f"{pid}.log"
    with log.open("w") as fh:
        fh.write(f"# plant {pid}: {intent}\n")
        for old, new in edits:
            fh.write(f"# - {old!r}\n# + {new!r}\n")
        b = subprocess.run(["make", "-s", "-C", str(tree / "tb/verilator" / suite),
                            "lockstep-build", f"{SUITE_VAR[suite]}={mpath}",
                            f"LS_MDIR={work}/obj"], capture_output=True, text=True)
        fh.write(f"# build rc={b.returncode}\n")
        if b.returncode != 0:
            fh.write(b.stdout[-3000:] + b.stderr[-3000:])
            return f"{pid}: BUILD-FAILED - {intent}"
        fails, rcs = [], []
        for shape in ("1", "8"):
            r = subprocess.run([str(work / f"obj{shape}" / EXE[suite])],
                               cwd=str(tree / "tb/verilator" / suite),
                               capture_output=True, text=True)
            fh.write(f"## shape {shape} rc={r.returncode}\n{r.stdout}{r.stderr}\n")
            rcs.append(r.returncode)
            fails += [f"[{shape}] " + ln.strip() for ln in r.stdout.splitlines()
                      if ln.strip().startswith("[FAIL]")]
    if fails:
        verdict = "CAUGHT"
    elif any(rcs):
        verdict = f"NONZERO-RC-NO-FAIL-LINE rcs={rcs}"
    else:
        verdict = "SURVIVED"
    first = "; ".join(f[:160] for f in fails[:3])
    return f"{pid}: {verdict} rcs={rcs} - {intent}" + (f"\n    first failed checks: {first}" if fails else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree")
    ap.add_argument("outdir")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("ids", nargs="*")
    a = ap.parse_args()
    tree, out = Path(a.tree).resolve(), Path(a.outdir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    ids = a.ids or list(PLANTS)
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        results = list(ex.map(lambda p: run_one(tree, out, p), ids))
    text = "\n".join(results) + "\n"
    (out / "SUMMARY.txt").write_text(text)
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
