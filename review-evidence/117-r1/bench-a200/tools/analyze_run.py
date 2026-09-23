#!/usr/bin/env python3
"""Correlate one bench run's console CSR samples, controller AECP samples and tap
capture (issue 117, A200).

usage: analyze_run.py <run_dir> <pcap> [--host-offset-s <capture_host_minus_build_box>]

Reads <run_dir>/console.txt (console_poll.py transcript) and
<run_dir>/pw1-watch.jsonl (avdecc_ro.py watch output) when present, and the
tap capture through wire_summary.py's decoder. Prints facts; asserts nothing.
"""
import json
import re
import statistics as st
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wire_summary as ws  # noqa: E402

STATUS_RE = re.compile(
    r"GPTP_GM=(?P<gm>[0-9a-f]{16}) GPTP_PARENT=(?P<parent>[0-9a-f]{16}) PDELAY_NS=(?P<pdelay>\d+) "
    r"AS_PATH_COUNT=(?P<pc>\d+) AS_PATH_GEN=(?P<pg>\d+) CLKV_STAT=(?P<clkv>[0-9a-f]{8}) "
    r"SYNC=(?P<sync>\d) ASCAPABLE=(?P<asc>\d) TU=(?P<tu>\d) GPTP_LAT=(?P<lat>[0-9a-f]{8})")
TAI_RE = re.compile(r"TAI_NS=0x(?P<tai>[0-9a-f]+)")
MEM_RE = re.compile(r"^0x(?P<addr>[0-9a-f]{8})\s+(?P<b>(?:[0-9a-f]{2} ){4})", re.M)
HDR_RE = re.compile(r"^### (?P<ts>\S+)Z cmd='(?P<cmd>[^']*)'", re.M)

NAMES = {0x9000062C: "ADP_GPTP_DOMAIN", 0x90000644: "ADP_STATUS(available_index)",
         0x90000780: "CLKV_TUCNT", 0x900007E4: "ASP_CMD", 0x900007E8: "GPTP_DROPW",
         0x900007EC: "GPTP_DROPE", 0x90000774: "LINKG_STAT", 0x90000720: "RST_EPOCH",
         0x900006F4: "CTLR_DIAG", 0x90000750: "CRFT_CTRL", 0x90000764: "CRFT_COUNT",
         0x9000066C: "ACMP_TALKER", 0x90000660: "AAF_FRAMES", 0x900006A4: "ACMPL_STATE"}


