#!/usr/bin/env python3
"""Reviewer probes for the #584 8x8 render leg: plant one DUT fault per copy, build through the suite's
own `make ship8-build` recipe, run the leg, and report which named checks failed.

usage: python3 -I reviewer_probes.py REPO WORKDIR [--jobs N] [--fresh]
(--fresh runs the two freshness-gate plants instead of the first three)
Requires `make ship8-build` to have produced ship8_aemi.bin in the suite directory. Tracked sources are
never edited; each planted copy lives under WORKDIR.
"""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

PROBES_ALL = [
    # (tag, source relpath, make variable, pattern, replacement)
    ("zerofill_copies_slot0", "hdl/ieee1722/aaf/KL_tdm_render_master.sv", "TDMRM_SRC",
     "                     : 24'd0;", "                     : frame_sel_w[0 +: 24];"),
    ("epoch_unqualified", "hdl/milan/milan_datapath.sv", "DP_SRC",
     "  wire tdmr_epoch_evt_w = |(strtbl_bind_fall_w & tdmr_lane_streams_w);",
     "  wire tdmr_epoch_evt_w = |strtbl_bind_fall_w;"),
    ("remove_as_add", "hdl/milan/milan_datapath.sv", "DP_SRC",
     "assign pp_amap_edit_remove_w = amr_own_r ? amr_ed_remove_r : ppo_amap_edit_remove_w;",
     "assign pp_amap_edit_remove_w = 1'b0;"),
]


PROBES_FRESH = [
    ("freshness_gate_open", "hdl/milan/milan_datapath.sv", "DP_SRC",
     "  wire tdmr_fresh_w = &(tdmr_fresh_r | ~tdmr_lane_streams_w);",
     "  wire tdmr_fresh_w = 1'b1;"),
    ("freshness_not_cleared_on_fall", "hdl/milan/milan_datapath.sv", "DP_SRC",
     "        if (strtbl_bind_fall_w[s])  tdmr_fresh_r[s] <= 1'b0;\n        else if (rq_pop_p_w[s])",
     "        if (rq_pop_p_w[s])"),
]
PROBES = PROBES_ALL


def run(repo: Path, work: Path, probe) -> str:
    tag, rel, var, pat, rep = probe
    text = (repo / rel).read_text()
    if text.count(pat) != 1:
        return f"{tag}: PATTERN COUNT {text.count(pat)}"
    copy = work / f"{tag}_{Path(rel).name}"
    copy.write_text(text.replace(pat, rep))
    suite = repo / "tb/verilator/milan_dp_render"
    mdir = work / f"obj_{tag}"
    b = subprocess.run(["make", "--no-print-directory", "-s", "-C", str(suite), "ship8-build",
                        f"SHIP8_MDIR={mdir}", f"{var}={copy}"], capture_output=True, text=True)
    (work / f"{tag}.build.log").write_text(b.stdout + b.stderr)
    exe = mdir / "Vmilan_dp_ship8"
    if b.returncode != 0 or not exe.is_file():
        return f"{tag}: BUILD FAILED rc={b.returncode}"
    r = subprocess.run([str(exe)], cwd=str(suite), capture_output=True, text=True)
    out = r.stdout + r.stderr
    (work / f"{tag}.run.log").write_text(out)
    fails = [ln.strip() for ln in out.splitlines() if "[FAIL]" in ln]
    summary = [ln.strip() for ln in out.splitlines() if "checks:" in ln]
    return f"{tag}: rc={r.returncode} {summary[-1] if summary else 'NO VERDICT'}\n  " + "\n  ".join(fails[:12])


def main() -> int:
    repo, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[3] == "--jobs" else 3
    global PROBES
    if "--fresh" in sys.argv:
        PROBES = PROBES_FRESH
    work.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for line in pool.map(lambda p: run(repo, work, p), PROBES):
            print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
