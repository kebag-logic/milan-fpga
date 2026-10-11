#!/usr/bin/env bash
# Base-vs-head netlist identity: protocol_processor_top at nine shapes and each of
# the twelve other guard-carrying modules at its defaults, from sv2v-lowered
# trees (<scratch>/lower/{base,head}-<v>.v), via netlist_cmp.sh. Prints one
# EQUAL/DIFFER line per (sv2v, top, shape).
# usage: netlists_all.sh <scratch> <jobs>
set -u
S=$1; J=${2:-6}; K=$(cd "$(dirname "$0")/.." && pwd)
out=$S/netall; rm -rf "$out"; mkdir -p "$out"
jobs=()
shapes=("default:" "1x1:-set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 1"
        "2x2:-set N_STREAM_IN_P 2 -set N_STREAM_OUT_P 2"
        "4x4:-set N_STREAM_IN_P 4 -set N_STREAM_OUT_P 4"
        "5x5:-set N_STREAM_IN_P 5 -set N_STREAM_OUT_P 5"
        "8x1:-set N_STREAM_IN_P 8 -set N_STREAM_OUT_P 1"
        "1x8:-set N_STREAM_IN_P 1 -set N_STREAM_OUT_P 8"
        "16x16:-set N_STREAM_IN_P 16 -set N_STREAM_OUT_P 16"
        "9x9_2if:-set N_STREAM_IN_P 9 -set N_STREAM_OUT_P 9 -set N_AVB_IF_P 2")
mods=(KL_acmp_nvm_shadow KL_pp_acmp_listener KL_aecp_desc_store KL_aecp_engine
      KL_aecp_notify KL_aecp_nvm_writer KL_aecp_resp_buf KL_aecp_ucpu KL_pp_nvm_port
      KL_pp_originator KL_pp_release_merge KL_srp_encoder)
for v in 012 013; do
  for t in base head; do
    R=$S/roms; [ $t = base ] && R=$S/roms_base
    for sh in "${shapes[@]}"; do
      jobs+=("$v|$t|protocol_processor_top|${sh%%:*}|$R|${sh#*:}")
    done
    for m in "${mods[@]}"; do jobs+=("$v|$t|$m|default|$R|"); done
  done
done
printf '%s\n' "${jobs[@]}" | xargs -P "$J" -I{} bash -c '
  IFS="|" read -r v t top shape R sets <<<"$1"
  PATH="$2/tc$v:$PATH" "$3/scripts/netlist_cmp.sh" "$2/lower/$t-$v.v" "$R" \
    "$4/$v-$t-$top-$shape" "$top" $sets >/dev/null 2>&1 || true' _ {} "$S" "$K" "$out"
for v in 012 013; do
  for top in protocol_processor_top "${mods[@]}"; do
    for f in "$out/$v-base-$top-"*.rc; do
      shape=${f##*/$v-base-$top-}; shape=${shape%.rc}
      b="$out/$v-base-$top-$shape"; h="$out/$v-head-$top-$shape"
      bd=$(cat "$b.canon.sha256" 2>/dev/null); hd=$(cat "$h.canon.sha256" 2>/dev/null)
      verdict=DIFFER; [ -n "$bd" ] && [ "$bd" = "$hd" ] && verdict=EQUAL
      echo "sv2v0.0.$v $top $shape rc $(cat "$b.rc")/$(cat "$h.rc" 2>/dev/null) lines $(cat "$b.lines" 2>/dev/null)/$(cat "$h.lines" 2>/dev/null) canon ${bd:0:16}/${hd:0:16} $verdict"
    done
  done
done
