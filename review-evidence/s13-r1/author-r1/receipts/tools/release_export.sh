#!/usr/bin/env bash
# release_export.sh <repo> <out> [placement]: the AX7101 1x1 release (all-fabric) gateware export, no Vivado: the
# launcher's dry run (BUILD_PLACEMENT=<placement> when given, the flip's switch) and its printed milan_soc.py command
# without --build (the train's release_export.sh, with the placement passed through).
set -euo pipefail
L=$1; W=$2; PL=${3:-}; mkdir -p "$W"; cd "$L"
PY=<home>/litex-milan/venv/bin/python3
export PATH=<home>/litex-milan/venv/bin:/usr/local/bin:/usr/bin:/bin:<home>/br-milan-rv32/host/bin PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true REPO=$L WORK=$W LITEX_PYTHON=$PY HOME=<scratch>/home
if [ -n "$PL" ]; then export BUILD_PLACEMENT=$PL; fi
(cd sw/litex && bash ./build.sh ax7101 --dry-run) > "$W/ax7101-dry-run.log" 2>&1
"$PY" - <<'PYEOF'
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
lines = [l for l in (work / "ax7101-dry-run.log").read_text().splitlines() if "exec python3 milan_soc.py " in l]
argv = shlex.split(lines[0].split("exec python3 ", 1)[1]); argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax7101")
(work / "ax7101-argv.json").write_text(json.dumps(argv, indent=2))
with (work / "ax7101-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PYEOF
echo "export done: $(find "$W/ax7101" -type f | wc -l) files"
