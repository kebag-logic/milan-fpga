#!/usr/bin/env python3
"""pack_parent.py <parent-root> <out-dir>

Packs every configs/endstation_*.yaml of a disposable parent tree through the
parent's builder caller (endstation_builder._entity_model_image, lint on) and
through gen_desc_image.build() with adp= from the overlay. Writes each image
(aem_desc.bin) and each build() report to <out-dir>, and for a model that
carries waivers, the refusal without them. Prints one summary line per model.
Exit 1 if any model is refused with its own waivers."""
import copy
import hashlib
import sys
from pathlib import Path

root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for d in (root, root / "sw" / "builder", root / "avdecc",
          root / "protocol-processor" / "hdl" / "aecp" / "desc"):
    sys.path.insert(0, str(d))
import endstation_builder as eb          # noqa: E402
import gen_aem_store as aem              # noqa: E402
import gen_aemi_image as join            # noqa: E402
import gen_desc_image as image           # noqa: E402

failed = 0
for path in sorted((root / "configs").glob("endstation_*.yaml")):
    name = path.stem
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
        failed += 1
        (out / f"{name}.refused.txt").write_text(str(exc) + "\n")
        print(f"{name}: REFUSED {str(exc).splitlines()[0]}")
        continue
    builder_bin = files["aem_desc.bin"]
    (out / f"{name}.builder.bin").write_bytes(builder_bin)
    (out / f"{name}.build.bin").write_bytes(img)
    (out / f"{name}.report.txt").write_text(report)
    doms = [d for d in doc.get("descriptors", []) if str(d.get("type", "")).upper()
            in ("CLOCK_SOURCE", "0X000A", "10")]
    print(f"{name}: PACKED builder {len(builder_bin)} B sha256 "
          f"{hashlib.sha256(builder_bin).hexdigest()[:16]} build {len(img)} B sha256 "
          f"{hashlib.sha256(img).hexdigest()[:16]} waivers {len(doc.get('lint_waivers') or [])}")
    if doc.get("lint_waivers"):
        bare = copy.deepcopy(doc)
        del bare["lint_waivers"]
        try:
            image.build(bare, 576)
            print(f"{name} without waivers: PACKED (unexpected)")
            failed += 1
        except image.ImageError as exc:
            (out / f"{name}.nowaiver.txt").write_text(str(exc) + "\n")
            print(f"{name} without waivers: REFUSED, {len(str(exc).splitlines())} line(s)")
sys.exit(1 if failed else 0)
