#!/bin/bash
# Usage: pin_probe.sh <repo> <workdir>: the differential must refuse (exit 2, REFUSED, nothing built) an edited
# tsn-c-stack clone in both modes, and accept the pin of an unmodified clone (build then fails: VERILATOR=false).
set -u; R=$1; W=$2; cd "$R" || exit 9
pin=$(git ls-tree HEAD third_party/tsn-c-stack | awk '{print $3}')
git clone -q --no-hardlinks third_party/tsn-c-stack "$W/clone" && git -C "$W/clone" checkout -q "$pin" || exit 9
run() { local tag=$1; shift; out=$(env VERILATOR=false python3 -B sw/firmware/ctrl/test/maap_differential.py --stack "$W/clone" --keep "$W/keep-$tag" "$@" 2>&1); rc=$?
  echo "[$tag] rc=$rc built=$( [ -e "$W/keep-$tag" ] && echo yes || echo no ) :: $(printf '%s\n' "$out" | grep -m2 -E 'tsn-c-stack|REFUSED' | tr '\n' ' ')"; }
run pinned-default
run pinned-selftest --self-test
printf '\n/* r558 probe */\n' >> "$W/clone/src/maap.c"
run edited-default
run edited-selftest --self-test
git -C "$W/clone" checkout -q -- src/maap.c
run restored-default
