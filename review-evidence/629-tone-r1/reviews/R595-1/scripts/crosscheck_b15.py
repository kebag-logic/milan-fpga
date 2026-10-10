#!/usr/bin/env python3
"""R595-1: derive lane B15's published figures from the archived packet and check the page states them.

usage: crosscheck_b15.py <packet_author_dir> <findings_page.md>

<packet_author_dir> is review-evidence/629-tone-r1/author from the published evidence commit.
Prints one line per check (PASS/FAIL) and exits 1 when any check fails. Read-only.
"""
import json
import os
import sys

A, PAGE = sys.argv[1], sys.argv[2]
page = open(PAGE, encoding="utf-8").read()
sec = page[page.index("## Dev 5603c353, 2026-10-10: lane B15"):]
fails = 0


def check(name, ok, detail=""):
    global fails
    fails += 0 if ok else 1
    print(f"{'PASS' if ok else 'FAIL'} {name}{(' :: ' + detail) if detail else ''}")


def j(*p):
    return json.load(open(os.path.join(A, *p)))


def lv(rows, n=4):
    return " / ".join(f"{r['rms_dbfs']:.2f}" for r in rows[:n])


def pct(x):
    return round(100 * x, 2)


for run in ("pts1", "pts2"):
    a, b, c = j("summary", run, "a-peer-tap.json"), j("summary", run, "b-dut-tap.json"), j("summary", run, "c-mcasp.json")
    for tag, d in (("(a)", a), ("(b)", b), ("(c)", c)):
        check(f"{run} {tag} verdict TONE ABSENT", d["verdict"] == "TONE ABSENT", d["verdict"])
        s = lv(d["channels"])
        check(f"{run} {tag} levels '{s}' on the page", s in sec)
        shares = [pct(r[k]) for r in d["channels"][:4] for k in ("share_997", "share_9973")]
        check(f"{run} {tag} every share below 0.06 %", max(shares) < 0.06, str(shares))
        check(f"{run} {tag} low byte zero", all(r["low_byte_values"] == [0] for r in d["channels"]))
    for tag, d in (("(a)", a), ("(b)", b)):
        i = d["info"]
        row = f"| `{run}` | {tag} | {i['pdus']:,} | {i['seq_gaps']} | {i['tv0']} | {i['mr_toggles']} |"
        check(f"{run} {tag} PDU row on the page", row in sec, row)
        check(f"{run} {tag} one format, cpf 4, sdl 96", list(i["formats"]) == ["fmt=0x02 nsr=5 cpf=4 depth=32 sdl=96"])
        check(f"{run} {tag} hash on the page", d["sha256"] in sec)
    check(f"{run} (c) hash on the page", c["sha256"] in sec)
    check(f"{run} (c) channels 4-7 every word zero", all(r["min"] == r["max"] == 0 for r in c["channels"][4:]))
    al = j("summary", run, "align-b-c.json")
    row = f"| `{run}` | {al['matches_of_first_window']} | {al['mcasp_frames']:,} | {al['compared_equal']:,} | {len(al['slips'])} | {al['frames_differing']} | {al['verdict']} |"
    check(f"{run} alignment row on the page", row in sec, row)
    check(f"{run} alignment covers the whole recording", al["covered_recording_frames"] == [0, al["mcasp_frames"]])
    rng = [(r["min"], r["max"]) for r in (b["channels"][:4] + c["channels"][:4])]
    check(f"{run} (b),(c) values inside the align key's lossless lane", all(-128 <= lo and hi <= 127 for lo, hi in rng), str(rng))

ctl = {k: j("summary", "pts2", f"ctl-{k}-tap-dut-talker.json") for k in ("peer", "dut")}
ctl["ext"] = j("summary", "pts2", "d-extcap-pair.json")
for k, d in ctl.items():
    rows = d.get("channels") or d.get("rows")
    t0, t1 = rows[0]["tone_997"], rows[1]["tone_9973"]
    at = [sum(1 for b in t["per_block"] if b["level_dbfs"] > -2 and b["thdn_db"] < -140) for t in (t0, t1)]
    check(f"control {k}: TONE PRESENT", d["verdict"] == "TONE PRESENT")
    check(f"control {k}: medians -1.00 dBFS, exact frequency", t0["median"]["level_dbfs"] == -1.0 and t0["median"]["f_hz"] == 997.0
          and t1["median"]["f_hz"] == 9973.0, json.dumps([t0["median"], t1["median"]]))
    check(f"control {k}: blocks at floor '{at[0]} of {t0['blocks']}' on the page", f"{at[0]} of {t0['blocks']}" in sec and at[0] == at[1])

raw = j("RAW-ARTIFACTS.json")["files"]
for f in raw:
    if not f["path"].startswith("tone-loop"):
        check(f"raw hash {f['path']} on the page", f["sha256"] in sec)
        if isinstance(f["bytes"], int):
            check(f"raw size {f['path']} on the page", f"{f['bytes']:,}" in sec)

cc = open(os.path.join(A, "restore", "census-compare.txt")).read().splitlines()
same = json.loads(cc[-1])
check("census 45 of 46 equal", same == {"same": 45, "compared": 46}, cc[-1])
check("census: the one difference is GET_AVB_INFO (propagation delay 0x17d -> 0x183)",
      len(cc) == 3 and '"GET_AVB_INFO"' in cc[1] and "0000017d" in cc[1] and "00000183" in cc[1])
print(f"FAILS {fails}")
sys.exit(1 if fails else 0)
