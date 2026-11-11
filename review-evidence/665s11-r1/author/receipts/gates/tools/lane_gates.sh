#!/bin/bash
# lane_gates.sh <head> <root> <group>: the lane's standalone gates on one fresh clean clone of <head> under
# <root>/lane-<group>, each with its log and rc in <root>/lane/. Groups run concurrently, each its own clone.
#   fw     the firmware self-test, the coverage ratchet, the AECP mutant driver, behave, git diff --check
#   s2     S2's harness at 1x1/1if and 8x8/2if, and its self-test
#   cpu    the REBOOT simulation with its self-test, the split boot simulation and its self-test, the saved-state
#          target's portable self-test
#   build  the end-station builder gates
set -u
head=$1; root=$2; group=$3
LANE=<lane>
G=<scratch>/gates
wt=$root/lane-$group/wt
logs=$root/lane
mkdir -p $logs $root/lane-$group/scratch
git clone -q --shared --no-checkout $LANE $wt
git -C $wt fetch -q $LANE $head
git -C $wt -c advice.detachedHead=false checkout -q --detach $head
test "$(git -C $wt rev-parse HEAD)" = "$head" || exit 3
git -C $wt fetch -q $LANE refs/remotes/origin/dev-soft-core:refs/remotes/origin/dev-soft-core
for dep in $(git -C $wt config --blob $head:.gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  [ "$dep" = external ] && continue
  [ -e $LANE/$dep/.git ] && git -C $wt config submodule.$dep.url $LANE/$dep
done
git -C $wt -c protocol.file.allow=always submodule update -q --init --force $(git -C $wt config --blob $head:.gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -v '^external$')
test -z "$(git -C $wt status --porcelain)" || exit 4
git -C $wt status --porcelain > $logs/$group-tree-before.txt
S=$root/lane-$group/scratch
cd $wt
run() {
  name=$1; shift
  echo "# head $head gate $name: $*" > $logs/$name.log
  ( "$@" ) >> $logs/$name.log 2>&1
  echo $? > $logs/$name.rc
  echo "$(date +%T) $name rc=$(cat $logs/$name.rc)"
}
litex() { bash -c "source <scratch>/tools/env.sh; $*"; }
case $group in
  fw)
    run diffcheck git diff --check "$(git merge-base HEAD origin/dev-soft-core)" HEAD
    run fw_selftest /usr/bin/python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
    run fw_coverage /usr/bin/python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
    run aecp_mutants /usr/bin/python3 sw/firmware/ctrl/test/aecp_mutants.py --output $S/aecp-mutants
    run behave bash -c "cd tests && $G/venv/bin/behave"
    ;;
  s2)
    run s2_selftest litex "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
    run s2_1x1 litex "python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir $S/s2-1x1 --record-budget-findings --jobs 8"
    run s2_8x8 litex "python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/s2-8x8 --record-budget-findings --jobs 8"
    ;;
  cpu)
    run reboot litex "python3 -B tb/verilator/ctrl_reboot/run.py --build-dir $S/reboot --self-test --jobs 3"
    run boot_1x1 litex "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/boot-1x1"
    run boot_selftest litex "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/boot-plants --self-test"
    run nvm_target_selftest /usr/bin/python3 -B tb/verilator/nvm_split_target/run.py --self-test
    ;;
  build)
    run builder /usr/bin/python3 sw/builder/test_builder.py --require-rv32
    ;;
  nvm)
    # the saved-state store's planted-defect campaign (nvm_mutants.py), which no workflow job runs
    run nvm_selftest /usr/bin/python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8
    ;;
  s2-1x1|s2-8x8)
    # one S2 point alone, for a comparison run at another commit (the base)
    p=${group#s2-}
    run s2_$p litex "python3 -B tb/verilator/ctrl_service_budget/run.py --point $p --build-dir $S/s2-$p --record-budget-findings --jobs 8"
    ;;
  *)
    echo "unknown group $group"; exit 2
    ;;
esac
git -C $wt status --porcelain > $logs/$group-tree-after.txt
echo "LANE $group DONE $(date +%T)"
