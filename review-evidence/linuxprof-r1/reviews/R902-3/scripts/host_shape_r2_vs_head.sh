#!/usr/bin/env bash
# host_shape_r2_vs_head.sh <r2-tree> <head-tree> <work>: at the host profile's shape (its own srp_entity header) with
# -DCTRL_HOST_PLATFORM, compare ctrl_loop.h's macro set (minus its include guards) and loop/ctrl_loop.c's -E -P token
# stream and -O2 object between the two trees; then the same shape without the macro must be refused by THE SHAPES.
set -u
r2=$1 head=$2 w=$3; rm -rf "$w"; mkdir -p "$w"; rc=0
python3 -B "$head/sw/firmware/ctrl/srp/srp_entity.py" "$head/configs/host/endstation_host_example.yaml" -o "$w/host.h" >/dev/null || exit 2
grep -E '^#define CTRL_SRP_(SOURCES|SINKS)' "$w/host.h"
for tag in r2 head; do tree=$r2; [ $tag = head ] && tree=$head; C=$tree/sw/firmware/ctrl; mkdir -p "$w/$tag"
  fl=(-std=c11 -O2 -DNDEBUG -pedantic -DCTRL_HOST_PLATFORM -include "$w/host.h" -I"$C/mbx" -I"$C/loop" -I"$C/port" -I"$C/app" -I"$C/aecp" -I"$C/srp" -I"$C/adp" -I"$C/acmp" -I"$C/maap" -I"$tree/third_party/tsn-c-stack/include" -I"$tree/third_party/lwSRP/src/include")
  printf '#include "ctrl_loop.h"\n' | cc "${fl[@]}" -E -dM -x c - 2> "$w/$tag/err" | grep -v 'CTRL_LOOP_HOST_H' | sort > "$w/$tag/macros"
  cc "${fl[@]}" -E -P "$C/loop/ctrl_loop.c" -o "$w/$tag/ctrl_loop.i" 2>> "$w/$tag/err"
  cc "${fl[@]}" -c "$C/loop/ctrl_loop.c" -o "$w/$tag/ctrl_loop.o" 2>> "$w/$tag/err"
  printf '#include "ctrl_loop.h"\n' | cc "${fl[@]/-DCTRL_HOST_PLATFORM/-UCTRL_HOST_PLATFORM}" -E -x c - -o /dev/null 2> "$w/$tag/plain.err"
  echo "$tag: macros=$(wc -l < "$w/$tag/macros") diagnostics=$(wc -c < "$w/$tag/err") without-macro-refused=$(grep -c 'THE SHAPES: the shape' "$w/$tag/plain.err")"
  grep -E '^#define (CTRL_LOOP_(SLICE_US|BUILD_PASS_US|BUILD_ONE_PASS_US|SRP_UNIT_US|RETRY_COLD_US|RETRY_ATTEMPT_US|QUEUED_MS|TX_MS)|MBX_N_IF) ' "$w/$tag/macros" | tr '\n' ' '; echo
done
for f in macros ctrl_loop.i ctrl_loop.o; do cmp -s "$w/r2/$f" "$w/head/$f" && echo "$f r2==head" || { echo "$f DIFFER"; rc=1; }; done
exit $rc
