#!/usr/bin/env python3
"""Reviewer probe: which reject write-back defects does the N=4 [SQ] harness
catch when each is planted in the engine AND the lockstep reference together?

usage: python3 -I probe_sq_claims.py <head-tree> <out-dir> [jobs]

Each mutant replaces the reject's MON_STATE write-back line in a COPY of the
engine and of the reference. The NX harness is built through the tree's own
`nx-build` recipe (RXMON_SRC, NX_MDIR) and the lockstep legs through
`lockstep-build` (RXMON_SRC, REF_SRC, LS_MDIR), each with a private Mdir.
No file of <head-tree> is edited.

MON_STATE: prev_seq[7:0] settle[11:8] media_locked[12] bound_q[13]
wire_chans[21:14] prev_mr[22] mr_seeded[23].
"""
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

ENG_ANCHOR = "            monst_r <= {ram_q_r[31:8], cur_w.seq};"
REF_ANCHOR = "            monst_r <= {ram_q_r[31:8], cur_r.seq};"
# name -> replacement body with %s for the bundle (cur_w / cur_r)
MUTANTS = {
    "settle_restart": "{ram_q_r[31:12], 4'd8, %s.seq};",
    "lock_clear": "{ram_q_r[31:13], 1'b0, ram_q_r[11:8], %s.seq};",
    "mr_seed_clear": "{ram_q_r[31:24], 1'b0, ram_q_r[22:8], %s.seq};",
    "mr_seed_set": "{ram_q_r[31:24], 1'b1, ram_q_r[22:8], %s.seq};",
    "mr_prev_from_reject": "{ram_q_r[31:23], %s.mr, ram_q_r[21:8], %s.seq};",
    "mr_seed_and_ref_from_reject": "{ram_q_r[31:24], 1'b1, %s.mr, ram_q_r[21:8], %s.seq};",
}


def plant(text: str, anchor: str, body: str, bundle: str) -> str:
    if text.count(anchor) != 1:
        raise SystemExit(f"anchor count {text.count(anchor)} != 1")
    rep = "            monst_r <= " + body.replace("%s", bundle)
    return text.replace(anchor, rep)


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return p.returncode, p.stdout + p.stderr


def variant(name: str, head: Path, out: Path) -> str:
    tb = head / "tb/verilator/avtp_rxmon"
    eng = (head / "hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv").read_text()
    ref = (tb / "reference/KL_avtp_rx_monitor_ctx_ref.sv").read_text()
    d = out / "work" / name
    d.mkdir(parents=True, exist_ok=True)
    e_p, r_p = d / "KL_avtp_rx_monitor_ctx.sv", d / "KL_avtp_rx_monitor_ctx_ref.sv"
    e_p.write_text(plant(eng, ENG_ANCHOR, MUTANTS[name], "cur_w"))
    r_p.write_text(plant(ref, REF_ANCHOR, MUTANTS[name], "cur_r"))
    lines = [f"{name} [engine+reference]: " + MUTANTS[name].replace("%s", "cur")]
    rc, log = run(["make", "-s", "-C", str(tb), "nx-build", f"RXMON_SRC={e_p}",
                   f"NX_MDIR={d / 'nx'}"])
    (out / f"{name}.nx.build.log").write_text(log[-6000:])
    if rc != 0:
        return "\n".join(lines + [f"  nx BUILD FAILED rc={rc}"])
    rc, log = run([str(d / "nx" / "Vavtp_rxmon_nx_sim")], cwd=str(tb))
    (out / f"{name}.nx.run.log").write_text(log)
    tail = [ln for ln in log.splitlines() if "checks," in ln][-1:] or ["<no summary>"]
    lines.append(f"  nx rc={rc} " + " | ".join(tail))
    lines += ["    " + ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
    rc, log = run(["make", "-s", "-C", str(tb), "lockstep-build", f"RXMON_SRC={e_p}",
                   f"REF_SRC={r_p}", f"LS_MDIR={d / 'ls'}"])
    (out / f"{name}.ls.build.log").write_text(log[-6000:])
    if rc != 0:
        return "\n".join(lines + [f"  lockstep BUILD FAILED rc={rc}"])
    for n in ("1", "8"):
        rc, log = run([str(d / f"ls{n}" / "Vavtp_rxmon_lockstep")], cwd=str(tb))
        (out / f"{name}.ls{n}.run.log").write_text(log)
        tail = log.strip().splitlines()[-1:] if log.strip() else ["<no output>"]
        lines.append(f"  lockstep N={n} rc={rc} " + " | ".join(tail))
    return "\n".join(lines)


def main() -> int:
    head, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    out.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        res = list(ex.map(lambda n: variant(n, head, out), MUTANTS))
    text = "\n".join(res) + "\n"
    (out / "SUMMARY.txt").write_text(text)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
