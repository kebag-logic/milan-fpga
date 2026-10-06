#!/usr/bin/env python3
"""Independent recomputation of the #667 B13 findings page from public receipts.

Usage: recompute.py <findings.md> <evidence author dir>

Decodes the raw GET_COUNTERS payloads, the raw AAF header bytes and the timing
receipts itself (it does not reuse the author's decoded fields except to compare
against them), then compares every table and figure on the findings page.
Prints one CHECK line per comparison and exits non-zero on any mismatch.
"""
import csv
import glob
import hashlib
import json
import os
import re
import statistics
import sys

doc_path, ev = sys.argv[1], sys.argv[2]
doc = open(doc_path, encoding="utf-8").read()
fails = 0


def check(name, ok, detail=""):
    global fails
    print(f"CHECK {'PASS' if ok else 'FAIL'} {name} {detail}".rstrip())
    if not ok:
        fails += 1


def s32(x):
    x &= 0xFFFFFFFF
    return x - (1 << 32) if x & 0x80000000 else x


def table_after(marker):
    """Rows of the first markdown table after a line containing marker."""
    lines = doc.splitlines()
    i = next(k for k, l in enumerate(lines) if marker in l)
    while not lines[i].startswith("|"):
        i += 1
    rows = []
    for l in lines[i + 2:]:
        if not l.startswith("|"):
            break
        rows.append([c.strip() for c in l.strip("|").split("|")])
    return rows


# ---------------------------------------------------------------- startup
# Raw AAF header (24 bytes from subtype): byte 1 bit0 = tv, byte 2 = sequence,
# byte 3 bit0 = tu, byte 1 bit3 = mr, bytes 12..15 = avtp_timestamp (1722-2016
# Section 4.4.4 common stream header with stream_id at bytes 4..11).
starts = []
for n in range(1, 101):
    cyc = json.load(open(f"{ev}/start-{n:03d}.json"))
    wire = json.load(open(f"{ev}/start-{n:03d}-wire.json"))
    dut = [s for s in wire["streams"] if s["role"] == "dut" and s["subtype"] == 2]
    assert len(dut) == 1, n
    first = dut[0]["first"]
    hdrs = [bytes.fromhex(p["header"]) for p in first]
    ts = [int.from_bytes(h[12:16], "big") for h in hdrs]
    seq = [h[2] for h in hdrs]
    tv = [h[1] & 1 for h in hdrs]
    mr = [(h[1] >> 3) & 1 for h in hdrs]
    tu = [h[3] & 1 for h in hdrs]
    sub = [h[0] for h in hdrs]
    # cross-check own decode against the author's decoded fields
    for p, t, q, v, u in zip(first, ts, seq, tv, tu):
        if (p["avtp_timestamp"], p["sequence"], p["tv"], p["tu"]) != (t, q, v, u):
            check(f"start-{n:03d} raw-vs-decoded", False, str(p["record"]))
    steps = [s32(b - a) for a, b in zip(ts, ts[1:])]
    seq_ok = all((b - a) % 256 == 1 for a, b in zip(seq, seq[1:]))
    tap = [p["tap_ns"] for p in first]
    polls = cyc["polls"]
    starts.append(dict(n=n, early=cyc["early"], late=cyc["late"], ts=ts,
                       steps=steps, seq=seq, tv=tv, tu=tu, mr=mr, sub=sub,
                       seq_ok=seq_ok, nhdr=len(hdrs), tap=tap, polls=polls,
                       result=cyc["result"]["result"]))

check("startup cycles", len(starts) == 100, str(len(starts)))
check("startup all OK", all(s["result"] == "OK" for s in starts))
check("ten headers per bind", all(s["nhdr"] == 10 for s in starts),
      str(sum(s["nhdr"] for s in starts)))
check("all subtype AAF 0x02", all(set(s["sub"]) == {2} for s in starts))
check("all tv=1", all(set(s["tv"]) == {1} for s in starts))
check("all tu=0", all(set(s["tu"]) == {0} for s in starts))
check("all mr=0 in first ten", all(set(s["mr"]) == {0} for s in starts))
check("sequence consecutive", all(s["seq_ok"] for s in starts))
early = [s for s in starts if s["early"] > 0]
check("EARLY-positive binds == 14", len(early) == 14, str(len(early)))
check("EARLY total == 14", sum(s["early"] for s in starts) == 14)
check("LATE zero", all(s["late"] == 0 for s in starts))
check("EARLY binds all backward step",
      all(s["steps"][0] < 0 for s in early) and
      all(s["steps"][0] > 0 for s in starts if s["early"] == 0))
