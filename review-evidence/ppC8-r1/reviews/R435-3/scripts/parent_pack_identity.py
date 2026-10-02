#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Pack the parent's five shipping models and print a sha256 per artifact.

usage: parent_pack_identity.py PARENT_TREE

PARENT_TREE holds the parent's sw/, avdecc/ and configs/ (with the adoption
patches applied) and protocol-processor/ pointing at the processor tree under
test. For each model: the builder path (_entity_model_image, every artifact it
returns), and the packer called directly on the same document with the
overlay's driven ADP values (image bytes and layout report). Run once per
processor tree and diff the outputs: identical lines mean byte-identical packing.
"""
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root), str(root / "sw/builder"), str(root / "avdecc"),
                str(root / "protocol-processor/hdl/aecp/desc")]
import endstation_builder as eb  # noqa: E402
import gen_aem_store as aem  # noqa: E402
import gen_aemi_image as join  # noqa: E402
import gen_desc_image as img  # noqa: E402

CONFIGS = ("arty_current", "arty_4x4", "arty_8ch", "ax7101_1x1_tdm8", "ax7101_8x8")


def h(value) -> str:
    data = value if isinstance(value, (bytes, bytearray)) else str(value).encode()
    return hashlib.sha256(data).hexdigest()


status = 0
for name in CONFIGS:
    cfg = eb.load_config(str(root / "configs" / f"endstation_{name}.yaml"))
    overlay = eb.emit_aem_overlay(cfg)
    try:
        out = eb._entity_model_image(cfg, overlay)
        for key in sorted(out):
            print(f"{name} builder {key} {h(out[key])}")
        digest = [ln for ln in str(out.get("aem_desc.map", "")).splitlines() if "digest" in ln]
        print(f"{name} builder digest-line {digest}")
        waived = [ln for ln in str(out.get("aem_desc.map", "")).splitlines() if "waive" in ln]
        print(f"{name} builder waiver-lines {waived}")
    except Exception as exc:  # noqa: BLE001
        status = 1
        print(f"{name} builder REFUSED {type(exc).__name__}: {exc}")
        continue
    document = join.model_to_document(aem.build_model(aem.spec_from_overlay(overlay)),
                                      join.identity_from_overlay(overlay))
    adp = {"entity_model_id": int(overlay["entity"]["entity_model_id"], 16),
           "talker_sources": overlay["adp"]["talker_stream_sources"],
           "listener_sinks": overlay["adp"]["listener_stream_sinks"]}
    try:
        image, report = img.build(document, 576, adp=adp)
        print(f"{name} direct image {h(image)} report {h(report)}")
    except img.ImageError as exc:
        status = 1
        print(f"{name} direct REFUSED {exc}")
sys.exit(status)
