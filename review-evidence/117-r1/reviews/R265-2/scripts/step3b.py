#!/usr/bin/env python3
"""Re-derive the Step 3 loss-edge, counter, PHC and stream claims.

usage: step3b.py <bench-a202 dir>

Same clocks as step3.py. Console mem_read words are little-endian.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import step3 as S  # noqa: E402
import tapdec as T  # noqa: E402

A_TUCNT, A_LINKG, A_EPOCH, A_CRFT, A_CRFCNT = "90000780", "90000774", "90000720", "90000750", "90000764"


def word(b):
    return int.from_bytes(bytes.fromhex(b.replace(" ", "")), "little")


def main():
    root = Path(sys.argv[1])
    on_prev = None
    for c in range(1, 7):
        cd = root / "bench" / f"cycle{c}"
        ps = cd.joinpath("powerstrip.txt").read_text()
        t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1))
        t_on = float(re.search(r"T_ON_CMD (\S+)", ps).group(1))
        off = S.offsets(cd)
        pi = off["pi"]
        cap = [v for k, v in off.items() if k.startswith("ubuntu")][0]
        t0 = t_off - pi
        s, mem = S.console(cd / "console.txt")
        for x in s:
            x["r"] = x["t"] - t0
        mem = {a: [(t - t0, word(b)) for t, b in v] for a, v in mem.items()}
        recs, _h = T.tap_records(cd / f"tap-c{c}.pcap")
        fit, _res = T.host_fit(recs)
        for r in recs:
            r["r"] = fit(r["tap_ns"]) / 1e9 - cap - t0
            r["d"] = T.decode(r["frame"])
        sw = [r for r in recs if r["port"] == 2]
        gi = max(range(1, len(sw)), key=lambda i: sw[i]["r"] - sw[i - 1]["r"])
        pre = sw[:gi]

        def last(pred):
            v = [r["r"] for r in pre if pred(r["d"])]
            return v[-1] if v else None
        l_sync = last(lambda d: d.get("mt") == 0 and d["et"] == 0x88F7)
        l_ann = last(lambda d: d.get("mt") == 0xB and d["et"] == 0x88F7)
        l_presp = last(lambda d: d.get("mt") == 3 and d["et"] == 0x88F7)
        l_any = pre[-1]["r"]

        def first(pred, after=0.0):
            for x in s:
                if x["r"] > after and pred(x):
                    return x
            return None
        sync0 = first(lambda x: x.get("SYNC") == "0")
        gm_self = first(lambda x: x.get("GPTP_GM") == T.DUT)
        asc0 = first(lambda x: x.get("ASCAPABLE") == "0")
        # holdover bit 3 at the loss edge
        hold = [x for x in s if 0 < x["r"] < 10 and int(x.get("CLKV_STAT", "0"), 16) & 8]
        hold_first = hold[0]["r"] if hold else None
        hold_clear = first(lambda x: not (int(x.get("CLKV_STAT", "0"), 16) & 8), after=hold_first or 0)
        tuc = mem.get(A_TUCNT, [])
        linkg = mem.get(A_LINKG, [])
        l03 = next((t for t, v in linkg if t > 0 and v & 0xFF == 0x03), None)
        epoch = sorted({v for _t, v in mem.get(A_EPOCH, [])})
        # PHC step: TAI_NS jump against wall time
        steps = []
        for a, b in zip(s, s[1:]):
            if "TAI_NS" in a and "TAI_NS" in b:
                dt = (int(b["TAI_NS"], 16) - int(a["TAI_NS"], 16)) / 1e9 - (b["t"] - a["t"])
                if abs(dt) > 1:
                    steps.append(round(dt, 1))
        gaps = max(b["t"] - a["t"] for a, b in zip(s, s[1:]))
        line = (f"cycle {c}: sync0-lastSync {sync0['r'] - l_sync:.2f}; gmself-lastAnn {gm_self['r'] - l_ann:.2f}; "
                f"ascap0-lastPresp {asc0['r'] - l_presp:.2f}; holdover samples {len(hold)} "
                f"first-set->first-clear {hold_clear['r'] - hold_first:.2f}; "
                f"LINKG 0x03 - last rx frame {l03 - l_any:.2f}; TUCNT delta {tuc[-1][1] - tuc[0][1]}; "
                f"RST_EPOCH values {epoch}; PHC steps {steps}; "
                f"on-on interval {'' if on_prev is None else round(t_on - on_prev, 1)}; "
                f"milan_status samples {len(s)}, largest gap {gaps:.3f} s")
        print(line)
        on_prev = t_on
        if c >= 4:
            crf = [r for r in recs if r["port"] == 3 and r["d"].get("subtype") == 4]
            loss = [r for r in crf if 0 < r["r"] < 20]
            tu1 = [r for r in loss if r["d"]["tu"] == 1]
            ret = [r for r in crf if r["r"] > 30]
            crft = mem.get(A_CRFT, [])
            drop = next((t for t, v in crft if t > 0 and v == 0x3), None)
            relic = next((t for t, v in crft if t > 30 and v != 0x3), None)
            tu_rise = first(lambda x: int(x.get("CLKV_STAT", "0"), 16) & 1)
            prev = max((x for x in s if x["r"] < tu_rise["r"]), key=lambda x: x["r"])
            print(f"  CRF: first tu=1 PDU {tu1[0]['r']:.2f} (CLKV_STAT[0] rose between {prev['r']:.2f} and "
                  f"{tu_rise['r']:.2f}); tu=1 PDUs {len(tu1)}; emission end {loss[-1]['r']:.2f}; "
                  f"licence drop (CRFT_CTRL=0x3) {drop:.2f}; relicensed {relic:.2f}; first PDU after return "
                  f"{ret[0]['r']:.2f}; tu values after return {sorted({r['d']['tu'] for r in ret})}; "
                  f"licensed CRFT_CTRL values {sorted({hex(v) for t, v in crft if v != 3})}")


if __name__ == "__main__":
    main()
