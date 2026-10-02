#!/usr/bin/env python3
"""Pack every configs/endstation_*.yaml of a scratch parent (cwd) through the
builder caller and through build() with the overlay's driven ADP values, lint
on. Prints, per config: image sha256 and size, the lint report block, the
clock-source list of each CLOCK_DOMAIN with each source's type and location;
for a config with waivers, the refusal without them and with each waiver's
index range widened by one. Exit 1 on an unexpected outcome."""
import copy
import hashlib
import struct
import sys
from pathlib import Path

ROOT = Path.cwd()
for d in (ROOT, ROOT / "sw" / "builder", ROOT / "avdecc",
          ROOT / "protocol-processor" / "hdl" / "aecp" / "desc"):
    sys.path.insert(0, str(d))
sys.dont_write_bytecode = True
import endstation_builder as eb  # noqa: E402
import gen_aem_store as aem      # noqa: E402
import gen_aemi_image as join    # noqa: E402
import gen_desc_image as image   # noqa: E402

KIND = {0: "INTERNAL", 1: "EXTERNAL", 2: "INPUT_STREAM"}


def sources(doc) -> list[str]:
    """Each CLOCK_DOMAIN's clock_sources list, and each CLOCK_SOURCE's type and location."""
    out = []
    rows = [(r, image.descriptor_bytes(r)) for r in doc["descriptors"]]
    for r, b in rows:
        dtype = struct.unpack_from(">H", b, 0)[0]
        if dtype == 0x0024:
            n = struct.unpack_from(">H", b, 74)[0]
            out.append(f"CLOCK_DOMAIN cfg {r.get('configuration')} {struct.unpack_from('>H', b, 2)[0]}: "
                       f"{list(struct.unpack_from(f'>{n}H', b, 76))}")
    for r, b in rows:
        dtype = struct.unpack_from(">H", b, 0)[0]
        if dtype == 0x000A:
            st, lt, li = (struct.unpack_from(">H", b, o)[0] for o in (72, 82, 84))
            out.append(f"  CLOCK_SOURCE {struct.unpack_from('>H', b, 2)[0]}: {KIND.get(st, st)} at type {lt:#06x} index {li}")
    return out


bad = 0
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
        img, report = image.build(doc, 576, adp=adp)
    except Exception as exc:  # noqa: BLE001
        bad += 1
        print(f"== {path.stem}: REFUSED\n   " + str(exc).replace("\n", "\n   "))
        continue
    shipped = files["aem_desc.bin"]
    print(f"== {path.stem}: PACKED builder {len(shipped)} B sha256 {hashlib.sha256(shipped).hexdigest()}; "
          f"build(adp=) {len(img)} B sha256 {hashlib.sha256(img).hexdigest()}; same={img == shipped}")
    print("   " + report[report.index("semantic lint"):].rstrip().replace("\n", "\n   "))
    print("   map sha256 " + hashlib.sha256(report.encode()).hexdigest())
    for line in sources(doc):
        print("   " + line)
    waivers = doc.get("lint_waivers") or []
    if waivers:
        bare = copy.deepcopy(doc); del bare["lint_waivers"]
        try:
            image.build(bare, 576); print("   without waivers: PACKED (unexpected)"); bad += 1
        except image.ImageError as exc:
            print("   without waivers: REFUSED\n      " + str(exc).replace("\n", "\n      "))
        wide = copy.deepcopy(doc)
        for w in wide["lint_waivers"]:
            if "last" in w:
                w["last"] += 1
        try:
            image.build(wide, 576); print("   widened waiver: PACKED (unexpected)"); bad += 1
        except image.ImageError as exc:
            print("   widened waiver: REFUSED\n      " + str(exc).replace("\n", "\n      "))
sys.exit(1 if bad else 0)
