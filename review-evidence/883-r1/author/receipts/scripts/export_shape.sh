#!/usr/bin/env bash
# export_shape.sh <shape> <work> <repo>: the recipe's export of one shape (docs/testing/PP_SHADOW_BASELINE_RECIPE.md,
# unchanged) in the given clone, with its own ROM links. Runs no Vivado.
set -uo pipefail
shape=$1; work=$2; export REPO=$3; here=$(cd "$(dirname "$0")" && pwd)
source "$here/env.sh"
export LITEX_PYTHON=<litex>/venv/bin/python3
export SDK=$RV32_SDK
export PATH="$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
cd "$REPO" || exit 2
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts python3 -c 'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only || exit 2
python3 syn/ooc/pp_baseline.py --selftest || exit 2
mkdir -p "$work/builder" "$work/roms"
test ! -e sw/builder/out && test ! -e configs/generated/ltn_rom.hex && test ! -e configs/generated/ucode.hex || exit 2
ln -s "$work/builder" sw/builder/out
ln -s "$work/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
ln -s "$work/roms/ucode.hex" configs/generated/ucode.hex
bash sw/litex/build.sh "$shape" --dry-run > "$work/$shape-dry-run.log" || exit 3
SHAPE=$shape WORKDIR=$work python3 - <<'PY' || exit 3
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORKDIR"]); shape = os.environ["SHAPE"]
python = os.environ["LITEX_PYTHON"]
preview = (work / f"{shape}-dry-run.log").read_text()
lines = [l for l in preview.splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / shape)
(work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
with (work / f"{shape}-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
echo "EXPORT-$shape-DONE"
