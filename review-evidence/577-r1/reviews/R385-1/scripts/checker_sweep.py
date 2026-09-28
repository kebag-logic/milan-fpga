#!/usr/bin/env python3
"""Direct boundary sweep and index-corruption fuzz of aem_image_checks at <tree>."""
import itertools, random, struct, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root)); sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb
from sw.builder import aem_image_checks as I
cfg = eb.load_config(str(root / "configs/endstation_arty_current.yaml"))
blob = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
def reason(fn, *a):
    try:
        fn(*a); return "ACCEPT"
    except I.ImageCheckError as e:
        return str(e).split(":")[0]
hdr = bytes(144)
def au(off, cnt, nwords, extra=0):
    b = bytearray(hdr); struct.pack_into(">HH", b, 140, off, cnt)
    return bytes(b) + bytes(4 * nwords + extra) if extra >= 0 else (bytes(b) + bytes(4 * nwords))[:extra]
A = lambda d: reason(I._audio_unit, d, "t", 144, 8)
print("L10 matched count/extent:", {n: A(au(144, n, n)) for n in range(0, 10)})
bad_off = {o: A(au(o, 1, 1)) for o in range(0, 300) if o != 144}
print("L10 offsets != 144 all L10_OFFSET:", set(bad_off.values()) == {"L10_OFFSET"}, len(bad_off))
print("L10 partial tails:", {(n, d): A(au(144, n, n, d)) for n in (1, 8) for d in (-3, -2, -1, 1, 2, 3)})
print("L10 count vs extent:", {(n, w): A(au(144, n, w)) for n in (1, 2, 8) for w in (n - 1, n + 1) if w >= 0})
print("L10 header lengths:", {l: A(hdr[:l]) for l in (0, 139, 140, 143)})
ch = bytes(76)
def cd(src, off=76, trail=b""):
    b = bytearray(ch); struct.pack_into(">HH", b, 72, off, len(src))
    return bytes(b) + (bytes(off - 76) if off > 76 else b"") + struct.pack(f">{len(src)}H", *src) + trail
D = lambda d: reason(I._clock_domain, d, "t")
res = {}
for k in range(1, 5):
    for src in itertools.product(range(k + 1), repeat=k):
        res[src] = D(cd(list(src)))
acc = sorted(s for s, r in res.items() if r == "ACCEPT")
print("L6 accepted lists over all k<=4 tuples from 0..k:", acc)
print("L6 reason histogram:", {r: sum(1 for v in res.values() if v == r) for r in sorted(set(res.values()))})
print("L6 empty:", D(cd([])), "offset 78 padded identity:", D(cd([0, 1], off=78)),
      "identity + trailing word:", D(cd([0, 1], trail=b"\0\0")))
# fuzz: corrupt header/index bytes; only ImageCheckError or acceptance is allowed
rng = random.Random(577)
idx_end = struct.unpack_from(">I", blob, 12)[0] + 16 * struct.unpack_from(">H", blob, 8)[0]
other = 0; outcomes = {}
for _ in range(3000):
    b = bytearray(blob)
    for _ in range(rng.randint(1, 4)):
        b[rng.randrange(0, idx_end)] = rng.randrange(256)
    try:
        I.validate_shipping_image(bytes(b)); r = "ACCEPT"
    except I.ImageCheckError as e:
        r = str(e).split(":")[0]
    except Exception as e:  # noqa: BLE001
        r = "OTHER:" + type(e).__name__; other += 1
    outcomes[r] = outcomes.get(r, 0) + 1
print("index fuzz outcomes:", dict(sorted(outcomes.items())), "non-ImageCheckError:", other)
print("truncations:", {n: reason(I.validate_shipping_image, blob[:n]) for n in (0, 3, 10, 15, 40, 700, 3930)})