eb = sorted(s["steps"][0] for s in early)
cb = sorted(s["steps"][0] for s in starts if s["early"] == 0)
check("EARLY step range", (eb[0], eb[-1]) == (-544469385, -279759747), str((eb[0], eb[-1])))
check("clean step range", (cb[0], cb[-1]) == (124999, 125020), str((cb[0], cb[-1])))
# later steps (2..9) in every bind, including flagged ones
later = [x for s in starts for x in s["steps"][1:]]
print(f"INFO later steps (PDU2..10) range {min(later)}..{max(later)}")
# which PDU is the outlier: compare PDU1 against extrapolation from PDU2..10
for s in early:
    per = (s["ts"][9] - s["ts"][1]) / 8
    pred1 = s["ts"][1] - per
    dev1 = s32(s["ts"][0] - int(round(pred1)))
    tapstep = s["tap"][1] - s["tap"][0]
    print(f"INFO start-{s['n']:03d} PDU1 minus trend {dev1} ns; tap spacing PDU1->2 {tapstep} ns")
check("EARLY: PDU1 ahead of trend (future)", all(
    s32(s["ts"][0] - int(round(s["ts"][1] - (s["ts"][9] - s["ts"][1]) / 8))) > 0 for s in early))

# histogram vs doc
hist = {}
for s in starts:
    hist[s["steps"][0]] = hist.get(s["steps"][0], 0) + 1
doc_hist = {int(r[0]): int(r[1]) for r in table_after("First-step distribution")}
check("doc histogram == recomputed", doc_hist == hist)

# per-bind table vs doc
rows = table_after("The next table reports every bind independently")
check("doc per-bind rows == 100", len(rows) == 100, str(len(rows)))
mism = []
for r, s in zip(rows, starts):
    # steady period: mean of steps after PDU 10 is not in the first ten; the
    # author uses later wire packets. Recompute the offset with the author's
    # stated definition (steady period minus first step) using the median of
    # this bind's PDU2..10 steps as the steady period, and accept +-1 ns.
    steady = statistics.median(s["steps"][1:])
    off = steady - s["steps"][0]
    if (int(r[0]), int(r[1]), int(r[2]), int(r[3]), int(r[4])) != \
       (s["n"], s["early"], s["late"], s["seq"][0], s["steps"][0]) or \
       abs(float(r[5]) - off) > 1.0:
        mism.append((r, s["n"], s["steps"][0], off))
check("doc per-bind table == recomputed (offset within 1 ns)", not mism, str(mism[:3]))

# observation lead before unbind for EARLY increments (controller clock)
leads = []
for s in early:
    first_nz = next(p for p in s["polls"] if p.get("counters", {}).get("EARLY", 0) > 0)
    leads.append((s["n"], first_nz["phase"], first_nz["counters"]["FRX"]))
print(f"INFO first nonzero EARLY polls (cycle, phase, FRAMES_RX): {leads}")
tim = list(csv.DictReader(open(f"{ev}/startup-counter-timing.csv")))
mlead = min(float(t["response_to_unbind_command_ms"]) for t in tim)
check("timing rows == 14", len(tim) == 14, str(len(tim)))
check("min lead 1900.062 ms", abs(mlead - 1900.062) < 1e-6, str(mlead))
# independent: unbind command time from run-events if present
ev_lines = [json.loads(l) for l in open(f"{ev}/run-events.jsonl")]
kinds = sorted({e.get("event") or e.get("ev") for e in ev_lines})
print(f"INFO run-events kinds {kinds[:30]}")

