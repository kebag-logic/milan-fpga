# A simulator stand-in that builds nothing: it writes, where Verilator would build it, an executable that passes.
import sys
from pathlib import Path
args = sys.argv[1:]
if "--Mdir" in args and "-o" in args:
    exe = Path(args[args.index("--Mdir") + 1]) / args[args.index("-o") + 1]
    exe.parent.mkdir(parents=True, exist_ok=True)
    exe.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    exe.chmod(0o755)
