#!/usr/bin/env python3
"""sha256 of the five tracked shipping images from both emitters in <tree>.

Round 2: besides endstation_builder._entity_model_image (aem_desc.bin/json/map), runs the
deployed-image emitter sw/litex/milan_soc.py:build_desc_image, extracted verbatim by AST
(litex is not importable here) with only the overlay-path lookup supplied.
"""
import ast, hashlib, json, sys, tempfile
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root)); sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb
assert Path(eb.__file__).resolve().is_relative_to(root)
src = (root / "sw/litex/milan_soc.py").read_text()
fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "build_desc_image")
tmp = Path(tempfile.mkdtemp(prefix="imghash_", dir=str(root.parent)))
g = dict(__builtins__=__builtins__, json=json, sys=sys, REPO_ROOT=root, Path=Path,
         _builder_out=lambda _d, name: tmp / name)
exec(compile(ast.Module([fn], []), "milan_soc.build_desc_image", "exec"), g)
for stem in ("arty_current", "arty_4x4", "arty_8ch", "ax7101_8x8", "ax7101_1x1_tdm8"):
    cfg = eb.load_config(str(root / f"configs/endstation_{stem}.yaml"))
    overlay = eb.emit_aem_overlay(cfg)
    out = eb._entity_model_image(cfg, overlay)
    for k in sorted(out):
        v = out[k] if isinstance(out[k], bytes) else out[k].encode()
        print(stem, k, len(v), hashlib.sha256(v).hexdigest())
    (tmp / "aem_overlay.json").write_text(json.dumps(overlay))
    blob, report, _ov = g["build_desc_image"]("x")
    print(stem, "soc:aem_desc.bin", len(blob), hashlib.sha256(blob).hexdigest())
    print(stem, "soc:aem_desc.map", len(report.encode()), hashlib.sha256(report.encode()).hexdigest())
