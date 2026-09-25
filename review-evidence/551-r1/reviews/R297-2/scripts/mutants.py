#!/usr/bin/env python3
"""Reviewer mutation driver for the obj_crflic leg (parallel, disposable).

Runs the shipped crflic_mutants.MUTATIONS table plus reviewer-added arms,
each against the same Makefile recipe (crflic-build, DP_SRC/CRFLIC_MDIR
overridden), and grades each with the shipped verdict() so a crash or a
wrong-check failure is not counted as a catch.

usage: mutants.py <clone> <packet> [workers]
env:   VERILATOR (pinned wrapper), VERILATOR_JOBS (per build)
"""
import concurrent.futures as cf
import json
import os
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
packet = Path(sys.argv[2]).resolve()
workers = int(sys.argv[3]) if len(sys.argv) > 3 else 6
here = clone / "tb/verilator/milan_dp"
sys.path.insert(0, str(here))
import crflic_mutants as cm  # noqa: E402

GATE = ("  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] &\n"
        "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];")
EXTRA = [
    ("reviewer: gate is ACTIVE OR grant",
     GATE,
     "  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0] |\n"
     "                             pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];",
     "the CRF licence never opened (every cycle sampled)"),
    ("reviewer: AAF sources above 0 drop the real grant (no such source in AX1x1)",
     "           (acmp_talker_active_aaf_w[gs] & lwsrp_stream_gate[gs]));",
     "           (acmp_talker_active_aaf_w[gs] & pp_cd_srp_active_w[gs]));",
     None),
]

src = cm.DP_RTL.read_text()
work = packet / "scratch/mutants"
work.mkdir(parents=True, exist_ok=True)
rec = packet / "receipts/mutants"
rec.mkdir(parents=True, exist_ok=True)


def one(idx_mut):
    idx, (name, pattern, repl, breaks) = idx_mut
    tag = f"m{idx:02d}"
    n = src.count(pattern)
    if n != 1:
        return {"id": tag, "name": name, "result": f"pattern count {n}"}
    mpath = work / f"milan_datapath_{tag}.sv"
    mpath.write_text(src.replace(pattern, repl))
    mdir = work / f"obj_{tag}"
    b = subprocess.run(["make", "-s", "-C", str(here), "crflic-build",
                        f"DP_SRC={mpath}", f"CRFLIC_MDIR={mdir}",
                        f"VERILATOR={os.environ['VERILATOR']}",
                        f"VERILATOR_JOBS={os.environ.get('VERILATOR_JOBS', '1')}"],
                       capture_output=True, text=True, check=False)
    (rec / f"{tag}.build.log").write_text(b.stdout + b.stderr)
    exe = mdir / cm.EXE_NAME
    if b.returncode or not exe.is_file():
        return {"id": tag, "name": name, "result": "did not build"}
    rc, out = cm.run_leg(exe)
    (rec / f"{tag}.run.log").write_text(out)
    fails = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]
    return {"id": tag, "name": name, "must_fail": breaks, "rc": rc,
            "verdict": cm.verdict(rc, out, breaks), "n_fail": len(fails),
            "fails": fails[:40], "tally": out.strip().splitlines()[-2:]}


muts = list(enumerate(cm.MUTATIONS + EXTRA, 1))
only = os.environ.get("ONLY")
if only:
    keep = {int(x) for x in only.split(",")}
    muts = [m for m in muts if m[0] in keep]
with cf.ThreadPoolExecutor(max_workers=workers) as ex:
    res = list(ex.map(one, muts))
for r in res:
    (rec / f"{r['id']}.json").write_text(json.dumps(r, indent=1))
for r in res:
    print(r["id"], "|", r["name"], "|", r.get("verdict", r.get("result")), "|",
          r.get("n_fail"), "|", r.get("tally"))
