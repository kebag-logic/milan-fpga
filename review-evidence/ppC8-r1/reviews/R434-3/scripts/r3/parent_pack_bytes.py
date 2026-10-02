#!/usr/bin/env python3
"""Pack the parent's five models through the builder path and print, per
model, the sha256 of the packed image and of its report (lint on), the model
digest, the sha256 of the image with the lint off, and for a waived model the
refusal without its waiver and with it widened by one port.
Run once per parent tree (each carries its own protocol-processor copy), then
diff the outputs to show byte identity across processor heads.
Usage: parent_pack_bytes.py <parent-tree>"""
import copy
import hashlib
import pathlib
import sys

root = pathlib.Path(sys.argv[1]).resolve()
for d in (root / "sw/builder", root / "avdecc", root / "protocol-processor/hdl/aecp/desc"):
    sys.path.insert(0, str(d))
import endstation_builder as eb      # noqa: E402
import gen_aem_store as aem          # noqa: E402
import gen_aemi_image as join        # noqa: E402
import gen_desc_image as img         # noqa: E402

CONFIGS = ["arty_current", "arty_4x4", "arty_8ch", "ax7101_8x8", "ax7101_1x1_tdm8"]
sha = lambda b: hashlib.sha256(b).hexdigest()


def document(cfg):
    ovl = eb.emit_aem_overlay(cfg)
    return join.model_to_document(aem.build_model(aem.spec_from_overlay(ovl)), join.identity_from_overlay(ovl))


def refusal(doc):
    try:
        img.build(doc, 576)
        return "PACKED"
    except img.ImageError as e:
        return "REFUSED " + " | ".join(l.split(" (")[0] for l in str(e).splitlines())


for name in CONFIGS:
    cfg = eb.load_config(str(root / f"configs/endstation_{name}.yaml"))
    doc = document(cfg)
    try:
        blob, report = img.build(copy.deepcopy(doc), 576)
        dig = [l for l in report.splitlines() if "model digest" in l][0].split()[3]
        waived = [l.strip() for l in report.splitlines() if " waived" in l]
        print(f"{name}: PACKED image {sha(blob)} report {sha(report.encode())} digest {dig} waivers {waived}")
    except img.ImageError as e:
        print(f"{name}: REFUSED {str(e).splitlines()[:3]}")
    off, _ = img.build(copy.deepcopy(doc), 576, lint=False)
    print(f"    lint off: image {sha(off)}")
    if cfg.get("model_lint_waivers"):
        bare = copy.deepcopy(cfg); bare["model_lint_waivers"] = []
        print(f"    without waiver: {refusal(document(bare))}")
        wide = copy.deepcopy(doc)
        for w in wide.get("lint_waivers", []):
            w["last"] = w["last"] + 1
        print(f"    waiver widened by one: {refusal(wide)}")