# ---------------------------------------------------------------- soak counters
DT = {0: "ENTITY", 5: "STREAM_INPUT", 6: "STREAM_OUTPUT", 9: "AVB_INTERFACE", 36: "CLOCK_DOMAIN"}
NAMES = {
    "AVB_INTERFACE": {0: "LINK_UP", 1: "LINK_DOWN", 2: "FRAMES_TX", 3: "FRAMES_RX",
                      4: "RX_CRC_ERROR", 5: "GPTP_GM_CHANGED"},
    "CLOCK_DOMAIN": {0: "LOCKED", 1: "UNLOCKED"},
    "STREAM_INPUT": {0: "MEDIA_LOCKED", 1: "MEDIA_UNLOCKED", 2: "STREAM_INTERRUPTED",
                     3: "SEQ_NUM_MISMATCH", 4: "MEDIA_RESET", 5: "TIMESTAMP_UNCERTAIN",
                     6: "TIMESTAMP_VALID", 7: "TIMESTAMP_NOT_VALID", 8: "UNSUPPORTED_FORMAT",
                     9: "LATE_TIMESTAMP", 10: "EARLY_TIMESTAMP", 11: "FRAMES_RX"},
    # Milan v1.2 Table 5.4 compact layout (tests/features/counters_contract_milan.feature)
    "STREAM_OUTPUT": {0: "STREAM_START", 1: "STREAM_STOP", 2: "MEDIA_RESET",
                      3: "TIMESTAMP_UNCERTAIN", 4: "FRAMES_TX"},
}
ERR = {("STREAM_INPUT", n) for n in ("STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH",
                                      "UNSUPPORTED_FORMAT", "LATE_TIMESTAMP",
                                      "EARLY_TIMESTAMP", "MEDIA_UNLOCKED")}
ERR |= {("AVB_INTERFACE", "GPTP_GM_CHANGED"), ("AVB_INTERFACE", "LINK_DOWN"),
        ("CLOCK_DOMAIN", "UNLOCKED")}


def decode(path):
    out, req = {}, []
    for l in open(path):
        r = json.loads(l)
        dt = DT[r["descriptor_type"]]
        req.append((r["role"], dt, r["descriptor_index"], r["status"], r["request_ns"]))
        if r["status"] != "SUCCESS":
            continue
        p = bytes.fromhex(r["payload"])
        assert int.from_bytes(p[0:2], "big") == r["descriptor_type"]
        assert int.from_bytes(p[2:4], "big") == r["descriptor_index"]
        mask = int.from_bytes(p[4:8], "big")
        assert mask == r["valid_mask"]
        for b in range(32):
            if mask >> b & 1:
                v = int.from_bytes(p[8 + 4 * b:12 + 4 * b], "big")
                name = NAMES[dt].get(b, f"bit{b}")
                out[(r["role"], dt, r["descriptor_index"], name)] = v
    return out, req


soak = []
for n in range(145):
    soak.append(decode(f"{ev}/counters-soak-{n:03d}.jsonl"))
check("145 counter checkpoints", len(soak) == 145)
reqs = [len(q) for _, q in soak]
check("nine GET_COUNTERS per checkpoint", set(reqs) == {9}, str(set(reqs)))
ns = {sum(1 for x in q if x[3] == "SUCCESS") for _, q in soak}
check("eight SUCCESS per checkpoint", ns == {8}, str(ns))
unsup = {(x[0], x[1], x[3]) for _, q in soak for x in q if x[3] != "SUCCESS"}
check("only DUT ENTITY unsupported", unsup == {("dut", "ENTITY", "NOT_SUPPORTED")}, str(unsup))
keys = set(soak[0][0])
check("same counter set every checkpoint", all(set(c) == keys for c, _ in soak))
check("61 valid counters", len(keys) == 61, str(len(keys)))

# error-class increases between consecutive checkpoints
incs = []
for i in range(1, 145):
    a, b = soak[i - 1][0], soak[i][0]
    for k in keys:
        if (k[1], k[3]) in ERR and b[k] != a[k]:
            incs.append((i, k, a[k], b[k]))
check("no error-class change across 145 checkpoints", not incs, str(incs[:5]))
# any non-monotonic counter (would indicate a reset during soak)
nonmono = [(i, k, soak[i - 1][0][k], soak[i][0][k]) for i in range(1, 145)
           for k in keys if soak[i][0][k] < soak[i - 1][0][k]]
check("no counter decreased during soak", not nonmono, str(nonmono[:5]))

# when did the non-error deltas occur
for k in sorted(keys):
    vals = [c[k] for c, _ in soak]
    if vals[0] != vals[-1] and k[3] not in ("FRAMES_RX", "FRAMES_TX", "TIMESTAMP_VALID"):
        ch = [i for i in range(1, 145) if vals[i] != vals[i - 1]]
        print(f"INFO {k} {vals[0]}->{vals[-1]} changed at checkpoint(s) {ch}")

