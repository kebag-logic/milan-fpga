#!/usr/bin/env python3
"""Boundary/robustness probes of validate_shipping_image outside the committed
fixtures.  Usage: edge_probe.py <checkout-root>"""
import os, struct, sys
root = os.path.abspath(sys.argv[1]); sys.path.insert(0, os.path.join(root, "sw", "builder")); os.chdir(root)
import endstation_builder as eb, test_builder as tb
chk = eb.aem_image_checks
cfg = eb.load_config(tb.CONFIGS["arty_current"])
pristine = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
import gen_desc_image as packer
au = bytearray(tb.image_descriptor(pristine, 0x0002)[:144])
cd = bytearray(tb.image_descriptor(pristine, 0x0024)[:76])
def doc(au_body, cd_body):
    return dict(format="kl-aem-image", version=1, descriptors=[
        dict(configuration=0, type=0x0002, index=0, bytes=bytes(au_body).hex()),
        dict(configuration=0, type=0x0024, index=0, bytes=bytes(cd_body).hex())])
def rates(words, cur=None):
    b = bytearray(au); struct.pack_into(">HH", b, 140, 144, len(words))
    if cur is not None: struct.pack_into(">I", b, 136, cur)
    return bytes(b) + struct.pack(f">{len(words)}I", *words)
def sources(idx, off=76, pad=b""):
    b = bytearray(cd); struct.pack_into(">HH", b, 72, off, len(idx))
    return bytes(b) + pad + struct.pack(f">{len(idx)}H", *idx)
def verdict(label, blob):
    try:
        chk.validate_shipping_image(blob); v = "ACCEPTED"
    except chk.ImageCheckError as e:
        v = "REFUSED " + str(e).split(":")[0]
    except Exception as e:
        v = f"CRASH {type(e).__name__}: {e}"
    print(f"{label}: {v}")
good = rates([48000], cur=48000); ids = sources([0, 1])
verdict("control: one rate + [0,1]", packer.build(doc(good, ids), 576)[0])
verdict("rate count 0, length 144 (Milan 5.3.3.3: current rate must be listed)",
        packer.build(doc(rates([], cur=48000), ids), 576)[0])
verdict("current_sampling_rate 44100 not in list [48000]",
        packer.build(doc(rates([48000], cur=44100), ids), 576)[0])
verdict("clock_sources_offset 78 with 2 pad bytes (IEEE Table 7-61: 76)",
        packer.build(doc(good, sources([0, 1], 78, b"\0\0")), 576)[0])
verdict("CLOCK_DOMAIN identity [0,1] with trailing extra bytes",
        packer.build(doc(good, ids + b"\0\0"), 576)[0])
b = bytearray(packer.build(doc(good, sources([1, 0])), 576)[0])
idx = struct.unpack_from(">I", b, 12)[0]; n = struct.unpack_from(">H", b, 8)[0]
for r in range(n):
    if struct.unpack_from(">H", b, idx + 16 * r + 2)[0] in (2, 0x24):
        struct.pack_into(">H", b, idx + 16 * r + 2, 0x0025)
verdict("index rows retyped so no AUDIO_UNIT/CLOCK_DOMAIN row exists ([1,0] in body)", bytes(b))
verdict("truncated blob, 14 bytes", pristine[:14])
verdict("truncated blob, 3 bytes", pristine[:3])
verdict("pristine arty_current image", pristine)
