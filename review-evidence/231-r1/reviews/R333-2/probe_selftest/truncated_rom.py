#!/usr/bin/env python3
"""Show what the surviving generated-ROM depth mutant admits on a real export.
usage: truncated_rom.py <pp_baseline.py> <gateware-copy-with-truncated-rom>
Runs prepare(..., synthesis_only=True) from the pristine helper and from the
mutant that drops the generated-ROM depth argument; prints each outcome."""
import importlib.util, sys, tempfile
from pathlib import Path
src = Path(sys.argv[1]).read_text()
gateware = Path(sys.argv[2])
old = "            inputs.append(image_record(path, int(words), int(width)))\n"
assert src.count(old) == 1
for name, text in (("pristine", src),
                   ("mutant", src.replace(old, "            inputs.append(image_record(path, None, int(width)))\n"))):
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "pp_baseline.py"
        f.write_text(text)
        spec = importlib.util.spec_from_file_location(name, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            mod.prepare(gateware, gateware, None, True)
        except (ValueError, FileNotFoundError) as error:
            print(f"{name}: refused: {error}")
        else:
            print(f"{name}: ACCEPTED truncated firmware ROM")
