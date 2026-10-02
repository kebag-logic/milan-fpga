#!/usr/bin/env python3
"""Scratch: ax7101_8x8's packed document with its waiver widened by one port
(0..8) must be refused as stale. Run from a scratch parent root."""
import copy
import sys
from pathlib import Path

ROOT = Path.cwd()
for d in (ROOT, ROOT / "sw" / "builder", ROOT / "avdecc", ROOT / "protocol-processor" / "hdl" / "aecp" / "desc"):
    sys.path.insert(0, str(d))
import endstation_builder as eb          # noqa: E402
import gen_aem_store as aem              # noqa: E402
import gen_aemi_image as join            # noqa: E402
import gen_desc_image as image           # noqa: E402

overlay = eb.emit_aem_overlay(eb.load_config(ROOT / "configs/endstation_ax7101_8x8.yaml"))
doc = join.model_to_document(aem.build_model(aem.spec_from_overlay(overlay)), join.identity_from_overlay(overlay))
wide = copy.deepcopy(doc)
wide["lint_waivers"][0]["last"] = 8
try:
    image.build(wide, 576)
    print("widened waiver: PACKED (unexpected)")
    sys.exit(1)
except image.ImageError as exc:
    print("widened waiver: REFUSED:", str(exc))
