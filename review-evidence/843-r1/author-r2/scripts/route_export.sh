#!/usr/bin/env bash
# route_export.sh <rev> <tag>: the recipe's ax7101 export and measurement script in a clean clone at <rev>
# (docs/testing/PP_SHADOW_BASELINE_RECIPE.md, unchanged, --single-thread-synthesis). Runs no Vivado.
set -uo pipefail
rev=$1; tag=$2; here=$(cd "$(dirname "$0")" && pwd)
source "$here/env.sh"
S=$VALIDATION_STORAGE/scratch/843-a737b/route-$tag
export WORK=$S/w REPO=$S/clone
export LITEX_PYTHON=$HOME/litex-milan/venv/bin/python3
export SDK=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host
export PATH="$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
mkdir -p "$WORK/builder" "$WORK/roms"
[ -d "$REPO" ] || bash "$here/make_clone.sh" "$REPO" "$rev" || exit 2
cd "$REPO" || exit 2
[ "$(git rev-parse HEAD)" = "$(git rev-parse "$rev^{commit}")" ] || { echo CLONE-NOT-AT-REV; exit 2; }
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c 'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only || exit 2
python3 syn/ooc/pp_baseline.py --selftest || exit 2
test ! -e sw/builder/out && test ! -e configs/generated/ltn_rom.hex && test ! -e configs/generated/ucode.hex || exit 2
ln -s "$WORK/builder" sw/builder/out
ln -s "$WORK/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$WORK/roms/ucode.hex" configs/generated/ucode.hex
bash sw/litex/build.sh ax7101 --dry-run > "$WORK/ax7101-dry-run.log" || exit 3
python3 - <<'PY' || exit 3
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
lines = [l for l in (work / "ax7101-dry-run.log").read_text().splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax7101")
(work / "ax7101-argv.json").write_text(json.dumps(argv, indent=2))
with (work / "ax7101-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
python3 syn/ooc/pp_baseline.py "$WORK/ax7101/gateware" --single-thread-synthesis || exit 4
echo EXPORT-PREPARED
