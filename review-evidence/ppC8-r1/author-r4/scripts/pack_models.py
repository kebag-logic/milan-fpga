#!/usr/bin/env python3
"""Scratch: pack every tracked parent config through the real builder path,
from a scratch parent root. For each configs/endstation_*.yaml: the builder
caller endstation_builder._entity_model_image (lint on, and the parent's own
post-pack shipping checks), then build() again with adp= from the overlay;
for a config that carries waivers, once more with them removed. Prints the
lint's report block or the refusal. Exit 1 if a config with its own waivers
is refused."""
import copy
import sys
from pathlib import Path

ROOT = Path.cwd()
for d in (ROOT, ROOT / "sw" / "builder", ROOT / "avdecc",
          ROOT / "protocol-processor" / "hdl" / "aecp" / "desc"):
    sys.path.insert(0, str(d))
import endstation_builder as eb          # noqa: E402
import gen_aem_store as aem              # noqa: E402
import gen_aemi_image as join            # noqa: E402
import gen_desc_image as image           # noqa: E402

failed = 0
for path in sorted((ROOT / "configs").glob("endstation_*.yaml")):
    cfg = eb.load_config(path)
    overlay = eb.emit_aem_overlay(cfg)
    try:
        files = eb._entity_model_image(cfg, overlay)
        doc = join.model_to_document(aem.build_model(aem.spec_from_overlay(overlay)),
                                     join.identity_from_overlay(overlay))
        adp = {"entity_model_id": int(overlay["entity"]["entity_model_id"], 16),
               "talker_sources": int(overlay["adp"]["talker_stream_sources"]),
               "listener_sinks": int(overlay["adp"]["listener_stream_sinks"])}
        _, report = image.build(doc, 576, adp=adp)
    except Exception as exc:  # noqa: BLE001 - scratch: report and continue
        failed += 1
        print(f"== {path.stem}: REFUSED\n   " + str(exc).replace("\n", "\n   "))
        continue
    lint = report[report.index("semantic lint"):]
    print(f"== {path.stem}: PACKED, {len(files['aem_desc.bin'])} bytes; driven ADP values checked")
    print("   " + lint.rstrip().replace("\n", "\n   "))
    if doc.get("lint_waivers"):
        bare = copy.deepcopy(doc)
        del bare["lint_waivers"]
        try:
            image.build(bare, 576)
            print(f"== {path.stem} without its waivers: PACKED (unexpected)")
            failed += 1
        except image.ImageError as exc:
            lines = str(exc).splitlines()
            print(f"== {path.stem} without its waivers: REFUSED, {len(lines)} line(s)")
            print("   " + "\n   ".join(lines))
sys.exit(1 if failed else 0)
