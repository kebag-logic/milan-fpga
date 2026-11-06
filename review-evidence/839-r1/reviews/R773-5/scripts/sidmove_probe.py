#!/usr/bin/env python3
"""Usage: sidmove_probe.py <milan_dp-dir>: insert the two legs the Makefile runs into LEGACY_LEGS, in Makefile order. Disposable copies only."""
import os, re, shlex, subprocess, sys
from pathlib import Path
here = Path(sys.argv[1]).resolve()
env = {k: v for k, v in os.environ.items() if not k.startswith(("MAKE", "MFLAGS"))}
text = subprocess.run(["make", "-n", "-C", str(here), "run"], env=env, capture_output=True, text=True).stdout.replace("\\\n", " ")
words = shlex.split([l for l in text.splitlines() if "sim_pool.py" in l][0])[4:]
rows = ""
for i, w in enumerate(words):
    if "sidmove" in w and w.startswith("./"):
        rows += f"    ({words[i-1]!r},\n     {w!r}),\n"
path = here / "test_sim_pool.py"
src = path.read_text()
anchor = re.search(r'^    \("---- #658 the power-on audio maps', src, re.M)
path.write_text(src[:anchor.start()] + rows + src[anchor.start():])
print(rows)
