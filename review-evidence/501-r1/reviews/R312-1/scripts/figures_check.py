#!/usr/bin/env python3
"""[R312] probe: compare base/head emitted rows and recompute every #501
figure from the generated shape and the head fixture."""
import json, math, sys
b = json.load(open(sys.argv[1])); h = json.load(open(sys.argv[2])); fx = sys.argv[3]
ok = True
def req(c, msg):
    global ok
    print(("OK   " if c else "FAIL ") + msg); ok &= bool(c)
for s in b:
    if s != "endstation_ax7101_8x8":
        req(b[s] == h[s], f"{s}: every row, image length and SHA-256 identical base->head")
B = {r[0]: r for r in b["endstation_ax7101_8x8"]["rows"]}; H = {r[0]: r for r in h["endstation_ax7101_8x8"]["rows"]}
req(set(B) == set(H), "8x8: identical record-id set base->head")
diff = [i for i in B if B[i][4:] != H[i][4:] or (B[i][2] != H[i][2] and B[i][4] != "MAPS_OUT")]
req(not diff, "8x8: group/index per id unchanged; only MAPS_OUT lengths changed")
grown = [i for i in H if H[i][2] != B[i][2]]
req(sorted(grown) == list(range(0x70, 0x78)) and all(H[i][3] == 576 and B[i][3] == 72 for i in grown),
    "8x8: exactly ids 0x70..0x77 grow 72 -> 576 payload bytes (9 -> 72 entries)")
# contiguity at head
rows = sorted(H.values(), key=lambda r: r[1]); pos = 0
for r in rows:
    req_ok = r[1] == pos; pos += r[2]
    if not req_ok: req(False, f"8x8 head: non-contiguous at id 0x{r[0]:02X}")
req(True, f"8x8 head: records contiguous, area sum {pos}")
area = pos; img = 40 + area + (-area) % 4 + 4
req(img == h["endstation_ax7101_8x8"]["imglen"] == 12680, f"8x8: 40 + align4({area}) + 4 = {img} = 12680")
req(img - b["endstation_ax7101_8x8"]["imglen"] == 8 * (72 - 9) * 8 == 4032, "8x8: growth 8*(72-9)*8 = 4032")
# group sums from rows (independent of doc)
def gsum(grp): return sum(r[2] for r in H.values() if r[4] == grp)
names = sum(1 for r in H.values() if r[4] == "NAME")
fixed = sum(r[2] for r in H.values() if r[4] not in ("MAPS_IN", "MAPS_OUT", "NAME"))
print(f"     fixed={fixed} mapin={gsum('MAPS_IN')} mapout={gsum('MAPS_OUT')} names={gsum('NAME')} ({names} names)")
req((fixed, gsum('MAPS_IN'), gsum('MAPS_OUT'), gsum('NAME')) == (770, 64, 4672, 7128), "8x8: doc terms 770 + 64 + 4672 + 7128 = 12634")
req(len(H) == 156 and max(H) == 0xE2 == 0x80 + names - 1, "8x8: 156 records, top id 0x80+99-1 = 0xE2")
w = 3000 + math.ceil(img / 256) * 5 + img * 8 * 1000 / 12_500_000
req(abs(w - 3258.1152) < 1e-9 and 2 * w < 8000, f"8x8: commit worst {w:.4f} ms, 2x = {2*w:.4f} < 8000")
# fixture parity
fr = {}
for ln in open(fx):
    if ln.startswith("rec "):
        _, rid, off, fl, pl, g, i = ln.split(); fr[int(rid, 16)] = (int(rid, 16), int(off), int(fl), int(pl), g, int(i))
    elif ln.startswith("imglen"): fimg = int(ln.split()[1])
req(fr == {k: tuple(v) for k, v in H.items()} and fimg == img, "8x8: committed fixture rows and imglen equal the head emit")
# 1x1 terms
X = {r[0]: r for r in h["endstation_ax7101_1x1_tdm8"]["rows"]}
fx1 = sum(r[2] for r in X.values() if r[4] not in ("MAPS_IN", "MAPS_OUT", "NAME"))
t1 = (fx1, sum(r[2] for r in X.values() if r[4]=="MAPS_IN"), sum(r[2] for r in X.values() if r[4]=="MAPS_OUT"), sum(r[2] for r in X.values() if r[4]=="NAME"))
req(t1 == (266, 72, 144, 2736) and len(X) == 53 and max(X) == 0xA5, f"1x1: doc terms {t1}, 53 records, top 0xA5")
sys.exit(0 if ok else 1)
