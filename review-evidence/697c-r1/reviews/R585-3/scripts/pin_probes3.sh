#!/usr/bin/env bash
# Round-3 reviewer pin probes of the mailbox bench's Makefile targets, in place on a disposable clone's
# tsn-c-stack submodule, restored after every arm. Each arm must refuse on the pin check (exit non-zero with
# "differs from the pinned" / "is not the pinned") and never compile the poisoned header.
# Usage: pin_probes3.sh <clone>
set -u
R=$(cd "$1" && pwd); S=$R/third_party/tsn-c-stack; B=$R/tb/verilator/mbx
restore() {
  git -C "$S" update-index --no-assume-unchanged src/adp.c include/wire.h 2>/dev/null
  git -C "$S" checkout --quiet -- . ; git -C "$S" clean -fdq
  [ -z "$(git -C "$S" status --porcelain)" ] || { echo "RESTORE FAILED"; exit 9; }
}
arm() {  # name, spoil, make args...
  local name=$1 spoil=$2; shift 2
  restore; eval "$spoil"
  local log=/tmp/pin3-$$-$name.log
  ( cd "$B" && timeout 900 make --no-print-directory VERILATOR=true "$@" ) > "$log" 2>&1; local rc=$?
  local said; said=$(grep -m1 -E "differs from the pinned|is not the pinned" "$log" | cut -c1-160)
  local poison=no; grep -q "PLANTED_WIRE_EDIT\|PLANTED_TEST_EDIT" "$log" && poison=COMPILED
  local verdict=ESCAPED; [ $rc -ne 0 ] && [ -n "$said" ] && [ $poison = no ] && verdict=REFUSED
  printf '%s %s rc=%s poisoned-header=%s : %s\n' "$verdict" "$name" "$rc" "$poison" "${said:-no pin verdict}"
  rm -f "$log"
}
WIRE='printf "#error PLANTED_WIRE_EDIT\n" >> "$S/include/wire.h"'
HIDEW='printf "#error PLANTED_WIRE_EDIT\n" >> "$S/include/wire.h"; git -C "$S" update-index --assume-unchanged include/wire.h'
TESTS='printf "#error PLANTED_TEST_EDIT\n" >> "$S/tests/test_adp.cpp"'
make -C "$B" clean > /dev/null
arm WIRE-all "$WIRE" all
arm WIRE-all-j16 "$WIRE" -j16 all
arm WIRE-all-keep-going "$WIRE" -k all
arm WIRE-run-if2-j16 "$WIRE" -j16 run-if2
arm WIRE-run-cosim "$WIRE" run-cosim
arm WIRE-libctrlfw "$WIRE" obj_fw/libctrlfw.a
arm HIDDEN-WIRE-run-if2 "$HIDEW" run-if2
# a library built clean, then a stack file it does not depend on edited: the phony pin check still refuses
restore; ( cd "$B" && make --no-print-directory obj_fw/libctrlfw.a > /dev/null 2>&1 ) && echo "clean library built: rc=0"
arm STALE-LIB-tests-edit-run-cosim "$TESTS" run-cosim
arm STALE-LIB-tests-edit-libctrlfw "$TESTS" obj_fw/libctrlfw.a
restore; make -C "$B" clean > /dev/null
echo "restored: $(git -C "$S" rev-parse HEAD) status='$(git -C "$S" status --porcelain)' bench-untracked=$(git -C "$R" status --porcelain --ignored tb/verilator/mbx | wc -l)"
