#!/bin/bash
# run_probe.sh TREE PROBE.c OUT [extra cc args]: compile PROBE against TREE sources and run.
set -u
T=$1; P=$2; O=$3; shift 3
MILAN=${MILAN:-0}
srcs="$T/src/core/mrp_mad.c $T/src/core/mrp_pdu.c $T/src/modules/msrp.c $T/src/modules/mvrp.c $T/src/modules/mmrp.c $T/src/ports/timer.c"
[ -z "${NOALLOC:-}" ] && srcs="$srcs $T/src/ports/alloc.c"
cc -std=c11 -g -O1 -fsanitize=address,undefined -fno-omit-frame-pointer -DLWSRP_MILAN=$MILAN -I"$T/src/include" -I"$T/src" "$P" $srcs "$@" -o "$O.bin" > "$O.cc.log" 2>&1
echo $? > "$O.cc.rc"
"$O.bin" > "$O.log" 2>&1; echo $? > "$O.rc"
