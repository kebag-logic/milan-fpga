#!/usr/bin/env python3
"""Re-derive the Step 3 controller-view claims from the A202 watcher logs.

usage: step3_ctl.py <bench-a202 dir>

Watcher times are on the controller host's NTP clock and are moved to the
build-box clock with the cycle's mean offset for that host. Times printed
are seconds after the outlet-off command (build-box clock).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import step3 as S  # noqa: E402
import tapdec as T  # noqa: E402

PEER = "3cc0c60102030000"
PEER_CLK = "3cc0c6fffe010203"


def gm_changed(payload_hex):
    """AVB_INTERFACE GET_COUNTERS: descriptor(4) valid(4) then 32 counters."""
    b = bytes.fromhex(payload_hex)
    return int.from_bytes(b[8 + 4 * 5:8 + 4 * 6], "big")


def main():
    root = Path(sys.argv[1])
    for c in range(1, 7):
        cd = root / "bench" / f"cycle{c}"
        ps = cd.joinpath("powerstrip.txt").read_text()
        t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1))
        off = S.offsets(cd)
        t0 = t_off - off["pi"]
        pw = off["pw1"]
        ev = [json.loads(line) for line in cd.joinpath("pw1-watch.jsonl").read_text().splitlines()]
        for x in ev:
            x["r"] = x["t"] - pw - t0
        carrier = [(x["r"], x["value"]) for x in ev if x.get("type") == "carrier"]
        down = next(r for r, v in carrier if v == 0 and r > 0)
        up = next(r for r, v in carrier if v == 1 and r > down)
        polls = [x for x in ev if x.get("type") == "poll" and x["r"] > up and x.get("status") == "SUCCESS"]
        peer_info = [x for x in polls if x["target"] == PEER and x["cmd"] == "GET_AVB_INFO"
                     and x["payload"][:8] == "00090000"]
        dut_info = [x for x in polls if x["target"] == T.DUT and x["cmd"] == "GET_AVB_INFO"]
        first_peer = peer_info[0]
        named = next(x for x in peer_info if x["decoded"]["gm"] == T.SWITCH)
        adp_named = next((x["r"] for x in ev if x.get("type") == "adp" and x["r"] > up
                          and str(x.get("entity_id", x.get("eid", ""))).lower() == PEER
                          and str(x.get("gptp_gm", "")).lower() == T.SWITCH), None)
        adp_self = [round(x["r"], 2) for x in ev if x.get("type") == "adp" and x["r"] > up
                    and str(x.get("entity_id", x.get("eid", ""))).lower() == PEER
                    and str(x.get("gptp_gm", "")).lower() == PEER_CLK]
        ctr = {}
        for x in ev:
            if x.get("type") == "poll" and x.get("cmd") == "GET_COUNTERS" and x.get("status") == "SUCCESS" \
                    and x["payload"][:8] == "00090000":
                ctr.setdefault(x["target"], []).append(gm_changed(x["payload"]))
        dfirst = dut_info[0]["decoded"]
        asc_while_self = any(x["decoded"]["gm"] == T.DUT and x["decoded"]["as_capable"] == 1 for x in dut_info)
        print(f"cycle {c}: carrier down {down:.2f} up {up:.2f}; peer first poll {first_peer['r']:.2f} gm "
              f"{'switch' if first_peer['decoded']['gm'] == T.SWITCH else first_peer['decoded']['gm']} "
              f"as_cap {first_peer['decoded']['as_capable']}; peer names switch {named['r']:.2f} "
              f"(ADP {adp_named if adp_named is None else round(adp_named, 2)}); peer ADP naming itself {adp_self[:3]}; "
              f"GPTP_GM_CHANGED delta DUT {ctr[T.DUT][-1] - ctr[T.DUT][0]} peer {ctr[PEER][-1] - ctr[PEER][0]}; "
              f"DUT first poll gm {'self' if dfirst['gm'] == T.DUT else dfirst['gm']} as_cap {dfirst['as_capable']}; "
              f"DUT as_cap=1 while gm=self seen {asc_while_self}")


if __name__ == "__main__":
    main()
