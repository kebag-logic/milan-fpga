#!/usr/bin/env python3
"""R394-1 reviewer-owned mutants for tb/verilator/capture_coherence (#617).

Plants one defect at a time in a COPY of hdl/ieee1722/aaf/KL_chan_map_capture.sv,
builds the suite's junction harness through its own Makefile recipe
(CMAP_SRC / MDIR overrides, as the committed mutants.py does) and runs it.
The tree is never edited. Usage:

  python3 r394_mutants.py <suite-dir> <workdir> [--full] [--jobs N]

<suite-dir> is a checkout's tb/verilator/capture_coherence. --full runs the
harness without --quick (adds the true plan's whole beat). Exit 0 when every
mutant fails its harness with at least one [FAIL] line; each result is printed.
"""

import argparse
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ("RM1 snapshot one cycle late (first STEP cycle, slot 0 reads the old walk bank)",
     [("wire tdm_snap_w = (st_r == CM_POP_S) && (32'(pop_idx_r) == LB_PAIRS_C);",
       "wire tdm_snap_w = (st_r == CM_STEP_S) && (slot_r == '0);")]),
    ("RM2 closing pair published from the stale stage (pair 3 one frame behind)",
     [("          tdm_frame_r[t] <= (t == int'(TDM_FRAME_PAIRS_P) - 1) ? tdm_pair_w\n"
       "                                                               : tdm_stage_r[t];",
       "          tdm_frame_r[t] <= tdm_stage_r[t];")]),
    ("RM3 walk bank also takes a whole new frame when one closes mid-walk",
     [("    else if (tdm_snap_w) begin\n"
       "      for (int t = 0; t < N_TDM_PAIRS_C; t++) tdm_walk_r[t] <= tdm_frame_r[t];",
       "    else if (tdm_snap_w || tdm_close_w) begin\n"
       "      for (int t = 0; t < N_TDM_PAIRS_C; t++) tdm_walk_r[t] <= !tdm_close_w ? tdm_frame_r[t]"
       " : (t == int'(TDM_FRAME_PAIRS_P) - 1) ? tdm_pair_w : tdm_stage_r[t];")]),
    ("RM4 close coinciding with the snapshot cycle hands the walk the half-built stage",
     [("      for (int t = 0; t < N_TDM_PAIRS_C; t++) tdm_walk_r[t] <= tdm_frame_r[t];",
       "      for (int t = 0; t < N_TDM_PAIRS_C; t++) tdm_walk_r[t] <= tdm_close_w ? tdm_stage_r[t] : tdm_frame_r[t];")]),
]


def run_one(suite: Path, work: Path, name: str, edits, full: bool) -> tuple[str, str, str]:
    src = (suite / "../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv").resolve().read_text()
    for pat, rep in edits:
        if src.count(pat) != 1:
            return name, "PATTERN", f"pattern count {src.count(pat)}"
        src = src.replace(pat, rep)
    tag = name.split()[0]
    d = work / tag
    d.mkdir(parents=True, exist_ok=True)
    rtl = d / "KL_chan_map_capture.sv"
    rtl.write_text(src)
    mdir = d / "obj"
    b = subprocess.run(["make", "-s", "-C", str(suite), "build", f"CMAP_SRC={rtl}", f"MDIR={mdir}"],
                       capture_output=True, text=True, check=False)
    (d / "build.log").write_text(b.stdout + b.stderr)
    exe = mdir / "Vcoherence_sim"
    if b.returncode != 0 or not exe.is_file():
        return name, "NOBUILD", ""
    args = [str(exe)] + ([] if full else ["--quick"])
    r = subprocess.run(args, cwd=suite, capture_output=True, text=True, check=False)
    (d / "run.log").write_text(r.stdout + r.stderr)
    fails = [ln.strip() for ln in r.stdout.splitlines() if ln.strip().startswith("[FAIL]")]
    tally = [ln for ln in r.stdout.splitlines() if "checks:" in ln]
    verdict = "KILLED" if (r.returncode != 0 and fails) else ("SURVIVED" if r.returncode == 0 else f"rc={r.returncode}")
    return name, verdict, (tally[-1] if tally else "") + "\n    " + "\n    ".join(fails[:12])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("suite", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    sel = [m for m in MUTANTS if not a.only or m[0].split()[0] in a.only.split(",")]
    bad = 0
    with cf.ThreadPoolExecutor(max_workers=min(a.jobs, 8)) as ex:
        futs = [ex.submit(run_one, a.suite.resolve(), a.work.resolve(), n, e, a.full) for n, e in sel]
        for f in futs:
            name, verdict, detail = f.result()
            print(f"[{verdict}] {name}\n    {detail}")
            bad += verdict != "KILLED"
    print(f"\n{len(sel)} mutants, {len(sel) - bad} killed, {bad} not killed ({'full' if a.full else 'quick'})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
