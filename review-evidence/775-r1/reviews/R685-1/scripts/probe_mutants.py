#!/usr/bin/env python3
"""Reviewer-owned disposable mutation probes for #775 (AAF ctx engine and CRF input).

usage: python3 -I probe_mutants.py <head-tree> <work-dir> <out-dir> [jobs]

Each mutant is planted in a COPY of one RTL file under <work-dir>; the head
tree's own Makefile recipe builds the harness against that copy (RXMON_SRC /
RX_RTL override, private Mdir). No tracked file is edited. A mutant is CAUGHT
when the harness exits nonzero and prints at least one [FAIL] line; the
failing check names are recorded per mutant.
"""
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

AAF_ANCHOR = "            monst_r <= {ram_q_r[31:8], cur_w.seq};"
PSEQ_ADDR = ("      M_PSEQ_S : begin\n        eng_we_w    = 1'b1;\n"
             "        eng_waddr_w = laddr(ev_s_r, W_MONST_C);")
CRF_ANCHOR = "          exp_seq_r <= seq_i + 8'd1;\n        end else begin"

AAF = [
    ("aaf_lock_set", AAF_ANCHOR,
     "            monst_r <= {ram_q_r[31:13], 1'b1, ram_q_r[11:8], cur_w.seq};"),
    ("aaf_settle_dec", AAF_ANCHOR,
     "            monst_r <= {ram_q_r[31:12], (ram_q_r[11:8] == 4'd0) ? 4'd0 "
     ": (ram_q_r[11:8] - 4'd1), cur_w.seq};"),
    ("aaf_settle_restart", AAF_ANCHOR,
     "            monst_r <= {ram_q_r[31:12], 4'd8, cur_w.seq};"),
    ("aaf_mr_seed", AAF_ANCHOR,
     "            monst_r <= {ram_q_r[31:24], 1'b1, cur_w.mr, ram_q_r[21:8], cur_w.seq};"),
    ("aaf_wire_chans", AAF_ANCHOR,
     "            monst_r <= {ram_q_r[31:22], p_chans_w, ram_q_r[13:8], cur_w.seq};"),
    ("aaf_off_by_one", AAF_ANCHOR,
     "            monst_r <= {ram_q_r[31:8], cur_w.seq + 8'd1};"),
    ("aaf_pseq_stream0_addr", PSEQ_ADDR,
     PSEQ_ADDR.replace("laddr(ev_s_r, W_MONST_C)", "laddr('0, W_MONST_C)")),
    ("aaf_pseq_no_write", PSEQ_ADDR, PSEQ_ADDR.replace("eng_we_w    = 1'b1;", "eng_we_w    = 1'b0;")),
    ("aaf_reject_refreshes_silence", AAF_ANCHOR,
     AAF_ANCHOR + "\n            sil_ms_r[ev_s_r] <= '0;"),
]
CRF = [
    ("crf_no_plus_one", CRF_ANCHOR,
     "          exp_seq_r <= seq_i;\n        end else begin"),
    ("crf_reject_clears_have_seq", CRF_ANCHOR,
     "          exp_seq_r <= seq_i + 8'd1;\n          have_seq_r <= 1'b0;\n        end else begin"),
    ("crf_reject_seeds_mr", CRF_ANCHOR,
     "          exp_seq_r <= seq_i + 8'd1;\n          prev_mr_r <= mr_i;\n"
     "          mr_seeded_r <= 1'b1;\n        end else begin"),
    ("crf_reject_moves_delta", CRF_ANCHOR,
     "          exp_seq_r <= seq_i + 8'd1;\n          delta_o <= w_tsd;\n        end else begin"),
]


def plant(src: str, pat: str, rep: str) -> str:
    n = src.count(pat)
    if n != 1:
        raise SystemExit(f"pattern count {n} != 1: {pat!r}")
    return src.replace(pat, rep)


def one(kind: str, name: str, pat: str, rep: str, head: Path, work: Path, out: Path) -> str:
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    if kind == "aaf":
        rtl = head / "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv"
        tb = head / "tb/verilator/avtp_rxmon"
        m = d / rtl.name
        m.write_text(plant(rtl.read_text(), pat, rep))
        cmd = ["make", "-s", "-C", str(tb), "nx-build", f"RXMON_SRC={m}", f"NX_MDIR={d}/obj"]
        exe = d / "obj" / "Vavtp_rxmon_nx_sim"
    else:
        rtl = head / "hdl/ieee1722/crf/KL_crf_rx.sv"
        tb = head / "tb/verilator/crf_rx"
        m = d / rtl.name
        m.write_text(plant(rtl.read_text(), pat, rep))
        cmd = ["make", "-s", "-C", str(tb), "unit-build", f"RX_RTL={m}", f"UNIT_MDIR={d}/obj"]
        exe = d / "obj" / "Vcrf_rx_sim"
    b = subprocess.run(cmd, capture_output=True, text=True, check=False)
    (out / f"{name}.build.log").write_text(b.stdout[-4000:] + b.stderr[-4000:])
    if b.returncode != 0 or not exe.is_file():
        return f"{name}: BUILD-FAIL rc={b.returncode}"
    r = subprocess.run([str(exe)], cwd=str(tb), capture_output=True, text=True, check=False)
    log = r.stdout + r.stderr
    (out / f"{name}.run.log").write_text(log)
    fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    named = [f for f in fails if "pdu#" not in f]
    verdict = "CAUGHT" if (r.returncode != 0 and fails) else "SURVIVED"
    summary = f"{name}: {verdict} rc={r.returncode} fails={len(fails)} named={len(named)}"
    for f in named[:12]:
        summary += "\n    " + f
    return summary


def main() -> int:
    head, work, out = (Path(a).resolve() for a in sys.argv[1:4])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    out.mkdir(parents=True, exist_ok=True)
    tasks = [("aaf",) + t for t in AAF] + [("crf",) + t for t in CRF]
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = [ex.submit(one, k, n, p, r, head, work, out) for (k, n, p, r) in tasks]
        res = [f.result() for f in futs]
    text = "\n".join(res) + "\n"
    (out / "SUMMARY.txt").write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
