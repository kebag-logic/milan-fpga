"""Per-makefile: make -pqrR rc, whether parse completed, shape tokens (scratch probe)."""
import os, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import shape_consumer_inventory as sci
for name in sys.argv[2:]:
    d = root / Path(name).parent
    env = dict(os.environ, MAKEFLAGS="", MFLAGS="")
    run = subprocess.run(["make", "-pqrR", "-f", Path(name).name], cwd=d, env=env,
                         capture_output=True, text=True, timeout=120)
    stop = [l for l in run.stderr.splitlines() if "Stop." in l]
    ok, toks = sci.shape_prereqs_from_database(d, Path(name).name)
    print(f"{name}: rc={run.returncode} stop={stop[:1]} ok={ok} tokens={toks}")
