#!/usr/bin/env python3
"""Check the page's step-context and counter claims against archived analyses.

Usage: step_context_check.py <archive_dir>
For each cycle's author/cycleNN/analysis.json:
  * servo state (MCSRV_STAT[2:0], 5 = HOLDOVER) in force at both ends of the
    large-PHC-discontinuity bracket;
  * whether any DUT or peer CRF PDU was captured between the last wire frame
    before the gap and the step bracket end (first_after_on > bracket end);
  * DUT and peer AVB_INTERFACE LINK_UP/LINK_DOWN (counter-9-0 quadlets 0/1)
    first values and deltas; DUT MAC_STATUS value set;
  * outage media recovery interval = servo_locked_at / media_locked_at /
    tu=0 latest minus bracket, for comparison with the page column.
Exit 1 if any cycle contradicts the page's HOLDOVER / streams-absent /
flat-counter / MAC_STATUS claims.
"""
import json
import os
import sys


def state_at(changes, t):
    cur = None
    for ts, v in changes:
        if ts <= t:
            cur = v
    return cur


def main() -> int:
    adir = sys.argv[1]
    bad = 0
    for n in range(1, 11):
        a = json.load(open(os.path.join(adir, f"author/cycle{n:02d}/analysis.json")))
        steps = a["large_phc_discontinuities"]
        b0, b1 = steps[0]["bracket"]
        s0, s1 = state_at(a["servo_states"], b0), state_at(a["servo_states"], b1)
        dut_first, peer_first = a["wire"]["dut"]["first_after_on"], a["wire"]["peer"]["first_after_on"]
        absent = dut_first > b1 and peer_first > b1 and a["last_wire_before_gap"] < b0
        dut_link = a["counter_endpoints"]["dut:counter-9-0"]
        peer_link = a["counter_endpoints"]["peer:counter-9-0"]
        flat = all(x["first"]["0"] == 1 and x["first"]["1"] == 0 and x["delta"]["0"] == 0
                   and x["delta"]["1"] == 0 for x in (dut_link, peer_link))
        macs = sorted({v for _, v in a["mac_status"]})
        tu0 = [t for t, h in a["health"] if h[2] == "0" and t > b0]
        end = max(a["servo_locked_at"], a["media_locked_at"]["dut"], tu0[0] if tu0 else 0)
        ok = s0 == 5 and s1 == 5 and absent and flat and macs == [13] and len(steps) == 1
        bad += not ok
        print(f"cycle {n:2d}: steps {len(steps)} amount {steps[0]['phc_minus_wall_delta_s']:.2f} s; "
              f"servo at bracket {s0}/{s1}; DUT/peer first PDU after bracket end "
              f"+{dut_first - b1:.2f}/+{peer_first - b1:.2f} s; streams absent {absent}; "
              f"link counters flat (DUT, peer) {flat}; MAC_STATUS {macs}; "
              f"media recovery {end - b1:.2f}-{end - b0:.2f} s; {'OK' if ok else 'CONTRADICTS PAGE'}")
    print("RESULT", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
