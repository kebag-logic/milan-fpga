#!/usr/bin/env python3
"""Run register freshness with a caller-selected interpreter carrying wavedrom==2.0.3.post3."""
from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
cmd=[sys.executable,"-B","scripts/gen_register_reference.py","--check"]
with (p/"register-generation-scoped.log").open("w") as log:
 log.write("COMMAND: "+repr(cmd)+"\n");log.flush()
 result=subprocess.run(cmd,cwd=Path(sys.argv[1]).resolve(),stdout=log,stderr=subprocess.STDOUT)
(p/"register-generation-scoped.rc").write_text(str(result.returncode)+"\n")
print((p/"register-generation-scoped.log").read_text());sys.exit(result.returncode)
