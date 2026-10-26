#!/bin/bash
# Export every shipped config (all-fabric default, no Vivado) at the base, twice,
# and at the head, from ONE scratch tree path into per-run output dirs.
#   $1 scratch tree (a copy of the clone)  $2 head sha  $3 work dir
set -u
T=$1 HEADSHA=$2 W=$3
BASE=e76a755afc0536453161e3cd33f6f4d2dcd7641f
LITEX=$HOME/litex-milan
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$W/tmp
export PATH=$HOME/br-milan-rv32/host/bin:$LITEX/venv/bin:$PATH
export PYTHONPATH=$LITEX/litex:$LITEX/migen
mkdir -p "$W" "$TMPDIR"
CONFIGS="endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_current endstation_arty_4x4 endstation_arty_8ch"
run() {  # $1 label
  for c in $CONFIGS; do
    case $c in
      endstation_ax7101_1x1_tdm8) flow="--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt" ;;
      endstation_ax7101_8x8) flow="--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive AltSpreadLogic_high" ;;
      *) flow="" ;;
    esac
    rm -rf "$T/sw/builder/out"
    (cd "$T" && /usr/bin/python3 sw/builder/endstation_builder.py "configs/$c.yaml") > "$W/$1-builder-$c.log" 2>&1 || { echo "builder fail $1 $c"; return 1; }
    argv=$(/usr/bin/python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1]))['argv']))" "$T/sw/builder/out/$c/soc_params.json")
    case $c in endstation_arty_*) argv=$(echo "$argv" | sed -E 's/--sys-clk-freq [^ ]+/--sys-clk-freq 100e6/') ;; esac
    (cd "$T/sw/litex" && "$LITEX/venv/bin/python3" milan_soc.py $argv $flow \
       --entity-gen-dir "$T/configs/generated/$c" --vivado-max-threads 8 --output-dir "$W/out-$c") > "$W/$1-export-$c.log" 2>&1
    rc=$?
    echo "$1 $c rc=$rc tree=$(git -C "$T" rev-parse HEAD)"
    [ $rc = 0 ] || return 1
    mv "$W/out-$c" "$W/$1-$c"
  done
  rm -rf "$T/sw/builder/out"
}
git -C "$T" checkout -q --detach $BASE && [ -z "$(git -C "$T" status --short)" ] || exit 3
run base1 || exit 5
run base2 || exit 5
git -C "$T" checkout -q --detach "$HEADSHA" && [ -z "$(git -C "$T" status --short)" ] || exit 4
run head || exit 6
echo "status-after=$(git -C "$T" status --short | wc -l)"
