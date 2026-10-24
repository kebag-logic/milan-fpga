#!/usr/bin/env python3
"""Reviewer probe: does any avtp_rxmon leg catch an off-format PDU that advances
lock acquisition (sets media_locked, or steps the settle count) on the AAF input?

usage: python3 -I probe_lock_settle.py <head-tree> <work-dir> <out-dir>

Each mutant is planted in COPIES of the engine (and, in the "both" arm, of the
lockstep reference too, the way a real defect written into both would be),
then the NX harness and the lockstep N=1 / N=8 legs are built through the
head's own Makefile recipes with private Mdirs and run. No tracked file is
edited.
"""
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

ENG_ANCHOR = "            monst_r <= {ram_q_r[31:8], cur_w.seq};"
REF_ANCHOR = "            monst_r <= {ram_q_r[31:8], cur_r.seq};"
MUTANTS = {
    "lock_set": ("{ram_q_r[31:13], 1'b1, ram_q_r[11:8], %s.seq};"),
    "settle_dec": ("{ram_q_r[31:12], (ram_q_r[11:8] == 4'd0) ? 4'd0 : "
                   "(ram_q_r[11:8] - 4'd1), %s.seq};"),
}


def plant(text: str, anchor: str, rep: str) -> str:
    if text.count(anchor) != 1:
        raise SystemExit(f"anchor count {text.count(anchor)} != 1")
    return text.replace(anchor, rep)


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return r.returncode, r.stdout + r.stderr


def variant(name: str, arm: str, head: Path, work: Path, out: Path) -> str:
    tb = head / "tb/verilator/avtp_rxmon"
    d = work / f"{name}_{arm}"
    d.mkdir(parents=True, exist_ok=True)
    eng = (head / "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv").read_text()
    ref = (tb / "reference/KL_avtp_rx_monitor_ctx_ref.sv").read_text()
    m = MUTANTS[name]
    eng_m = d / "KL_avtp_rx_monitor_ctx.sv"
    ref_m = d / "KL_avtp_rx_monitor_ctx_ref.sv"
    eng_m.write_text(plant(eng, ENG_ANCHOR, "            monst_r <= " + m % "cur_w"))
    ref_m.write_text(plant(ref, REF_ANCHOR, "            monst_r <= " + m % "cur_r")
                     if arm == "both" else ref)
    lines = [f"{name} [{arm}]"]
    rc, log = run(["make", "-s", "-C", str(tb), "nx-build", f"RXMON_SRC={eng_m}",
                   f"NX_MDIR={d}/nx"])
    (out / f"{name}_{arm}.nx.build.log").write_text(log[-6000:])
    rc, log = run([str(d / "nx" / "Vavtp_rxmon_nx_sim")], cwd=str(tb))
    (out / f"{name}_{arm}.nx.run.log").write_text(log)
    lines.append(f"  nx rc={rc} " + (log.strip().splitlines()[-2] if log.strip() else ""))
    lines += ["    " + ln.strip() for ln in log.splitlines() if "[FAIL]" in ln][:8]
    rc, log = run(["make", "-s", "-C", str(tb), "lockstep-build", f"RXMON_SRC={eng_m}",
                   f"REF_SRC={ref_m}", f"LS_MDIR={d}/ls"])
    (out / f"{name}_{arm}.ls.build.log").write_text(log[-6000:])
    for n in ("1", "8"):
        rc, log = run([str(d / f"ls{n}" / "Vavtp_rxmon_lockstep")], cwd=str(tb))
        (out / f"{name}_{arm}.ls{n}.run.log").write_text(log)
        tail = log.strip().splitlines()[-2:] if log.strip() else ["<no output>"]
        lines.append(f"  lockstep N={n} rc={rc} " + " | ".join(tail))
        lines += ["    " + ln.strip() for ln in log.splitlines() if "[FAIL]" in ln][:4]
    return "\n".join(lines)


def main() -> int:
    head, work, out = (Path(a).resolve() for a in sys.argv[1:4])
    out.mkdir(parents=True, exist_ok=True)
    jobs = [(n, a) for n in MUTANTS for a in ("engine", "both")]
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        res = list(ex.map(lambda t: variant(t[0], t[1], head, work, out), jobs))
    text = "\n".join(res) + "\n"
    (out / "SUMMARY.txt").write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
