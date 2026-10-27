#!/bin/bash
# The all-fabric default (S1's method, docs/design/MAILBOX_SPLIT.md "Default build"): every
# shipped config exported (no Vivado) at the base, then at the head, from ONE scratch worktree
# path into ONE output path per config; then compare_same.py over each pair. The AX7101
# configs run at their shipping arguments; the Arty configs at 100 MHz, which this LiteX
# checkout needs at the base and the head alike. Then the shipping 1x1 config's split export
# (--ctrl-mailbox --ctrl-firmware ELF) at the base and the head: the product split CPU netlist
# without and with the instruction cache.
#   $1 the scratch worktree (a detached worktree of the lane, outside the tree)
#   $2 the head commit   $3 the work directory   $4 the receipts directory   $5 the 1x1 split ELF
set -u
T=$1 HEADSHA=$2 S=$3/export R=$4 ELF=$5
BASE=e76a755afc0536453161e3cd33f6f4d2dcd7641f
LITEX=$HOME/litex-milan
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$3/tmp
export PATH=$HOME/br-milan-rv32/host/bin:$LITEX/venv/bin:$PATH
export PYTHONPATH=$LITEX/litex:$LITEX/migen
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
mkdir -p "$S" "$TMPDIR" "$R"
[ "$(git -C "$T" rev-parse --show-toplevel)" = "$T" ] || exit 2
CONFIGS="endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_current endstation_arty_4x4 endstation_arty_8ch"
export_one() {  # $1: label  $2: config  $3: extra milan_soc arguments  $4: output name
  local c=$2 flow argv start rc
  case $c in
    endstation_ax7101_1x1_tdm8) flow="--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt" ;;
    endstation_ax7101_8x8) flow="--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive AltSpreadLogic_high" ;;
    *) flow="" ;;
  esac
  [ -e "$T/sw/builder/out" ] && mv "$T/sw/builder/out" "$S/builder-out-$1-$4"
  (cd "$T" && /usr/bin/python3 sw/builder/endstation_builder.py "configs/$c.yaml") > "$S/$1-builder-$4.log" 2>&1 || return 1
  argv=$(/usr/bin/python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1]))['argv']))" \
         "$T/sw/builder/out/$c/soc_params.json")
  case $c in
    endstation_arty_*) argv=$(echo "$argv" | sed -E 's/--sys-clk-freq [^ ]+/--sys-clk-freq 100e6/') ;;
  esac
  echo "$1 $4 argv: $argv $3"
  start=$(date +%s)
  (cd "$T/sw/litex" && "$LITEX/venv/bin/python3" milan_soc.py $argv $flow $3 \
     --entity-gen-dir "$T/configs/generated/$c" --vivado-max-threads 32 --output-dir "$S/out-$4") \
     > "$S/$1-export-$4.log" 2>&1
  rc=$?
  echo "$1 $4 rc=$rc $(( $(date +%s) - start ))s tree=$(git -C "$T" rev-parse HEAD) status=$(git -C "$T" status --short | wc -l)"
  [ $rc = 0 ] || return 1
  [ -e "$S/$1-$4" ] && return 1
  mv "$S/out-$4" "$S/$1-$4"
}
export_all() {  # $1: label
  for c in $CONFIGS; do export_one "$1" "$c" "" "$c" || return 1; done
  export_one "$1" endstation_ax7101_1x1_tdm8 "--ctrl-mailbox --ctrl-firmware $ELF" split-1x1 || return 1
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
/usr/bin/python3 -B "$(dirname "$0")/export_digest.py" $(for c in $CONFIGS; do echo "$S/base-$c" "$S/head-$c"; done) \
  > "$R/export-digests.txt"
/usr/bin/python3 -B "$(dirname "$0")/compare_same.py" "$S/base-split-1x1" "$S/head-split-1x1" \
  "$R/export-compare-split-1x1.json" > "$R/export-compare-split-1x1.txt" 2>&1
echo "split 1x1 compare rc=$? (expected to differ in the CPU netlist only)"
echo "export proof rc=$rc"
exit $rc
