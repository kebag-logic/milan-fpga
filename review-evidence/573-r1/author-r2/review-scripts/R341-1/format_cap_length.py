"""Packed STREAM_INPUT length at the accepted format-count boundary.

Run: python3 -B format_cap_length.py <tree>
IEEE 1722.1-2021 7.2: a descriptor is at most 508 octets; Table 7-8: formats at
138, number_of_formats at most 46.
"""
from pathlib import Path
import sys
import tempfile

import yaml

TREE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(TREE / "sw/builder"))
import endstation_builder as eb  # noqa: E402
import gen_aemi_image as join  # noqa: E402

for final in (46, 47):
    raw = yaml.safe_load((TREE / "configs/endstation_arty_4x4.yaml").read_text())
    raw["streams"]["talkers"][0]["formats"] = ["0x0205022000806000"] * final
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "case.yaml"
        path.write_text(yaml.safe_dump(raw))
        cfg = eb.load_config(path)
    overlay = eb.emit_aem_overlay(cfg)
    document = join.model_to_document(
        join.aem.build_model(join.aem.spec_from_overlay(overlay)),
        join.identity_from_overlay(overlay))
    blob, _ = join.image.build(document, 576)
    row = next(r for r in document["descriptors"] if r["type"] == 0x0006 and r["index"] == 0)
    body = bytes.fromhex(row["bytes"])
    print(f"STREAM_OUTPUT[0] final formats={final}: loader ACCEPTED, image packed "
          f"({len(blob)} bytes); descriptor length {len(body)} octets; "
          f"formats_offset {int.from_bytes(body[82:84], 'big')}; "
          f"number_of_formats {int.from_bytes(body[84:86], 'big')}; "
          f"exceeds 508-octet maximum: {len(body) > 508}")
