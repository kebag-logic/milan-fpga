#!/usr/bin/env python3
"""Reviewer-owned disposable mutation probes for PR #107 at one exact head.

Each mutant is planted exactly once into a fresh `git archive` export of the
reviewed revision (never into the clone), the named Verilator suites are run
there, and the per-suite tallies plus every FAIL line are written to a
receipt. A replacement that does not match exactly once aborts the mutant as
NOT PLANTED, so a stale probe can never report a false survival.

usage: mutants.py <clone> <rev> <scratch-dir> <receipt> [mutant-id ...]
env:   REAL_VERILATOR  pinned simulator wrapper
       VL_JOBS         per-build compile jobs (default 2); four suites run
                       in parallel, so the total stays at 8
"""
import concurrent.futures
import hashlib
import os
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SUITES = ("srp_decoder", "srp_encoder", "srp_stream_fsms", "srp_top")
DEC = "hdl/srp/KL_srp_decoder.sv"
TOP = "hdl/srp/KL_srp_top.sv"

GATE_SET = (
    "              if (la_first_w) begin\n"
    "                la_done_r[la_lane_w] <= 1'b1;\n"
)
REARM = "            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n"
DOM_TICK = ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),"

# id -> (description, [(file, old, new), ...])
MUTANTS = {
    "K0": ("control: no change (the export must pass)", []),
    "K1": ("X1-class: every VectorHeader of a type closes its gate, flagged or not",
           [(DEC, GATE_SET,
             "              la_done_r[la_lane_w] <= 1'b1;\n"
             "              if (la_first_w) begin\n")]),
    "K3": ("X7-class: gate re-armed only at a clean dual EndMark",
           [(DEC, REARM, ""),
            (DEC, "              pdu_ok_o        <= 1'b1;\n",
             "              pdu_ok_o        <= 1'b1;\n              la_done_r       <= 4'd0;\n")]),
    "K5": ("X7-class: gate re-armed at a malformed end or an unpadded clean end, "
           "never after a padded MRPDU",
           [(DEC, REARM, ""),
            (DEC, "    last_seen_r     <= 1'b0;\n    state_r         <= S_IDLE;\n  endtask",
             "    last_seen_r     <= 1'b0;\n    state_r         <= S_IDLE;\n"
             "    la_done_r       <= 4'd0;\n  endtask"),
            (DEC, "              state_r         <= mrp_last_i ? S_IDLE : S_PAD;\n",
             "              state_r         <= mrp_last_i ? S_IDLE : S_PAD;\n"
             "              if (mrp_last_i) la_done_r <= 4'd0;\n")]),
    "K6": ("once-per-MRPDU gate remembers only the last type that fired "
           "(one register instead of one bit per type)",
           [(DEC, "                la_done_r[la_lane_w] <= 1'b1;\n",
             "                la_done_r <= 4'b0001 << la_lane_w;\n")]),
    "K7": ("an unflagged VectorHeader of a type re-opens that type's gate",
           [(DEC, GATE_SET,
             "              la_done_r[la_lane_w] <= (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C);\n"
             + GATE_SET)]),
    "K8": ("gate re-armed at every message whose AttributeType differs from "
           "the previous message's",
           [(DEC, "              attr_type_r <= mrp_data_i;\n",
             "              attr_type_r <= mrp_data_i;\n"
             "              if (mrp_data_i != attr_type_r) la_done_r <= 4'd0;\n")]),
    "K10": ("X7-class: gate re-armed at a new MRPDU only when it is MSRP",
            [(DEC, REARM,
              "            if (mrp_msrp_i) la_done_r <= 4'd0;\n")]),
    "K12": ("Domain participant also takes the Listener lane",
            [(TOP, DOM_TICK,
              ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || "
              "dec_la_msrp_w[SRP_LA_LISTENER_C] || p_la_msrp_r),")]),
    "K13": ("Domain participant also takes the Talker Advertise lane",
            [(TOP, DOM_TICK,
              ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || "
              "dec_la_msrp_w[SRP_LA_TALKER_ADV_C] || p_la_msrp_r),")]),
    "K14": ("Domain participant also takes the Talker Failed lane",
            [(TOP, DOM_TICK,
              ".leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || "
              "dec_la_msrp_w[SRP_LA_TALKER_FAILED_C] || p_la_msrp_r),")]),
    # status at this head of the inherited gaps a prior round left as suggestions
    "K15": ("VLAN participant also takes every MSRP lane (prior R271-1 S1 R5)",
            [(TOP, ".leaveall_tick_i (dec_la_mvrp_w || p_la_mvrp_r),",
              ".leaveall_tick_i (dec_la_mvrp_w || (|dec_la_msrp_w) || p_la_mvrp_r),")]),
    "K16": ("own LeaveAll dropped from the talker registrar's aging (prior R271-1 S1 R10)",
            [("hdl/srp/KL_srp_talker_fsm.sv",
              "assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;",
              "assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C];")]),
    "K17": ("own LeaveAll dropped from the listener registrar's aging (prior R271-1 S1 R11)",
            [("hdl/srp/KL_srp_listener_fsm.sv",
              "      leaveall_any_w[s] = leaveall_own_i\n                       || (",
              "      leaveall_any_w[s] = 1'b0\n                       || (")]),
}

TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def export(clone: str, rev: str, dest: pathlib.Path) -> None:
    """Extract `rev` of `clone` into an empty `dest` with git archive."""
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    arch = subprocess.run(["git", "-C", clone, "archive", rev],
                          check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=arch, check=True)


def plant(tree: pathlib.Path, edits: list) -> list:
    """Apply each (file, old, new) exactly once; return planted sha256 lines."""
    shas = []
    for rel, old, new in edits:
        path = tree / rel
        text = path.read_text()
        count = text.count(old)
        if count != 1:
            raise ValueError(f"{rel}: pattern matched {count} times, not once")
        path.write_text(text.replace(old, new, 1))
    for rel in sorted({e[0] for e in edits}):
        shas.append(f"{hashlib.sha256((tree / rel).read_bytes()).hexdigest()}  {rel}")
    return shas


def run_suite(tree: pathlib.Path, suite: str) -> tuple:
    """Build and run one suite; return (suite, status, tally, fail lines)."""
    env = dict(os.environ)
    wrapper = str(HERE / "verilator_capped.sh")
    proc = subprocess.run(["make", f"VERILATOR={wrapper}"], cwd=tree / "tb" / suite,
                          env=env, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    (tree / f"{suite}.log").write_text(out)
    tallies = TALLY.findall(out)
    tally = "%s checks: %s PASS, %s FAIL" % tallies[-1] if tallies else "no tally"
    fails = [ln for ln in out.splitlines() if ln.startswith("FAIL")]
    status = "PASS" if proc.returncode == 0 else "FAIL"
    return suite, status, tally, fails


def main() -> int:
    """Plant and run every requested mutant; write one receipt."""
    clone, rev, scratch, receipt = sys.argv[1:5]
    ids = sys.argv[5:] or list(MUTANTS)
    sha = subprocess.run(["git", "-C", clone, "rev-parse", rev], check=True,
                         capture_output=True, text=True).stdout.strip()
    lines = [f"# mutation probes at {sha}", ""]
    for mid in ids:
        desc, edits = MUTANTS[mid]
        tree = pathlib.Path(scratch) / mid
        export(clone, rev, tree)
        lines.append(f"## {mid}: {desc}")
        try:
            lines += ["planted " + s for s in plant(tree, edits)]
        except ValueError as err:
            lines += [f"NOT PLANTED: {err}", ""]
            continue
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda s: run_suite(tree, s), SUITES))
        killed = False
        for suite, status, tally, fails in results:
            lines.append(f"{status} {suite} ({tally})")
            lines += ["    " + f for f in fails[:12]]
            if len(fails) > 12:
                lines.append(f"    ... {len(fails) - 12} more FAIL lines")
            killed = killed or status == "FAIL"
        verdict = "KILLED" if killed else "SURVIVED"
        if mid == "K0":
            verdict = "CONTROL FAILED" if killed else "CONTROL PASSES"
        lines += [f"=> {mid} {verdict}", ""]
        print(f"{mid}: {verdict}", flush=True)
    pathlib.Path(receipt).write_text("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
