#!/usr/bin/env python3
"""Generator-level plant (the prior external round's F1 variant): reverse the
identity list inside avdecc/aem_descriptors.py d_clock_domain in a farm copy,
then run the loader, the builder emitter and the SoC emitter (ast-extracted
build_desc_image; only _builder_out stubbed).
Usage: generator_plant_probe.py <farm-root> <tmpdir>   (the farm's avdecc/aem_descriptors.py
must be a real copy; this script edits it in place)"""
import ast, json, os, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); tmp = Path(sys.argv[2]).resolve(); tmp.mkdir(parents=True, exist_ok=True)
gen = root / "avdecc" / "aem_descriptors.py"
assert not gen.is_symlink(), "aem_descriptors.py must be a real copy in the farm"
text = gen.read_text(); old = "    sources = list(range(n_sources))\n"
assert text.count(old) == 1
gen.write_text(text.replace(old, "    sources = list(reversed(range(n_sources)))  # PROBE PLANT\n"))
sys.path.insert(0, str(root / "sw" / "builder")); os.chdir(root)
import endstation_builder as eb, test_builder as tb
import aem_descriptors
print("planted generator:", Path(aem_descriptors.__file__).resolve() == gen, "| PROBE PLANT present:", "PROBE PLANT" in gen.read_text())
cfg = eb.load_config(tb.CONFIGS["arty_current"]); ovl = eb.emit_aem_overlay(cfg)
print("loader + overlay: accepted")
op = tmp / "arty_current.json"; op.write_text(json.dumps(ovl))
try:
    eb._entity_model_image(cfg, ovl); print("builder emitter: ACCEPTED")
except eb.ConfigError as e:
    print("builder emitter: REFUSED", str(e)[:100])
src = (root / "sw/litex/milan_soc.py").read_text()
fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "build_desc_image")
ns = {"REPO_ROOT": root, "sys": sys, "json": json, "Path": Path, "_builder_out": lambda d, n: op}
exec(compile(ast.Module([fn], []), "milan_soc.py", "exec"), ns)
try:
    ns["build_desc_image"]("unused"); print("SoC emitter: ACCEPTED")
except RuntimeError as e:
    print("SoC emitter: REFUSED", str(e)[:100])
