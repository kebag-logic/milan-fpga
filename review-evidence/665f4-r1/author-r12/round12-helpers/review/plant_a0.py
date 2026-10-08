#!/usr/bin/env python3
"""Copy CTRL to DEST and apply the acmp-init-too-many-sources plant exactly."""
import shutil, sys
from pathlib import Path
src, dest = Path(sys.argv[1]), Path(sys.argv[2])
if dest.exists():
    shutil.rmtree(dest)
shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__"))
f = dest / "acmp/acmp.c"
text = f.read_text()
old, new = "cfg->n_sources > ACMP_MAX_SOURCES) {", "cfg->n_sources > ACMP_MAX_SOURCES + 1u) {"
assert text.count(old) == 1, "plant site not unique"
f.write_text(text.replace(old, new))
print("planted", f)
