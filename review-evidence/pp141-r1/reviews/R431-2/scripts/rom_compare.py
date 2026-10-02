#!/usr/bin/env python3
"""Compare rom_probe.json plants: same words, same values, across revisions."""
import json, sys
d = json.load(open(sys.argv[1]))
def cw(lab, name): return d[lab]["plants"][name].get("changed_words")
pfx = "tb/pp_top/"
names = sorted(n for n in d["head"]["plants"] if n.startswith(pfx))
print(f"gen_ucode.py patches at head: {len(names)}")
bad = 0
for n in names:
    h, r2, r1 = cw("head", n), cw("r2", n), cw("r1", n)
    m = cw("main", n) if n in d["main"]["plants"] else None
    same_r2 = h == r2
    same_main = (m == h) if m is not None else "n/a"
    hit_c6 = [int(a) for a in (h or {}) if 464 <= int(a) <= 469 or 480 <= int(a) <= 500]
    ok = same_r2 and same_main in (True, "n/a") and not hit_c6 and h
    bad += not ok
    print(f"  {'OK ' if ok else 'BAD'} {n[len(pfx):]}: {len(h)} words; =76b09ff0 {same_r2}; =main {same_main}; touches C6 words {hit_c6}")
print("old (39fd019) lk-prefix-zero-body at 39fd019 vs refreshed at 76b09ff0: words equal",
      cw("r1", "old-lk") == cw("r2", pfx + "aecp_dispatch_mutations/lk-prefix-zero-body.patch"),
      "; full ucode.hex equal", d["r1"]["plants"]["old-lk"]["ucode_sha256"] == d["r2"]["plants"][pfx + "aecp_dispatch_mutations/lk-prefix-zero-body.patch"]["ucode_sha256"])
print("old lk at head refused:", d["head"]["plants"]["old-lk"].get("apply_rc"), "; old lk at 76b09ff0 refused:", d["r2"]["plants"]["old-lk"].get("apply_rc"))
for s in ("three", "incl"):
    fn = {"three": "sclks-bound-three", "incl": "sclks-bound-inclusive"}[s]
    print(f"old {fn} (39fd019) at 39fd019 vs refreshed at 76b09ff0: full ucode equal",
          d["r1"]["plants"]["old-" + s]["ucode_sha256"] == d["r2"]["plants"][pfx + "aecp_dispatch_mutations/" + fn + ".patch"]["ucode_sha256"],
          "; words", cw("r1", "old-" + s))
print("4a40b17-form sclks-bound-three at head, words equal to committed:", cw("head", "r1b-three") == cw("head", pfx + "aecp_dispatch_mutations/sclks-bound-three.patch"))
print("head ucode.hex == main ucode.hex:", d["head"]["ucode_sha256"] == d["main"]["ucode_sha256"])
print("head program map == main program map:", d["head"]["map"] == d["main"]["map"])
print("76b09ff0 ucode == base ucode:", d["r2"]["ucode_sha256"] == d["base"]["ucode_sha256"])
sc = [p for p in d["head"]["map"]["programs"] if set(p["names"]) & {"E_SCLKS","E_SCLKSRF"}]
c6 = [p for p in d["head"]["map"]["programs"] if set(p["names"]) & {"E_IDNOTIF","E_SINFOUNS"}]
ov = [(a["names"], b["names"]) for a in sc for b in c6 if not (a["end"] < b["start"] or b["end"] < a["start"])]
print("E_SCLKS/E_SCLKSRF vs C6 overlaps:", ov)
# words that differ between lane-head ROM and merge ROM must be C6 words only
import pathlib
w = lambda p: pathlib.Path(p).read_text().split()
print("BAD count:", bad)
