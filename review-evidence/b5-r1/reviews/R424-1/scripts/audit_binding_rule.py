#!/usr/bin/env python3
"""Audit the owner's binding rule in every run's controller log (ctl.jsonl):
before each bind, the talker's and listener's formats are read after the previous
connection event; on a difference the listener (peer) is set to the talker's format and
read back equal; the talker (DUT) is never set; after the final unbind the listener is
set back to its as-found format and read back. usage: audit_binding_rule.py <author dir>"""
import json, sys
from pathlib import Path
A = Path(sys.argv[1])
ok_all = True
for run in ["a-try1", "diag1", "a-long", "cap-test1", "abort-agent-start"]:
    L = [json.loads(l) for l in open(A / "runs" / run / "ctl.jsonl")]
    tf = lf = None; pending_set = None; binds = []; unbinds = 0; problems = []; sets = []
    last_op = None; asfound = None; final_lf = None; dut_sets = 0
    for l in L:
        x = l.get("line", {}); req = l.get("req")
        if req: last_op = req.get("op")
        if x.get("cmd") == "GET_STREAM_FORMAT":
            fmt = x["payload"][8:]
            if x["role"] == "dut": tf = fmt
            else:
                if asfound is None: asfound = fmt
                lf = fmt; final_lf = fmt
        if x.get("cmd") == "SET_STREAM_FORMAT":
            if x["role"] == "dut": dut_sets += 1
            sets.append((x["role"], x["payload"][8:], x["status"]))
        if "status" in x and "conn_count" in x and "cmd" not in x:
            if last_op == "bind" and x.get("stream_id") != "0000000000000000":
                # bind response (the second, carrying the stream id)
                rec = dict(talker=tf, listener=lf, status=x["status"], cc=x["conn_count"])
                if tf is None or lf is None: problems.append(("bind without both reads", rec))
                elif tf != lf: problems.append(("bind with formats unequal", rec))
                if x["status"] != 0 or x["conn_count"] != 1: problems.append(("bind status", rec))
                binds.append(rec); tf = lf = None
            elif last_op == "unbind":
                unbinds += 1
    # count bind responses by op even if stream id zero
    nb_req = sum(1 for l in L if l.get("req", {}).get("op") == "bind")
    nu_req = sum(1 for l in L if l.get("req", {}).get("op") == "unbind")
    ok = not problems and dut_sets == 0 and (not binds or final_lf == asfound)
    ok_all &= ok
    print(f"{run}: bind requests {nb_req}, bind SUCCESS responses graded {len(binds)}, unbind requests {nu_req}, "
          f"listener sets {sets}, talker sets {dut_sets}, listener as found {asfound}, listener last read {final_lf}, "
          f"problems {problems[:3]} -> {'OK' if ok else 'FAIL'}")
print("ALL OK" if ok_all else "NOT OK")