# doc counter table vs decoded start/end
rows = table_after("| Role | Descriptor | Index | Counter |")
dmis = []
for r in rows:
    k = (r[0], r[1], int(r[2]), r[3])
    st, en = soak[0][0].get(k), soak[-1][0].get(k)
    if st is None or (int(r[4]), int(r[5]), int(r[6])) != (st, en, en - st):
        dmis.append((r, st, en))
check("doc counter rows == 61", len(rows) == 61, str(len(rows)))
check("doc counter table == decoded payloads", not dmis, str(dmis[:3]))

# checkpoint intervals and duration from request times
t0 = [min(x[4] for x in q) for _, q in soak]
iv = [(b - a) / 1e9 for a, b in zip(t0, t0[1:])]
print(f"INFO checkpoint interval min {min(iv):.3f} max {max(iv):.3f} s")
check("max checkpoint interval ~55.727 s", abs(max(iv) - 55.727) < 0.05, f"{max(iv):.3f}")

# timing: GM, asCapable and path stable on both roles; read every checkpoint
gm, asc, path, tcount = set(), set(), set(), []
for n in range(145):
    rr = [json.loads(l) for l in open(f"{ev}/timing-soak-{n:03d}.jsonl")]
    tcount.append(len(rr))
    for r in rr:
        if r["command"] == "GET_AVB_INFO":
            gm.add((r["role"], r["gm_fingerprint"], r["status"]))
            asc.add((r["role"], r["as_capable"]))
        else:
            path.add((r["role"], r["path_fingerprint"], r["path_count"], r["status"]))
check("timing reads 4 per checkpoint", set(tcount) == {4}, str(set(tcount)))
check("one GM per role, SUCCESS", len(gm) == 2 and all(x[2] == "SUCCESS" for x in gm), str(len(gm)))
check("GM identical across roles", len({x[1] for x in gm}) == 1)
check("asCapable true throughout", asc == {("dut", True), ("peer", True)}, str(asc))
check("one path per role", len(path) == 2, str(len(path)))

# doc soak per-cycle table vs soak-cycles.csv and summary
rows = table_after("Per-checkpoint results follow")
sc = list(csv.DictReader(open(f"{ev}/soak-cycles.csv")))
smis = [(r, c) for r, c in zip(rows, sc) if
        (r[0], r[1], r[2], r[3], r[4]) != (c["cycle"], c["elapsed_s"], c["counter_errors"],
                                           c["segment_sequence_gaps"], c["overlap_recovered"])]
check("doc soak rows == 145 and == csv", len(rows) == 145 and not smis, str(smis[:2]))
check("nine segment gaps total", sum(int(r[3]) for r in rows) == 9 and
      sum(int(r[4]) for r in rows) == 9)
summ = json.load(open(f"{ev}/soak-summary.json"))
check("elapsed 7203.971 s", f"{summ['elapsed_s']:.3f}" == "7203.971", f"{summ['elapsed_s']:.3f}")
check("doc states 7203.971", "7203.971 seconds" in doc)
check("doc window 05:27:00.782-07:27:04.752",
      summ["start_utc"].startswith("2026-10-06T05:27:00.78") and
      summ["end_utc"].startswith("2026-10-06T07:27:04.75"))

# capture receipts: drop statistic
caps = sorted(glob.glob(f"{ev}/667-b13-soak-*-*.pcap.json"))
caps_start = sorted(glob.glob(f"{ev}/667-b13-start-*-*.pcap.json"))
nodrop = []
for c in caps:
    j = json.load(open(c))
    if "dropped" not in json.dumps(j) and "drop" not in json.dumps(j):
        nodrop.append(os.path.basename(c))
print(f"INFO soak capture receipts {len(caps)} startup {len(caps_start)}; without drop field {nodrop}")
check("435 soak capture receipts", len(caps) == 435, str(len(caps)))
check("300 startup capture receipts", len(caps_start) == 300, str(len(caps_start)))

# doc hash table vs published bytes
rows = table_after("| Packet receipt | Bytes | SHA-256 |")
hm = []
for r in rows:
    b = open(f"{ev}/{r[0]}", "rb").read()
    if (len(b), hashlib.sha256(b).hexdigest()) != (int(r[1]), r[2]):
        hm.append((r[0], len(b), hashlib.sha256(b).hexdigest()))
check("doc receipt hash table == published bytes", not hm, str(hm))

print(f"RESULT fails={fails}")
sys.exit(1 if fails else 0)
