#!/usr/bin/env python3
"""Recompute the per-cycle table and the #387 step-context claims from the
public archive's author/cycleNN/analysis.json files.

Usage: recompute_cycles.py <page.md> <archive-dir review-evidence/394-387-r1>
Per cycle it checks, independently of the author's report script:
  - OFF duration, GM return, PHC step bracket, gPTP recovery, first DUT/peer
    PDU (all relative to OFF) and the outage media recovery interval
    (endpoint = latest of DUT MEDIA_LOCKED and servo LOCKED, minus the bracket)
    against the page row, to the page's two decimals (+/-0.01);
  - the media servo (MCSRV_STAT state 5 = HOLDOVER) is in HOLDOVER for the
    whole step bracket;
  - neither CRF stream had a PDU on the wire at the step: the last PDU before
    the gap precedes the bracket and the first PDU after power-on follows it;
  - MAC_STATUS stayed 0x0d and LINK_UP/LINK_DOWN (AVB_INTERFACE counter
    indices 0/1) did not move.
"""
import json, os, re, sys

HOLDOVER = 5


def page_rows(page):
    rows = {}
    for line in open(page, encoding="utf-8"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 9 and c[0].isdigit():
            rows[int(c[0])] = c
    return rows


def state_at(series, t):
    s = None
    for ts, v in series:
        if ts <= t:
            s = v
    return s


def states_in(series, t0, t1):
    out = {state_at(series, t0)}
    out |= {v for ts, v in series if t0 <= ts <= t1}
    return out


def close(a, b):
    return abs(a - b) <= 0.0101


def main():
    page, root = sys.argv[1], sys.argv[2]
    rows = page_rows(page)
    ok = True
    for c in range(1, 11):
        a = json.load(open(os.path.join(root, "author", f"cycle{c:02d}", "analysis.json")))
        off = a["off"]
        steps = a["large_phc_discontinuities"]
        b0, b1 = steps[0]["bracket"]
        endpoint = max(a["media_locked_at"]["dut"], a["servo_locked_at"])
        dut, peer = a["wire"]["dut"], a["wire"]["peer"]
        calc = {
            "off": a["off_hold_s"],
            "gm": a["first_gm"] - off,
            "step0": b0 - off, "step1": b1 - off,
            "rec": a["gptp_recovery_s"],
            "pdu_dut": dut["first_after_on"] - off, "pdu_peer": peer["first_after_on"] - off,
            "med0": endpoint - b1, "med1": endpoint - b0,
        }
        r = rows[c]
        gm, st = r[3].split(" / ")
        s0, s1 = st.split("-")
        pd, pp = r[5].split(" / ")
        m0, m1 = r[6].split("-")
        want = {"off": r[1], "gm": gm, "step0": s0, "step1": s1, "rec": r[4],
                "pdu_dut": pd, "pdu_peer": pp, "med0": m0, "med1": m1}
        diffs = [k for k in want if not close(float(want[k]), calc[k])]
        hold = states_in(a["servo_states"], b0, b1)
        in_holdover = hold == {HOLDOVER}
        # last PDU before the outage gap: the latest wire mr/PDU landmark before OFF+gap
        last_before = a.get("last_wire_before_gap")
        dut_absent = dut["first_after_on"] > b1 and (last_before is None or last_before < b0)
        peer_absent = peer["first_after_on"] > b1 and (last_before is None or last_before < b0)
        macs = {v for _, v in a["mac_status"]}
        ce = a["counter_endpoints"]["dut:counter-9-0"]["delta"]
        link_flat = ce.get("0") == 0 and ce.get("1") == 0
        nsteps = len(steps)
        good = (not diffs and in_holdover and dut_absent and peer_absent
                and macs == {0x0d} and link_flat and nsteps == 1)
        ok &= good
        print(f"cycle {c:2d}: row-diffs={diffs or 'none'} steps={nsteps} "
              f"servo-states-over-bracket={sorted(hold)} holdover={in_holdover} "
              f"dut-first-PDU-after-step={dut['first_after_on'] - b1:+.2f}s "
              f"peer-first-PDU-after-step={peer['first_after_on'] - b1:+.2f}s "
              f"wire-silent-before-step={last_before is not None and last_before < b0} "
              f"MAC_STATUS={sorted(hex(m) for m in macs)} LINK_UP/DOWN-delta={ce.get('0')}/{ce.get('1')} "
              f"{'OK' if good else 'FAIL'}")
    print("RESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
