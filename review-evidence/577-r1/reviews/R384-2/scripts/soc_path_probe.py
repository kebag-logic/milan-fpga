#!/usr/bin/env python3
"""Plant one L6 fault (reversed CLOCK_DOMAIN sources) at the packer and compare
the two emitters of aem_desc.bin at one checkout:
  A. builder  endstation_builder._entity_model_image  (the PR's hook)
  B. SoC      sw/litex/milan_soc.py build_desc_image   (writes aem_desc.bin beside
     the bitstream and CRC-binds it into firmware constants)
B is executed from its own source text (ast-extracted, since the SoC module needs
LiteX); its only stub is _builder_out, pointed at an overlay the builder emitted.
Also checks that the unfaulted images are byte-identical for all five configs.
Round 2: strict verdict line, plus a zero-rate plant.
Usage: soc_path_probe.py <checkout-root> <tmpdir>
"""
import ast, copy, json, os, sys, struct
from pathlib import Path
from unittest.mock import patch
root = Path(sys.argv[1]).resolve(); tmp = Path(sys.argv[2]).resolve(); tmp.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "sw" / "builder")); os.chdir(root)
import endstation_builder as eb
import test_builder as tb
eb._entity_model_image  # noqa
src = (root / "sw/litex/milan_soc.py").read_text()
fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "build_desc_image")
print("SoC emitter: sw/litex/milan_soc.py:%d build_desc_image" % fn.lineno)
print("SoC emitter mentions aem_image_checks:", "aem_image_checks" in ast.get_source_segment(src, fn))
def soc_build_desc_image(overlay_path):
    ns = {"REPO_ROOT": root, "sys": sys, "json": json, "Path": Path,
          "_builder_out": lambda d, name: overlay_path}
    exec(compile(ast.Module([fn], []), "milan_soc.py", "exec"), ns)
    return ns["build_desc_image"]("unused")
for name, path in tb.CONFIGS.items():
    cfg = eb.load_config(path); ovl = eb.emit_aem_overlay(cfg)
    op = tmp / f"{name}_aem_overlay.json"; op.write_text(json.dumps(ovl))
    a = eb._entity_model_image(cfg, ovl)["aem_desc.bin"]
    b, _, _ = soc_build_desc_image(op)
    print(f"{name}: unfaulted builder==SoC bytes: {a == b} ({len(a)} B)")
import gen_desc_image as packer  # on sys.path after the builder ran
cfg = eb.load_config(tb.CONFIGS["arty_current"]); ovl = eb.emit_aem_overlay(cfg)
op = tmp / "arty_current_aem_overlay.json"
orig = packer.build
def planted(document, *a, **k):
    d = copy.deepcopy(document)
    row = next(r for r in d["descriptors"] if r["type"] == 0x0024 and r["index"] == 0)
    body = bytearray.fromhex(row["bytes"]); off, cnt = struct.unpack_from(">HH", body, 72)
    struct.pack_into(f">{cnt}H", body, off, *reversed(range(cnt))); row["bytes"] = body.hex()
    return orig(d, *a, **k)
with patch.object(packer, "build", side_effect=planted):
    try:
        eb._entity_model_image(cfg, ovl); print("A builder: ACCEPTED planted [1,0]")
    except eb.ConfigError as e:
        print("A builder: REFUSED", str(e)[:90])
    try:
        blob, _, _ = soc_build_desc_image(op)
        cd = tb.image_descriptor(blob, 0x0024)
        o, c = struct.unpack_from(">HH", cd, 72)
        print("B SoC: ACCEPTED planted list", list(struct.unpack_from(f">{c}H", cd, o)), "- would be written as aem_desc.bin")
    except RuntimeError as e:
        tag = str(e).split(":")[1].strip() if str(e).startswith("aem_desc.bin:") else "?"
        print("B SoC: REFUSED", type(e).__name__, str(e)[:90])
        print("B SoC verdict:", "REFUSED L6_ORDER" if tag == "L6_ORDER" else f"UNEXPECTED refusal {tag}")
    except Exception as e:
        print("B SoC: UNEXPECTED", type(e).__name__, str(e)[:90])
# Round 2 addition: plant an empty AUDIO_UNIT rate list (F2) through the SoC emitter.
def planted_empty(document, *a, **k):
    d = copy.deepcopy(document)
    row = next(r for r in d["descriptors"] if r["type"] == 0x0002 and r["index"] == 0)
    body = bytearray.fromhex(row["bytes"])[:144]; struct.pack_into(">HH", body, 140, 144, 0)
    row["bytes"] = body.hex()
    return orig(d, *a, **k)
with patch.object(packer, "build", side_effect=planted_empty):
    try:
        soc_build_desc_image(op); print("B SoC zero-rate plant: ACCEPTED")
    except RuntimeError as e:
        print("B SoC zero-rate plant: REFUSED", str(e)[:80])
