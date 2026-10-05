#!/usr/bin/env bash
# usage: meas.sh <combo> <phase>   phases: export | elab1 | ooc1 | unlink
# #638's recipe (docs/testing/PP_SHADOW_BASELINE_RECIPE.md in the scratch parent), 1x1 only.
set -u
S=$VALIDATION_STORAGE/pp148-a532
export REPO=$S/parent
export LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3
export SDK=$VALIDATION_STORAGE/231-a337-sdk
export PATH="$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$SDK/bin:$(dirname "$LITEX_PYTHON"):$PATH"
export PYTHONHASHSEED=0
export TMPDIR=$S/tmp
export LITEX_ENV_CC_TRIPLE="$(cd $REPO && PYTHONPATH=scripts python3 -c 'from ci_rv32_sdk import COMPILER; print(COMPILER.removeprefix("bin/").removesuffix("-gcc"))')"
combo=$1; phase=$2
W=$S/meas/$combo
vrun() {  # <dir> <tcl> <log>
  ( cd "$1" && date -Is > "$3.start" && { flock /tmp/milan-vivado.lock vivado -mode batch -source "$2" -nojournal -log "$3" > "$3.stdout" 2>&1; echo $? > "$3.rc"; } ; date -Is > "$3.end" )
}
case $phase in
  export)
    mkdir -p "$W/builder" "$W/roms"
    cd "$REPO"
    git -C protocol-processor rev-parse HEAD > "$W/processor-head.txt"
    python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only > "$W/sdk-verify.log" 2>&1 || { echo sdk-verify-failed; exit 2; }
    python3 syn/ooc/pp_baseline.py --selftest > "$W/pp_baseline-selftest.log" 2>&1 || { echo selftest-failed; exit 2; }
    test ! -e sw/builder/out || { echo "sw/builder/out exists"; exit 2; }
    test ! -e configs/generated/ltn_rom.hex && test ! -e configs/generated/ucode.hex || { echo "roms exist"; exit 2; }
    ln -s "$W/builder" sw/builder/out
    ln -s "$W/roms/ltn_rom.hex" configs/generated/ltn_rom.hex
    ln -s "$W/roms/ucode.hex" configs/generated/ucode.hex
    bash sw/litex/build.sh ax7101 --dry-run > "$W/ax7101-dry-run.log" 2>&1 || { echo dry-run-failed; exit 2; }
    WORK=$W python3 - <<'PY'
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
preview = (work / "ax7101-dry-run.log").read_text()
lines = [l for l in preview.splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1])
argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax7101")
(work / "ax7101-argv.json").write_text(json.dumps(argv, indent=2))
with (work / "ax7101-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
    echo "export rc $?" ;;
  unlink)
    cd "$REPO"
    for l in sw/builder/out configs/generated/ltn_rom.hex configs/generated/ucode.hex; do [ -L "$l" ] && unlink "$l"; done; git status --short ;;
  elab1)
    E=$W/ax7101-elab; mkdir -p "$E"; cp "$W"/ax7101/gateware/*.xdc "$W"/ax7101/gateware/*.init "$E"/
    python3 - "$W/ax7101/gateware/alinx_ax7101.tcl" "$E/elaborate.tcl" <<'PY'
import sys
lines = open(sys.argv[1]).read().splitlines()
ix = [i for i, l in enumerate(lines) if l.startswith("synth_design ")]
assert len(ix) == 1
i = ix[0]
synth = lines[i].replace("synth_design ", "synth_design -rtl -rtl_skip_mlo ", 1)
out = lines[:i] + ["set_msg_config -id {Synth 8-4445} -new_severity ERROR", synth, "quit"]
open(sys.argv[2], "w").write("\n".join(out) + "\n")
PY
    vrun "$E" elaborate.tcl elaborate.log; echo "elab rc $(cat $E/elaborate.log.rc)" ;;
  ooc1)
    cd "$REPO"
    python3 syn/ooc/pp_baseline.py "$W/ax7101/gateware" --output "$W/ax7101-ooc" --integrated-log "$W/ax7101-elab/elaborate.log" --integrated-clock > "$W/ooc1-prepare.log" 2>&1 || { echo prepare-failed; exit 2; }
    vrun "$W/ax7101-ooc" baseline_ooc.tcl baseline.log; echo "ooc rc $(cat $W/ax7101-ooc/baseline.log.rc)" ;;
esac
