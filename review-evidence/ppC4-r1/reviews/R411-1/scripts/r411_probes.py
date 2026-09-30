#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer discrimination probes for PR #137 (lane C4, ACMP).

Each probe is an extra planted defect, outside the author's table, that the new
checks are expected to catch. It reuses the author's own driver machinery
(tb/pp_top/acmp_mutants.py: private extract per mutant, golden first, KILLED only
when the run completes with its tally, exits non-zero and every named check
fails) so a probe is graded by the same rule as the author's mutants.

Usage: python3 r411_probes.py --root <exported head tree> --output DIR
                              [--verilator V] [--jobs N]
"""

import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path


def load_driver(root: Path):
    spec = importlib.util.spec_from_file_location(
        "acmp_mutants", root / "tb/pp_top/acmp_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def probes(dm):
    M = dm.Mutant
    L, V, S = dm.LISTENER, dm.VALIDATOR, dm.SRP_LISTENER
    MSG_OK = dm.MSG_OK

    def admit(code: str) -> str:
        return ("  assign txn_msg_ok_w   = (txn_i.msg_type == 4'd%s)"
                " || (txn_i.msg_type == AMSG_PROBE_TX_RESP_C)\n" % code)

    seq_free = dm.GUARD.replace("(seq_x_r == rec_r.probe_seq)", "1'b1", 1)
    sid_term = ("                     && (evt_stream_id_i == sid_r[s])\n"
                "                     && (evt_da_i == da_r[s])\n")
    return (
        # #47: the census is complete per type, not only in aggregate
        M("r411_admit_13", dm.ACMP_LISTENER, ((L, MSG_OK, admit("13")),),
          ("B13 msg 13 status 0 in PWR", "B13 msg 13 status 5 in PW2")),
        M("r411_admit_9", dm.ACMP_LISTENER, ((L, MSG_OK, admit("9")),),
          ("B13 msg 9 status 0 in PWR", "B13 msg 9 status 5 in PW2")),
        M("r411_admit_5", dm.ACMP_LISTENER, ((L, MSG_OK, admit("5")),),
          ("B13 msg 5 status 0 in PWR", "B13 msg 5 status 5 in PW2")),
        M("r411_admit_14", dm.PP_TOP, ((L, MSG_OK, admit("14")),),
          ("AI3: the sink never left PRB_W_RESP",)),
        M("r411_admit_7", dm.PP_TOP, ((L, MSG_OK, admit("7")),),
          ("AI3: the sink never left PRB_W_RESP",)),
        # #47: the fourth guard term (pre-existing B8) completes the per-term set
        M("r411_guard_seq_dropped", dm.ACMP_LISTENER, ((L, dm.GUARD, seq_free),),
          ("B8",)),
        # #45: rejecting only LONGER ACMP (short form untouched) is still caught
        M("r411_cdl_gt_44_rejected", dm.RX_VALIDATOR, ((V, dm.V1_END,
          "                      && (lim_w <= 12'(BYTES_P))\n"
          "                      && !((subtype_r == SUB_ACMP_C) && (cdl_r > 11'd44));\n"),),
          ("F29 BIND_RX cdl 84", "F29 PROBE_TX cdl 84")),
        M("r411_cdl_gt_44_rejected", dm.PP_TOP, ((V, dm.V1_END,
          "                      && (lim_w <= 12'(BYTES_P))\n"
          "                      && !((subtype_r == SUB_ACMP_C) && (cdl_r > 11'd44));\n"),),
          ("AL1: a 96-B UNBIND_RX", "AL2: a 96-B BIND_RX", "AL3: the 96-B PROBE_TX")),
        # #48: the third near miss (stream_id) discriminates too
        M("r411_matcher_sid_ignored", dm.PP_TOP, ((S, sid_term,
          "                     && (evt_da_i == da_r[s])\n"),),
          ("AS3: near misses (DA, VLAN, stream_id) put no Listener declaration",
           "AS3: near misses register nothing", "AS3: no TK_ATTR_REGISTERED{1}")),
        # #48 item 1: the VLAN and talker-EID lanes of the bound view are graded
        M("r411_bound_vlan_not_latched", dm.PP_TOP, ((dm.TOP,
          "bound_vlan_r[lstn_act_sink_w] <= lstn_act_settle_vlan_w;",
          "bound_vlan_r[lstn_act_sink_w] <= 12'd0;"),),
          ("AS2: acmp_bound_o/eid/sid/dmac/vlan_o[1] carry the settled stream",
           "AS5: the bound view still carries the settled stream")),
        M("r411_bound_eid_not_latched", dm.PP_TOP, ((dm.TOP,
          "bound_eid_r[lstn_act_sink_w] <= lstn_disc_eid_w;",
          "bound_eid_r[lstn_act_sink_w] <= 64'd0;"),),
          ("AS2: acmp_bound_o/eid/sid/dmac/vlan_o[1] carry the settled stream",)),
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", default="verilator")
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args()
    root, out = a.root.resolve(), a.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    dm = load_driver(root)
    chosen = probes(dm)
    work = (root, out, a.verilator)
    suites = {m.suite.directory: m.suite for m in chosen}
    recs = [dm.judge("golden-" + Path(d).name, s, (), (), work)
            for d, s in sorted(suites.items())]
    if all(r["verdict"] == "PASS" for r in recs):
        with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as pool:
            futs = [pool.submit(dm.judge, dm.label_of(m), m.suite, m.edits,
                                m.checks, work) for m in chosen]
            for f in concurrent.futures.as_completed(futs):
                recs.append(f.result())
    for r in recs:
        print(json.dumps({k: r.get(k) for k in
                          ("mutant", "verdict", "run_rc", "missing")}))
        if "failing_checks" in r:
            print("   failing:", len(r["failing_checks"]))
    (out / "results.json").write_text(json.dumps(recs, indent=1) + "\n")
    ok = all(r["verdict"] in ("PASS", "KILLED") for r in recs)
    print("R411 probes:", sum(r["verdict"] == "KILLED" for r in recs), "of",
          len(chosen), "KILLED;", "all expected" if ok else "NOT all killed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
