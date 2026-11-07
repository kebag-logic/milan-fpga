#!/usr/bin/env python3
"""Reviewer arms beyond the planted set. Each arm rewrites one expression of a
scratch copy of the exact head; the suite then says whether any check fails.
Usage: 02_extra_arms.py <exported-head> <work-dir> <receipt-dir> <suite> [arm ...]"""
import shutil, subprocess, sys, concurrent.futures as cf
from pathlib import Path
head, work, rec, suite = map(Path, sys.argv[1:5]); suite = str(suite)
only = sys.argv[5:]
F = "hdl/srp/KL_srp_encoder.sv"
ARMS = {
 "x-start-collect-term-dropped": ("                     ? (start0_w || ((st_r == E_COLLECT) && go0_w)\n                        || ((st_r == E_IDLE) && la_prepare_i)) : start1_w;",
                                  "                     ? (start0_w || ((st_r == E_IDLE) && la_prepare_i)) : start1_w;"),
 "x-start-laprepare-term-dropped": ("                     ? (start0_w || ((st_r == E_COLLECT) && go0_w)\n                        || ((st_r == E_IDLE) && la_prepare_i)) : start1_w;",
                                  "                     ? (start0_w || ((st_r == E_COLLECT) && go0_w)) : start1_w;"),
 "x-start0-term-dropped": ("                     ? (start0_w || ((st_r == E_COLLECT) && go0_w)\n", "                     ? (((st_r == E_COLLECT) && go0_w)\n"),
 "x-start1-term-dropped": ("|| ((st_r == E_IDLE) && la_prepare_i)) : start1_w;", "|| ((st_r == E_IDLE) && la_prepare_i)) : 1'b0;"),
 "x-busy-not-in-alloc": ("assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT)\n", "assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT) && (st_r != E_ALLOC)\n"),
 "x-identity-top-octet-low7-dropped": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, v[271], 7'd0, v[263:208]};"),
 "x-identity-octet3-bit0-dropped": ("return {APP_MSRP_C, t, v[271:208]};", "return {APP_MSRP_C, t, v[271:241], 1'b0, v[239:208]};"),
}
def one(name):
    old, new = ARMS[name]
    t = work / name
    shutil.rmtree(t, ignore_errors=True); t.mkdir(parents=True)
    shutil.copytree(head / "hdl", t / "hdl")
    (t / "tb").mkdir()
    for s in ("common", suite):
        shutil.copytree(head / "tb" / s, t / "tb" / s, ignore=shutil.ignore_patterns("obj_*"))
    p = t / F; src = p.read_text()
    assert src.count(old) == 1, name
    p.write_text(src.replace(old, new))
    log = rec / f"{name}.{suite}.log"
    target = ["make", "-C", str(t / "tb" / suite)] + (["run"] if suite == "srp_encoder" else [])
    with log.open("w") as f:
        rc = subprocess.run(target, stdout=f, stderr=subprocess.STDOUT).returncode
    txt = log.read_text(errors="replace")
    tally = [l for l in txt.splitlines() if " checks: " in l]
    fails = [l for l in txt.splitlines() if l.startswith("FAIL:")]
    return name, rc, (tally[-1] if tally else "no tally"), fails[:4]
names = only or list(ARMS)
with cf.ThreadPoolExecutor(8) as ex:
    for name, rc, tally, fails in ex.map(one, names):
        print(f"{name}: suite={suite} rc={rc} {tally}")
        for f in fails: print("   ", f[:140])
