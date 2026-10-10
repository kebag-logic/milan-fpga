#!/usr/bin/env python3
"""Cross-check lane B15 page figures against the published packet's own records.

usage: crosscheck_b15.py <packet author dir: review-evidence/629-tone-r1/author>
Prints one OK/BAD line per check; exit 1 on any BAD.
"""
import json
import os
import re
import sys

A = sys.argv[1]
bad = 0


def chk(label, cond, got=""):
    global bad
    bad += not cond
    print(("OK  " if cond else "BAD ") + label + (f" [{got}]" if got != "" else ""))


def J(p):
    return json.load(open(os.path.join(A, p)))


# Per-point decoder summaries: PDUs, gaps, tv, mr, format, levels, ranges
want = {"pts1": dict(a=191843, b=191842), "pts2": dict(a=191639, b=191637)}
for run, w in want.items():
    for pt, f in (("a", "a-peer-tap.json"), ("b", "b-dut-tap.json")):
        d = J(f"summary/{run}/{f}")
        i = d["info"]
        chk(f"{run} ({pt}) PDUs {w[pt]}", i["pdus"] == w[pt], i["pdus"])
        chk(f"{run} ({pt}) 0 gaps, 0 tv clear, 0 mr toggles, 0 bad length",
            (i["seq_gaps"], i["tv0"], i["mr_toggles"], i["bad_length"]) == (0, 0, 0, 0))
        chk(f"{run} ({pt}) every PDU INT_32BIT nsr=5 cpf=4 depth=32 sdl=96",
            i["formats"] == {"fmt=0x02 nsr=5 cpf=4 depth=32 sdl=96": w[pt]})
        lv = [c["rms_dbfs"] for c in d["channels"]]
        chk(f"{run} ({pt}) levels -141.09/-141.10/-141.48/-141.4x", lv[:3] == [-141.09, -141.1, -141.48]
            and lv[3] in (-141.48, -141.49), lv)
        chk(f"{run} ({pt}) shares all < 0.1 %, verdict TONE ABSENT",
            max(max(c["share_997"], c["share_9973"]) for c in d["channels"]) < 0.001 and d["verdict"] == "TONE ABSENT")
        chk(f"{run} ({pt}) low byte always zero", all(c["low_byte_nonzero"] == 0 for c in d["channels"]))
    c = J(f"summary/{run}/c-mcasp.json")
    chk(f"{run} (c) 480,000 frames, ch4-7 all zero, ch0-3 ranges within -2..0",
        c["frames"] == 480000 and all(ch["nonzero"] == 0 for ch in c["channels"][4:])
        and all(ch["min"] >= -2 and ch["max"] <= 0 for ch in c["channels"][:4]))
    al = J(f"summary/{run}/align-b-c.json")
    chk(f"{run} align SAMPLE-EXACT 480,000/480,000, one match, no slip, covered [0,480000]",
        al["verdict"] == "SAMPLE-EXACT" and al["compared_equal"] == 480000 == al["mcasp_frames"]
        and al["matches_of_first_window"] == 1 and al["slips"] == [] and al["covered_recording_frames"] == [0, 480000])

# Positive control: medians and blocks at the floor
for f, n_all, n_floor in (("ctl-peer-tap-dut-talker.json", 23, 15), ("ctl-dut-tap-dut-talker.json", 23, 15)):
    d = J(f"summary/pts2/{f}")
    for ch, t, snr in ((0, "tone_997", 146.07), (1, "tone_9973", 145.99)):
        tt = d["channels"][ch][t]
        fl = sum(1 for b in tt["per_block"] if -147 < b["thdn_db"] < -145)
        chk(f"control {f} {t}: -1.00 dBFS, SNR {snr}, {n_floor} of {n_all} blocks at floor",
            tt["median"]["level_dbfs"] == -1.0 and round(tt["median"]["snr_db"], 2) == snr
            and tt["blocks"] == n_all and fl == n_floor, (tt["median"], fl))
d = J("summary/pts2/d-extcap-pair.json")
for r, t in ((d["rows"][0], "tone_997"), (d["rows"][1], "tone_9973")):
    fl = sum(1 for b in r[t]["per_block"] if -147 < b["thdn_db"] < -145)
    chk(f"control extcap {t}: 13 of 16 blocks at floor", r[t]["blocks"] == 16 and fl == 13, fl)

# Census 45 of 46, the one difference GET_AVB_INFO propagation delay 381 -> 387 ns
cc = open(os.path.join(A, "restore/census-compare.txt")).read()
chk("census 45 of 46", '"same": 45, "compared": 46' in cc)
m = re.findall(r'00090000<gm-id>([0-9a-f]{8})', cc)
chk("propagation delay 381 -> 387 ns", [int(x, 16) for x in m] == [381, 387], m)

# NVM seq/commits; SLIP_LB 146 -> 152
s, e = (open(os.path.join(A, f"restore/dut-{x}.txt")).read() for x in ("start", "end"))
chk("NVM start image seq 272, commits 38", "image seq 272" in s and "commits ok=38" in s)
chk("NVM end image seq 276, commits 42, pend=0, VD_OK", "image seq 276" in e and "commits ok=42" in e
    and "pend=0" in e and "verdict=VD_OK" in e)
sl = [int(re.search(r"0x900008d4\s+([0-9a-f]{2}) ([0-9a-f]{2})", x).group(2) + re.search(
    r"0x900008d4\s+([0-9a-f]{2}) ([0-9a-f]{2})", x).group(1), 16) for x in (s, e)]
chk("SLIP_LB dups 146 -> 152", sl == [146, 152], sl)

# FRAMES_RX increments from the run summaries
pm = open(os.path.join(A, "summary/points.md")).read()
fr = [int(x) for x in re.findall(r"counters (?:before|after) dut STREAM_INPUT 0: .*FRAMES_RX (\d+)", pm)]
chk("FRAMES_RX +191,998 (pts1) and +199,998 (pts2)", [fr[1] - fr[0], fr[3] - fr[2]] == [191998, 199998], fr)

# Peer survey: 20 NO_SUCH_DESCRIPTOR, each READ_DESCRIPTOR of type 0x0010 in configuration 1
# (payload: configuration, a 16-bit field the responder fills, descriptor type, index)
n, ok = 0, True
for line in open(os.path.join(A, "restore/peer-descs.jsonl")):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("status") == "NO_SUCH_DESCRIPTOR":
        n += 1
        ok &= d["payload"][0:4] == "0001" and d["payload"][8:12] == "0010" and d["what"].startswith("desc-peer-1-0x0010-")
chk("peer survey: 20 NO_SUCH_DESCRIPTOR, all type 0x0010 in configuration 1", n == 20 and ok, n)

# Outage: kill to restart by board uptime, about 63 s
lg = open(os.path.join(A, "soc/pts1-legs.log")).read()
up_stop = float(re.findall(r"^(\d+\.\d+) \d+\.\d+$", lg, re.M)[0]) - 5.0  # printed after sleep 2 + sleep 3
trig = [float(x) for x in re.findall(r"trigger_time: (\d+\.\d+)", lg)]
chk("outage about 63 s by board uptime", 62 <= min(trig) - up_stop <= 64.5, round(min(trig) - up_stop, 1))
chk("first restart printed LEG_PRESENT_NOT_STARTED at 13:27:55 UTC",
    "13:27:55" in lg and "LEG_PRESENT_NOT_STARTED" in lg)

print("BAD:", bad)
sys.exit(1 if bad else 0)
