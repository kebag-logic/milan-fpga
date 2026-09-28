#!/usr/bin/env python3
"""R394-2 reviewer-owned mutants against the #617 round-2 guard.

Plants one defect at a time in a COPY of the file named, builds the named
harness through its suite's own Makefile recipe (WRAP_SRC / CMAP_SRC / MDIR
overrides, exactly as the committed mutants.py does) and runs it. Nothing in
the tree is written; builds land under <workdir>.

  python3 r394_mutants2.py <checkout-root> <workdir> [--jobs N]

Each result line: mutant, harness run, rc, tally, and the [FAIL] lines.
"""

import argparse
import concurrent.futures as cf
import re
import subprocess
import sys
from pathlib import Path

WRAP = "tb/verilator/capture_coherence/coherence_wrap.sv"
XBAR = "hdl/ieee1722/aaf/KL_chan_map_capture.sv"
CC = "tb/verilator/capture_coherence"
CH = "tb/verilator/chmap_capture"

# (tag, description, file, edits, [(suite, make-target, src-var, exe, args)])
MUTANTS = [
    ("RM5", "keep-off halved to 128 cycles (still above nothing the true plan needs, below the 200-cycle "
            "proportional equilibrium a 50 ppm source forces on a pulled engagement)",
     WRAP, [("    .LOCK_KEEPOFF_CYC_P (256)", "    .LOCK_KEEPOFF_CYC_P (128)")],
     [(CC, "build", "WRAP_SRC", "Vcoherence_sim", ()),          # the committed full suite
      (CC, "build", "WRAP_SRC", "Vcoherence_sim", ("--band",))]),  # the committed arm's band leg
    ("RM6", "lock-target split one cycle late: the aligner sees the tick two cycles late",
     WRAP, [("  end : align_tick_delay",
             "  end : align_tick_delay\n  logic tick_q2_r;\n  always_ff @(posedge clk) begin : r394_delay2\n"
             "    if (!rst_n) tick_q2_r <= 1'b0;\n    else        tick_q2_r <= tick_q_r;\n  end : r394_delay2"),
            ("    .tick_i (tick_q_r),", "    .tick_i (tick_q2_r),")],
     [(CC, "build", "WRAP_SRC", "Vcoherence_sim", ("--band",))]),
    ("RM7", "a tick queued behind a running walk snapshots nothing (the late-snapshot path removed)",
     XBAR, [("  wire tdm_snap_w = (st_r == CM_IDLE_S) && (tick_pend_r ? tick_late_r : tick_i);",
             "  wire tdm_snap_w = (st_r == CM_IDLE_S) && !tick_pend_r && tick_i;")],
     [(CC, "build", "CMAP_SRC", "Vcoherence_sim", ("--quick",)),
      (CH, "build", "CMAP_SRC", "Vchmap_wrap", ())]),
    ("RM8", "a queued tick snapshots at the tick instant anyway (tick_late_r ignored: the walk bank reloads "
            "while the walk the tick queued behind is still reading it)",
     XBAR, [("  wire tdm_snap_w = (st_r == CM_IDLE_S) && (tick_pend_r ? tick_late_r : tick_i);",
             "  wire tdm_snap_w = tick_i;")],
     [(CC, "build", "CMAP_SRC", "Vcoherence_sim", ("--quick",)),
      (CH, "build", "CMAP_SRC", "Vchmap_wrap", ())]),
    ("RB1", "reference, not a mutant of the guard's parts: the whole round-1 aligner binding (slot-0 marker, the "
            "tick itself, the default keep-off), to count the band the guard removes",
     WRAP, [("    .FS_HZ_P            (FS_HZ_C),\n    .LOCK_KEEPOFF_CYC_P (256)", "    .FS_HZ_P            (FS_HZ_C)"),
            ("    .tick_i (tick_q_r),", "    .tick_i (tick_w),"),
            ("    .frame_ev_i (cap_pv_w && (32'(cap_slot_w) == TDM_SLOTS_P / 2 - 1)),",
             "    .frame_ev_i (cap_pv_w && (cap_slot_w == 4'd0)),")],
     [(CC, "build", "WRAP_SRC", "Vcoherence_sim", ("--band",))]),
]


def job(root: Path, work: Path, tag: str, fname: str, edits, run) -> str:
    src = (root / fname).read_text()
    for pat, rep in edits:
        if src.count(pat) != 1:
            return f"{tag}: PATTERN count {src.count(pat)} for {pat!r}"
        src = src.replace(pat, rep)
    suite, target, var, exe_name, args = run
    d = work / f"{tag}_{Path(suite).name}_{'_'.join(a.strip('-') for a in args) or 'full'}"
    d.mkdir(parents=True, exist_ok=True)
    mf = d / Path(fname).name
    mf.write_text(src)
    mdir = d / "obj"
    b = subprocess.run(["make", "-s", "-C", str(root / suite), target, f"{var}={mf}", f"MDIR={mdir}"],
                       capture_output=True, text=True, check=False)
    (d / "build.log").write_text(b.stdout + b.stderr)
    exe = mdir / exe_name
    if b.returncode != 0 or not exe.is_file():
        return f"{tag} [{suite} {' '.join(args)}]: DID NOT BUILD (see {d}/build.log)"
    r = subprocess.run([str(exe), *args], cwd=root / suite, capture_output=True, text=True, check=False)
    (d / "run.log").write_text(r.stdout + r.stderr)
    tally = re.findall(r"checks: \d+\s+failures: \d+|\d+ checks, \d+ failures|FAIL: \d+", r.stdout)
    fails = [ln.strip() for ln in r.stdout.splitlines() if "[FAIL]" in ln or " FAIL " in ln]
    head = f"{tag} [{suite} {' '.join(args) or '(full)'}]: rc={r.returncode} {tally[-1] if tally else ''}"
    return head + "".join(f"\n     {f}" for f in fails[:25]) + (f"\n     ... {len(fails)} FAIL lines" if len(fails) > 25 else "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("work")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    root, work = Path(a.root).resolve(), Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    jobs = [(t, f, e, r) for t, _d, f, e, runs in MUTANTS for r in runs if not a.only or t in a.only.split(",")]
    for t, dsc, *_ in MUTANTS:
        print(f"{t}: {dsc}")
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        for res in ex.map(lambda j: job(root, work, *j), jobs):
            print(res, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
