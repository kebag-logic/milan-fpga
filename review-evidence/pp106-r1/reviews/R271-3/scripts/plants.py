#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Independent fault plants for PR #107 round R271-3, written from the
assignment's plant descriptions (not copied from any earlier script).

Each plant is applied to a fresh `git archive` export of COMMIT, every edit
must match its anchor exactly once, and the four SRP suites run with the
pinned simulator through verilator_capped.sh. A plant is KILLED when any
suite fails, SURVIVED when all four pass; the control must pass all four.

usage: plants.py REPO COMMIT WORKDIR OUTFILE [PLANT ...]
env:   PINNED_VERILATOR (required), VL_JOBS (build jobs per suite, default 2),
       PLANT_POOL (plants in parallel, default 4)
"""
import concurrent.futures as cf
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tarfile
import io

DEC = "hdl/srp/KL_srp_decoder.sv"
TOP = "hdl/srp/KL_srp_top.sv"
TFSM = "hdl/srp/KL_srp_talker_fsm.sv"
LFSM = "hdl/srp/KL_srp_listener_fsm.sv"
SUITES = ["srp_decoder", "srp_encoder", "srp_stream_fsms", "srp_top"]

CLEAR_AT_PV = ("            app_msrp_r <= mrp_msrp_i;\n"
               "            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n")
FIRE = ("              if (la_first_w) begin\n"
        "                la_done_r[la_lane_w] <= 1'b1;\n")
FIRE_BLOCK = ("              if (la_first_w) begin\n"
              "                la_done_r[la_lane_w] <= 1'b1;\n"
              "                if (app_msrp_r) la_msrp_o[la_lane_w] <= 1'b1;\n"
              "                else            la_mvrp_o            <= 1'b1;\n"
              "              end\n")
FAIL_TASK = ("    last_seen_r     <= 1'b0;\n"
             "    state_r         <= S_IDLE;\n"
             "  endtask\n")
END2_OK = "              state_r         <= mrp_last_i ? S_IDLE : S_PAD;\n"
PAD_LAST = "            if (mrp_last_i) state_r <= S_IDLE;  // padding after the dual EndMark\n"
MSGTYPE = ("              attr_type_r <= mrp_data_i;\n"
           "              if (mrp_last_i) pdu_fail_t();\n"
           "              else            state_r <= S_ALEN;\n")
DOM_TICK = ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),"
VLAN_TICK = ".leaveall_tick_i (dec_la_mvrp_w || p_la_mvrp_r),"

# plant id -> (description, [(path, old, new), ...])
PLANTS = {
    "K0": ("control, no change", []),
    "K5": ("gate re-armed at a malformed or an unpadded clean end, never after a padded MRPDU",
           [(DEC, CLEAR_AT_PV, "            app_msrp_r <= mrp_msrp_i;\n"),
            (DEC, FAIL_TASK, "    last_seen_r     <= 1'b0;\n    la_done_r       <= 4'd0;\n"
                             "    state_r         <= S_IDLE;\n  endtask\n"),
            (DEC, END2_OK, END2_OK + "              if (mrp_last_i) la_done_r <= 4'd0;\n")]),
    "K6": ("the gate remembers only the last type that fired",
           [(DEC, FIRE, "              if (la_first_w) begin\n"
                        "                la_done_r <= 4'b0001 << la_lane_w;\n")]),
    "K7": ("an unflagged VectorHeader re-opens its type's gate",
           [(DEC, FIRE_BLOCK, FIRE_BLOCK.rstrip("\n")
             + " else if (vhdr1_r[7:5] != SRP_LEAVEALL_EV_C) begin\n"
               "                la_done_r[la_lane_w] <= 1'b0;\n"
               "              end\n")]),
    "K8": ("gate re-armed at every message whose AttributeType differs from the previous one",
           [(DEC, MSGTYPE, "              attr_type_r <= mrp_data_i;\n"
                           "              if (mrp_data_i != attr_type_r) la_done_r <= 4'd0;\n"
                           "              if (mrp_last_i) pdu_fail_t();\n"
                           "              else            state_r <= S_ALEN;\n")]),
    "K13": ("Domain participant also takes the Talker Advertise lane",
            [(TOP, DOM_TICK, ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || "
                             "dec_la_msrp_w[SRP_LA_TALKER_ADV_C] || p_la_msrp_r),")]),
    "K14": ("Domain participant also takes the Talker Failed lane",
            [(TOP, DOM_TICK, ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || "
                             "dec_la_msrp_w[SRP_LA_TALKER_FAILED_C] || p_la_msrp_r),")]),
    # --- extra boundary plants of this round (not assigned) ---------------
    "X-A": ("gate re-armed at every message, whatever its type",
            [(DEC, MSGTYPE, "              attr_type_r <= mrp_data_i;\n"
                            "              la_done_r <= 4'd0;\n"
                            "              if (mrp_last_i) pdu_fail_t();\n"
                            "              else            state_r <= S_ALEN;\n")]),
    "X-B": ("gate re-armed only after a padded MRPDU or a malformed one, never at an unpadded clean end",
            [(DEC, CLEAR_AT_PV, "            app_msrp_r <= mrp_msrp_i;\n"),
             (DEC, FAIL_TASK, "    last_seen_r     <= 1'b0;\n    la_done_r       <= 4'd0;\n"
                              "    state_r         <= S_IDLE;\n  endtask\n"),
             (DEC, PAD_LAST, "            if (mrp_last_i) begin state_r <= S_IDLE; la_done_r <= 4'd0; end\n")]),
    "X-C": ("gate never re-arms after reset",
            [(DEC, CLEAR_AT_PV, "            app_msrp_r <= mrp_msrp_i;\n")]),
    "X-D": ("Domain participant also takes the Listener lane",
            [(TOP, DOM_TICK, ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || "
                             "dec_la_msrp_w[SRP_LA_LISTENER_C] || p_la_msrp_r),")]),
    "X-E": ("VLAN participant also takes every MSRP lane (inherited routing gap)",
            [(TOP, VLAN_TICK, ".leaveall_tick_i (dec_la_mvrp_w || (|dec_la_msrp_w) || p_la_mvrp_r),")]),
    # own LeaveAll dropped from registrar aging (inherited gap); head anchors
    "X-F": ("talker registrar no longer aged by an own LeaveAll (head RTL)",
            [(TFSM, "  assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;\n",
              "  assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C];\n")]),
    "X-G": ("listener registrars no longer aged by an own LeaveAll (head RTL)",
            [(LFSM, "      leaveall_any_w[s] = leaveall_own_i\n                       || (",
              "      leaveall_any_w[s] = 1'b0\n                       || (")]),
    # the same two plants against the base RTL's one-bit strobe
    "X-Fb": ("talker registrar no longer aged by an own LeaveAll (base RTL)",
             [(TFSM, "  assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;\n",
               "  assign leaveall_any_w = leaveall_rx_i;\n")]),
    "X-Gb": ("listener registrars no longer aged by an own LeaveAll (base RTL)",
             [(LFSM, "  assign leaveall_any_w = leaveall_rx_i || leaveall_own_i;\n",
               "  assign leaveall_any_w = leaveall_rx_i;\n")]),
}

TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def export(repo, commit, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    data = subprocess.run(["git", "-C", repo, "archive", "--format=tar", commit],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        t.extractall(dest, filter="tar")


def apply(dest, edits):
    touched = {}
    for path, old, new in edits:
        p = os.path.join(dest, path)
        with open(p, encoding="utf-8") as f:
            s = f.read()
        n = s.count(old)
        if n != 1:
            raise RuntimeError(f"anchor matched {n} times in {path}: {old[:60]!r}")
        s = s.replace(old, new)
        with open(p, "w", encoding="utf-8") as f:
            f.write(s)
        touched[path] = hashlib.sha256(s.encode()).hexdigest()
    return touched


def run_suite(dest, suite, wrapper):
    d = os.path.join(dest, "tb", suite)
    r = subprocess.run(["make", "-C", d, f"VERILATOR={wrapper}"],
                       capture_output=True, text=True)
    log = r.stdout + r.stderr
    with open(os.path.join(dest, f"{suite}.log"), "w") as f:
        f.write(log)
    m = TALLY.findall(log)
    fails = [ln[6:] for ln in log.splitlines() if ln.startswith("FAIL: ")]
    tally = m[-1] if m else None
    return r.returncode, tally, fails


def run_plant(repo, commit, work, pid, wrapper):
    desc, edits = PLANTS[pid]
    dest = os.path.join(work, pid)
    export(repo, commit, dest)
    touched = apply(dest, edits)
    res = {}
    for s in SUITES:
        res[s] = run_suite(dest, s, wrapper)
    return pid, desc, touched, res


def main():
    repo, commit, work, outfile = sys.argv[1:5]
    ids = sys.argv[5:] or list(PLANTS)
    wrapper = os.path.join(os.path.dirname(os.path.abspath(__file__)), "verilator_capped.sh")
    os.environ.setdefault("VL_JOBS", "2")
    pool = int(os.environ.get("PLANT_POOL", "4"))
    full = subprocess.run(["git", "-C", repo, "rev-parse", commit + "^{commit}"],
                          check=True, capture_output=True, text=True).stdout.strip()
    lines = [f"commit {full}", f"plants {' '.join(ids)}",
             f"build jobs per suite {os.environ['VL_JOBS']}, plants in parallel {pool}", ""]
    with cf.ThreadPoolExecutor(max_workers=pool) as ex:
        futs = [ex.submit(run_plant, repo, full, work, i, wrapper) for i in ids]
        results = {f.result()[0]: f.result() for f in futs}
    for i in ids:
        pid, desc, touched, res = results[i]
        verdict = []
        unreadable = False
        for s in SUITES:
            rc, tally, fails = res[s]
            if tally is None:
                unreadable = True
                verdict.append(f"{s}: NO TALLY (rc {rc})")
            else:
                verdict.append(f"{s}: {tally[0]} checks, {tally[2]} FAIL (rc {rc})")
        failing = [s for s in SUITES if res[s][1] and res[s][1][2] != "0"]
        if unreadable:
            v = "UNREADABLE"
        elif pid == "K0":
            v = "CONTROL PASSES" if not failing else "CONTROL FAILS"
        else:
            v = "KILLED" if failing else "SURVIVED"
        lines.append(f"== {pid}: {v} -- {desc}")
        for path, h in sorted(touched.items()):
            lines.append(f"   planted {path} sha256 {h}")
        for x in verdict:
            lines.append(f"   {x}")
        for s in SUITES:
            for fl in res[s][2]:
                lines.append(f"   {s} FAIL: {fl}")
        lines.append("")
    text = "\n".join(lines) + "\n"
    with open(outfile, "w") as f:
        f.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
