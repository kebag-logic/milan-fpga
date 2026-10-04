#!/usr/bin/env bash
# R463-2: re-run a slice of the author's published arm-port lockstep bench (round-2
# packet, lockstep/armq) after regenerating its inputs, and compare each log with the
# published one byte for byte.
# usage: lockstep_slice.sh PACKET_LOCKSTEP_DIR PROCESSOR_CLONE WORK
# `verilator` on PATH must be the pinned 5.050. build.sh is used unchanged: its
# redacted package path resolves through VALIDATION_STORAGE, pointed at a copy of
# pp_pkg.sv from processor 5c71928a.
set -euo pipefail
pkt=$1; repo=$2; work=$3
rm -rf "$work"; cp -r "$pkt" "$work"
export VALIDATION_STORAGE="$work/vs"
mkdir -p "$VALIDATION_STORAGE/pp639-a525/base/hdl/common"
git -C "$repo" show 5c71928a:hdl/common/pp_pkg.sv > "$VALIDATION_STORAGE/pp639-a525/base/hdl/common/pp_pkg.sv"
cd "$work/armq"
git -C "$repo" show 5c71928a:hdl/top/protocol_processor_top.sv > top_main.sv
git -C "$repo" show 9eebc61:hdl/top/protocol_processor_top.sv > top_head.sv
python3 extract.py top_main.sv armq_ref ref.sv
python3 extract.py top_head.sv armq_dut dut.sv
sh controls.sh top_head.sv
(cd .. && while read -r h _ f; do echo "$h  $f"; done < GENERATED.sha256 | grep '  armq/' | sha256sum -c)
pub=results-head9eebc61
rc=0
run() {  # name sv aw seed
  local n=$1 sv=$2 aw=$3 s=$4 m=0
  [ "$s" -gt 4 ] && m=1
  [ -x "obj_${n}_$aw/sim" ] || sh ./build.sh "$sv" "$aw" "obj_${n}_$aw"
  set +e; "./obj_${n}_$aw/sim" "$s" 1000000 "$m" > "again_${n}_aw${aw}_s$s.log" 2>&1; local r=$?; set -e
  local p
  if [ "$n" = dut ]; then p="$pub/dut_aw${aw}_s$s.log"; else p="$pub/${n}_s$s.log"; fi
  if cmp -s "again_${n}_aw${aw}_s$s.log" "$p"; then same=identical; else same=DIFFERS; rc=1; fi
  echo "$n aw=$aw seed=$s rc=$r published-log=$same"
}
run dut dut.sv 6 1
run dut dut.sv 6 5
run dut dut.sv 7 2
run ctl_write_refused ctl_write_refused.sv 6 1
run ctl_write_refused ctl_write_refused.sv 6 5
exit $rc
