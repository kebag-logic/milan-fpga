"""Scratch: per tracked parent config, the CLOCK_SOURCE descriptors (type,
location type, location index) and each CLOCK_DOMAIN's clock_sources list, as
build() receives them. Run from a scratch parent root."""
import struct
import sys
from pathlib import Path

ROOT = Path.cwd()
for d in (ROOT, ROOT / "sw" / "builder", ROOT / "avdecc", ROOT / "protocol-processor" / "hdl" / "aecp" / "desc"):
    sys.path.insert(0, str(d))
import endstation_builder as eb          # noqa: E402
import gen_aem_store as aem              # noqa: E402
import gen_aemi_image as join            # noqa: E402
import gen_desc_image as image           # noqa: E402

KIND = {0: "INTERNAL", 1: "EXTERNAL", 2: "INPUT_STREAM"}
for path in sorted((ROOT / "configs").glob("endstation_*.yaml")):
    overlay = eb.emit_aem_overlay(eb.load_config(path))
    doc = join.model_to_document(aem.build_model(aem.spec_from_overlay(overlay)), join.identity_from_overlay(overlay))
    rows = {}
    for row in doc["descriptors"]:
        code = image._type_code(row["type"])
        rows.setdefault(code, {})[row["index"]] = image.descriptor_bytes(row)
    srcs = []
    for i, b in sorted(rows.get(0x000A, {}).items()):
        t, lt, li = struct.unpack_from(">H", b, 72)[0], *struct.unpack_from(">HH", b, 82)
        srcs.append(f"{i}:{KIND.get(t, t)}@{'STREAM_INPUT ' + str(li) if lt == 5 else hex(lt) + '/' + str(li)}")
    doms = []
    for i, b in sorted(rows.get(0x0024, {}).items()):
        off, n = struct.unpack_from(">HH", b, 72)
        doms.append(f"domain {i}: {list(struct.unpack_from(f'>{n}H', b, off))}")
    fam = []
    for i, b in sorted(rows.get(0x0005, {}).items()):
        cur = struct.unpack_from(">Q", b, 74)[0]
        fam.append({0x02: "AAF", 0x04: "CRF"}.get(cur >> 56 & 0x7F, hex(cur >> 56)))
    print(f"== {path.stem}: STREAM_INPUTs {fam}\n   sources {srcs}\n   " + "; ".join(doms))
