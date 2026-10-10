#!/usr/bin/env python3
"""Independent recheck of the archived round2-recompute records against the
archived packet. usage: recheck_round2_records.py <author-dir>
Checks: (1) every raw-inputs.tsv row equals its cited raw-index line (sha256,
bytes, path); (2) the two snapshot copies hash to their raw-index/soak.jsonl
digests; (3) from ta_lv_all.txt alone, the cycles with a DUT Talker Advertise
Lv and their delays; (4) ta_lv_all.txt's bridge Lv against item3/cycles.tsv
lv_after_disconnect_s, and TA presence against dut_ta_lv_in_hold."""
import csv, hashlib, json, os, re, sys
au = sys.argv[1]
r2 = os.path.join(au, "round2-recompute")
ok = True
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
rows = list(csv.DictReader(open(os.path.join(r2, "inputs/raw-inputs.tsv")), delimiter="\t"))
bad = 0
for r in rows:
    lines = open(os.path.join(au, "raw-index", r["index"])).read().splitlines()
    rec = json.loads(lines[int(r["line"]) - 1])
    if not (rec["sha256"] == r["sha256"] and str(rec["bytes"]) == r["bytes"] and rec["path"] == r["published_path"]):
        bad += 1
        print("ROW MISMATCH", r)
caps = [r for r in rows if r["published_path"].endswith("tap.pcap") and "/item3/" in r["published_path"]]
print(f"(1) raw-inputs rows {len(rows)}, equal to cited index line {len(rows)-bad}; item3 captures {len(caps)}, bytes {sum(int(r['bytes']) for r in caps)}")
ok &= bad == 0 and len(caps) == 101
soak = [json.loads(l) for l in open(os.path.join(au, "raw-index/soak.jsonl"))]
for n in ("snapshot-prebind.jsonl", "snapshot-final.jsonl"):
    want = [s["sha256"] for s in soak if s["path"].endswith("/soak/" + n)]
    got = sha(os.path.join(r2, "inputs", n))
    print(f"(2) {n}: copy {got[:16]} index {[w[:16] for w in want]} {'EQUAL' if want == [got] else 'DIFF'}")
    ok &= want == [got]
txt = open(os.path.join(r2, "outputs/ta_lv_all.txt")).read()
blocks = re.split(r"^(?=\S.*tap\.pcap$)", txt, flags=re.M)
dec = {}
for b in blocks:
    m = re.search(r"cycle-(\d{3})/tap\.pcap", b)
    if not m:
        continue
    c = int(m.group(1))
    lv = re.search(r"bridge Listener Lv after the response\s+([0-9.]+) s", b)
    ta = re.search(r"DUT Talker Advertise Lv after bridge Lv\s+([0-9.]+) s", b)
    dec[c] = (float(lv.group(1)) if lv else None, float(ta.group(1)) if ta else None)
tas = {c: v[1] for c, v in dec.items() if v[1] is not None}
print(f"(3) decoded captures {len(dec)}; DUT TA Lv in cycles {sorted(tas)} at {[round(tas[c], 4) for c in sorted(tas)]} s after the bridge Lv")
ok &= len(dec) == 101 and sorted(tas) == [1, 2, 42]
cyc = {int(r["cycle"].rsplit("-", 1)[-1]): r for r in csv.DictReader(open(os.path.join(au, "item3/cycles.tsv")), delimiter="\t")}
worst, agree, tagree = 0.0, 0, 0
for c, (lv, ta) in dec.items():
    d = abs(lv - float(cyc[c]["lv_after_disconnect_s"])) * 1e6
    worst = max(worst, d)
    agree += d < 0.5
    tagree += (ta is not None) == (cyc[c]["dut_ta_lv_in_hold"].strip() not in ("", "0", "no", "False"))
print(f"(4) cycles in cycles.tsv {len(cyc)}; bridge Lv within 0.5 us {agree}/101, worst {worst:.3f} us; TA presence agrees {tagree}/101")
ok &= agree == 101 and tagree == 101 and len(cyc) == 101
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
