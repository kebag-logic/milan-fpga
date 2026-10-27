#!/usr/bin/env python3
"""Reviewer-owned mutant arms for issue #205, graded by tb/acmp_talker.

Usage: python3 rv_mutants.py --tree TREE --output DIR --verilator V [--jobs N]

TREE is a disposable copy of the processor at the reviewed head. This reuses that tree's own
tb/pp_top/acmp_mutants.py machinery (plant: every old text must occur exactly once; judge:
KILLED only if the build succeeds, the tally completes, the run exits non-zero and every
named check fails). Arms whose expectation is EQUIVALENT or INFO are reported, not graded
as kills.
"""
import argparse
import concurrent.futures
import json
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--tree", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
ap.add_argument("--verilator", required=True)
ap.add_argument("--jobs", type=int, default=4)
args = ap.parse_args()
sys.path.insert(0, str(args.tree / "tb/pp_top"))
import acmp_mutants as am  # noqa: E402  (the reviewed head's own driver)

T = am.TALKER
UNK = am.GTX_UNKNOWN_ECHO
FETCH = am.GTX_FETCH
SUCC = am.GTX_SUCCESS_ZERO
C2H3_EID = ("C2 unknown-id listener_eid", "H3 disabled source GET_TX_STATE listener_eid")
C2H3_UID = ("C2 unknown-id listener_uid", "H3 disabled source GET_TX_STATE listener_uid")
PROBE_UNK = ("            resp_status_o       = ST_TALKER_UNKNOWN_C;\n"
             "            resp_listener_eid_o = pdu_leid_r;\n"
             "            resp_listener_uid_o = pdu_luid_r;\n"
             "            resp_flags_o        = pdu_flags_r & FLG_ECHO_MASK_C;\n"
             "          end else if (iface_ok_w) begin\n")
DISC = ("resp_status_o       = uid_valid_w ? ST_SUCCESS_C : ST_TALKER_UNKNOWN_C;\n"
        "          resp_listener_eid_o = pdu_leid_r;\n")
GTXCN = ("resp_status_o       = ST_NOT_SUPPORTED_C;\n"
         "          resp_listener_eid_o = pdu_leid_r;\n")
CLEAR = ("            pdu_leid_r  <= 64'd0;\n"
         "            pdu_luid_r  <= 16'd0;\n")

M = am.Mutant
S = am.ACMP_TALKER
ARMS = [
    # (mutant, expectation)
    (M("rv_unknown_uid_zeroed", S, ((T, UNK, UNK.replace("= pdu_luid_r", "= 16'd0")),),
       C2H3_UID), "KILL"),
    (M("rv_unknown_eid_zeroed", S, ((T, UNK, UNK.replace("= pdu_leid_r", "= 64'd0")),),
       C2H3_EID), "KILL"),
    (M("rv_unknown_eid_halves_swapped", S,
       ((T, UNK, UNK.replace("= pdu_leid_r", "= {pdu_leid_r[31:0], pdu_leid_r[63:32]}")),),
       C2H3_EID), "KILL"),
    (M("rv_fetch_inverted", S, ((T, FETCH, FETCH.replace("!uid_valid_w", "uid_valid_w")),),
       C2H3_EID + C2H3_UID), "KILL"),
    (M("rv_unknown_echoes_flags", S,
       ((T, UNK, UNK.replace("          end\n", "            resp_flags_o        = pdu_flags_r;\n          end\n")),),
       ("C2 unknown-id flags", "H3 disabled source GET_TX_STATE flags")), "KILL"),
    (M("rv_success_explicit_zero_removed", S, ((T, SUCC, ""),), ("B2 listener_eid",)),
     "EQUIVALENT"),
    (M("rv_probe_unknown_zeroed", S,
       ((T, PROBE_UNK, PROBE_UNK.replace("= pdu_leid_r", "= 64'd0").replace("= pdu_luid_r", "= 16'd0")),),
       ("C1 unknown-id listener_eid", "C1 unknown-id listener_uid",
        "H2 disabled source listener_eid", "H2 disabled source listener_uid")), "KILL"),
    (M("rv_disconnect_eid_zeroed", S, ((T, DISC, DISC.replace("= pdu_leid_r", "= 64'd0")),),
       ("C4 disconnect no-op listener_eid", "TD1")), "KILL"),
    (M("rv_gtx_connection_eid_zeroed", S, ((T, GTXCN, GTXCN.replace("= pdu_leid_r", "= 64'd0")),),
       ("C5 get_tx_connection listener_eid",)), "KILL"),
    (M("rv_no_clear_on_dispatch", S, ((T, CLEAR, ""),), ("never-named",)), "INFO"),
]

out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
work = (args.tree.resolve(), out, args.verilator)
records = [am.judge(am.golden_label(S), S, (), (), work)]
print(json.dumps({"mutant": records[0]["mutant"], "verdict": records[0]["verdict"]}), flush=True)
with concurrent.futures.ThreadPoolExecutor(max(1, args.jobs)) as pool:
    futs = {pool.submit(am.judge, am.label_of(m), m.suite, m.edits, m.checks, work): exp
            for m, exp in ARMS}
    for f in concurrent.futures.as_completed(futs):
        r = f.result()
        r["expectation"] = futs[f]
        records.append(r)
        print(json.dumps({k: r.get(k) for k in ("mutant", "expectation", "verdict", "missing")}),
              flush=True)
(out / "results.json").write_text(json.dumps(records, indent=1) + "\n")
ok = records[0]["verdict"] == "PASS"
for r in records[1:]:
    exp = r["expectation"]
    if exp == "KILL":
        ok &= r["verdict"] == "KILLED"
    elif exp == "EQUIVALENT":
        ok &= r.get("run_rc") == 0 and not r.get("failing_checks")
print("RV summary:", "as expected" if ok else "UNEXPECTED")
sys.exit(0 if ok else 1)
