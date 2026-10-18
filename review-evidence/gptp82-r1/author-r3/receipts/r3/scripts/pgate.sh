#!/bin/bash
# One parent consumer gate in the scratch parent PARENT, its log and rc under
# OUT. Usage: pgate.sh PARENT OUT NAME
set -u
P=$1 OUT=$2 NAME=$3
export PATH=<tools>/sv2v-v0.0.12:<tools>/pinned-verilator-5.050:$PATH
export TMPDIR=<scratch>/tmpdir
export TSN_GEN_ROOT=<scratch>/tsn-gen
mkdir -p "$OUT"
cd "$P" || exit 9
case $NAME in
  yosys-ci3) syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow ;;
  lint_rtl) python3 scripts/lint_rtl.py --check --self-test ;;
  port_contracts) python3 scripts/check_port_contracts.py ;;
  port_contracts-selftest) python3 scripts/check_port_contracts.py --selftest ;;
  wire_acc) python3 scripts/check_wire_accountability.py --self-test ;;
  check_gptp_docs) python3 scripts/check_gptp_docs.py ;;
  check_gptp_docs-selftest) python3 scripts/check_gptp_docs.py --selftest ;;
  ooc-tcam) syn/yosys/ooc.sh tcam ;;
  builder-clock-contract) python3 sw/builder/test_clock_contract.py ;;
  gptp_shadow-run) make -C tb/verilator/gptp_shadow run ;;
  gptp_shadow-lifecycle) make -C tb/verilator/gptp_shadow lifecycle ;;
  gptp_shadow-mutants) make -C tb/verilator/gptp_shadow mutants ;;
  gptp_tables) make -C tb/verilator/gptp_tables ;;
  gptp_txts-run) make -C tb/verilator/gptp_txts run ;;
  gptp_txts-mutants) make -C tb/verilator/gptp_txts mutants ;;
  gptp_plane-run) make -C tb/verilator/gptp_plane run ;;
  gptp_plane-phc-step) make -C tb/verilator/gptp_plane phc-step ;;
  tsn_fuzz-ptp) make -C tb/verilator/tsn_fuzz ptp ;;
  milan_dp-gptp) make -C tb/verilator/milan_dp gptp ;;
  milan_dp-gptp-lat) make -C tb/verilator/milan_dp gptp-lat ;;
  milan_dp-gmstep) make -C tb/verilator/milan_dp gmstep ;;
  *) echo "unknown gate $NAME"; exit 9 ;;
esac > "$OUT/$NAME.log" 2>&1
rc=$?
echo $rc > "$OUT/$NAME.rc"
echo "$NAME rc=$rc"
