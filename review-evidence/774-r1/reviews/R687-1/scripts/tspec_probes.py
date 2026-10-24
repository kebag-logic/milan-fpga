#!/usr/bin/env python3
"""Reviewer fault probes for the #774 per-source TSpec MaxFrameSize.

Each probe plants one textual mutation in a COPY of milan_datapath.sv
(DP_SRC) or KL_pp_shadow.sv (SHADOW_SRC), builds the named milan_dp leg
through the suite's own recipe into a scratch objdir, runs it, and grades:
  expect "catch":   the leg must report RESULT: FAIL and the named check must
                    be among the [FAIL] lines;
  expect "survive": the leg is expected to pass (an equivalence the shape
                    cannot observe); recorded, not a pass/fail of the leg.
The tracked sources are never written.

usage: python3 tspec_probes.py <repo> <scratch-dir> <verilator> [--jobs N]
"""
import argparse
import concurrent.futures as cf
import re
import subprocess
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("scratch")
ap.add_argument("verilator")
ap.add_argument("--jobs", type=int, default=8)
args = ap.parse_args()
repo = Path(args.repo).resolve()
work = Path(args.scratch).resolve()
work.mkdir(parents=True, exist_ok=True)
tb = repo / "tb/verilator/milan_dp"
FILES = {"dp": ("DP_SRC", repo / "hdl/milan/milan_datapath.sv"),
         "shadow": ("SHADOW_SRC", repo / "hdl/milan/KL_pp_shadow.sv")}
LEGS = {"crflic": ("crflic-build", "CRFLIC_MDIR", "Vmilan_dp_crflic"),
        "tspec8": ("tspec8-build", "TSPEC8_MDIR", "Vmilan_dp_tspec8")}
CRF = "CRF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 28 + 1"
AAF = "AAF TSpec MaxFrameSize is Milan v1.2 Table 4.4's 24*N + 24 + 1"

#: (tag, file, pattern, replacement, expect, the check that must fail)
PROBES = [
    ("talker0_every_slot", "dp", "      .cfg_tspec_max_frame_i (pp_src_maxf_w),",
     "      .cfg_tspec_max_frame_i ({ACMP_SRC_C{tctx_maxf_w[0]}}),", "catch", CRF),
    ("crf_drops_table_octet", "dp", "assign pp_src_maxf_w[16*gmf +: 16] = crft_maxf_w;",
     "assign pp_src_maxf_w[16*gmf +: 16] = crft_maxf_w - 16'd1;", "catch", CRF),
    ("crf_padded_msdu_42", "dp", "assign pp_src_maxf_w[16*gmf +: 16] = crft_maxf_w;",
     "assign pp_src_maxf_w[16*gmf +: 16] = 16'd42;", "catch", CRF),
    ("aaf_drops_table_octet", "dp", "assign pp_src_maxf_w[16*gmf +: 16] = tctx_maxf_w[gmf];",
     "assign pp_src_maxf_w[16*gmf +: 16] = tctx_maxf_w[gmf] - 16'd1;", "catch", AAF),
    ("aaf_slots_read_talker0", "dp", "assign pp_src_maxf_w[16*gmf +: 16] = tctx_maxf_w[gmf];",
     "assign pp_src_maxf_w[16*gmf +: 16] = tctx_maxf_w[0];", "survive", None),
    ("shadow_slot0_every_slot", "shadow", ".cfg_tspec_max_frame_i(cfg_tspec_max_frame_i),",
     ".cfg_tspec_max_frame_i({N_STREAM_OUT_P{cfg_tspec_max_frame_i[15:0]}}),", "catch", CRF),
]


def one(probe, leg):
    tag, kind, pat, rep, expect, must = probe
    var, src = FILES[kind]
    text = src.read_text()
    n = text.count(pat)
    if n != 1:
        return f"[ERROR] {tag}@{leg}: pattern appears {n} times"
    mfile = work / f"{tag}_{src.name}"
    mfile.write_text(text.replace(pat, rep))
    target, mvar, exe = LEGS[leg]
    mdir = work / f"obj_{tag}_{leg}"
    log = work / f"{tag}_{leg}.log"
    b = subprocess.run(["make", "-s", "-C", str(tb), target, f"{var}={mfile}", f"{mvar}={mdir}",
                        f"VERILATOR={args.verilator}", "VERILATOR_JOBS=2"],
                       capture_output=True, text=True, check=False)
    if b.returncode != 0 or not (mdir / exe).is_file():
        log.write_text(b.stdout[-4000:] + b.stderr[-4000:])
        return f"[ERROR] {tag}@{leg}: build failed rc={b.returncode}"
    r = subprocess.run([str(mdir / exe)], cwd=tb, capture_output=True, text=True, check=False,
                       timeout=3000)
    log.write_text(r.stdout + r.stderr)
    out = r.stdout
    tally = re.search(r"checks: (\d+)\s+failures: (\d+)", out)
    tally_s = f"checks {tally.group(1)} failures {tally.group(2)}" if tally else "no tally"
    fails = [ln.strip() for ln in out.splitlines() if ln.lstrip().startswith("[FAIL]")]
    failed = r.returncode != 0 and "RESULT: FAIL" in out
    if expect == "catch":
        hit = failed and any(must in ln for ln in fails)
        verdict = "CAUGHT" if hit else "NOT CAUGHT"
    else:
        verdict = "SURVIVED (as expected)" if (r.returncode == 0 and "RESULT: PASS" in out) \
            else "FAILED (unexpected)"
    first = "; ".join(fails[:3])
    return f"[{verdict}] {tag}@{leg}: rc={r.returncode} {tally_s}; first fails: {first or '-'}"


jobs = [(p, leg) for p in PROBES for leg in LEGS]
with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
    for line in ex.map(lambda a: one(*a), jobs):
        print(line, flush=True)