def parse_console(path):
    text = Path(path).read_text(errors="replace")
    blocks = []
    heads = list(HDR_RE.finditer(text))
    for i, h in enumerate(heads):
        body = text[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        t = datetime.strptime(h["ts"], "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc).timestamp()
        blocks.append((t, h["cmd"], body))
    samples = []
    cur = None
    for t, cmd, body in blocks:
        if cmd == "milan_status":
            m = STATUS_RE.search(body)
            ta = TAI_RE.search(body)
            cur = dict(t=t, **(m.groupdict() if m else {"parse": "FAILED"}))
            if ta:
                cur["tai_ns"] = int(ta["tai"], 16)
            samples.append(cur)
        elif cmd.startswith("mem_read") and cur is not None:
            m = MEM_RE.search(body)
            if m:
                addr = int(m["addr"], 16)
                cur[NAMES.get(addr, hex(addr))] = int.from_bytes(bytes.fromhex(m["b"].replace(" ", "")), "little")
    return samples


def summarize_console(samples):
    print(f"\n== console samples: {len(samples)}")
    if not samples:
        return
    print(f"   first {datetime.fromtimestamp(samples[0]['t'], timezone.utc).isoformat()}  "
          f"last {datetime.fromtimestamp(samples[-1]['t'], timezone.utc).isoformat()}")
    for k in ("gm", "parent", "pc", "pg", "clkv", "sync", "asc", "tu", "lat"):
        print(f"   {k:8s} values {dict(Counter(s.get(k) for s in samples))}")
    pd = [int(s["pdelay"]) for s in samples if "pdelay" in s]
    print(f"   PDELAY_NS n={len(pd)} median={st.median(pd)} min={min(pd)} max={max(pd)}")
    for name in NAMES.values():
        vals = [s[name] for s in samples if name in s]
        if not vals:
            continue
        if len(set(vals)) <= 3:
            print(f"   {name:28s} values {[hex(v) for v in sorted(set(vals))]}")
        else:
            print(f"   {name:28s} first {vals[0]:#010x} last {vals[-1]:#010x} distinct {len(set(vals))}")
    tai = [(s["t"], s["tai_ns"]) for s in samples if "tai_ns" in s]
    if len(tai) > 1:
        rates = [((b[1] - a[1]) / 1e9) / (b[0] - a[0]) for a, b in zip(tai, tai[1:])]
        print(f"   PHC seconds per build-box second: median {st.median(rates):.6f} "
              f"min {min(rates):.6f} max {max(rates):.6f}")


def summarize_watch(path):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.startswith("{")]
    print(f"\n== controller-host AECP poll: {len(rows)} records")
    by = defaultdict(list)
    for r in rows:
        if r.get("type") in ("avb_info", "as_path"):
            by[(r["target"], r["type"])].append(r)
    for (tgt, typ), rs in sorted(by.items()):
        stc = Counter(r["status"] for r in rs)
        dec = Counter(json.dumps({k: v for k, v in r.get("decoded", {}).items() if k != "pdelay_ns"},
                                 sort_keys=True) for r in rs)
        line = f"   {tgt} {typ}: status {dict(stc)}"
        print(line)
        for d, n in dec.items():
            print(f"      x{n} {d}")
        if typ == "avb_info":
            pd = [r["decoded"]["pdelay_ns"] for r in rs if "decoded" in r]
            if pd:
                print(f"      propagation_delay n={len(pd)} median={st.median(pd)} min={min(pd)} max={max(pd)}")
        rtt = [r["rtt_ms"] for r in rs if "rtt_ms" in r]
        if rtt:
            print(f"      response time ms median={st.median(rtt):.3f} max={max(rtt):.3f}")
    adp = [r for r in rows if r.get("type") == "adp"]
    gm = Counter((r["entity_id"], r["gptp_gm"]) for r in adp)
    print(f"   ADP seen by the controller host: {dict(gm)}")


def pdelay_exchanges(recs, requester_port):
    """Pair Req (requester_port) with Resp/Resp_FU (the other port) by seq and requester id."""
    reqs = [r for r in recs if r["kind"] == "gPTP Pdelay_Req" and r["port"] == requester_port]
    other = 5 - requester_port
    resp = {(r["ptp"]["req_port_id"], r["ptp"]["seq"]): r for r in recs
            if r["kind"] == "gPTP Pdelay_Resp" and r["port"] == other}
    fu = {(r["ptp"]["req_port_id"], r["ptp"]["seq"]): r for r in recs
          if r["kind"] == "gPTP Pdelay_Resp_Follow_Up" and r["port"] == other}
    out = []
    missing = 0
    for q in reqs:
        k = (q["ptp"]["src_port_id"], q["ptp"]["seq"])
        if k not in resp or k not in fu:
            missing += 1
            continue
        rs, f = resp[k], fu[k]
        claimed = (f["ptp"]["body_ts"] + f["ptp"]["corr_ns"]) - (rs["ptp"]["body_ts"] + rs["ptp"]["corr_ns"])
        out.append(dict(tap_turn=rs["tap_ns"] - q["tap_ns"], fu_lag=f["tap_ns"] - rs["tap_ns"],
                        claimed=claimed, diff=(rs["tap_ns"] - q["tap_ns"]) - claimed))
    return out, missing, len(reqs)


def dist(v):
    v = sorted(v)
    p99 = v[min(len(v) - 1, int(round(0.99 * (len(v) - 1))))]
    return f"n={len(v)} median={st.median(v):.1f} min={v[0]:.1f} p99={p99:.1f} max={v[-1]:.1f}"


def within(v, nominal, frac):
    lo, hi = nominal * (1 - frac), nominal * (1 + frac)
    return sum(1 for x in v if lo <= x <= hi), len(v)


def summarize_wire(pcap, samples, host_offset_s):
    recs = sorted((ws.decode(r) for r in ws.records(pcap)), key=lambda d: d["tap_ns"])
    print(f"\n== wire: {len(recs)} tapped records, host-generated excluded {ws.HOST_RECORDS[0]}")
    for port, who in ((2, "far end (bridge port 1) as requester, DUT responds"),
                      (3, "DUT as requester, bridge responds")):
        ex, miss, n = pdelay_exchanges(recs, port)
        print(f"   Pdelay {who}: requests {n}, complete exchanges {len(ex)}, incomplete {miss}")
        if ex:
            print(f"      tap turnaround ns   {dist([e['tap_turn'] for e in ex])}")
            print(f"      Resp->Resp_FU lag ns {dist([e['fu_lag'] for e in ex])}")
            print(f"      claimed t3-t2 ns    {dist([e['claimed'] for e in ex])}")
            print(f"      tap - claimed ns    {dist([e['diff'] for e in ex])}")
    for kind, port, nominal in (("gPTP Sync", 2, 125.0), ("gPTP Announce", 2, 1000.0),
                                ("gPTP Pdelay_Req", 2, 1000.0), ("gPTP Pdelay_Req", 3, 1000.0)):
        ts = [r["tap_ns"] for r in recs if r["kind"] == kind and r["port"] == port]
        iv = ws.intervals_ms(ts)
        if iv:
            k30, n30 = within(iv, nominal, 0.30)
            print(f"   {kind} port {port}: intervals {ws.fmt_stats(iv)}; within +/-30% of {nominal} ms: {k30}/{n30}")
    ann = [r for r in recs if r["kind"] == "gPTP Announce"]
    print(f"   Announce GM identities {dict(Counter(r['ptp']['gm_id'] for r in ann))} "
          f"stepsRemoved {dict(Counter(r['ptp']['steps_removed'] for r in ann))} "
          f"PathTrace {dict(Counter(json.dumps(r['ptp']['tlvs']) for r in ann))}")
    adp = [r for r in recs if r["kind"] == "ADP" and r["port"] == 3]
    print(f"   DUT ADP gptp_grandmaster_id {dict(Counter(r['adp']['gm_id'] for r in adp))}")
    dut_ptp = Counter(r["kind"] for r in recs if r["port"] == 3 and r["kind"].startswith("gPTP"))
    print(f"   gPTP message kinds the DUT sent: {dict(dut_ptp)}")
    avtp = [r for r in recs if r["kind"] in ("AAF", "CRF")]
    print(f"   AVTP stream frames: {len(avtp)}; by (port, kind, stream, tu): "
          f"{dict(Counter((r['port'], r['kind'], r['avtp']['stream_id'], r['avtp']['tu']) for r in avtp))}")
    fus = [r for r in recs if r["kind"] == "gPTP Follow_Up"]
    tai = [s for s in samples if "tai_ns" in s]
    if fus and tai and host_offset_s is not None:
        errs = []
        for s in tai:
            host_ns = (s["t"] + host_offset_s) * 1e9
            f = min(fus, key=lambda r: abs(r["host_ns"] - host_ns))
            gm_at = f["ptp"]["body_ts"] + f["ptp"]["corr_ns"] + (host_ns - f["host_ns"])
            errs.append((s["tai_ns"] - gm_at) / 1e9)
        print(f"   DUT PHC minus grandmaster time at the console read (coarse, host clocks, "
              f"offset {host_offset_s} s): median {st.median(errs):+.3f} s min {min(errs):+.3f} max {max(errs):+.3f}")
    return recs


def main():
    run = Path(sys.argv[1])
    pcap = sys.argv[2]
    off = float(sys.argv[sys.argv.index("--host-offset-s") + 1]) if "--host-offset-s" in sys.argv else None
    samples = parse_console(run / "console.txt") if (run / "console.txt").exists() else []
    summarize_console(samples)
    if (run / "pw1-watch.jsonl").exists():
        summarize_watch(run / "pw1-watch.jsonl")
    summarize_wire(pcap, samples, off)
    return 0


if __name__ == "__main__":
    sys.exit(main())
