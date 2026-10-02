#!/usr/bin/env python3
"""parent_clock_sources.py <parent-root>

For each configs/endstation_*.yaml, assembles the packer document the
builder packs, and prints per configuration: each CLOCK_DOMAIN's
clock_sources list, and each CLOCK_SOURCE's type and location (IEEE
1722.1-2021 §7.2.9: clock_source_type at 72, location type at 82, location
index at 84), naming STREAM_INPUTs as CRF or AAF by their current format's
subtype octet (current_format at 74, §7.2.6)."""
import struct
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
for d in (root, root / "sw" / "builder", root / "avdecc",
          root / "protocol-processor" / "hdl" / "aecp" / "desc"):
    sys.path.insert(0, str(d))
import endstation_builder as eb          # noqa: E402
import gen_aem_store as aem              # noqa: E402
import gen_aemi_image as join            # noqa: E402
import gen_desc_image as image           # noqa: E402

KIND = {0: "INTERNAL", 1: "EXTERNAL", 2: "INPUT_STREAM"}
for path in sorted((root / "configs").glob("endstation_*.yaml")):
    cfg = eb.load_config(path)
    overlay = eb.emit_aem_overlay(cfg)
    doc = join.model_to_document(aem.build_model(aem.spec_from_overlay(overlay)),
                                 join.identity_from_overlay(overlay))
    groups = image._grouped_descriptors(doc)
    for c in sorted({k[0] for k in groups}):
        sins = groups.get((c, 0x0005), {})
        fam = {}
        for i, (b, _) in sins.items():
            fam[i] = {0x02: "AAF", 0x04: "CRF"}.get(b[74] & 0x7F, f"0x{b[74]:02X}")
        for i, (b, _) in sorted(groups.get((c, 0x0024), {}).items()):
            off, cnt = struct.unpack_from(">HH", b, 72)
            lst = list(struct.unpack_from(f">{cnt}H", b, off))
            print(f"{path.stem} cfg {c} CLOCK_DOMAIN {i}: count {cnt} list {lst}")
        for i, (b, _) in sorted(groups.get((c, 0x000A), {}).items()):
            st, lt, li = (struct.unpack_from(">H", b, o)[0] for o in (72, 82, 84))
            where = f"STREAM_INPUT {li} ({fam.get(li, '?')})" if lt == 0x0005 else f"type 0x{lt:04X} {li}"
            print(f"{path.stem} cfg {c}   CLOCK_SOURCE {i}: {KIND.get(st, st)} at {where}")
