#!/usr/bin/env python3
"""Receive half of #106: plant one mutation at a time in the SRP receive RTL,
run the named suites, record the tally and the failing checks, restore every
file, verify each restore by SHA-256.

RX0 arms run the base receive side (the lane's first commit, 9370f8ab, whose
decoder strobes one application-wide rLA! per flagged VectorHeader) against
the new suites. Usage: mutate_rx.py [ARM ...] (no argument = every arm)."""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

LANE = Path("$LANES/pp106-leaveall-scope")
SRP = LANE / "hdl/srp"
OUT = Path("$REVIEWS/pp106-a206-packet/mutations_rx")
ENV = dict(os.environ,
           PATH="$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:" + os.environ["PATH"])
BASE = "9370f8a"
FILES = ["KL_srp_decoder.sv", "KL_srp_talker_fsm.sv", "KL_srp_listener_fsm.sv",
         "KL_srp_top.sv", "srp_pkg.sv"]

DEC = "KL_srp_decoder.sv"
TKF = "KL_srp_talker_fsm.sv"
LSF = "KL_srp_listener_fsm.sv"
TOP = "KL_srp_top.sv"

# tag: (what it plants, {file: [(old, new)]} or "BASE:<files>", [suites])
ARMS = {
    "RX0-dec": ("the base decoder (9370f8ab): one application-wide strobe per "
                "flagged VectorHeader, read by the new suite as lane 0",
                "BASE:" + DEC, ["srp_decoder"]),
    "RX0-top": ("the base receive side (9370f8ab decoder, both FSMs, KL_srp_top, "
                "srp_pkg): per-application rLA! end to end",
                "BASE:" + ",".join(FILES), ["srp_top"]),
    "D1": ("decoder: every lane strobed at every flagged VectorHeader (the old "
           "per-application rLA!, in the new port shape)",
           {DEC: [("              if (la_first_w) begin\n"
                   "                la_done_r[la_lane_w] <= 1'b1;\n"
                   "                if (app_msrp_r) la_msrp_o[la_lane_w] <= 1'b1;\n"
                   "                else            la_mvrp_o            <= 1'b1;\n"
                   "              end",
                   "              if (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C) begin\n"
                   "                if (app_msrp_r) la_msrp_o <= 4'hF;\n"
                   "                else            la_mvrp_o <= 1'b1;\n"
                   "              end")]},
           ["srp_decoder", "srp_top"]),
    "D2": ("decoder: once-per-MRPDU gate removed (every flagged header strobes)",
           {DEC: [("  assign la_first_w = (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C) && !la_done_r[la_lane_w];",
                   "  assign la_first_w = (vhdr1_r[7:5] == SRP_LEAVEALL_EV_C);")]},
           ["srp_decoder"]),
    "D3": ("decoder: the gate is never re-armed at the next MRPDU",
           {DEC: [("            la_done_r  <= 4'd0;          // a new MRPDU: every type may LeaveAll once\n",
                   "")]},
           ["srp_decoder"]),
    "D4": ("decoder: lane = AttributeType instead of AttributeType - 1",
           {DEC: [("  assign la_lane_w  = attr_type_r[1:0] - 2'd1;",
                   "  assign la_lane_w  = attr_type_r[1:0];")]},
           ["srp_decoder"]),
    "T1": ("talker FSM: the Listener registrar ages on every lane",
           {TKF: [("  assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;",
                   "  assign leaveall_any_w = (|leaveall_rx_i) || leaveall_own_i;")]},
           ["srp_stream_fsms"]),
    "T2": ("talker FSM: the Listener registrar deaf to the Listener lane "
           "(takes the Domain lane)",
           {TKF: [("  assign leaveall_any_w = leaveall_rx_i[SRP_LA_LISTENER_C] || leaveall_own_i;",
                   "  assign leaveall_any_w = leaveall_rx_i[SRP_LA_DOMAIN_C] || leaveall_own_i;")]},
           ["srp_stream_fsms"]),
    "T3": ("talker FSM: the applicant takes every lane",
           {TKF: [("      la_rx_app_w[s] = fail_r[s] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]\n"
                   "                                 : leaveall_rx_i[SRP_LA_TALKER_ADV_C];",
                   "      la_rx_app_w[s] = |leaveall_rx_i;")]},
           ["srp_stream_fsms"]),
    "T4": ("talker FSM: the applicant ignores the declared variant "
           "(Talker Advertise lane always)",
           {TKF: [("      la_rx_app_w[s] = fail_r[s] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]\n"
                   "                                 : leaveall_rx_i[SRP_LA_TALKER_ADV_C];",
                   "      la_rx_app_w[s] = leaveall_rx_i[SRP_LA_TALKER_ADV_C];")]},
           ["srp_stream_fsms"]),
    "L1": ("listener FSM: the talker registrar ages on every lane",
           {LSF: [("      leaveall_any_w[s] = leaveall_own_i\n"
                   "                       || (rtype_r[s] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]\n"
                   "                                      : leaveall_rx_i[SRP_LA_TALKER_ADV_C]);",
                   "      leaveall_any_w[s] = leaveall_own_i || (|leaveall_rx_i);")]},
           ["srp_stream_fsms"]),
    "L2": ("listener FSM: the talker registrar ignores the registered type "
           "(Talker Advertise lane always)",
           {LSF: [("      leaveall_any_w[s] = leaveall_own_i\n"
                   "                       || (rtype_r[s] ? leaveall_rx_i[SRP_LA_TALKER_FAILED_C]\n"
                   "                                      : leaveall_rx_i[SRP_LA_TALKER_ADV_C]);",
                   "      leaveall_any_w[s] = leaveall_own_i || leaveall_rx_i[SRP_LA_TALKER_ADV_C];")]},
           ["srp_stream_fsms"]),
    "L3": ("listener FSM: the Listener applicant takes every lane",
           {LSF: [("  assign la_rx_app_w = leaveall_rx_i[SRP_LA_LISTENER_C];",
                   "  assign la_rx_app_w = |leaveall_rx_i;")]},
           ["srp_stream_fsms"]),
    "P1": ("KL_srp_top: every lane broadcast to every plane (per-application "
           "routing at the top)",
           {TOP: [("      .leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
                   "      .leaveall_tick_i     ((|dec_la_msrp_w) || p_la_msrp_r),"),
                  ("      .leaveall_rx_i       (dec_la_msrp_w),",
                   "      .leaveall_rx_i       ({4{|dec_la_msrp_w}}),"),
                  ("      .leaveall_rx_i           (dec_la_msrp_w),",
                   "      .leaveall_rx_i           ({4{|dec_la_msrp_w}}),")]},
           ["srp_top"]),
    "P2": ("KL_srp_top: the Domain participant deaf to the Domain lane "
           "(takes the Listener lane)",
           {TOP: [("      .leaveall_tick_i     (dec_la_msrp_w[SRP_LA_DOMAIN_C] || p_la_msrp_r),",
                   "      .leaveall_tick_i     (dec_la_msrp_w[SRP_LA_LISTENER_C] || p_la_msrp_r),")]},
           ["srp_top"]),
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run_suite(tag: str, suite: str) -> str:
    tb = LANE / "tb" / suite
    log = OUT / f"{tag}_{suite}.log"
    with log.open("w") as fh:
        subprocess.run(["make", "clean"], cwd=tb, env=ENV, stdout=subprocess.DEVNULL)
        rc = subprocess.run(["timeout", "900", "make"], cwd=tb, env=ENV,
                            stdout=fh, stderr=subprocess.STDOUT).returncode
    text = log.read_text(errors="replace")
    tally = re.findall(r"\d+ checks: \d+ PASS, \d+ FAIL", text)
    fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
    return (f"  {suite}: rc={rc} tally={tally[-1] if tally else 'NONE'} "
            f"fail_lines={len(fails)}\n" + "\n".join("    " + l for l in fails[:16]))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    orig = {f: (SRP / f).read_bytes() for f in FILES}
    orig_sha = {f: sha(SRP / f) for f in FILES}
    only = sys.argv[1:]
    summary = []
    try:
        for tag, (what, plant, suites) in ARMS.items():
            if only and tag not in only:
                continue
            if isinstance(plant, str):
                for f in plant.split(":", 1)[1].split(","):
                    (SRP / f).write_bytes(subprocess.run(
                        ["git", "show", f"{BASE}:hdl/srp/{f}"], cwd=LANE,
                        capture_output=True, check=True).stdout)
            else:
                for f, reps in plant.items():
                    s = orig[f].decode()
                    for a, b in reps:
                        assert s.count(a) == 1, (tag, f, a)
                        s = s.replace(a, b)
                    (SRP / f).write_text(s)
            block = [f"== {tag} {what}"]
            for suite in suites:
                block.append(run_suite(tag, suite))
            summary.append("\n".join(block))
            for f in FILES:
                (SRP / f).write_bytes(orig[f])
    finally:
        for f in FILES:
            (SRP / f).write_bytes(orig[f])
    for f in FILES:
        ok = sha(SRP / f) == orig_sha[f]
        summary.append(f"restored {f} sha256 {sha(SRP / f)} {'OK' if ok else 'MISMATCH'}")
    text = "\n".join(summary)
    name = "SUMMARY.txt" if not only else f"SUMMARY_{'_'.join(only)}.txt"
    (OUT / name).write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
