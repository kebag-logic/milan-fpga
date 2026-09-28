#!/usr/bin/env python3
"""What the configuration-outside-header refusal buys: run two images through the
checker at a checkout (head, or the surviving-mutant farm).
  X: two complete configurations, header n_config forced to 1 (AUDIO_UNIT/CLOCK_DOMAIN rows for cfg 1)
  Y: pristine image with one non-AUDIO_UNIT/CLOCK_DOMAIN index row retargeted to cfg 1, n_config 1
Usage: bound_probe.py <checkout-root>"""
import os, struct, sys
root = os.path.abspath(sys.argv[1]); sys.path.insert(0, os.path.join(root, "sw", "builder")); os.chdir(root)
import endstation_builder as eb, test_builder as tb
chk = eb.aem_image_checks
cfg = eb.load_config(tb.CONFIGS["arty_current"])
pristine = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
import gen_desc_image as packer  # on sys.path after the builder ran
au, cd = (tb.image_descriptor(pristine, t) for t in (0x0002, 0x0024))
def build(rows):
    return packer.build(dict(format="kl-aem-image", version=1, descriptors=[
        dict(configuration=c, type=t, index=0, bytes=b.hex()) for c, t, b in rows]), 576)[0]
def force(blob, n):
    b = bytearray(blob); struct.pack_into(">H", b, 6, n); return bytes(b)
def verdict(label, blob):
    try:
        chk.validate_shipping_image(blob); v = "ACCEPTED"
    except chk.ImageCheckError as e:
        v = "REFUSED " + str(e).split(":")[0]
    except Exception as e:
        v = f"UNNAMED {type(e).__name__}: {e}"
    print(f"{label}: {v}")
verdict("X two configurations, n_config forced 1", force(build([(c, t, b) for c in (0, 1) for t, b in ((2, au), (0x24, cd))]), 1))
b = bytearray(pristine); idx = struct.unpack_from(">I", b, 12)[0]; n = struct.unpack_from(">H", b, 8)[0]
row = next(r for r in range(n) if struct.unpack_from(">H", b, idx + 16 * r + 2)[0] not in (2, 0x24))
struct.pack_into(">H", b, idx + 16 * row, 1)
verdict(f"Y pristine arty_current, non-AUDIO_UNIT/CLOCK_DOMAIN index row {row} retargeted to cfg 1 (n_config 1)", bytes(b))
