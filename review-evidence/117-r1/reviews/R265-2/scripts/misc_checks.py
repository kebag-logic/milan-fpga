#!/usr/bin/env python3
"""Spot-check Step 4, Step 5 and the asCapable-return claims.

usage: misc_checks.py <archive-dir>   (review-evidence/117-r1)
"""
import json
import re
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import step3 as S  # noqa: E402
import tapdec as T  # noqa: E402


def main():
    root = Path(sys.argv[1])
    a2 = root / "bench-a200" / "bench"
    # Step 4: Run A controller polls of the DUT
    ev = [json.loads(line) for line in (a2 / "runA" / "pw1-watch.jsonl").read_text().splitlines()]
    info = [x for x in ev if x.get("cmd") == "GET_AVB_INFO" and x.get("target") == T.DUT
            and x.get("status") == "SUCCESS"]
    path = [x for x in ev if x.get("cmd") == "GET_AS_PATH" and x.get("target") == T.DUT
            and x.get("status") == "SUCCESS"]
    pd = [x["decoded"]["pdelay_ns"] for x in info]
    print(f"Run A DUT GET_AVB_INFO: {len(info)} polls, gm switch {sum(x['decoded']['gm'] == T.SWITCH for x in info)}, "
          f"as_capable {sum(x['decoded']['as_capable'] == 1 for x in info)}, flags {sorted({x['decoded']['flags'] for x in info})}, "
          f"propagation_delay {min(pd)}..{max(pd)} median {st.median(pd)}")
    print(f"Run A DUT GET_AS_PATH: {len(path)} polls, paths {sorted({tuple(x['decoded']['path']) for x in path})}")
    # CLKV_TUCNT over Run A, Run B and final
    tuc = []
    for f in ("runA/console.txt", "runB/console.txt", "final/console-final.txt"):
        _s, mem = S.console(a2 / f)
        tuc += [int.from_bytes(bytes.fromhex(b.replace(" ", "")), "little") for _t, b in mem.get("90000780", [])]
    print(f"CLKV_TUCNT values over Run A, Run B and final: {sorted(set(tuc))} ({len(tuc)} reads)")
    s, _m = S.console(a2 / "runB" / "console.txt")
    print(f"Run B CLKV_STAT[0]: {sum(int(x['CLKV_STAT'], 16) & 1 for x in s)} set in {len(s)} samples")
    # Step 5: counters probe parity
    p1 = (root / "bench-a200/bench/runC/counters-probe-020000fffe000001.log").read_text().splitlines()
    p2 = (root / "bench-a200/bench/runC/counters-probe-3cc0c60102030000.log").read_text().splitlines()
    norm = lambda ls: [re.sub(r"0x[0-9a-fA-F]{16}|[0-9a-f]{16}", "<eid>", l) for l in ls]
    print(f"counters probe: DUT {len(p1)} lines, peer {len(p2)} lines, identical after entity-id masking: "
          f"{norm(p1) == norm(p2)}; byte-identical files: {p1 == p2}")
    enum = (root / "bench-a200/bench/runC/a200-enum.log").read_text()
    for k in ("Milan mandatory counters missing for STREAM_INPUT", "Entity not fully Milan compliant", "IEEE17221", "MILAN"):
        print(f"enumeration log contains {k!r}: {k in enum}")
    # asCapable return vs the DUT's second completed Pdelay exchange after the return
    a3 = root / "bench-a202" / "bench"
    for c in range(1, 7):
        cd = a3 / f"cycle{c}"
        ps = (cd / "powerstrip.txt").read_text()
        t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1))
        off = S.offsets(cd)
        t0 = t_off - off["pi"]
        cap = [v for k, v in off.items() if k.startswith("ubuntu")][0]
        recs, _h = T.tap_records(cd / f"tap-c{c}.pcap")
        fit, _r = T.host_fit(recs)
        for r in recs:
            r["r"] = fit(r["tap_ns"]) / 1e9 - cap - t0
            r["d"] = T.decode(r["frame"])
        sw = [r for r in recs if r["port"] == 2]
        gi = max(range(1, len(sw)), key=lambda i: sw[i]["r"] - sw[i - 1]["r"])
        t_ret = sw[gi]["r"]
        after = [r for r in recs if r["r"] >= t_ret - 3 and r["d"]["et"] == 0x88F7 and "mt" in r["d"]]
        reqs = [r for r in after if r["port"] == 3 and r["d"]["mt"] == 2]
        fus = {(r["d"]["seq"]): r for r in after if r["port"] == 2 and r["d"]["mt"] == 0xA
               and r["d"]["reqport"].startswith(T.DUT)}
        done = sorted(fus[r["d"]["seq"]]["r"] for r in reqs if r["d"]["seq"] in fus and fus[r["d"]["seq"]]["r"] > t_ret)
        s, _m = S.console(cd / "console.txt")
        for x in s:
            x["r"] = x["t"] - t0
        asc1 = next(x for x in s if x["r"] > 20 and x.get("ASCAPABLE") == "1")
        print(f"cycle {c}: 2nd completed DUT Pdelay exchange after return {done[1]:.2f}, console asCapable=1 "
              f"{asc1['r']:.2f} (diff {asc1['r'] - done[1]:.2f}), PDELAY at that sample {asc1.get('PDELAY_NS')}")


if __name__ == "__main__":
    main()
