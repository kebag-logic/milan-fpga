#!/bin/bash
# Export (no Vivado) every shipped config from one tree copy: S1 item 5's method.
# usage: export_all_fabric.sh <tree> <outdir>
tree=$1; out=$2; mkdir -p "$out"; cd "$tree" || exit 9
rc=0
for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_current endstation_arty_4x4 endstation_arty_8ch; do
  board=${cfg#endstation_}; board=${board%%_*}
  python3 sw/builder/endstation_builder.py "configs/$cfg.yaml" > "$out/$cfg.builder.log" 2>&1 || { echo "$cfg builder FAILED"; rc=1; continue; }
  OPTS=$(bash -c ". configs/generated/sweep_opts_$board.sh; printf '%s' \"\$OPTS\"")
  extra=""
  case $board in arty) extra="--sys-clk-freq 100e6";; esac
  # shellcheck disable=SC2086
  python3 sw/litex/milan_soc.py $OPTS $extra --entity-gen-dir "$PWD/configs/generated/$cfg" --output-dir "$out/$cfg" --no-compile > "$out/$cfg.log" 2>&1
  r=$?; echo "$cfg export rc=$r"; [ $r = 0 ] || rc=1
done
exit $rc
