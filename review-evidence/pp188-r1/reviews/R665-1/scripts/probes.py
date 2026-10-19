#!/usr/bin/env python3
"""Reviewer fault probes for processor PR #195 (issues #188, #189).

Usage: probes.py HEAD_TREE OUT_DIR [--jobs N] [--only NAME ...]

Each probe is one or more exact edits (each old text must occur exactly once)
planted in a private copy of hdl/ and tb/ under OUT_DIR/work/<probe>, then the
named suite is built and run with the pinned Verilator. A probe is KILLED when
the run completes with its tally line and exits non-zero; SURVIVED when it exits
0 with the tally; anything else (refused edit, no tally) is INCONCLUSIVE.
HEAD_TREE is never modified.
"""
import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

L = "hdl/srp/KL_srp_listener_fsm.sv"
A = "hdl/acmp/KL_pp_acmp_listener.sv"
FSMS = ("tb/srp_stream_fsms", ["make"])        # walk arms at four shapes, then the suite
ACMPL = ("tb/acmp_listener", ["make", "run"])

PROBES = {
    # goldens: unmodified copies, must pass (verdict SURVIVED = rc 0 with tally)
    "G0-golden-fsms": (FSMS, []),
    "G0-golden-acmp_listener": (ACMPL, []),
    # #188: an applicant in LO (an Empty owed) is not parked
    "U1-lo-not-owed": (FSMS, [(L, "set_owes_w = set_lv_w inside {A_LA_C, A_LO_C};",
                               "set_owes_w = (set_lv_w == A_LA_C);")]),
    # #188: a txLA! walk retires the park although the applicant stays LO
    "U2-park-retires-on-txla": (FSMS, [(L, "          if (walk_grant_w && lvp_r[wsrc_r]\n"
                                           "              && !(wnext_w inside {A_LA_C, A_LO_C})) begin\n",
                                        "          if (walk_grant_w && lvp_r[wsrc_r]) begin\n")]),
    # #188: received Listener values are applied to a parked sink
    "U3-parked-applies-rx": (FSMS, [(L, "                     && !lvp_r[s]   // neither stream's values while parked\n", "")]),
    # #188: the owed Lv carries FourPacked 0 instead of the declared parameter
    "U4-owed-fourpack-cleared": (FSMS, [(L, "if (!set_owes_w) fourpack_r[ctl_sink_i] <= 2'd0;",
                                         "fourpack_r[ctl_sink_i] <= 2'd0;")]),
    # #188: a settle while parked compares and parks the matcher's stream_id,
    # not the one the applicant holds (both elaboration arms)
    "U5-csid-ignores-park": (FSMS, [
        (L, "    assign csid_w = lvp_r[ctl_sink_i] ? lsid_r[ctl_sink_i]\n"
            "                                      : wsid_r[ctl_sink_i];\n",
         "    assign csid_w = wsid_r[ctl_sink_i];\n"),
        (L, "    assign csid_w = lvp_r[ctl_sink_i] ? lsid_r[ctl_sink_i]\n"
            "                                      : sid_r[ctl_sink_i];\n",
         "    assign csid_w = sid_r[ctl_sink_i];\n")]),
    # #188: the retire keeps the old FourPacked (candidate equivalent)
    "U6-retire-keeps-fourpack": (FSMS, [(L, "            lvp_r[wsrc_r]      <= 1'b0;\n"
                                            "            fourpack_r[wsrc_r] <= 2'd0;\n",
                                         "            lvp_r[wsrc_r]      <= 1'b0;\n")]),
    # #188: "same" without the record-valid term (candidate equivalent)
    "U7-same-ignores-rec-valid": (FSMS, [(L, "set_same_w = rec_valid_r[ctl_sink_i] && (csid_w == ctl_stream_id_i);",
                                          "set_same_w = (csid_w == ctl_stream_id_i);")]),
    # #189: the type bookkeeping in every state, not only SOK (candidate equivalent)
    "U8-swap-any-state": (ACMPL, [(A, "if ((evt_r == LEV_TK_REG) && (rec_r.sm_state == 3'(LSM_SOK))) begin",
                                   "if (evt_r == LEV_TK_REG) begin")]),
    # #189: harness positive control, the same edit as the author's rf_swap_unlatched
    "U9-swap-unlatched": (ACMPL, [(A, "            rec_r.f_srp_decl[1] <= tkfail_r;\n          end\n          if (!rom_valid_w",
                                   "            rec_r.f_srp_decl[1] <= rec_r.f_srp_decl[1];\n          end\n          if (!rom_valid_w")]),
}
TALLY = re.compile(r"^\d+ checks: \d+ PASS, \d+ FAIL$", re.M)


def one(name, head, out):
    (suite, cmd), edits = PROBES[name]
    work = out / "work" / name
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    shutil.copytree(head / "hdl", work / "hdl")
    shutil.copytree(head / "tb", work / "tb", ignore=shutil.ignore_patterns("obj*", "__pycache__"))
    for rel, old, new in edits:
        p = work / rel
        t = p.read_text()
        if t.count(old) != 1:
            return {"probe": name, "verdict": "INCONCLUSIVE", "reason": f"{rel}: {t.count(old)} matches"}
        p.write_text(t.replace(old, new, 1))
    log = out / f"{name}.log"
    env = dict(os.environ)
    with log.open("w") as f:
        rc = subprocess.run(cmd + ["VERILATOR=" + env.get("VERILATOR", "verilator")],
                            cwd=work / suite, stdout=f, stderr=subprocess.STDOUT, env=env).returncode
    text = log.read_text(errors="replace")
    tally = TALLY.findall(text)
    fails = [l for l in text.splitlines() if l.startswith("FAIL")]
    verdict = ("KILLED" if rc != 0 and tally else "SURVIVED" if rc == 0 and tally else "INCONCLUSIVE")
    shutil.rmtree(work)
    return {"probe": name, "suite": suite, "rc": rc, "tally": tally[-1:] , "fail_lines": fails[:12],
            "n_fail_lines": len(fails), "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("head", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    names = a.only or list(PROBES)
    with concurrent.futures.ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda n: one(n, a.head, a.out), names))
    for r in res:
        print(json.dumps(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
