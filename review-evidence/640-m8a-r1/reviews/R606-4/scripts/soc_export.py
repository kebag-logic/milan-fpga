#!/usr/bin/env python3
"""Export one shipping config's SoC gateware (no Vivado, no software) from a given source tree.

usage: soc_export.py <tree> <config-name> <out-dir> [extra milan_soc.py arguments...]

The argv is the end-station builder's own (`emit_soc_argv`), as the tree's
sw/litex/test_ctrl_memory.py derives it. As that test's SoC child does, LiteX's
firmware data packages are refused and LiteX's headers are written without
the firmware make inputs, so a pins-only interpreter can export. Writes
<out-dir> and <out-dir>.result.json (rc and any error).
"""
import importlib.abc
import json
import os
import sys
from pathlib import Path

tree, name, out, *extra = sys.argv[1:]
tree = Path(tree).resolve()
out = Path(out).resolve()
sys.path[:0] = [str(tree / "sw/litex"), str(tree / "sw/builder")]
os.chdir(tree / "sw/litex")


class Refuse(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.startswith("pythondata_software_"):
            raise ImportError(f"{fullname}: refused in this export")
        return None


import endstation_builder as eb  # noqa: E402

config = tree / "configs" / f"{name}.yaml"
cfg = eb.load_config(str(config))
eb.build(str(config))
argv = eb.emit_soc_argv(cfg) + ["--entity-gen-dir", str(tree / "configs/generated" / cfg["name"]),
                                "--output-dir", str(out), "--no-compile-software", *extra]
sys.meta_path.insert(0, Refuse())
from litex.soc.integration.builder import Builder  # noqa: E402
original = Builder._generate_includes
Builder._generate_includes = lambda self, with_bios=True: original(self, with_bios=False)
import milan_soc  # noqa: E402

result = {"argv": argv, "rc": 0}
sys.argv = ["milan_soc.py", *argv]
try:
    milan_soc.main()
except SystemExit as exc:
    result["rc"] = 0 if exc.code is None else exc.code if isinstance(exc.code, int) else 1
except Exception as exc:  # recorded as itself
    result.update(rc=1, error=f"{type(exc).__name__}: {exc}")
Path(str(out) + ".result.json").write_text(json.dumps(result, indent=1) + "\n")
print(json.dumps({"rc": result["rc"], "error": result.get("error")}))
sys.exit(1 if result["rc"] else 0)
