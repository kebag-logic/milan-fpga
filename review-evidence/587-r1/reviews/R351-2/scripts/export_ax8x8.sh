#!/bin/bash
# Recipe "Prerequisites" + "Export the shipping builds", ax8x8 only, in a disposable relocated checkout copy.
# Usage: export_ax8x8.sh CHECKOUT WORK   (both absolute; reviewer-private)
set -u
S=$REVIEWS/587-r351-2-packet/scratch
export REPO="$1" WORK="$2" LITEX_PYTHON=$S/pybin/python3 SDK=$S/sdk
export PATH="$SDK/bin:$S/pybin:/usr/bin:/bin"
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
cd "$REPO"
export LITEX_ENV_CC_TRIPLE="$(PYTHONPATH=scripts /usr/bin/python3 -c 'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
mkdir -p "$WORK/builder" "$WORK/roms"
test ! -e sw/builder/out && ln -s "$WORK/builder" sw/builder/out
test ! -e configs/generated/ltn_rom.hex && ln -s "$WORK/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
test ! -e configs/generated/ucode.hex && ln -s "$WORK/roms/ucode.hex" configs/generated/ucode.hex
bash sw/litex/build.sh ax8x8 --dry-run > "$WORK/ax8x8-dry-run.log" 2>&1; echo "dry-run rc=$?"
/usr/bin/python3 - <<'PY'
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
for shape in ("ax8x8",):
    preview = (work / f"{shape}-dry-run.log").read_text()
    lines = [line for line in preview.splitlines() if "exec python3 milan_soc.py " in line]
    assert len(lines) == 1
    argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
    argv.remove("--build")
    argv[argv.index("--output-dir") + 1] = str(work / shape)
    (work / f"{shape}-argv.json").write_text(json.dumps(argv, indent=2))
    with (work / f"{shape}-elaboration.log").open("w") as log:
        subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
echo "export rc=$?"
