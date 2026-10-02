#!/usr/bin/env python3
"""List each parent model's CLOCK_SOURCEs and input-stream families. Usage: parent_clock_sources.py <parent-tree>"""
import sys, pathlib, struct
root = pathlib.Path(sys.argv[1]).resolve()
for d in (root / "sw/builder", root / "avdecc", root / "protocol-processor/hdl/aecp/desc"): sys.path.insert(0, str(d))
import endstation_builder as eb, gen_aem_store as aem, gen_desc_image as img, gen_aemi_image as join
for name in ["arty_current", "arty_4x4", "arty_8ch", "ax7101_8x8", "ax7101_1x1_tdm8"]:
    cfg = eb.load_config(str(root / f"configs/endstation_{name}.yaml")); ovl = eb.emit_aem_overlay(cfg)
    doc = join.model_to_document(aem.build_model(aem.spec_from_overlay(ovl)), join.identity_from_overlay(ovl))
    g = img._grouped_descriptors(doc)
    srcs = [(i, struct.unpack_from(">HHH", b, 72)[0], struct.unpack_from(">HH", b, 82)) for i, (b, _) in sorted(g.get((0, 0x0A), {}).items())]
    fam = {i: {"AAF" if w >> 56 == 2 else "CRF" if w >> 56 == 4 else hex(w >> 56) for w in [int.from_bytes(b[138+8*k:146+8*k], "big") for k in range(struct.unpack_from(">H", b, 84)[0])]} for i, (b, _) in sorted(g.get((0, 0x05), {}).items())}
    print(f"{name}: sources (index,type,(loc_type,loc_index)) {srcs}; STREAM_INPUT families {fam}")
