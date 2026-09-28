#!/usr/bin/env python3
"""Round-2 edge probe of aem_image_checks at <tree>: F2, offset 76, current-rate membership, presence.

Direct calls on synthetic bodies and on real shipping images; no committed test is used.
"""
import struct, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root)); sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb
from sw.builder import aem_image_checks as I
assert Path(I.__file__).resolve().is_relative_to(root)
def reason(fn, *a):
    try:
        fn(*a); return "ACCEPT"
    except I.ImageCheckError as e:
        return str(e).split(":")[0]
    except Exception as e:  # noqa: BLE001
        return "OTHER:" + type(e).__name__
def au(words, current, off=144, cnt=None):
    b = bytearray(144); struct.pack_into(">I", b, 136, current)
    struct.pack_into(">HH", b, 140, off, len(words) if cnt is None else cnt)
    return bytes(b) + struct.pack(f">{len(words)}I", *words)
A = lambda d: reason(I._audio_unit, d, "t", 144, 8)
P = 0x2000BB80  # 48 kHz base with pull field 1
print("F2 count 0, no words, current 0/48000:", A(au([], 0)), A(au([], 48000)))
print("F2 count 0 with one trailing word:", A(au([48000], 48000, cnt=0)))
print("F2 count 0 at wrong offset (offset checked first):", A(au([], 48000, off=146)))
print("current at each position of 8:", [A(au([48000 + i if i != k else 48000 for i in range(8)], 48000)) for k in range(8)])
print("current absent (1..8 entries):", [A(au([96000] * n if n == 1 else [96000 + i for i in range(n)], 48000)) for n in range(1, 9)])
print("pull: current P vs [48000]:", A(au([48000], P)), "current 48000 vs [P]:", A(au([P], 48000)), "P vs [P]:", A(au([P], P)))
print("current matches only a word beyond count (count 1, 2 words):", A(au([96000, 48000], 48000, cnt=1)))
print("current 0 vs [0]:", A(au([0], 0)), " 0xFFFFFFFF vs [0xFFFFFFFF]:", A(au([0xFFFFFFFF], 0xFFFFFFFF)))
def cd(src, off=76, cnt=None, pad=0):
    b = bytearray(76); struct.pack_into(">HH", b, 72, off, len(src) if cnt is None else cnt)
    return bytes(b) + bytes(pad) + struct.pack(f">{len(src)}H", *src)
D = lambda d: reason(I._clock_domain, d, "t")
offs = {o: D(cd([0, 1], off=o, pad=max(0, o - 76))) for o in range(0, 200)}
print("L6 offsets accepted:", [o for o, r in offs.items() if r == "ACCEPT"],
      " others all L6_OFFSET:", set(r for o, r in offs.items() if o != 76) == {"L6_OFFSET"})
print("L6 offset 76 count 0:", D(cd([], cnt=0)), " offset 70 count 0:", D(cd([], off=70, cnt=0)))
print("L6 identity + trailing 2 bytes (unadopted suggestion, expected ACCEPT):", D(cd([0, 1]) + b"\0\0"))
# presence on real shipping images
for stem in ("arty_current", "arty_4x4", "arty_8ch", "ax7101_8x8", "ax7101_1x1_tdm8"):
    cfg = eb.load_config(str(root / f"configs/endstation_{stem}.yaml"))
    blob = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
    ncfg, nrow = struct.unpack_from(">HH", blob, 6); idx = struct.unpack_from(">I", blob, 12)[0]
    rows = [struct.unpack_from(">HHHHIHH", blob, idx + 16 * r) for r in range(nrow)]
    types = {(r[0], r[1]): r[2] for r in rows if r[1] in (2, 0x24)}
    def edit(fn):
        b = bytearray(blob); fn(b); return reason(I.validate_shipping_image, bytes(b))
    def row_at(dtype):
        return next(idx + 16 * i for i, r in enumerate(rows) if r[1] == dtype)
    res = {
        "pristine": reason(I.validate_shipping_image, blob),
        "n_config 0": edit(lambda b: struct.pack_into(">H", b, 6, 0)),
        "n_config +1": edit(lambda b: struct.pack_into(">H", b, 6, ncfg + 1)),
        "AU row count 0": edit(lambda b: struct.pack_into(">H", b, row_at(2) + 4, 0)),
        "CD row count 0": edit(lambda b: struct.pack_into(">H", b, row_at(0x24) + 4, 0)),
        "AU row retyped 0x0003": edit(lambda b: struct.pack_into(">H", b, row_at(2) + 2, 3)),
        "CD row retyped 0x0025": edit(lambda b: struct.pack_into(">H", b, row_at(0x24) + 2, 0x25)),
        "AU row cfg -> n_config": edit(lambda b: struct.pack_into(">H", b, row_at(2), ncfg)),
        "row0 (ENTITY) cfg -> n_config": edit(lambda b: struct.pack_into(">H", b, idx, ncfg)),
    }
    print(stem, f"n_config={ncfg} AU/CD rows={types}", res)
