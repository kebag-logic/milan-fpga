#!/usr/bin/env python3
"""Pack the parent's five shipping models through the processor's real lint.

For each config: load it, emit its overlay, and run the builder's own packing
path (_entity_model_image, which also runs the parent's post-pack shipping
checks); print the lint block of the layout report. Then pack the same
document with the overlay's ADP values as `adp=` (they must agree). For a
config that declares a waiver, also pack it with the waiver removed (the L1
refusal must come back) and with the waiver range widened by one port (must be
refused as stale).

usage: parent_models_lint.py <parent-tree with protocol-processor at the head>
"""
import copy
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/builder"), str(root / "avdecc"),
                str(root / "protocol-processor/hdl/aecp/desc")]
import endstation_builder as eb  # noqa: E402
import gen_aem_store as aem  # noqa: E402
import gen_aemi_image as join  # noqa: E402
import gen_desc_image as img  # noqa: E402

CONFIGS = ("arty_current", "arty_4x4", "arty_8ch", "ax7101_1x1_tdm8", "ax7101_8x8")
status = 0


def document(overlay):
    return join.model_to_document(aem.build_model(aem.spec_from_overlay(overlay)),
                                  join.identity_from_overlay(overlay))


def lint_block(report):
    lines = report.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("semantic lint"))
    return lines[start:]


for name in CONFIGS:
    cfg = eb.load_config(str(root / "configs" / f"endstation_{name}.yaml"))
    overlay = eb.emit_aem_overlay(cfg)
    print(f"== {name}: waivers declared {len(overlay.get('model_lint_waivers', []))}")
    try:
        report = eb._entity_model_image(cfg, overlay)["aem_desc.map"]
        print("   builder path: PACKED")
        for ln in lint_block(report):
            print("   | " + ln)
    except Exception as exc:  # noqa: BLE001 - report every refusal
        status = 1
        print(f"   builder path: REFUSED {type(exc).__name__}: {exc}")
        continue
    adp = {"entity_model_id": int(overlay["entity"]["entity_model_id"], 16),
           "talker_sources": overlay["adp"]["talker_stream_sources"],
           "listener_sinks": overlay["adp"]["listener_stream_sinks"]}
    try:
        _, rep = img.build(document(overlay), 576, adp=adp)
        print(f"   adp={adp}: PACKED, {rep.count('(driven value checked)')} driven values checked")
    except img.ImageError as exc:
        status = 1
        print(f"   adp={adp}: REFUSED {exc}")
    if overlay.get("model_lint_waivers"):
        bare = copy.deepcopy(overlay)
        bare.pop("model_lint_waivers")
        try:
            img.build(document(bare), 576)
            status = 1
            print("   waiver removed: PACKED (expected a refusal)")
        except img.ImageError as exc:
            lines = str(exc).splitlines()
            checks = sorted({ln.split(":")[0] for ln in lines})
            scopes = [ln.split(":")[1].strip() for ln in lines]
            print(f"   waiver removed: REFUSED {len(lines)} line(s), checks {checks}, scopes {scopes}")
        wide = copy.deepcopy(overlay)
        wide["model_lint_waivers"][0]["last"] += 1
        try:
            img.build(document(wide), 576)
            status = 1
            print("   waiver widened by one port: PACKED (expected stale)")
        except img.ImageError as exc:
            print(f"   waiver widened by one port: REFUSED {exc}")
print(f"status {status}")
sys.exit(status)
