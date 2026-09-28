#!/usr/bin/env python3
"""Does build_desc_image's `from sw.builder import aem_image_checks` resolve to
the repository checker under the sys.path that `python3 milan_soc.py` (run from
sw/litex, as build.sh/deploy.sh do) has at that point?  LiteX/migen are absent
here, so milan_soc's own sys.path inserts (lines 69-83 and 3352-3353) are
replayed in order, and the local modules milan_soc imports before the call are
imported first so any `sw` binding they make is kept.
Run as: python3 -I -B soc_import_probe.py <checkout-root>  (-B: -I ignores PYTHONDONTWRITEBYTECODE, and
nvm_shape resolves its own directory through the farm symlink into the checkout)
"""
import ast, importlib, os, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); soc = root / "sw" / "litex"
src = (soc / "milan_soc.py").read_text()
inserts = [n.lineno for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Call)
           and ast.unparse(n.func) == "sys.path.insert"]
print("milan_soc sys.path.insert lines:", inserts)
os.chdir(soc); sys.path[0] = str(soc)          # script directory, as for `python3 milan_soc.py`
sys.path.insert(0, str(root))                  # line 72
sys.path.insert(0, str(soc / "platforms"))     # line 76
sys.path.insert(0, str(root / "scripts"))      # line 83
for mod in ("boot_policy", "gptp_owner_contract", "qspi_owner_transition", "nvm_shape"):
    try:
        importlib.import_module(mod); print("pre-import", mod, "ok")
    except Exception as e:
        print("pre-import", mod, "unavailable:", type(e).__name__, str(e)[:80])
print("sw bound before call:", "sw" in sys.modules)
sys.path.insert(0, str(root / "avdecc"))       # line 3352
sys.path.insert(0, str(root / "protocol-processor/hdl/aecp/desc"))  # line 3353
from sw.builder import aem_image_checks
print("resolved:", Path(aem_image_checks.__file__).resolve().relative_to(root))
print("sw package kind:", "namespace" if getattr(sys.modules["sw"], "__file__", None) is None else sys.modules["sw"].__file__)
print("consumer walk:", aem_image_checks._sampling_rate_walk())
