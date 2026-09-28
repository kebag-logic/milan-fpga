#!/usr/bin/env python3
"""sha256 of the aem_desc.bin bytes from BOTH emitters for the five shipping configs:
  builder  endstation_builder._entity_model_image
  SoC      sw/litex/milan_soc.py build_desc_image (ast-extracted; only _builder_out stubbed)
Usage: image_hashes.py <checkout-root> <tmpdir>"""
import ast, hashlib, json, os, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); tmp = Path(sys.argv[2]).resolve(); tmp.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "sw" / "builder")); os.chdir(root)
import endstation_builder as eb, test_builder as tb
print("checker present:", hasattr(eb, "aem_image_checks"))
src = (root / "sw/litex/milan_soc.py").read_text()
fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "build_desc_image")
def soc(op):
    ns = {"REPO_ROOT": root, "sys": sys, "json": json, "Path": Path, "_builder_out": lambda d, n: op}
    exec(compile(ast.Module([fn], []), "milan_soc.py", "exec"), ns)
    return ns["build_desc_image"]("unused")[0]
for name, path in tb.CONFIGS.items():
    cfg = eb.load_config(path); ovl = eb.emit_aem_overlay(cfg)
    op = tmp / f"{name}.json"; op.write_text(json.dumps(ovl))
    a = eb._entity_model_image(cfg, ovl)["aem_desc.bin"]; b = soc(op)
    print(name, "builder", len(a), hashlib.sha256(a).hexdigest())
    print(name, "soc", len(b), hashlib.sha256(b).hexdigest())
