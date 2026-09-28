#!/usr/bin/env python3
"""Boundary/robustness probes of validate_shipping_image outside the committed
fixtures (round-1 lines kept verbatim in label; round-2 lines added).
Usage: edge_probe.py <checkout-root>"""
import os, struct, sys
root = os.path.abspath(sys.argv[1]); sys.path.insert(0, os.path.join(root, "sw", "builder")); os.chdir(root)
import endstation_builder as eb, test_builder as tb
chk = eb.aem_image_checks
cfg = eb.load_config(tb.CONFIGS["arty_current"])
pristine = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
import gen_desc_image as packer
au = bytearray(tb.image_descriptor(pristine, 0x0002)[:144])
cd = bytearray(tb.image_descriptor(pristine, 0x0024)[:76])
def rows(au_body, cd_body, cfgs=(0,)):
    return [dict(configuration=c, type=t, index=0, bytes=bytes(b).hex())
            for c in cfgs for t, b in ((0x0002, au_body), (0x0024, cd_body)) if b is not None]
def doc(au_body, cd_body, cfgs=(0,)):
    return dict(format="kl-aem-image", version=1, descriptors=rows(au_body, cd_body, cfgs))
def img(*a, **k): return packer.build(doc(*a, **k), 576)[0]
def rates(words, cur=None):
    b = bytearray(au); struct.pack_into(">HH", b, 140, 144, len(words))
    if cur is not None: struct.pack_into(">I", b, 136, cur)
    return bytes(b) + struct.pack(f">{len(words)}I", *words)
def sources(idx, off=76, pad=b"", cur=None):
    b = bytearray(cd); struct.pack_into(">HH", b, 72, off, len(idx))
    if cur is not None: struct.pack_into(">H", b, 70, cur)
    return bytes(b) + pad + struct.pack(f">{len(idx)}H", *idx)
def hdr(blob, off, fmt, val):
    b = bytearray(blob); struct.pack_into(fmt, b, off, val); return bytes(b)
def verdict(label, blob):
    try:
        chk.validate_shipping_image(blob); v = "ACCEPTED"
    except chk.ImageCheckError as e:
        v = "REFUSED " + str(e).split(":")[0]
    except Exception as e:
        v = f"CRASH {type(e).__name__}: {e}"
    print(f"{label}: {v}")
good = rates([48000], cur=48000); ids = sources([0, 1])
print("-- round-1 lines")
verdict("control: one rate + [0,1]", img(good, ids))
verdict("rate count 0, length 144 (Milan 5.3.3.3: current rate must be listed)", img(rates([], cur=48000), ids))
verdict("current_sampling_rate 44100 not in list [48000]", img(rates([48000], cur=44100), ids))
verdict("clock_sources_offset 78 with 2 pad bytes (IEEE Table 7-61: 76)", img(good, sources([0, 1], 78, b"\0\0")))
verdict("CLOCK_DOMAIN identity [0,1] with trailing extra bytes", img(good, ids + b"\0\0"))
b = bytearray(img(good, sources([1, 0])))
idx = struct.unpack_from(">I", b, 12)[0]; n = struct.unpack_from(">H", b, 8)[0]
for r in range(n):
    if struct.unpack_from(">H", b, idx + 16 * r + 2)[0] in (2, 0x24):
        struct.pack_into(">H", b, idx + 16 * r + 2, 0x0025)
verdict("index rows retyped so no AUDIO_UNIT/CLOCK_DOMAIN row exists ([1,0] in body)", bytes(b))
verdict("truncated blob, 14 bytes", pristine[:14])
verdict("truncated blob, 3 bytes", pristine[:3])
verdict("pristine arty_current image", pristine)
print("-- round-2 lines")
verdict("rate count 0 with current 0 (nothing to be a member of)", img(rates([], cur=0), ids))
verdict("current differs only in pull bits (0x2000BB80 vs 48000)", img(rates([48000], cur=0x2000BB80), ids))
verdict("current is last of eight", img(rates([32000, 44100, 88200, 96000, 176400, 192000, 0x2000BB80, 48000], cur=48000), ids))
verdict("clock_sources_offset 74 (overlaps count field)", img(good, sources([0, 1], 74)))
verdict("clock_sources_offset 76, one source [0]", img(good, sources([0])))
verdict("image with AUDIO_UNIT only", img(good, None))
verdict("image with CLOCK_DOMAIN only", img(None, ids))
two = img(good, ids, cfgs=(0, 1))
verdict("control: two configurations, both complete", two)
verdict("two configurations, header n_config forced to 1 (row cfg 1 outside)", hdr(two, 6, ">H", 1))
verdict("one configuration, header n_config forced to 2", hdr(img(good, ids), 6, ">H", 2))
verdict("header n_config 65535, rows for configuration 0 only", hdr(img(good, ids), 6, ">H", 65535))
verdict("header n_config 0", hdr(img(good, ids), 6, ">H", 0))
verdict("index_off beyond image end", hdr(img(good, ids), 12, ">I", 0x7FFFFFF0))
verdict("row count larger than index", hdr(img(good, ids), 8, ">H", 500))
verdict("layout version 2", hdr(img(good, ids), 4, ">H", 2))
verdict("duplicate rate words [48000,48000] (loader-owned, not L10 image scope)", img(rates([48000, 48000], cur=48000), ids))
verdict("clock_source_index 5 with list [0,1] (outside frozen L6 scope)", img(good, sources([0, 1], cur=5)))
