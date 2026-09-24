#!/bin/sh
# Run the ghost-tuple matrix on one leg of the probe tree (see mk_ghost.py).
# usage: ghost_matrix.sh PACKET_DIR PROBE_TREE LEG N_STREAMS
# Each case is "<name> <plusargs...>"; at most 8 runs in parallel.
set -eu
P=$1; T=$2; L=$3; N=$4
hx() { printf '%x' "$1"; }
OUT=$P/receipts/ghost
mkdir -p "$OUT"
{
echo "c0-ghost-off +GHOST=0"
echo "c1-replace-by-sin-N +GHOST=1 +GHOST_REPLACE=1 +GHOST_TY=5 +GHOST_IX=$(hx $N)"
echo "c2-replace-by-nothing +GHOST=0 +GHOST_REPLACE=1"
echo "c3-extra-dup-sin-N +GHOST=1 +GHOST_TY=5 +GHOST_IX=$(hx $N)"
echo "x-sin-0 +GHOST=1 +GHOST_TY=5 +GHOST_IX=0"
echo "x-sin-Nm1 +GHOST=1 +GHOST_TY=5 +GHOST_IX=$(hx $((N-1)))"
echo "x-sin-Np1 +GHOST=1 +GHOST_TY=5 +GHOST_IX=$(hx $((N+1)))"
echo "x-sin-63 +GHOST=1 +GHOST_TY=5 +GHOST_IX=3f"
echo "x-sin-64 +GHOST=1 +GHOST_TY=5 +GHOST_IX=40"
echo "x-sin-64pN +GHOST=1 +GHOST_TY=5 +GHOST_IX=$(hx $((64+N)))"
echo "x-sin-ffff +GHOST=1 +GHOST_TY=5 +GHOST_IX=ffff"
echo "x-sout-0 +GHOST=1 +GHOST_TY=6 +GHOST_IX=0"
echo "x-sout-N +GHOST=1 +GHOST_TY=6 +GHOST_IX=$(hx $N)"
echo "x-sout-Np1 +GHOST=1 +GHOST_TY=6 +GHOST_IX=$(hx $((N+1)))"
echo "x-sout-63 +GHOST=1 +GHOST_TY=6 +GHOST_IX=3f"
echo "x-sout-64 +GHOST=1 +GHOST_TY=6 +GHOST_IX=40"
echo "x-avb-0 +GHOST=1 +GHOST_TY=9 +GHOST_IX=0"
echo "x-avb-1 +GHOST=1 +GHOST_TY=9 +GHOST_IX=1"
echo "x-ckd-0 +GHOST=1 +GHOST_TY=24 +GHOST_IX=0"
echo "x-ckd-1 +GHOST=1 +GHOST_TY=24 +GHOST_IX=1"
echo "x-entity-0 +GHOST=1 +GHOST_TY=0 +GHOST_IX=0"
echo "x-config-0 +GHOST=1 +GHOST_TY=1 +GHOST_IX=0"
echo "x-ffff-ffff +GHOST=1 +GHOST_TY=ffff +GHOST_IX=ffff"
echo "r-sin-Nm1 +GHOST=1 +GHOST_REPLACE=1 +GHOST_TY=5 +GHOST_IX=$(hx $((N-1)))"
echo "r-sin-Np1 +GHOST=1 +GHOST_REPLACE=1 +GHOST_TY=5 +GHOST_IX=$(hx $((N+1)))"
echo "r-sin-64pN +GHOST=1 +GHOST_REPLACE=1 +GHOST_TY=5 +GHOST_IX=$(hx $((64+N)))"
echo "r-sout-N +GHOST=1 +GHOST_REPLACE=1 +GHOST_TY=6 +GHOST_IX=$(hx $N)"
echo "r-ckd-N +GHOST=1 +GHOST_REPLACE=1 +GHOST_TY=24 +GHOST_IX=$(hx $N)"
} | while read -r name args; do
    printf '%s\0' "$name $args"
done | xargs -0 -P 8 -I{} sh -c '
    set -- {}; name=$1; shift
    python3 "'"$P"'/scripts/leg.py" "'"$T"'" "'"$L"'" run --tag "$name" --out "'"$OUT"'" "$@"
'
