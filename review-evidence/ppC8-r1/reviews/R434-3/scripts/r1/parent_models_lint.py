#!/usr/bin/env python3
"""Pack the parent's five models through the processor lint (both patches applied).
Usage: parent_models_lint.py <parent-tree>"""
import sys, copy, pathlib, json
root = pathlib.Path(sys.argv[1]).resolve()
for d in (root / "sw/builder", root / "avdecc", root / "protocol-processor/hdl/aecp/desc"):
    sys.path.insert(0, str(d))
import endstation_builder as eb, gen_aem_store as aem, gen_desc_image as img, gen_aemi_image as join
CONFIGS = ["arty_current", "arty_4x4", "arty_8ch", "ax7101_8x8", "ax7101_1x1_tdm8"]
def pack(cfg, **kw):
    ovl = eb.emit_aem_overlay(cfg)
    doc = join.model_to_document(aem.build_model(aem.spec_from_overlay(ovl)), join.identity_from_overlay(ovl))
    return ovl, doc, img.build(doc, 576, **kw)
for name in CONFIGS:
    cfg = eb.load_config(str(root / f"configs/endstation_{name}.yaml"))
    try:
        ovl, doc, (blob, report) = pack(cfg)
        lint = report[report.index("semantic lint:"):].rstrip().splitlines()
        print(f"{name}: PACKED lint_waivers_in_doc={len(doc.get('lint_waivers', []))}")
        for l in lint: print(f"    {l}")
        ec = ovl.get("entity_counts", {})
        print(f"    overlay keys with ids/counts: entity_counts={ec} entity_model_id={ovl.get('entity_model_id')}")
    except img.ImageError as e:
        print(f"{name}: REFUSED"); [print("    " + l.split(' (')[0]) for l in str(e).splitlines()]
    if cfg.get("model_lint_waivers"):
        c2 = copy.deepcopy(cfg); c2["model_lint_waivers"] = []
        try:
            pack(c2); print(f"{name} WITHOUT WAIVER: PACKED (unexpected)")
        except img.ImageError as e:
            lines = str(e).splitlines()
            print(f"{name} WITHOUT WAIVER: REFUSED, {len(lines)} line(s): " + "; ".join(sorted({l.split(':')[0] for l in lines})))
            for l in lines: print("    " + l.split(' (')[0])
