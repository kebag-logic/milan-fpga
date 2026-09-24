#!/usr/bin/env python3
"""Recheck countable claims of the issue 117 findings page from raw files.

Usage: recheck_counts.py <review-evidence/117-r1 directory>

Independent of the packet tools. Checks:
  1. Step 2 cadence over Run A, B, C and final tap captures: Sync, Announce
     and Pdelay_Req intervals per direction, and the Pdelay exchange
     request-to-response times in both directions.
  2. Run B CRF PDUs the DUT sent (tap port 3, AVTP subtype 0x04): count,
     `tu` bit, sequence continuity.
  3. Records without a tap envelope, per tap capture.
  4. Console commands across every console transcript: count by command
     word.
  5. tcpdump logs: the dropped-by-kernel figures.
  6. Step 3 power-strip on-command intervals (observation 7).
"""
import re
import statistics as st
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path

WRAP = 1 << 32


def records(path):
    raw = path.read_bytes()
    off, first, out, noenv = 24, None, [], 0
    while off + 16 <= len(raw):
        s, us, incl, _o = struct.unpack("<IIII", raw[off:off + 16])
        off += 16
        pkt = raw[off:off + incl]
        off += incl
        ok = len(pkt) >= 42 and pkt[:4] == b"\x06\x00\x00\x00"
        if ok:
            tag, _l, port = struct.unpack("<III", pkt[:12])
            w5 = struct.unpack("<I", pkt[20:24])[0]
            ok = port in (2, 3) and w5 == incl - 28
        if not ok:
            noenv += 1
            continue
        host_ns = s * 10**9 + us * 1000
        lo = struct.unpack("<I", pkt[16:20])[0]
        if first is None:
            first = (host_ns, lo)
        k = round(((host_ns - first[0]) - (lo - first[1])) / WRAP)
        out.append((lo - first[1] + k * WRAP, port, pkt[28:]))
    return out, noenv


def l2(fr):
    et = struct.unpack(">H", fr[12:14])[0]
    if et == 0x8100:
        return struct.unpack(">H", fr[16:18])[0], fr[18:]
    return et, fr[14:]


def main():
    root = Path(sys.argv[1])
    a200 = root / "bench-a200" / "bench"
    a202 = root / "bench-a202" / "bench"

    print("== 1. step 2 cadence (Run A, B, C, final)")
    iv = defaultdict(list)
    turn = {2: [], 3: []}
    exch = {2: [0, 0], 3: [0, 0]}
    for run in ("runA/tap-runA.pcap", "runB/tap-runB.pcap", "runC/tap-runC.pcap",
                "final/tap-final.pcap"):
        recs, _ = records(a200 / run)
        last = {}
        pending = {}
        for t, port, fr in recs:
            et, p = l2(fr)
            if et != 0x88F7:
                continue
            mt = p[0] & 0x0F
            key = (port, mt)
            if key in last:
                iv[key].append((t - last[key]) / 1e6)
            last[key] = t
            seq = struct.unpack(">H", p[30:32])[0]
            if mt == 2:
                pending[(port, seq)] = t
                exch[port][0] += 1
            elif mt == 3:
                req_port = 5 - port  # the request came from the other side
                if (req_port, seq) in pending:
                    turn[req_port].append((t - pending.pop((req_port, seq))) / 1e3)
                    exch[req_port][1] += 1
    names = {0: "Sync", 0xB: "Announce", 2: "Pdelay_Req"}
    for (port, mt), v in sorted(iv.items()):
        if mt not in names:
            continue
        src = "switch->DUT" if port == 2 else "DUT->switch"
        within = sum(1 for x in v if abs(x - (125 if mt == 0 else 1000)) <= 0.3 * (125 if mt == 0 else 1000))
        print(f"  {names[mt]:10s} {src}: {len(v)} intervals (includes run gaps), "
              f"within 30%: {within}, max in-run {max(x for x in v if x < 5000):.1f} ms, "
              f"min {min(v):.1f} ms")
    for req_port, v in turn.items():
        who = "switch requests, DUT responds" if req_port == 2 else "DUT requests, switch responds"
        v = sorted(v)
        print(f"  Pdelay {who}: requests {exch[req_port][0]}, answered {len(v)}, "
              f"tap req->resp min {v[0]:.3f} us max {v[-1]:.3f} us; top3 {v[-3:]}")

    print("== 2. Run B CRF PDUs sent by the DUT")
    recs, _ = records(a200 / "runB" / "tap-runB.pcap")
    n = tu1 = gaps = 0
    prev = None
    for t, port, fr in recs:
        et, p = l2(fr)
        if port != 3 or et != 0x22F0 or p[0] != 0x04:
            continue
        n += 1
        tu1 += p[1] & 0x01
        seq = p[2]
        if prev is not None and seq != (prev + 1) & 0xFF:
            gaps += 1
        prev = seq
    print(f"  CRF PDUs {n}, tu=1 {tu1}, sequence discontinuities {gaps}")

    print("== 3. tap records without an envelope")
    for p in sorted(root.rglob("*.pcap")):
        if "pw1" in p.name:
            continue
        _, noenv = records(p)
        print(f"  {p.relative_to(root)}: {noenv}")

    print("== 4. console commands")
    files = sorted(p for p in root.rglob("console*.txt"))
    total = Counter()
    for p in files:
        c = Counter(m.split()[0] if m.split() else "" for m in
                    re.findall(r"^### \S+ cmd='([^']*)'", p.read_text(errors="replace"), re.M))
        total += c
        print(f"  {p.relative_to(root)}: {sum(c.values())} {dict(c)}")
    print(f"  transcripts {len(files)}; total {sum(total.values())}; by word {dict(total)}")

    print("== 5. tcpdump logs")
    logs = sorted(root.rglob("tcpdump*.log"))
    for p in logs:
        m = re.findall(r"(\d+) packets? dropped by kernel", p.read_text())
        print(f"  {p.relative_to(root)}: dropped {m}")
    print(f"  logs: {len(logs)}")

    print("== 6. step 3 outlet on-command intervals")
    ons = []
    for d in ["attempt1-aborted"] + [f"cycle{i}" for i in range(1, 7)]:
        txt = (a202 / d / "powerstrip.txt").read_text()
        ons.append((d, float(re.search(r"T_ON_CMD (\S+)", txt).group(1))))
    for (d0, t0), (d1, t1) in zip(ons, ons[1:]):
        print(f"  {d0} -> {d1}: {t1 - t0:.2f} s")


if __name__ == "__main__":
    main()
