#!/usr/bin/env python3
"""Reviewer probe (R313-1): grade head figures against base and the shape.

Usage: python3 compare_figures.py <figures_base.json> <figures_head.json> <head-tree>

Every expected value is derived here from the shape counts in the JSON
(STREAM_OUTPUT, per-port clusters/map_mode, names), not copied from the PR.
Also replays the firmware's nvm_rebase_backend prefix/length loop from the
generated MILAN_NVM_MAP*_ENTRIES_k constants and checks each MAPS_OUT record
offset against the backend's decode rule
  base(0x70+k) = B_MAPI + mapi_pref[N-1] + mapi_len[N-1] + mapo_pref[k]
with the 16-bit table fields and the 12-bit rec_len_w of KL_nvm_backend.sv,
and compares with the committed nvm_backend fixture.
"""
import json
import math
import sys
from pathlib import Path

base = json.loads(Path(sys.argv[1]).read_text())
head = json.loads(Path(sys.argv[2]).read_text())
tree = Path(sys.argv[3])
BASE_1X1 = "103ce107b1402884914036a363055800ad2cd97b8067df41f5cc54be9d3a3aea"
fails = []


def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)


# 1x1: byte-identical image and unchanged record counts
s = "endstation_ax7101_1x1_tdm8"
check(base[s]["image_sha256"] == BASE_1X1, f"base 1x1 sha256 == pinned {BASE_1X1[:12]}")
check(head[s]["image_sha256"] == BASE_1X1, "head 1x1 sha256 == pinned (byte-identical)")
check(base[s]["records"] == head[s]["records"], "1x1 record table identical base/head")
check(base[s]["nrec"] == head[s]["nrec"] == 53, f"1x1 record count unchanged ({head[s]['nrec']})")

# 8x8: derive from the shape
s = "endstation_ax7101_8x8"
h, b = head[s], base[s]
so = h["dc"]["STREAM_OUTPUT"]
for p in h["spo"]:
    want = max(p["clusters"], so * 8) if p["map_mode"] == "dynamic" else p["clusters"]
    rec = [r for r in h["records"] if r[0] == "MAPS_OUT" and r[1] == p["index"]][0]
    check(rec[5] == want * 8 and rec[4] == 8 + want * 8,
          f"8x8 MAPS_OUT[{p['index']}] mode={p['map_mode']} clusters={p['clusters']} "
          f"-> entries {want}, payload {rec[5]}, framed {rec[4]}")
    check(h["decoded_maps_out_len"].get(str(p["index"])) == want * 8,
          f"8x8 MAPS_OUT[{p['index']}] decoded journal payload {want * 8}")
    check(h["fw_map_consts"][f"MILAN_NVM_MAPOUT_ENTRIES_{p['index']}"] == want,
          f"8x8 firmware MAPOUT_ENTRIES_{p['index']} == {want}")
check(h["decode_verdict"] == 0, "8x8 head image decodes VD_OK")
growth = sum(8 * (max(p["clusters"], so * 8) - p["clusters"]) for p in h["spo"]
             if p["map_mode"] == "dynamic")
check(h["image_len"] - b["image_len"] == growth,
      f"8x8 image growth {h['image_len'] - b['image_len']} == derived {growth}")
check(h["nrec"] == b["nrec"] and h["top_id"] == b["top_id"],
      f"8x8 record count {h['nrec']} and top id 0x{h['top_id']:02X} unchanged")
pages = math.ceil(h["image_len"] / 256)
worst = 3000 + pages * 5 + h["image_len"] * 8 * 1000 / 12_500_000
check(abs(worst - h["commit_worst_ms"]) < 1e-9 and 2 * worst < 8000,
      f"8x8 commit worst {worst:.4f} ms ({pages} pages), 2x = {2 * worst:.4f} < 8000; "
      f"margin {8000 / worst:.3f}x")
raw = sum(r[4] for r in h["records"])
print(f"INFO 8x8 raw record area {raw} B, image {h['image_len']} B, "
      f"base raw {sum(r[4] for r in b['records'])} B")

# firmware table replay against the backend decode rule and the fixture
fw = h["fw_map_consts"]
nin, nout = h["dc"].get("STREAM_PORT_INPUT", len(h["spi"])), len(h["spo"])
tabs = {}
for d, lab, n in ((0, "IN", len(h["spi"])), (1, "OUT", nout)):
    pref, rows = 0, []
    for k in range(min(n, 16)):
        flen = 8 + 8 * fw[f"MILAN_NVM_MAP{lab}_ENTRIES_{k}"]
        word = (flen << 16) | pref
        rows.append((word & 0xFFFF, (word >> 16) & 0xFFFF))
        check(pref < 65536 and flen < 65536 and flen < 4096,
              f"table {lab}[{k}] prefix {pref} len {flen} fit 16-bit fields and 12-bit rec_len_w")
        pref += flen
    tabs[lab] = rows
recs = {r[2]: r for r in h["records"]}
b_mapi = recs[0x60][3]
b_mapo = b_mapi + tabs["IN"][-1][0] + tabs["IN"][-1][1]
for k, (pf, ln) in enumerate(tabs["OUT"]):
    r = recs[0x70 + k]
    check(r[3] == b_mapo + pf and r[4] == ln,
          f"backend decode of 0x{0x70 + k:02X}: base {b_mapo + pf} len {ln} == image offset {r[3]} framed {r[4]}")
b_name = b_mapo + tabs["OUT"][-1][0] + tabs["OUT"][-1][1]
check(recs[0x80][3] == b_name, f"NAME group base {b_name} == image offset {recs[0x80][3]}")
fixture = (tree / "tb/verilator/nvm_backend/records_endstation_ax7101_8x8.txt").read_text()
rows = [ln.split() for ln in fixture.splitlines() if ln.startswith("rec ")]
fx = [[g, int(i), int(rid, 16), int(off), int(fl), int(pl)] for _t, rid, off, fl, pl, g, i in rows]
check(fx == h["records"], "committed 8x8 nvm_backend fixture == independently assembled table")
check(f"imglen {h['image_len']}" in fixture, "fixture imglen matches")
print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
