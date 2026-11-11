#!/bin/sh
# Old-versus-new ACMP differential (reviewer probe, tsn-c-stack #32).
# Builds scripts/trace_walk.cpp against the head tree's src/acmp.c and against main's (9deb0ddb),
# both at ACMP_MAX_SINKS=33u under -fsanitize=shift,undefined, then runs every (sinks, seed, lift)
# case on both and requires byte-identical per-step call-trace digests.
# Usage: differential.sh HEAD_TREE MAIN_TREE OUT_DIR SEEDS
set -eu
P=$(cd "$(dirname "$0")/.." && pwd)
head=$1; main=$2; out=$3; seeds=$4
mkdir -p "$out"
flags="-O1 -g -DACMP_MAX_SINKS=33u -DNDEBUG -DCTRL_REENTRY_ASSERT -fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined"
for side in head main; do
    eval tree=\$$side
    gcc -std=c11 -Wall -Wextra -Werror $flags -I"$tree/include" -c "$tree/src/acmp.c" -o "$out/acmp-$side.o"
    g++ -std=c++20 -Wall -Wextra $flags -I"$tree/include" -I"$tree/tests" "$P/scripts/trace_walk.cpp" "$out/acmp-$side.o" -o "$out/trace-$side"
done
fail=0; cases=0
for lift in 0 1; do
  for sinks in 1 8 32 33; do
    steps=8000; [ "$sinks" = 1 ] && steps=4000; [ "$sinks" = 8 ] && steps=6000
    s=0
    while [ "$s" -lt "$seeds" ]; do
        seed=$((0x9E3779B9 + s * 7919))
        "$out/trace-head" $sinks $steps $seed $lift > "$out/t-head.txt"
        "$out/trace-main" $sinks $steps $seed $lift > "$out/t-main.txt"
        cases=$((cases + 1))
        if ! cmp -s "$out/t-head.txt" "$out/t-main.txt"; then
            echo "DIVERGE sinks=$sinks seed=$seed lift=$lift first: $(cmp "$out/t-head.txt" "$out/t-main.txt" | head -1)"
            cp "$out/t-head.txt" "$out/diverge-$sinks-$seed-$lift-head.txt"; cp "$out/t-main.txt" "$out/diverge-$sinks-$seed-$lift-main.txt"
            fail=1
        fi
        [ "$s" = 0 ] && echo "sinks=$sinks lift=$lift seed=$seed $(tail -1 "$out/t-head.txt")"
        s=$((s + 1))
    done
  done
done
echo "cases $cases divergent $fail"
exit $fail
