#!/usr/bin/env python3
"""Re-derive the Step 3 per-cycle table from the A202 raw files.

usage: step3.py <bench-a202 dir>

Clocks: the power-strip log is on its host's NTP clock, the tap pcap host
stamps on the capture server's NTP clock, console stamps on the build
box. Each host's offset to the build box is the mean of the cycle's
before/after clock files (offset_s_median_best5). Tap time is put on the
capture-server clock by tapdec.host_fit. Every time printed is seconds
after the outlet-off command, on the build-box clock.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import tapdec as T  # noqa: E402

HDR = re.compile(r"^### (\S+)Z cmd='([^']*)'")


def offsets(cdir):
    acc = {}
    for f in ("clock-before.jsonl", "clock-after.jsonl"):
        for line in (cdir / f).read_text().splitlines():
            x = json.loads(line)
            role = x["host"].split(">")[-1]
            acc.setdefault(role, []).append(x["offset_s_median_best5"])
    return {k: sum(v) / len(v) for k, v in acc.items()}


def console(path):
    samples, cur = [], None
    mem = {}
    for line in path.read_text(errors="replace").splitlines():
        m = HDR.match(line)
        if m:
            ts = datetime.fromisoformat(m.group(1) + "+00:00").timestamp()
            cur = {"t": ts, "cmd": m.group(2)}
            if m.group(2) == "milan_status":
                samples.append(cur)
            continue
        if cur is None:
            continue
        for k, v in re.findall(r"(\w+)=([0-9a-fA-Fx]+)", line):
            cur[k] = v
        mm = re.match(r"^0x(9000[0-9a-f]{4})\s+((?:[0-9a-f]{2} ){4})", line)
        if mm:
            mem.setdefault(mm.group(1), []).append((cur["t"], mm.group(2)))
    return samples, mem


def main():
    root = Path(sys.argv[1])
    print("cyc off_for sync0 gm_self ascap0 sw_first sw_first_ann sw_first_sync ascap1 gm_sw allgood recovery "
          "sw_last dut_last on->allgood host_recs resid_ms")
    for c in range(1, 7):
        cd = root / "bench" / f"cycle{c}"
        ps = cd.joinpath("powerstrip.txt").read_text()
        t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1))
        t_on = float(re.search(r"T_ON_CMD (\S+)", ps).group(1))
        off = offsets(cd)
        pi = [v for k, v in off.items() if k == "pi"][0]
        cap = [v for k, v in off.items() if k.startswith("ubuntu")][0]
        t0 = t_off - pi
        s, _mem = console(cd / "console.txt")
        for x in s:
            x["r"] = x["t"] - t0

        def first(pred, after=0.0):
            for x in s:
                if x["r"] > after and pred(x):
                    return x["r"]
            return None
        sync0 = first(lambda x: x.get("SYNC") == "0")
        gm_self = first(lambda x: x.get("GPTP_GM") == T.DUT)
        ascap0 = first(lambda x: x.get("ASCAPABLE") == "0")
        ascap1 = first(lambda x: x.get("ASCAPABLE") == "1", after=ascap0)
        gm_sw = first(lambda x: x.get("GPTP_GM") == T.SWITCH, after=gm_self)
        good = [x.get("GPTP_GM") == T.SWITCH and x.get("SYNC") == "1" and x.get("ASCAPABLE") == "1"
                and x.get("TU") == "0" for x in s]
        allgood = None
        for i in range(len(s) - 1, -1, -1):
            if not good[i]:
                allgood = s[i + 1]["r"] if i + 1 < len(s) else None
                break
        recs, host = T.tap_records(cd / f"tap-c{c}.pcap")
        fit, resid = T.host_fit(recs)
        for r in recs:
            r["r"] = fit(r["tap_ns"]) / 1e9 - cap - t0
        sw = [r for r in recs if r["port"] == 2]
        gap_i = max(range(1, len(sw)), key=lambda i: sw[i]["r"] - sw[i - 1]["r"])
        sw_last, sw_first = sw[gap_i - 1]["r"], sw[gap_i]["r"]
        dut_pre = [r for r in recs if r["port"] == 3 and r["r"] < sw_first]
        dut_last = dut_pre[-1]["r"]
        ann = sync = None
        for r in sw[gap_i:]:
            d = T.decode(r["frame"])
            if d["et"] == 0x88F7 and d.get("mt") == 0xB and ann is None:
                ann = r["r"]
            if d["et"] == 0x88F7 and d.get("mt") == 0 and sync is None:
                sync = r["r"]
            if ann and sync:
                break
        rec = allgood - min(ann, sync)
        print(f"{c} {t_on - t_off:.2f} {sync0:.2f} {gm_self:.2f} {ascap0:.2f} {sw_first:.2f} {ann:.2f} "
              f"{sync:.3f} {ascap1:.2f} {gm_sw:.2f} {allgood:.2f} {rec:.2f} {sw_last:.2f} {dut_last:.2f} "
              f"{allgood - (t_on - t_off):.2f} {host} {resid / 1e6:.2f}")


if __name__ == "__main__":
    main()
