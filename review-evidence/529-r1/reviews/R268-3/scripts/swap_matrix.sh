#!/bin/sh
# All 45 pairwise exchanges of the ten KL_crf_rx output bindings, one tree per
# mutant under SCRATCH/swap/<a>__<b>, built and run on LEG. Two lanes of 4
# Verilator jobs (8 in total).
# usage: swap_matrix.sh PACKET_DIR LEG [portA:portB ...]  (default: all 45)
set -eu
P=$1; L=$2; shift 2; S=$P/scratch; OUT=$P/receipts/swap
mkdir -p "$OUT" "$S/swap"
pairs="$*"
if [ -z "$pairs" ]; then
    ports=$(python3 "$P/scripts/mk_swap.py" --list | awk '{print $1}')
    set -- $ports
    while [ $# -gt 0 ]; do
        a=$1; shift
        for b in "$@"; do pairs="$pairs $a:$b"; done
    done
fi
for pr in $pairs; do printf '%s\0' "$pr"; done | xargs -0 -P 2 -I{} sh -c '
    a=${1%%:*}; b=${1##*:}; t="'"$S"'/swap/${a}__${b}"
    if [ ! -x "$t/tb/verilator/milan_dp/obj_'"$L"'/Vmilan_dp_'"$L"'" ]; then
        rm -rf "$t"; cp -a "'"$S"'/base" "$t"; rm -rf "$t"/tb/verilator/milan_dp/obj_*
        python3 "'"$P"'/scripts/mk_swap.py" "$t" "$a" "$b" >/dev/null
        (cd "$t" && git diff > "'"$OUT"'/${a}__${b}.diff")
        python3 "'"$P"'/scripts/leg.py" "$t" "'"$L"'" build --jobs 4 --tag "${a}__${b}" --out "'"$OUT"'"
    fi
    python3 "'"$P"'/scripts/leg.py" "$t" "'"$L"'" run --tag "${a}__${b}" --out "'"$OUT"'"
    rm -rf "$t"/tb/verilator/milan_dp/obj_*/*.o "$t"/tb/verilator/milan_dp/obj_*/*.cpp
' _ {}
