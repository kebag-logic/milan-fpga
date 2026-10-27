#!/usr/bin/env python3
"""Reviewer-owned fault probes on KL_acmp_talker for issue #205.

Each probe copies hdl/, tb/common/ and tb/acmp_talker/ from SOURCE into
WORK/NAME, applies exact-once text edits to hdl/acmp/KL_acmp_talker.sv, runs
`make run` with the given simulator and records the tally and FAIL lines.
The source tree is never written.

Usage: probe_mutants.py SOURCE WORK VERILATOR JOBS OUTFILE.json
"""
import concurrent.futures
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RTL = "hdl/acmp/KL_acmp_talker.sv"

UNK = ("            resp_status_o       = ST_TALKER_UNKNOWN_C;\n"
       "            resp_listener_eid_o = pdu_leid_r;\n"
       "            resp_listener_uid_o = pdu_luid_r;\n"
       "          end\n        end\n")
FETCH = "                         || ((txn_r.msg_type == MT_GTX_ST_C) && !uid_valid_w)\n"
OK_ZERO = ("            resp_listener_eid_o = 64'd0;\n"
           "            resp_listener_uid_o = 16'd0;\n")

PROBES = {
    # control: no edit, must pass
    "control_unmodified": [],
    # only the entity id echoed; the unique id left at 0
    "unknown_uid_zero": [(UNK, UNK.replace("= pdu_luid_r", "= 16'd0"))],
    # only the unique id echoed; the entity id left at 0
    "unknown_eid_zero": [(UNK, UNK.replace("= pdu_leid_r", "= 64'd0"))],
    # the refusal also echoes the command's flags (undefined in Table 5.46,
    # graded 0 by the suite)
    "unknown_echoes_flags": [(UNK, UNK.replace(
        "            resp_listener_uid_o = pdu_luid_r;\n",
        "            resp_listener_uid_o = pdu_luid_r;\n"
        "            resp_flags_o        = pdu_flags_r & FLG_ECHO_MASK_C;\n"))],
    # the refusal reports the declared stream fields (undefined in Table 5.46)
    "unknown_reports_stream": [(UNK, UNK.replace(
        "            resp_listener_uid_o = pdu_luid_r;\n",
        "            resp_listener_uid_o = pdu_luid_r;\n"
        "            resp_stream_id_o    = cur_sid_f(tsrc_w);\n"))],
    # fetch only for an out-of-range id: a disabled in-range source is not fetched
    "fetch_only_out_of_range": [(FETCH, FETCH.replace(
        "!uid_valid_w", "(uid16_w >= 16'(N_STREAM_OUT_P))"))],
    # the listener entity id bytes taken in the wrong order (byte-lane swap)
    "eid_byte_swap": [(UNK, UNK.replace(
        "= pdu_leid_r;", "= {pdu_leid_r[7:0], pdu_leid_r[63:8]};"))],
    # the unique id bytes swapped
    "uid_byte_swap": [(UNK, UNK.replace(
        "= pdu_luid_r;", "= {pdu_luid_r[7:0], pdu_luid_r[15:8]};"))],
    # success arm's explicit zeros removed (expected EQUIVALENT: no fetch on
    # success and the PDU registers are cleared at dispatch)
    "success_zero_lines_removed": [(OK_ZERO, "")],
    # success arm echoes the PDU registers without the fetch (expected
    # EQUIVALENT for the same reason)
    "success_echo_unfetched": [(OK_ZERO, OK_ZERO.replace("64'd0", "pdu_leid_r")
                                .replace("16'd0", "pdu_luid_r"))],
    # PDU registers no longer cleared at dispatch (stale previous command):
    # probes whether the suite sees stale echo from an earlier command
    "pdu_not_cleared_at_dispatch": [(
        "            txn_r       <= pp_txn_t'(txn_i);\n"
        "            pdu_leid_r  <= 64'd0;\n"
        "            pdu_luid_r  <= 16'd0;\n",
        "            txn_r       <= pp_txn_t'(txn_i);\n")],
}

TALLY = re.compile(r"^(\d+) checks: (\d+) PASS, (\d+) FAIL", re.M)


def run(name, edits, source, work, verilator):
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    for d in ("hdl", "tb/common", "tb/acmp_talker"):
        shutil.copytree(source / d, tree / d,
                        ignore=shutil.ignore_patterns("obj_dir"))
    rtl = tree / RTL
    text = rtl.read_text()
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            return {"probe": name, "verdict": "EDIT-REFUSED", "count": n}
        text = text.replace(old, new)
    rtl.write_text(text)
    p = subprocess.run(["make", "run", "VERILATOR=" + verilator],
                       cwd=tree / "tb/acmp_talker", capture_output=True, text=True)
    out = p.stdout + p.stderr
    (work / (name + ".log")).write_text(out)
    m = TALLY.search(out)
    fails = [l for l in out.splitlines() if l.startswith("FAIL")]
    if not m:
        verdict = "NO-TALLY"
    elif p.returncode != 0 and int(m.group(3)) > 0:
        verdict = "KILLED"
    elif p.returncode == 0 and int(m.group(3)) == 0:
        verdict = "SURVIVED"
    else:
        verdict = "INCONSISTENT"
    shutil.rmtree(tree / "tb/acmp_talker/obj_dir", ignore_errors=True)
    return {"probe": name, "verdict": verdict, "rc": p.returncode,
            "tally": m.group(0) if m else None, "fails": fails[:12],
            "n_fails": len(fails)}


def main():
    source, work, verilator, jobs, outfile = (Path(sys.argv[1]), Path(sys.argv[2]),
                                              sys.argv[3], int(sys.argv[4]),
                                              Path(sys.argv[5]))
    work.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        futs = {pool.submit(run, n, e, source, work, verilator): n
                for n, e in PROBES.items()}
        results = [f.result() for f in futs]
    results.sort(key=lambda r: list(PROBES).index(r["probe"]))
    outfile.write_text(json.dumps(results, indent=1) + "\n")
    for r in results:
        print(r["probe"], r["verdict"], r.get("tally"), r.get("n_fails", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
