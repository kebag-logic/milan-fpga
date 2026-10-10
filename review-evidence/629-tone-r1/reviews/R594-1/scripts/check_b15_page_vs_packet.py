#!/usr/bin/env python3
"""Cross-check the lane B15 section of the findings page against the published lane packet.

usage: check_b15_page_vs_packet.py <page.md> <packet author dir>

Checks: every raw-file row (bytes, SHA-256) against RAW-ARTIFACTS.json; every per-point level row and
the PDU/gap/tv/mr table against summary/pts*/{a,b}-*.json and c-mcasp.json; the alignment table
against summary/pts*/align-b-c.json; the counter table against runs/pts*/events.jsonl (decoded
GET_COUNTERS payloads); the census figure against restore/census-compare.txt; the control blocks
against the control JSONs. Prints one line per check and exits 1 on any mismatch.
"""
import json
import os
import re
import sys

page, A = sys.argv[1], sys.argv[2]
txt = open(page, encoding="utf-8").read()
sec = txt[txt.index("## Dev 5603c353, 2026-10-10: lane B15"):]
bad = 0


def chk(name, ok, detail=""):
    global bad
    bad += 0 if ok else 1
    print(("OK   " if ok else "FAIL ") + name + (f" :: {detail}" if detail else ""))


def J(p):
    return json.load(open(os.path.join(A, p)))


# raw hashes
raw = {f["path"]: f for f in J("RAW-ARTIFACTS.json")["files"]}
rows = re.findall(r"^\| (Tap probe|`pts[12]`) \| `([^`]+)`[^|]*\| ([^|]+) \| `([0-9a-f]{64})` \|$", sec, re.M)
chk("raw-hash rows found", len(rows) == 11, f"{len(rows)} rows")
for run, f, by, h in rows:
    key = f if run == "Tap probe" else f"{run.strip('`')}/{f}"
    r = raw.get(key)
    if r is None:
        chk(f"raw {key}", False, "not in RAW-ARTIFACTS"); continue
    want_b = "Withheld" if isinstance(r["bytes"], str) else f"{r['bytes']:,}"
    chk(f"raw {key}", r["sha256"] == h and by.strip() == want_b, f"page {by.strip()} {h[:12]}")

# levels and PDUs
for run in ("pts1", "pts2"):
    for pt, fn in (("(a)", "a-peer-tap.json"), ("(b)", "b-dut-tap.json"), ("(c)", "c-mcasp.json")):
        d = J(f"summary/{run}/{fn}")
        lv = " / ".join(f"{c['rms_dbfs']:.2f}" for c in d["channels"][:4])
        pat = rf"^\| `{run}` \| {re.escape(pt)} [^|]*\| 0 / 1 / 2 / 3 \| {re.escape(lv)} \|"
        chk(f"levels {run} {pt}", re.search(pat, sec, re.M) is not None, lv)
        if pt != "(c)":
            i = d["info"]
            pat = rf"^\| `{run}` \| {re.escape(pt)} \| {i['pdus']:,} \| {i['seq_gaps']} \| {i['tv0']} \| {i['mr_toggles']} \|"
            fm = list(i["formats"]) == ["fmt=0x02 nsr=5 cpf=4 depth=32 sdl=96"]
            chk(f"pdus {run} {pt}", re.search(pat, sec, re.M) is not None and fm, f"{i['pdus']} {i['formats']}")
        else:
            z = all(c["min"] == 0 and c["max"] == 0 for c in d["channels"][4:8])
            chk(f"(c) channels 4-7 zero {run}", z)
    al = J(f"summary/{run}/align-b-c.json")
    pat = rf"^\| `{run}` \| {al['matches_of_first_window']} \| {al['mcasp_frames']:,} \| {al['compared_equal']:,} \| {len(al['slips'])} \| {al['frames_differing']} \| {al['verdict']} \|"
    chk(f"align {run}", re.search(pat, sec, re.M) is not None, json.dumps({k: al[k] for k in ('compared_equal', 'slips', 'verdict')}))

