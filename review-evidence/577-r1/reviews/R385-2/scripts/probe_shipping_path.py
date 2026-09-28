#!/usr/bin/env python3
"""Which production paths run validate_shipping_image?

usage: probe_shipping_path.py <tree> [--plant-reversed-sources]
1. Builder CLI pipeline (endstation_builder.build, what build.sh runs): count checker calls.
2. Gateware image producer sw/litex/milan_soc.py:build_desc_image (writes the shipped
   aem_desc.bin beside the bitstream). litex is not importable here, so the function
   body is extracted verbatim by AST and executed with the module globals it uses.
3. The checked emitter endstation_builder._entity_model_image.
With --plant-reversed-sources the tree's avdecc/aem_descriptors.py d_clock_domain is
expected to have been mutated (by the caller) to emit a reversed source list.
"""
import ast, json, struct, sys, tempfile, types
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root)); sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb
from sw.builder import aem_image_checks as chk
assert Path(eb.__file__).resolve().is_relative_to(root)
calls = []
orig = chk.validate_shipping_image
def counting(blob):
    calls.append(len(blob)); return orig(blob)
chk.validate_shipping_image = counting
eb.aem_image_checks.validate_shipping_image = counting

def clock_domain_sources(blob):
    magic, ver = struct.unpack_from(">IH", blob, 0)
    n, idx = struct.unpack_from(">H", blob, 8)[0], struct.unpack_from(">I", blob, 12)[0]
    for r in range(n):
        cfg, t, cnt, ln, base, _nm, st = struct.unpack_from(">HHHHIHH", blob, idx + 16 * r)
        if t == 0x0024:
            d = blob[base:base + ln]
            off, c = struct.unpack_from(">HH", d, 72)
            return list(struct.unpack_from(f">{c}H", d, off))

cfgpath = root / "configs/endstation_arty_current.yaml"
out = Path(tempfile.mkdtemp(prefix="probe_out_", dir=str(root.parent)))
# 1. builder CLI pipeline
try:
    eb.build(str(cfgpath), outdir=str(out))
    print(f"1 builder.build: completed; checker calls={len(calls)}")
except eb.ConfigError as exc:
    print(f"1 builder.build: REFUSED {exc}; checker calls={len(calls)}")
n1 = len(calls)
# 2. gateware producer, verbatim function body
src = (root / "sw/litex/milan_soc.py").read_text()
fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "build_desc_image")
print("2 milan_soc.build_desc_image references checker:",
      "aem_image_checks" in ast.get_source_segment(src, fn) or "validate_shipping_image" in src)
ovl_dir = out / "entity"; ovl_dir.mkdir()
(ovl_dir / "aem_overlay.json").write_text(json.dumps(eb.emit_aem_overlay(eb.load_config(str(cfgpath)))))
g = dict(__builtins__=__builtins__, json=json, sys=sys, REPO_ROOT=root, Path=Path,
         _builder_out=lambda _d, name: ovl_dir / name)
exec(compile(ast.Module([fn], []), "milan_soc.build_desc_image", "exec"), g)
try:
    blob2, _rep, _ov = g["build_desc_image"]("entity")
    print(f"2 milan_soc.build_desc_image: returned {len(blob2)} B, clock sources {clock_domain_sources(blob2)}; "
          f"checker calls during it={len(calls) - n1}")
except Exception as exc:  # noqa: BLE001
    print(f"2 milan_soc.build_desc_image: RAISED {type(exc).__name__}: {exc}")
    blob2 = None
# 3. the checked emitter
cfg = eb.load_config(str(cfgpath))
try:
    blob3 = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
    print(f"3 _entity_model_image: returned; sources {clock_domain_sources(blob3)}; "
          f"identical to gateware image: {blob3 == blob2}")
except eb.ConfigError as exc:
    print(f"3 _entity_model_image: REFUSED {exc}")
print(f"total checker calls={len(calls)}")
