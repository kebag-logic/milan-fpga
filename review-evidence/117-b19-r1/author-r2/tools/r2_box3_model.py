"""Lane B19 round 2: the box 3 time-base model, derived from the hashed raws; no bench access.

usage: r2_box3_model.py <raw-root> <packet-root>
  reads <raw-root>/cycleNN/{console.jsonl,tap.pcap} and <packet-root>/bench/cycleNN/correlation.json,
  writes <packet-root>/round2/box3-model.json and prints it.

The read-to-PHC offset d. `milan_status` (sw/firmware/milan_baremetal/milan_baremetal.c:1896-1938)
reads GM, parent, PDELAY, AS_PATH and CLKV_STAT first, prints two lines, and only then calls
gettime_ns() (its snapshot takes microseconds, :84-96). correlation.json places each sample at that
PHC read (time p), so the publication words were read at r = p - d. The console is LiteX at
a1e1c3652ec2 (the build's banner): stdio sends every "\n" as "\n\r" (libc/stdio.c:14-24), and
uart_write() returns once the byte is stored in a 128-entry software ring (at most 127 held,
libbase/uart.c:24-29 and :93-118; UART_POLLING is not defined) in front of a 16-deep buffered
hardware FIFO with one output register that holds the byte on the wire until its tenth bit
(cores/uart.py:216-221, :54-99). So the console stores S = 127 + 16 + 1 = 144 bytes, and sends one
byte per tb = 10 bits / 115,200 baud (configs/endstation_ax7101_1x1_tdm8.yaml:51).

With N the bytes of the two lines, Q the bytes already queued when the handler starts and I the
time the line stood idle while bytes were still to be stored:
  lower: the last line byte cannot be stored before Q + N - S - 1 bytes have left, so
         d >= (N - S - 1) * tb, taking Q >= 0;
  upper: d <= (Q + N - S + 1) * tb + I + t_cpu.
Q is bounded by the bytes the console emitted for this command before line 1 (the echo and its
newline), because the poller sends a command only after it has read the previous prompt. I is
bounded per record by its elapsed time less the time to send every byte the record carries
(host latency is included, so the bound is loose, never short). t_cpu = 1 ms allows 100,000 cycles
at the 100 MHz system clock (yaml :43) for formatting 271 characters and the reads.

Placement error u. A PHC-placed sample is moved through the nearest DUT Pdelay response at most
3 s away in PHC time, at rate 1, so its error is at most the largest measured rate difference
between the DUT PHC and the tap clock over that span, plus 0.05 ms for the 0.1 ms rounding of the
published times. A calibrated sample (link dark) carries in addition the spread of the
coarse-minus-placed offset over the PHC-placed samples of the same action.
"""
from pathlib import Path
import json, statistics, sys

TB = 10 / 115200
S = 127 + 16 + 1
T_CPU = 1e-3
ROUND = 0.05e-3
SPAN = 3.0


def console_terms(path):
    n, q, idle, bad = [], [], [], 0
    for line in path.read_text().splitlines():
        r = json.loads(line)
        if r["cmd"] != "milan_status":
            continue
        parts = r["raw"].split("\n")
        if len(parts) < 4 or not parts[1].startswith("ID=") or not parts[2].startswith("GPTP_GM="):
            bad += 1
            continue
        n.append(len(parts[1]) + 2 + len(parts[2]) + 2)
        q.append(len(parts[0]) + 2)
        m = len(r["raw"].encode("latin-1", "replace")) + r["raw"].count("\n")
        idle.append((r["end"] - r["t"]) - m * TB)
    return dict(records=len(n), malformed=bad, N=[min(n), max(n)], Q_max=max(q),
                idle_ms=[round(1e3 * min(idle), 3), round(1e3 * statistics.median(idle), 3), round(1e3 * max(idle), 3)],
                idle_negative=sum(i < 0 for i in idle), idle_max_s=max(idle))


def phc_rate(path, tools):
    sys.path.insert(0, str(tools))
    from wire_summary import records, decode
    import struct
    resp, fu = {}, []
    for rec in records(str(path)):
        if rec["port"] != 3:
            continue
        try:
            d = decode(rec)
        except (IndexError, struct.error):
            continue
        if d.get("kind") == "gPTP Pdelay_Resp":
            resp[d["ptp"]["seq"]] = d["tap_ns"]
        elif d.get("kind") == "gPTP Pdelay_Resp_Follow_Up" and d["ptp"]["seq"] in resp:
            t = resp[d["ptp"]["seq"]]
            if 0 <= d["tap_ns"] - t < 1e8:
                fu.append((t, d["ptp"]["body_ts"] + d["ptp"]["corr_ns"]))
    fu.sort()
    rates, steps = [], 0
    for (ta, pa), (tb_, pb) in zip(fu, fu[1:]):
        dp = pb - pa
        if not 0.5e9 < dp < SPAN * 1e9 + 0.5e9:
            continue
        rate = ((tb_ - ta) - dp) / dp
        if abs(rate) > 1e-3:
            steps += 1
            continue
        rates.append(rate)
    return dict(pairs=len(fu), intervals=len(rates), excluded_steps=steps,
                rate_ppm=[round(1e6 * min(rates), 3), round(1e6 * statistics.median(rates), 3), round(1e6 * max(rates), 3)],
                max_abs_ppm=round(1e6 * max(abs(x) for x in rates), 3))


def main():
    raw, pkt = Path(sys.argv[1]), Path(sys.argv[2])
    tools = Path(__file__).resolve().parent
    out = dict(model="r = p - d - e; d in [d_lo, d_hi]; |e| <= u", tb_s=TB, S_bytes=S, t_cpu_s=T_CPU, span_s=SPAN, actions={})
    for i in range(1, 7):
        name = f"cycle{i:02d}"
        c = console_terms(raw / name / "console.jsonl")
        w = phc_rate(raw / name / "tap.pcap", tools)
        corr = json.loads((pkt / "bench" / name / "correlation.json").read_text())
        lo, med, hi = corr["coarse_minus_placed_ms"]
        u_phc = w["max_abs_ppm"] * 1e-6 * SPAN + ROUND
        u_cal = u_phc + 1e-3 * max(med - lo, hi - med) + ROUND
        d_lo = (c["N"][0] - S - 1) * TB
        d_hi = (c["Q_max"] + c["N"][1] - S + 1) * TB + c["idle_max_s"] + T_CPU
        out["actions"][name] = dict(console=c, phc_vs_tap=w, coarse_minus_placed_ms=[lo, med, hi],
                                    d_lo_s=round(d_lo, 6), d_hi_s=round(d_hi, 6), u_phc_s=round(u_phc, 6), u_cal_s=round(u_cal, 6))
    bad = [n for n, a in out["actions"].items() if a["console"]["idle_negative"] or a["console"]["malformed"] or a["d_lo_s"] <= 0]
    out["model_refuted_in"] = bad
    (pkt / "round2").mkdir(exist_ok=True)
    (pkt / "round2" / "box3-model.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
