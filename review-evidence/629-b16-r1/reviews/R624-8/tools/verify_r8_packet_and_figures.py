#!/usr/bin/env python3
"""R624-8: bind author-r8 to the evidence branch's MANIFEST.json, check every packet-file hash row of lane B16's
section against author-r8, and recompute key bench figures straight from the receipts (not through the check).

usage: python3 -I verify_r8_packet_and_figures.py <evidence root: review-evidence/629-b16-r1> <findings.md>"""
import csv, hashlib, json, os, re, sys
EV, PAGE = sys.argv[1:3]
P = os.path.join(EV, "author-r8")
out = {}
m = {e["file"]: e for e in json.load(open(os.path.join(EV, "MANIFEST.json")))}
r8 = [k for k in m if k.startswith("author-r8/")]
disk = {os.path.relpath(os.path.join(a, f), EV) for a, _, fs in os.walk(P) for f in fs}
bad = [k for k in r8 if hashlib.sha256(open(os.path.join(EV, k), "rb").read()).hexdigest() != m[k]["published_sha256"]
       or (m[k]["original_sha256"] != m[k]["published_sha256"]) != m[k]["path_redacted"]]
loc = dict(reversed(l.rstrip("\n").split("  ", 1)) for l in open(os.path.join(P, "MANIFEST.sha256")))
loc = {k[2:] if k.startswith("./") else k: v for k, v in loc.items()}
out["manifest"] = dict(entries=len(m), author_r8=len(r8), on_disk=len(disk), unlisted=len(disk - set(r8)),
                       missing=len(set(r8) - disk), published_mismatch_or_flag_error=len(bad),
                       path_redacted=sum(m[k]["path_redacted"] for k in r8),
                       sha256_lines=len(loc), sha256_lines_not_original=sum(m.get("author-r8/" + p, {}).get("original_sha256") != h for p, h in loc.items()))
page = open(PAGE, encoding="utf-8").read().split("\n")
s = next(i for i, x in enumerate(page) if x.startswith("## Dev 5603c353, 2026-10-12: lane B16"))
n = badrows = 0
for i, l in enumerate(page[s:], s + 1):
    x = re.match(r"^\| `([^`]+)`[^|]*\| ([\d,]+) \| `([0-9a-f]{64})` \|", l)
    if x and os.path.exists(os.path.join(P, x.group(1))):
        n += 1
        b = open(os.path.join(P, x.group(1)), "rb").read()
        e = m["author-r8/" + x.group(1)]
        if e["original_sha256"] != x.group(3) or (not e["path_redacted"] and (len(b) != int(x.group(2).replace(",", "")) or hashlib.sha256(b).hexdigest() != x.group(3))):
            badrows += 1
out["section_packet_hash_rows"] = dict(rows=n, bad=badrows)
f = {}
for r in ("b0-2", "bcrf", "baaf"):
    d = json.load(open(os.path.join(P, f"summary/{r}/c-b9-grade.json")))["summary"]
    f[r] = dict(blocks=d["blocks"], at_floor=d["blocks_at_floor"], events=d["events"],
                all_median=[d["ch0_all"]["thdn_db_median"], d["ch1_all"]["thdn_db_median"]],
                all_worst=[d["ch0_all"]["thdn_db_worst"], d["ch1_all"]["thdn_db_worst"]],
                floor_median=[d["ch0_floor"]["thdn_db_median"], d["ch1_floor"]["thdn_db_median"]],
                floor_worst=[d["ch0_floor"]["thdn_db_worst"], d["ch1_floor"]["thdn_db_worst"]])
    dl = json.load(open(os.path.join(P, f"summary/{r}/d-loop-decode.json")))
    f[r]["d_decoded"], f[r]["d_net_steps"], f[r]["d_events"] = dl["decoded"], dl["net_step_frames"], len(dl["events"])
    for p in "ab":
        a = json.load(open(os.path.join(P, f"summary/{r}/align-{p}-c.json")))
        f[r][f"align_{p}"] = [a["verdict"], a["compared_equal"], a["frames_differing"]]
b0 = json.load(open(os.path.join(P, "r2/b0-2-receipt.json")))
f["b0-2"]["overlap"] = {k: b0["overlap"][k] for k in ("seconds", "degraded_inside", "degraded_beyond")}
f["b0-2"]["degraded"] = b0["degraded"]
f["b0-2"]["recording_after_binds_s"] = b0["timing"]["recording_after_binds_s"]
f["compared_vs_a_b16c"] = f["bcrf"]["align_a"][1] + f["baaf"]["align_a"][1]
f["compared_vs_b_b16c"] = f["bcrf"]["align_b"][1] + f["baaf"]["align_b"][1]
f["compared_vs_a_b16b"] = 3 * 480000 + f["b0-2"]["align_a"][1]
f["compared_vs_b_b16b"] = 3 * 480000 + f["b0-2"]["align_b"][1]
for r in ("bcrf", "baaf"):
    rows = list(csv.DictReader(open(os.path.join(P, f"r2/{r}-poll-trace.tsv")), delimiter="\t"))
    rec = json.load(open(os.path.join(P, f"r2/{r}-poll-receipt.json")))
    k = rec["locked"]["first_locked_poll"]
    st = lambda x: int(x["0x8f8"], 16) & 7   # status_o[2:0]: 3 ACQUIRE, 4 LOCKED (KL_mmcm_drp_servo.sv:403-409)
    ws, we = rec["marks_after_set_s"]["window-start"], rec["marks_after_set_s"]["window-end"]
    w = [x for x in rows if ws <= float(x["start_after_set_s"]) and float(x["start_after_set_s"]) + float(x["length_ms"]) / 1000 <= we]
    f[r]["lock"] = dict(acquire_poll=rows[k - 1]["n"], acquire_state=st(rows[k - 1]), locked_poll=rows[k]["n"], locked_state=st(rows[k]),
                        bracket=[rows[k - 1]["start_after_set_s"], rec["locked"]["recomputed_s"][1]],
                        window_polls=len(w), window_locked=sum(st(x) == 4 for x in w))
out["figures"] = f
json.dump(out, sys.stdout, indent=1)
print()
