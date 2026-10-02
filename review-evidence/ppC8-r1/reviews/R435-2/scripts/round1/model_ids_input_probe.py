#!/usr/bin/env python3
"""What build() raises for a malformed recorded-digest map (model_ids).
usage: model_ids_input_probe.py <processor-tree>"""
import importlib.util, json, sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("gen_desc_image", tree / "hdl/aecp/desc/gen_desc_image.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
model = json.loads((tree / "hdl/aecp/desc/milan_min.json").read_text())
for ids in ({"not-hex": "00"}, {"0x020000FFFE00C801": None}, ["0x020000FFFE00C801"]):
    try:
        g.build(model, model_ids=ids)
        print(f"{ids!r}: PACKED")
    except g.ImageError as exc:
        print(f"{ids!r}: ImageError {str(exc)[:120]}")
    except Exception as exc:  # noqa: BLE001
        print(f"{ids!r}: {type(exc).__name__} (not an ImageError): {exc}")