# counters (IEEE 1722.1 STREAM_INPUT counter block: 32 x 32-bit after the valid mask)
NAMES = {0: "MEDIA_LOCKED", 1: "MEDIA_UNLOCKED", 2: "STREAM_INTERRUPTED", 3: "SEQ_NUM_MISMATCH", 4: "MEDIA_RESET",
         5: "TIMESTAMP_UNCERTAIN", 6: "TIMESTAMP_VALID", 7: "TIMESTAMP_NOT_VALID", 8: "UNSUPPORTED_FORMAT",
         9: "LATE_TIMESTAMP", 10: "EARLY_TIMESTAMP", 11: "FRAMES_RX"}
for run in ("pts1", "pts2"):
    cs = {}
    for line in open(os.path.join(A, f"runs/{run}/events.jsonl")):
        e = json.loads(line)
        if e["kind"] == "counters" and e["who"] == "dut":
            p = bytes.fromhex(e["payload"])
            vals = [int.from_bytes(p[8 + 4 * k:12 + 4 * k], "big") for k in range(12)]
            cs[e["tag"]] = (e["t"], dict(zip(NAMES.values(), vals)))
    (t0, b), (t1, a) = cs["before"], cs["after"]
    zero = all(a[k] == 0 and b[k] == 0 for k in ("STREAM_INTERRUPTED", "SEQ_NUM_MISMATCH", "MEDIA_RESET",
                                                 "TIMESTAMP_NOT_VALID", "TIMESTAMP_UNCERTAIN", "LATE_TIMESTAMP",
                                                 "EARLY_TIMESTAMP", "UNSUPPORTED_FORMAT"))
    lk = a["MEDIA_LOCKED"] == b["MEDIA_LOCKED"] == 1 and a["MEDIA_UNLOCKED"] == b["MEDIA_UNLOCKED"] == 0
    dfr = a["FRAMES_RX"] - b["FRAMES_RX"]
    pat = rf"^\| `{run}` \| 1 / 0 at both reads \| 0, 0, 0 \| 0, 0, 0, 0 \| 0 \| \+{dfr:,} in {t1 - t0:.1f} s \|"
    chk(f"counters {run}", zero and lk and re.search(pat, sec, re.M) is not None,
        f"FRAMES_RX +{dfr} over {t1 - t0:.3f} s; TIMESTAMP_VALID +{a['TIMESTAMP_VALID'] - b['TIMESTAMP_VALID']}")

# census
cc = open(os.path.join(A, "restore/census-compare.txt")).read()
m = re.search(r'"same": (\d+), "compared": (\d+)', cc)
chk("census", m and f"{m.group(1)} of {m.group(2)} entries equal" in sec, m.group(0) if m else cc[:80])

# positive control blocks at the loop floor
for fn, want in (("ctl-peer-tap-dut-talker.json", "15 of 23"), ("ctl-dut-tap-dut-talker.json", "15 of 23")):
    d = J(f"summary/pts2/{fn}")
    for c in d["channels"][:2]:
        for t in ("997", "9973"):
            if f"tone_{t}" in c:
                pb = c[f"tone_{t}"]["per_block"]
                n = sum(1 for x in pb if -150 < x["thdn_db"] < -145 and abs(x["level_dbfs"] + 1.0) < 0.01)
                chk(f"control {fn} ch{c['channel']} {t}", f"{n} of {len(pb)}" == want, f"{n} of {len(pb)}")
d = J("summary/pts2/d-extcap-pair.json")
for r in d["rows"]:
    for t in ("997", "9973"):
        if f"tone_{t}" in r:
            pb = r[f"tone_{t}"]["per_block"]
            n = sum(1 for x in pb if -150 < x["thdn_db"] < -145 and abs(x["level_dbfs"] + 1.0) < 0.01)
            chk(f"control extcap {t}", f"{n} of {len(pb)}" == "13 of 16", f"{n} of {len(pb)}")

print(f"mismatches: {bad}")
sys.exit(1 if bad else 0)
