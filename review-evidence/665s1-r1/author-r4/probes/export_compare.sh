#!/bin/bash
# The all-fabric default: every shipped config exported (no Vivado) at the base,
# then at the head, from ONE scratch worktree path into ONE output path per
# config, so no path differs between the two exports; each export is moved
# aside before the next, nothing deleted (the work directory must start empty).
# Then compare_same.py over each pair.
#   $1 the scratch worktree (a detached worktree of the lane, outside the tree)
#   $2 the head commit   $3 the work directory   $4 the receipts directory
# The AX7101 configs run at their shipping arguments; this LiteX checkout
# refuses the Arty configs' 83.333 MHz system clock at the base and the head
# alike, so they are exported at 100 MHz (docs/design/MAILBOX_SPLIT.md).
set -u
T=$1 HEADSHA=$2 S=$3/export R=$4
BASE=e76a755afc0536453161e3cd33f6f4d2dcd7641f
LITEX=$HOME/litex-milan
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$3/tmp
export PATH=$HOME/br-milan-rv32/host/bin:$LITEX/venv/bin:$PATH
export PYTHONPATH=$LITEX/litex:$LITEX/migen
mkdir -p "$S" "$TMPDIR"
[ "$(git -C "$T" rev-parse --show-toplevel)" = "$T" ] || exit 2
CONFIGS="endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_current endstation_arty_4x4 endstation_arty_8ch"
export_all() {  # $1: label
  for c in $CONFIGS; do
    case $c in
      endstation_ax7101_1x1_tdm8) flow="--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt" ;;
      endstation_ax7101_8x8) flow="--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive AltSpreadLogic_high" ;;
      *) flow="" ;;
    esac
    [ -e "$T/sw/builder/out" ] && mv "$T/sw/builder/out" "$S/builder-out-$1-$c"
    (cd "$T" && /usr/bin/python3 sw/builder/endstation_builder.py "configs/$c.yaml") > "$S/$1-builder-$c.log" 2>&1 || return 1
    argv=$(/usr/bin/python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1]))['argv']))" \
           "$T/sw/builder/out/$c/soc_params.json")
    case $c in
      endstation_arty_*) argv=$(echo "$argv" | sed -E 's/--sys-clk-freq [^ ]+/--sys-clk-freq 100e6/') ;;
    esac
    echo "$1 $c argv: $argv"
    start=$(date +%s)
    (cd "$T/sw/litex" && "$LITEX/venv/bin/python3" milan_soc.py $argv $flow \
       --entity-gen-dir "$T/configs/generated/$c" --vivado-max-threads 32 --output-dir "$S/out-$c") \
       > "$S/$1-export-$c.log" 2>&1
    rc=$?
    echo "$1 $c rc=$rc $(( $(date +%s) - start ))s tree=$(git -C "$T" rev-parse HEAD) status=$(git -C "$T" status --short | wc -l)"
    [ $rc = 0 ] || return 1
    [ -e "$S/$1-$c" ] && return 1
    mv "$S/out-$c" "$S/$1-$c"
  done
}
git -C "$T" checkout -q --detach $BASE || exit 3
[ -z "$(git -C "$T" status --short)" ] || exit 3
export_all base || exit 5
git -C "$T" checkout -q --detach "$HEADSHA" || exit 4
[ -z "$(git -C "$T" status --short)" ] || exit 4
export_all head || exit 6
rc=0
for c in $CONFIGS; do
  /usr/bin/python3 -B "$(dirname "$0")/compare_same.py" "$S/base-$c" "$S/head-$c" "$R/export-compare-$c.json" || rc=7
done
echo "export proof rc=$rc"
exit $rc
