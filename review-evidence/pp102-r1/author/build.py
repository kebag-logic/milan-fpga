import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

evidence = Path(__file__).parent
identity = json.loads((evidence / "context/tool-identity.json").read_text())
for item in identity["files"]:
    assert hashlib.sha256(Path(item["path"]).read_bytes()).hexdigest() == item["sha256"]
selector = identity["files"][0]["path"]
text = Path("tb/pp_top/Makefile").read_text()
flags = re.search(r"^VFLAGS = (.*?)(?=\n\n)", text, re.MULTILINE | re.DOTALL).group(1)
assert flags.count("-j 0") == 1
flags = flags.replace("-j 0", "-j 8").replace("\\\n", " ")
argv = ["rtk", "proxy", "make", "-j1", "-C", "tb/pp_top", "VERILATOR=" + selector,
        "VFLAGS=" + flags, "run"]
env = dict(os.environ, MAKEFLAGS="-j1", PYTHONDONTWRITEBYTECODE="1",
           TMPDIR=str(evidence / "tmp"))
(evidence / "tmp").mkdir(exist_ok=True)
print("Build command:", shlex.join(argv), flush=True)
print("Environment overrides:", {k: env[k] for k in ("MAKEFLAGS", "PYTHONDONTWRITEBYTECODE", "TMPDIR")}, flush=True)
(evidence / "build-command.json").write_text(json.dumps(dict(argv=argv, environment_overrides={
    k: env[k] for k in ("MAKEFLAGS", "PYTHONDONTWRITEBYTECODE", "TMPDIR")}), indent=2) + "\n")
sys.exit(subprocess.run(argv, env=env).returncode)
