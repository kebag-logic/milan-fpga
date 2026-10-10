#!/usr/bin/env bash
# `make all` (serial and -j16) on the mailbox bench with the stack's wire.h poisoned and a simulator stand-in
# that writes passing executables: the run must refuse on the pin check and never compile the poisoned header.
# Usage: pin_probe_all.sh <clone> <no_simulator.py>
set -u
R=$(cd "$1" && pwd); S=$R/third_party/tsn-c-stack; B=$R/tb/verilator/mbx
for j in "" "-j16"; do
  make -C "$B" clean > /dev/null; printf "#error PLANTED_WIRE_EDIT\n" >> "$S/include/wire.h"
  out=$(cd "$B" && timeout 900 make --no-print-directory $j "VERILATOR=python3 -I $2" all 2>&1); rc=$?
  said=$(printf '%s\n' "$out" | grep -m1 -E "differs from the pinned|is not the pinned")
  ran=$(printf '%s\n' "$out" | grep -cE '^\./obj')
  poison=no; printf '%s\n' "$out" | grep -q PLANTED_WIRE_EDIT && poison=COMPILED
  v=ESCAPED; [ $rc -ne 0 ] && [ -n "$said" ] && [ $poison = no ] && v=REFUSED
  echo "$v WIRE-all${j:+$j} rc=$rc poisoned-header=$poison stand-in executables run before the refusal=$ran : ${said:-no pin verdict}"
  git -C "$S" checkout --quiet -- .; make -C "$B" clean > /dev/null
done
echo "restored: $(git -C "$S" rev-parse HEAD) status='$(git -C "$S" status --porcelain)' bench-untracked=$(git -C "$R" status --porcelain --ignored tb/verilator/mbx | wc -l)"
