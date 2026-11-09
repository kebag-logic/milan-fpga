#!/usr/bin/env bash
# gates.sh <head> <which...>: the standalone gates, each on its own clean clone of <head> under gates/<which>,
# its log gates/<which>.log ending in rc=N. which: split census identity builder boundary
set -uo pipefail
H=$1; shift
S=$VALIDATION_STORAGE/scratch/a746f; G=$S/gates
LITEX=$HOME/litex-milan/venv/bin
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export TMPDIR=$S/tmp
fresh() { rm -rf "$G/$1"; bash $S/bin/clone.sh "$G/$1" "$2" > "$G/$1-clone.log" 2>&1; }
for which in "$@"; do
  case $which in
    split)
      fresh split "$H"
      (cd $G/split && make -C tb/verilator/milan_dp -j8 split-mutants VERILATOR=$V VERILATOR_JOBS=8) > $G/make-split-mutants.log 2>&1; echo "rc=$?" >> $G/make-split-mutants.log
      (cd $G/split && make -C tb/verilator/milan_dp split-cdc) > $G/make-split-cdc.log 2>&1; echo "rc=$?" >> $G/make-split-cdc.log
      (cd $G/split && make -C tb/verilator/milan_dp split VERILATOR=$V VERILATOR_JOBS=8) > $G/make-split.log 2>&1; echo "rc=$?" >> $G/make-split.log
      ;;
    census)
      fresh census "$H"
      (cd $G/census && /usr/bin/time -v python3 sw/mailbox/publication_census.py --check --jobs 4) > $G/census-check.log 2>&1; echo "rc=$?" >> $G/census-check.log
      ;;
    identity)
      fresh ident-head "$H"; fresh ident-base a9d69c774dee18b90eead74c9f2dda24cf8fdeb8
      cd $G/ident-head
      python3 sw/mailbox/placement_identity.py --dump $G/ident-base.json --tree $G/ident-base --jobs 4 > $G/identity-dump-base.log 2>&1; echo "rc=$?" >> $G/identity-dump-base.log
      python3 sw/mailbox/placement_identity.py --dump $G/ident-head.json --jobs 4 > $G/identity-dump-head.log 2>&1; echo "rc=$?" >> $G/identity-dump-head.log
      python3 sw/mailbox/placement_identity.py --compare $G/ident-base.json $G/ident-head.json > $G/identity-compare.log 2>&1; echo "rc=$?" >> $G/identity-compare.log
      cd $S
      ;;
    builder)
      fresh builder "$H"
      (cd $G/builder && PATH=$LITEX:$PATH python3 sw/builder/test_builder.py --require-rv32) > $G/test_builder.log 2>&1; echo "rc=$?" >> $G/test_builder.log
      ;;
    fwunit)
      fresh fwunit "$H"
      (cd $G/fwunit && python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test) > $G/test_ctrl_firmware.log 2>&1; echo "rc=$?" >> $G/test_ctrl_firmware.log
      ;;
    boundary)
      fresh boundary "$H"
      (cd $G/boundary && PATH=$LITEX:$PATH python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest) > $G/boundary.log 2>&1; echo "rc=$?" >> $G/boundary.log
      ;;
  esac
  echo "$(date +%T) $which done"
done
