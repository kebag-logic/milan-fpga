#!/usr/bin/env python3
"""Summarize a console_poll.py transcript of the gPTP soak (issue 387, A249). Offline.

Groups the transcript into rounds (a round starts at each milan_status), decodes the
milan_status fields and every mem_read word (little-endian), and reports:
  - per-field value sets (GM, parent, path, CLKV_STAT, SYNC, ASCAPABLE, TU, GPTP_LAT);
  - CLKV_STAT bit counts: [0] tu, [1] sync_ok, [3] discontinuity holdover, [16] asCapable;
  - every change of CLKV_TUCNT (0x780), ASP_CMD (0x7E4), GPTP_DROPW/E, RST_EPOCH, LINKG_STAT,
    with the build-box time of the samples on either side;
  - peer delay statistics; round spacing (to show the 1 s sampling held);
  - PHC (TAI_NS) against the build-box clock: rate and residual (coarse, console latency).

usage: a249_console_summary.py <console.txt> [--json out.json]
"""
import json
import re
import statistics as st
import sys
from datetime import datetime, timezone

HDR = re.compile(r"^### (\S+)Z cmd='(.*)' elapsed=([0-9.]+)s$")
MEM = re.compile(r"^(0x9000[0-9a-f]{4})\s+((?:[0-9a-f]{2} ){3}[0-9a-f]{2})")
KV = re.compile(r"([A-Z_]+)=([0-9A-Za-z]+)")
NAMES = {"0x90000780": "CLKV_TUCNT", "0x900007e4": "ASP_CMD", "0x900007e8": "GPTP_DROPW",
         "0x900007ec": "GPTP_DROPE", "0x90000720": "RST_EPOCH", "0x90000774": "LINKG_STAT",
         "0x9000077c": "CLKV_STAT_MEM", "0x90000750": "CRFT_CTRL"}


def parse(path):
    rounds, cur, cmd, t = [], None, None, None
    for line in open(path, errors="replace"):
        line = line.rstrip("\n")
        m = HDR.match(line)
        if m:
            t = datetime.strptime(m.group(1), "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc).timestamp()
            cmd = m.group(2)
            if cmd == "milan_status":
                cur = {"t": t, "elapsed": float(m.group(3))}
                rounds.append(cur)
            continue
        if cur is None:
            continue
        if cmd == "milan_status":
            if line.startswith("TAI_NS="):
                cur["TAI_NS"] = int(line.split("=")[1], 16)
                cur["t_tai"] = t
            elif "=" in line and (line.startswith("ID=") or line.startswith("GPTP_GM=")):
                for k, v in KV.findall(line):
                    cur[k] = v
        elif cmd.startswith("mem_read"):
            mm = MEM.match(line)
            if mm:
                b = bytes.fromhex(mm.group(2).replace(" ", ""))
                cur[NAMES.get(mm.group(1), mm.group(1))] = int.from_bytes(b, "little")
    return rounds


def iso(t):
    return datetime.fromtimestamp(t, timezone.utc).strftime("%H:%M:%S.%f")[:-3] + "Z"


def main():
    path = sys.argv[1]
    js = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    rounds = parse(path)
    full = [r for r in rounds if "CLKV_STAT" in r and "CLKV_TUCNT" in r]
    print(f"rounds: {len(rounds)} (complete: {len(full)})")
    if not full:
        return 1
    print(f"first {iso(full[0]['t'])}  last {iso(full[-1]['t'])}  span {full[-1]['t'] - full[0]['t']:.3f} s (build-box clock)")
    gaps = [b["t"] - a["t"] for a, b in zip(full, full[1:])]
    print(f"round spacing s: median {st.median(gaps):.3f} min {min(gaps):.3f} max {max(gaps):.3f}; "
          f"gaps > 1.5 s: {sum(g > 1.5 for g in gaps)}")
    for k in ("ID", "VERSION", "GPTP_GM", "GPTP_PARENT", "AS_PATH_COUNT", "AS_PATH_GEN", "CLKV_STAT",
              "SYNC", "ASCAPABLE", "TU", "GPTP_LAT", "AEM"):
        vals = {}
        for r in full:
            vals[r.get(k)] = vals.get(r.get(k), 0) + 1
        print(f"  {k:14s} {vals}")
    bits = {0: "tu", 1: "sync_ok", 3: "holdover", 16: "asCapable"}
    for b, name in bits.items():
        n = sum((int(r["CLKV_STAT"], 16) >> b) & 1 for r in full)
        print(f"  CLKV_STAT[{b}] {name:9s} set in {n} of {len(full)} samples")
    other = [(i, r["CLKV_STAT"]) for i, r in enumerate(full) if r["CLKV_STAT"] != "00010002"]
    print(f"  samples with CLKV_STAT != 00010002: {len(other)} {other[:10]}")
    pd = [int(r["PDELAY_NS"]) for r in full if "PDELAY_NS" in r]
    print(f"  PDELAY_NS n={len(pd)} median={st.median(pd)} min={min(pd)} max={max(pd)} "
          f"mean={st.fmean(pd):.2f} stdev={st.pstdev(pd):.2f}")
    changes = {}
    for k in ("CLKV_TUCNT", "ASP_CMD", "GPTP_DROPW", "GPTP_DROPE", "RST_EPOCH", "LINKG_STAT"):
        seq = [(r["t"], r.get(k)) for r in full]
        ch = [(iso(a[0]), a[1], iso(b[0]), b[1]) for a, b in zip(seq, seq[1:]) if a[1] != b[1]]
        changes[k] = ch
        vals = sorted({v for _, v in seq if v is not None})
        print(f"  {k:11s} first {seq[0][1]:#x} last {seq[-1][1]:#x} distinct {[hex(v) for v in vals]} "
              f"changes {len(ch)} {ch[:10]}")
    tai = [(r["t_tai"], r["TAI_NS"]) for r in full if "TAI_NS" in r]
    if len(tai) > 10:
        xs = [a - tai[0][0] for a, _ in tai]
        ys = [(b - tai[0][1]) / 1e9 for _, b in tai]
        mx, my = st.fmean(xs), st.fmean(ys)
        sxx = sum((x - mx) ** 2 for x in xs)
        slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
        res = [y - (my + slope * (x - mx)) for x, y in zip(xs, ys)]
        steps = [(y2 - y1) - (x2 - x1) for (x1, y1), (x2, y2) in zip(zip(xs, ys), zip(xs[1:], ys[1:]))]
        print(f"  PHC seconds per build-box second (LSQ over {len(tai)} reads): {slope:.9f} "
              f"({(slope - 1) * 1e6:+.3f} ppm; the build box is not NTP-disciplined)")
        print(f"  PHC residual vs that line, ms: min {min(res) * 1e3:+.3f} max {max(res) * 1e3:+.3f} "
              f"stdev {st.pstdev(res) * 1e3:.3f}")
        print(f"  PHC advance minus build-box advance between consecutive reads, ms: "
              f"min {min(steps) * 1e3:+.3f} max {max(steps) * 1e3:+.3f} (console latency jitter bounds this)")
        print(f"  PHC at first read: {tai[0][1]} ns ({tai[0][1] / 1e9:.3f} s); at last: {tai[-1][1]} ns")
    if js:
        with open(js, "w") as f:
            json.dump(dict(rounds=full, changes=changes), f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
