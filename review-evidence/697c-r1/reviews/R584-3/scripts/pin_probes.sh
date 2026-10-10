#!/usr/bin/env bash
# R584-3 pin probes: run each tb/verilator/mbx target standalone against a spoiled
# tsn-c-stack in a disposable copy of the checkout; each must refuse on the pin
# check (ctrl_build.py --stack-pin) and never compile the poisoned header.
# Usage: pin_probes.sh <disposable-checkout-copy> <verilator>
set -u
REPO=$1; VER=$2
STK=$REPO/third_party/tsn-c-stack; MBX=$REPO/tb/verilator/mbx
PIN=$(git -C "$REPO" ls-tree HEAD third_party/tsn-c-stack | awk '{print $3}')
restore() {
  git -C "$STK" update-index --no-assume-unchanged src/adp.c 2>/dev/null
  git -C "$STK" -c advice.detachedHead=false checkout -q "$PIN" && git -C "$STK" checkout -q -- . && git -C "$STK" clean -qfdx
  make -s -C "$MBX" clean >/dev/null 2>&1
}
poison() { printf '\n#error R584-POISON compiled\n' >> "$STK/include/wire.h"; }
hidden() { printf '\n#error R584-POISON compiled\n' >> "$STK/src/adp.c"; git -C "$STK" update-index --assume-unchanged src/adp.c; }
otherrev() { git -C "$STK" -c advice.detachedHead=false checkout -q HEAD~1; }
extra() { printf '#error R584-POISON compiled\n' > "$STK/include/stdint.h"; }
pass=0; fail=0
probe() { # name spoil expect(refuse|pass) make-args...
  local name=$1 spoil=$2 expect=$3; shift 3
  restore; $spoil
  out=$(timeout 900 make --no-print-directory -C "$MBX" VERILATOR="$VER" "$@" 2>&1); rc=$?
  local refused=no poisoned=no pinok=no
  grep -q "REFUSED" <<<"$out" && refused=yes
  grep -q "R584-POISON" <<<"$out" && poisoned=yes
  grep -q "tsn-c-stack at\|pinned.*ok\|^tsn-c-stack" <<<"$out" && pinok=yes
  local verdict
  if [ "$expect" = refuse ]; then
    [ $rc -ne 0 ] && [ $refused = yes ] && [ $poisoned = no ] && verdict=REFUSED-ON-PIN || verdict=ESCAPED
  else
    [ $rc -eq 0 ] && [ $poisoned = no ] && verdict=PASSED || verdict=UNEXPECTED
  fi
  case $verdict in REFUSED-ON-PIN|PASSED) pass=$((pass+1));; *) fail=$((fail+1));; esac
  echo "[$verdict] $name: make $* -> rc=$rc refused=$refused poisoned=$poisoned :: $(grep -m1 -E 'REFUSED|R584-POISON' <<<"$out" | cut -c1-220)"
}
probe "clean stack, stack-pin" true pass stack-pin
probe "clean stack, firmware library" true pass obj_fw/libctrlfw.a
for t in all run-cosim run-if2 obj_fw/libctrlfw.a stack-pin; do probe "poisoned wire.h" poison refuse "$t"; done
probe "poisoned wire.h" poison refuse -j16 all
probe "poisoned wire.h, keep-going (simulator false)" poison refuse -k -j16 VERILATOR=false all
probe "poisoned wire.h" poison refuse -j16 run-if2 run-cosim
probe "assume-unchanged hidden edit" hidden refuse run-if2
probe "assume-unchanged hidden edit" hidden refuse run-cosim
probe "stack at another revision" otherrev refuse run-if2
probe "stack at another revision" otherrev refuse obj_fw/libctrlfw.a
probe "extra header the pinned tree lacks" extra refuse run-cosim
probe "extra header the pinned tree lacks" extra refuse run-if2
restore
echo "pin probes: $pass as expected, $fail not"
[ $fail -eq 0 ]
