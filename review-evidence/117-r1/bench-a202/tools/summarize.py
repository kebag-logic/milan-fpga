#!/usr/bin/env python3
"""Per-cycle table across the analyzed cycles (issue 117, A202).

usage: summarize.py <bench_dir> <n> [<n> ...]   (reads cycle<n>/analysis.json)

Times are seconds from the outlet-off command of that cycle. "Return" is the
switch's first post-boot Announce or Sync on the tapped DUT link, whichever
came first. Recovery is the first 0.1 s console sample from which the DUT
reads GM = the switch, SYNC=1, ASCAPABLE=1 and TU=0 in every later sample;
the transition lies between the previous sample and that one.
"""
import json
import sys
from pathlib import Path

BOUND_S = 5.0


def main():
    base = Path(sys.argv[1])
    rows = []
    for n in sys.argv[2:]:
        a = json.loads((base / f"cycle{n}" / "analysis.json").read_text())
        g = a["tap"]["switch_gptp"]
        rec = a["recovery"]
        loss = a["dut_loss"]
        peer = a["poll"]["3cc0c60102030000"]["avb_info_transitions"]
        peer_after = [t for t in peer if t[0] is not None and t[0] > 1.5 and t[1] == "SUCCESS"]
        peer_first = peer_after[0] if peer_after else None
        peer_sw = next((t for t in peer_after if t[2] == "3cc0c6fffefe0210"), None)
        dut_ret = a["dut_wire"].get("far-end link to switch Announce/Sync", {})
        dut_post = a["dut_wire"].get("after switch Announce/Sync", {})
        master = []
        for ph in (dut_ret, dut_post):
            k = ph.get("kinds", {})
            if k.get("gPTP Sync"):
                master.append(f"Sync x{k['gPTP Sync']}")
            if k.get("gPTP Announce"):
                master.append(f"Announce x{k['gPTP Announce']} (GM {list(ph.get('announce_gm', {}))})")
        rows.append(dict(
            cycle=n, hold=a["power"]["hold_s"],
            last_sync=g["gPTP Sync"]["last_before"], last_ann=g["gPTP Announce"]["last_before"],
            sync0=loss["sync_0"]["first_seen"], gm_own=loss["gm_changed"]["first_seen"],
            gm_own_value=loss["gm_changed"]["value"], asc0=loss["asCapable_0"]["first_seen"],
            carrier_down=a["pw1_carrier"]["down"], carrier_up=a["pw1_carrier"]["up"],
            far_first=a["tap"]["first_far_end_frame_after"],
            ann1=g["gPTP Announce"]["first_after"], anns=g["gPTP Announce"].get("first_three_after"),
            sync1=g["gPTP Sync"]["first_after"], ret=a["t_return"],
            asc1=rec["asCapable_1"], gm_sw=rec["gm_switch"], sync_1=rec["sync_1"], tu0=rec["tu_0"],
            good=rec["all_good_first"], good_prev=rec["all_good_prev_sample"],
            recovery=rec["from_return_s"], from_ann=rec["from_first_announce_s"],
            from_sync=rec["from_first_sync_s"], from_far=rec["from_first_far_end_frame_s"],
            from_on=rec["from_on_cmd_s"], verdict="PASS" if rec["from_return_s"] <= BOUND_S else "FAIL",
            tucnt=rec["tucnt_start_end"], pg=rec["pg_start_end"], phc_steps=a["phc_steps"],
            dut_gmchg=a["poll"]["020000fffe000001"]["counters_delta"].get("5"),
            peer_gmchg=a["poll"]["3cc0c60102030000"]["counters_delta"].get("5"),
            peer_first=peer_first, peer_switch=peer_sw,
            peer_adp=a["adp"]["3cc0c60102030000"], dut_master=master,
            absent=a["console_absent"], console=a["console"], tap_fit=a["tap_fit"],
            crf_tu=a.get("crf_tu_edges"), crf_bursts=a.get("crf_bursts"),
            peer_rx=a.get("peer_rx_transitions"), watcher=a.get("watcher_events"),
            pre_all_good=a["console"]["pre_all_good"]))
    for r in rows:
        print(json.dumps(r, default=str))
    print()
    print("| Cycle | Hold (s) | DUT sync 0, tu 1 | DUT GM = own | DUT asCapable 0 | Switch first frame | "
          "Switch first Announce | DUT all-good | Recovery from return (s) | 5 s bound |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['cycle']} | {r['hold']:.2f} | {r['sync0']:.2f} | {r['gm_own']:.2f} | {r['asc0']:.2f} | "
              f"{r['far_first']:.2f} | {r['ann1']:.2f} | {r['good']:.2f} | {r['recovery']:.2f} | {r['verdict']} |")
    rec = [r["recovery"] for r in rows]
    print(f"\nrecovery from return: min {min(rec):.3f} max {max(rec):.3f} s over {len(rec)} cycles; "
          f"all within {BOUND_S} s: {all(x <= BOUND_S for x in rec)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
