#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# default_build_identity.sh - reviewer probe for PR #668 (#665 F0).
#
# Exports the gateware (milan_soc.py --no-compile, no vendor run) of every
# shipped end-station config three ways, from ONE tree so source paths agree:
#   base  the base commit's sw/litex/milan_soc.py (copied beside the head one)
#   head  the head milan_soc.py, switch off (the default build)
#   on    the head milan_soc.py with --ctrl-mailbox
# The design argv is the builder's own (endstation_builder.emit_soc_argv).
#
# usage: default_build_identity.sh <tree> <base-sha> <outdir> <python> [sysclk-override-for-arty]
set -u
T=$(cd "$1" && pwd); B=$2; O=$3; PY=$4; ARTY_CLK=${5:-}
CFGS="endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_4x4 endstation_arty_8ch endstation_arty_current"
mkdir -p "$O"
# the builder's per-config outputs (sw/builder/out/<cfg>/) the export reads
for cfg in $CFGS; do
    (cd "$T" && "$PY" sw/builder/endstation_builder.py "configs/$cfg.yaml") > "$O/builder_$cfg.log" 2>&1 \
        || { echo "builder failed for $cfg"; exit 2; }
done
git -C "$T" status --porcelain > "$O/tree_status_after_builder.txt"
git -C "$T" show "$B:sw/litex/milan_soc.py" > "$T/sw/litex/milan_soc_baseprobe.py"
run_one() {
    local cfg=$1 side=$2 script=milan_soc.py extra=""
    [ "$side" = base ] && script=milan_soc_baseprobe.py
    [ "$side" = on ] && extra="--ctrl-mailbox"
    local argv
    argv=$(cd "$T/sw/builder" && "$PY" -c "import endstation_builder as eb; print(' '.join(eb.emit_soc_argv(eb.load_config('../../configs/$cfg.yaml'))))")
    if [ -n "$ARTY_CLK" ] && [[ $cfg == *arty* ]]; then
        argv=$(printf '%s' "$argv" | sed "s/--sys-clk-freq [^ ]*/--sys-clk-freq $ARTY_CLK/")
    fi
    local out="$O/$side/$cfg"
    rm -rf "$out"; mkdir -p "$out"
    printf '%s\n' "$script $argv --entity-gen-dir configs/generated/$cfg --no-compile $extra" > "$out.argv"
    # shellcheck disable=SC2086
    (cd "$T" && PYTHONHASHSEED=0 "$PY" "sw/litex/$script" $argv --entity-gen-dir "configs/generated/$cfg" \
        --no-compile --output-dir "$out" $extra) > "$out.log" 2>&1
    echo $? > "$out.rc"
}
export -f run_one; export T O PY ARTY_CLK
for side in base head on; do for cfg in $CFGS; do echo "$cfg $side"; done; done \
    | xargs -P 5 -n 2 bash -c 'run_one "$0" "$1"'
rm -f "$T/sw/litex/milan_soc_baseprobe.py"
for side in base head on; do for cfg in $CFGS; do printf '%s %s rc=%s\n' "$side" "$cfg" "$(cat "$O/$side/$cfg.rc")"; done; done
