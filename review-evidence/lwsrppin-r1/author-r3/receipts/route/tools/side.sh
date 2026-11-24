#!/usr/bin/env bash
# side.sh <head|base>: the composed train's 8x8/1if split route (train1117-a794 round5 fit/tools/fitpoint.sh, the 8x8
# arm) for one side: the split boot for the stand-in image (boot8.sh), route_image8.sh (the split recipe's export, its
# identity gate, pp_baseline.py's integrated full-split script), then the integrated route through vivado-slot.sh
# (route_one8.sh: synthesis, ExtraPostPlacementOpt, the first of #818's three directives), then its signoff.
set -u
SIDE=$1; R=/data-2/milan/tmp/lwsrppin-a834/route; X=$R/tools; V=$MANAGEMENT/2026-09-23/vivado-slot.sh
case "$SIDE" in
  head) L=/data-2/milan/tmp/lwsrppin-r2;;
  base) L=/data-2/milan/tmp/lwsrppin-a834/base;;
  *) echo "side: head|base" >&2; exit 2;;
esac
D=$R/$SIDE; W=$D/route8; B=$D/boot-8x8; T=$D/tmp
mkdir -p "$W" "$T"
say() { echo "[route $SIDE $(date +%T)] $*"; }
say "src $L head $(git -C "$L" rev-parse HEAD) lwSRP $(git -C "$L/third_party/lwSRP" rev-parse HEAD)"
# 1. boot8.sh: the split boot at the head (its image-provisional and runtime archives are the stand-in inputs)
if [ "$(cat "$B.rc" 2>/dev/null)" != 0 ]; then
  ( export PATH=$WORKSPACE_HOME/br-milan-rv32/host/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
    export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
    export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$T MAKEFLAGS="-j8 --no-print-directory"
    cd "$L" || exit 3
    echo "head $(git rev-parse HEAD) tree: $(git status --porcelain | tr '\n' ' ')"
    date -Iseconds
    $WORKSPACE_HOME/litex-milan/venv/bin/python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$B" --shape endstation_ax7101_8x8
    rc=$?; date -Iseconds; echo $rc > "$B.rc" ) > "$W.boot.log" 2>&1
fi
say "boot rc=$(cat "$B.rc" 2>/dev/null)"
[ "$(cat "$B.rc" 2>/dev/null)" = 0 ] || exit 3
# 2. route_image8.sh
if [ ! -f "$W/split/gateware/baseline_integrated.tcl" ]; then
  TMPDIR=$T bash "$X/route_image8.sh" "$L" "$W" "$B" > "$W.image.log" 2>&1 || { say "route_image rc=$?"; exit 4; }
fi
say "route_image done: $(tail -3 "$W.image.log" | tr '\n' ' ')"
# 3. route_one8.sh, through a slot
export HOME=$WORKSPACE_HOME XILINXD_LICENSE_FILE=$WORKSPACE_HOME/.Xilinx/Xilinx.lic
g=$W/split/gateware
"$V" bash -c "source $WORKSPACE_HOME/Xilinx/2026.1/Vivado/settings64.sh; cd '$g' || exit 3
  date -Iseconds > route.start
  vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > vivado.out 2>&1
  echo \$? > route.rc; date -Iseconds > route.end" > "$W/slot-split.log" 2>&1
say "integrated rc=$(cat "$g/route.rc" 2>/dev/null)"
say "signoff"; python3 -I "$X/signoff.py" "$g"; say "signoff rc=$?"
echo done > "$W/FIT_DONE"
