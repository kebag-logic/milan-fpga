#!/usr/bin/env python3
"""Dark-window edges, holdover run lengths and final-capture host records.

usage: step3c.py <bench-a202 dir>
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import step3 as S  # noqa: E402
import tapdec as T  # noqa: E402


def main():
    root = Path(sys.argv[1])
    for c in range(1, 7):
        cd = root / "bench" / f"cycle{c}"
        ps = (cd / "powerstrip.txt").read_text()
        t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1))
        off = S.offsets(cd)
        t0 = t_off - off["pi"]
        cap = [v for k, v in off.items() if k.startswith("ubuntu")][0]
        recs, _h = T.tap_records(cd / f"tap-c{c}.pcap")
        fit, _r = T.host_fit(recs)
        for r in recs:
            r["r"] = fit(r["tap_ns"]) / 1e9 - cap - t0
        gi = max(range(1, len(recs)), key=lambda i: recs[i]["r"] - recs[i - 1]["r"])
        last, first = recs[gi - 1], recs[gi]
        d = T.decode(last["frame"])
        kind = {2: "Pdelay_Req", 3: "Pdelay_Resp", 0xA: "Pdelay_Resp_FU", 0: "Sync", 0xB: "Announce"}.get(d.get("mt"), hex(d["et"]))
        s, _m = S.console(cd / "console.txt")
        for x in s:
            x["r"] = x["t"] - t0
        run, best = 0, 0
        for x in s:
            if 0 < x["r"] < 3 and int(x.get("CLKV_STAT", "0"), 16) & 8:
                run += 1
                best = max(best, run)
            else:
                run = 0
        print(f"cycle {c}: silence from {last['r']:.2f} (last record port {last['port']}, {kind}) "
              f"to {first['r']:.2f} (first record port {first['port']}); holdover run at the sync loss "
              f"{best} consecutive samples")
    recs, host = T.tap_records(root / "bench" / "final" / "tap-final.pcap")
    print(f"step 3 final capture: {len(recs)} tap records, {host} host-only records")


if __name__ == "__main__":
    main()
