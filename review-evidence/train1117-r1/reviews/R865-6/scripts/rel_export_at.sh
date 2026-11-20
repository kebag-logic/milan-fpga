#!/usr/bin/env bash
# rel_export_at.sh <source-clone> <commit> <workdir>
# Disposable shared clone of <source-clone> at <commit> (submodules from the source clone's
# module stores), then the AX7101 1x1 all-fabric release export without Vivado
# (sw/litex/build.sh ax7101 --dry-run, then its milan_soc.py command without --build),
# then the sha256 of every file the image loads.
set -euo pipefail
SRC=$1 C=$2 W=$3
rm -rf "$W"; mkdir -p "$W"
git clone -q --shared --no-checkout "$SRC" "$W/repo"
cd "$W/repo"
git checkout -q --detach "$C"
for p in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
  name=$(git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk -v p="$p" '$2==p{sub(/^submodule\./,"",$1);sub(/\.path$/,"",$1);print $1}')
  git config "submodule.$name.url" "$SRC/.git/modules/$name"
  git -c protocol.file.allow=always submodule update -q --init -- "$p"
done
echo "head $(git rev-parse HEAD) porcelain $(git status --porcelain | wc -l)"
L=$PWD; OUT=$W/out; mkdir -p "$OUT"
PY=${HOME}/litex-milan/venv/bin/python3
export PATH=${HOME}/litex-milan/venv/bin:/usr/local/bin:/usr/bin:/bin:${HOME}/br-milan-rv32/host/bin PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true REPO=$L WORK=$OUT LITEX_PYTHON=$PY
(cd sw/litex && bash ./build.sh ax7101 --dry-run) > "$OUT/ax7101-dry-run.log" 2>&1
"$PY" -I - <<'PYEOF'
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
lines = [l for l in (work / "ax7101-dry-run.log").read_text().splitlines() if "exec python3 milan_soc.py " in l]
argv = shlex.split(lines[0].split("exec python3 ", 1)[1]); argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax7101")
with (work / "ax7101-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PYEOF
echo "export done: $(find "$OUT/ax7101" -type f | wc -l) files"
cd "$OUT/ax7101"
for f in software/bios/bios.bin aem_desc.bin $(find gateware -name '*.init' | sort); do
  echo "LOADED $f $(sha256sum < "$f" | cut -c1-64)"
done
echo "head-after $(git -C "$L" rev-parse HEAD) porcelain-after $(git -C "$L" status --porcelain | wc -l)"
