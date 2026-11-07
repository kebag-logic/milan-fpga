#!/usr/bin/env bash
# parent-gates.sh <runs> <parent> <jobs> <gate>...: run the named consumer gates of the scratch parent, in order, each
# with its cmd/log/rc/start/end/python under <runs>; every gate runs whatever the previous one's rc. The commands are
# the rtl-fast workflow's run steps (plus milan_dp), with CI's pinned Verilator 5.050, Yosys 0.66, sv2v v0.0.12,
# GoogleTest 1.14.0 and a CPython 3.12.3 venv of ci/constraints-ci.txt in this lane's own scratch.
R=$1; P=$2; J=$3; shift 3
. "$(dirname "$0")/common.sh"
G=$VALIDATION_TOOLS/gtest-1.14.0
PP=$VALIDATION_TOOLS/sv2v-v0.0.12:$V/bin:$VL:$BASE
export HOME=$HOME TMPDIR=$S/tmp/parent-$(basename "$P") SV2V=$VALIDATION_TOOLS/sv2v-v0.0.12/sv2v YOSYS=/usr/bin/yosys
export PIP_CONSTRAINT=$P/ci/constraints-ci.txt
export PKG_CONFIG_PATH=$G/lib/pkgconfig CMAKE_PREFIX_PATH=$G LD_LIBRARY_PATH=$G/lib CPLUS_INCLUDE_PATH=$G/include C_INCLUDE_PATH=$G/include LIBRARY_PATH=$G/lib
export MAKEFLAGS="-j$J --no-print-directory"
mkdir -p "$R" "$TMPDIR"
gp() { n=$1; shift; g "$R" "$P" "$V" "$PP" "$n" "$@"; }
for gate in "$@"; do
  case $gate in
    changes)
      gp ci_scope_selftest python3 scripts/ci_scope.py --selftest
      gp ci_scope_classify bash -c 'git diff --no-renames --name-only 604899c08ff1cd1830e1dd08b733109ef852400c HEAD | tee /dev/stderr | python3 scripts/ci_scope.py' ;;
    lint)
      gp lint_rtl python3 scripts/lint_rtl.py --check --self-test --jobs $J
      gp pp_srcs python3 scripts/pp_srcs.py --check --selftest ;;
    bdd)
      gp behave bash -c 'cd tests && behave --no-capture -f plain' ;;
    yosys)
      gp yosys_elaborate syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
      gp ooc_read_sets bash -c 'set -euo pipefail; python3 syn/ooc/dp_srcs.py --selftest; python3 syn/ooc/ooc_tcl_selftest.py; python3 syn/ooc/pp_baseline.py --selftest; python3 syn/ooc/pp_baseline_mutants.py; python3 syn/ooc/pp_baseline_reports_selftest.py; python3 syn/ooc/pp_resource_gate.py --selftest; python3 syn/ooc/pp_resource_gate_mutants.py; python3 syn/ooc/pp_resource_gate.py check-baseline; python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null; python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null'
      gp ooc_selftest python3 syn/yosys/ooc_selftest.py
      gp guard_selftest python3 syn/yosys/guard_selftest.py
      gp cache_selftest python3 syn/yosys/cache_selftest.py ;;
    census)
      gp publication_census python3 sw/mailbox/publication_census.py --check --selftest --jobs $J ;;
    fw-unit)
      gp fw_tally_selftest python3 sw/firmware/gtest/tally_selftest.py
      gp fw_rv32_sdk_selftest python3 scripts/ci_rv32_sdk_selftest.py
      gp fw_rv32_selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
      gp fw_shard0 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 0/4
      gp fw_ctrl_nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs $J
      gp fw_coverage_selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
      gp fw_coverage python3 sw/firmware/gtest/fw_coverage.py --check --jobs $J ;;
    fw-control)
      gp fw_shard1 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 1/4 ;;
    fw-aecp)
      gp fw_shard2 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 2/4 ;;
    fw-srp)
      gp fw_shard3_srp python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 3/4 ;;
    fw-boundary)
      gp fw_boundary python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator ;;
    fw-verilator)
      gp fw_verilator python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator ;;
    milan_dp)
      gp milan_dp make -C tb/verilator/milan_dp SIM_JOBS=2 ;;
    milan_dp_mclk)
      gp milan_dp_mclk make -C tb/verilator/milan_dp_mclk SIM_JOBS=2 ;;
    milan_dp_render)
      gp milan_dp_render make -C tb/verilator/milan_dp_render SIM_JOBS=2 ;;
    pp_shadow)
      gp pp_shadow make -C tb/verilator/pp_shadow ;;
    docs-ratchets)
      # the docs workflow's gates that read the processor tree
      gp docs_check python3 scripts/docs_check.py
      gp check_hygiene python3 scripts/check_hygiene.py --check
      gp measure_fail_fast python3 scripts/measure_fail_fast.py --check
      gp measure_test_evidence python3 scripts/measure_test_evidence.py --check
      gp measure_naming python3 scripts/measure_naming.py --check
      gp check_doc_paths python3 scripts/check_doc_paths.py
      gp check_port_contracts python3 scripts/check_port_contracts.py
      gp check_rtl_source_lists python3 scripts/check_rtl_source_lists.py ;;
    idiom)
      # the docs workflow's idiom gates (each the gate, then its fixture arms)
      for k in cpp py sv sh; do
        gp check_${k}_idiom python3 scripts/check_${k}_idiom.py
        gp check_${k}_idiom_selftest python3 scripts/check_${k}_idiom.py --selftest
      done ;;
  esac
done
