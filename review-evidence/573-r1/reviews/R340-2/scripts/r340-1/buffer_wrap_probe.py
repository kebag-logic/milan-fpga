"""Show the listener buffer_length that actually reaches the packed
STREAM_INPUT descriptor when the declared value exceeds the 32-bit field.

Usage: python3 buffer_wrap_probe.py <tree root>
"""
import json
from pathlib import Path
import sys
import tempfile

import yaml

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb  # noqa: E402
import gen_aemi_image as join  # noqa: E402

STREAM_INPUT, BUFFER_OFFSET = 0x0005, 128  # IEEE 1722.1-2021 Table 7-8


def packed_buffers(declared):
    raw = yaml.safe_load((ROOT / "configs/endstation_ax7101_8x8.yaml").read_text())
    raw["streams"]["listeners"][0]["buffer_length_ns"] = declared
    with tempfile.TemporaryDirectory(prefix="r340-wrap-") as tmp:
        path = Path(tmp) / "case.yaml"
        path.write_text(yaml.safe_dump(raw))
        try:
            cfg = eb.load_config(path)
        except eb.ConfigError as exc:
            return dict(declared=declared, loader="refused", reason=str(exc))
    overlay = eb.emit_aem_overlay(cfg)
    document = join.model_to_document(
        join.aem.build_model(join.aem.spec_from_overlay(overlay)),
        join.identity_from_overlay(overlay))
    blob, _ = join.image.build(document, 576)
    rows = [d for d in document["descriptors"]
            if d["type"] == STREAM_INPUT and d["index"] == 0]
    body = bytes.fromhex(rows[0]["bytes"])
    field = int.from_bytes(body[BUFFER_OFFSET:BUFFER_OFFSET + 4], "big")
    return dict(declared=declared, loader="accepted", image="accepted",
                image_bytes=len(blob), overlay_value=overlay["stream_inputs"][0]["buffer_length_ns"],
                packed_stream_input0_buffer_length=field,
                packed_below_floor=field < 2126000)


if __name__ == "__main__":
    out = [packed_buffers(v) for v in (2126000, 2125999, (1 << 32) - 1, 1 << 32,
                                       (1 << 32) + 2125999)]
    print(json.dumps(out, indent=1))
