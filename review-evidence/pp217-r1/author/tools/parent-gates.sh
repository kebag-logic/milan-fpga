#!/usr/bin/env bash
# parent-gates.sh <runs> <parent> <jobs> <gate>...: run the named consumer gates of the scratch parent, in order, each
# with its cmd/log/rc/start/end under <runs>; every gate runs whatever the previous one's rc. The commands are the
# rtl-fast workflow's run steps (plus milan_dp), with CI's pinned Verilator 5.050, sv2v v0.0.12, GoogleTest 1.14.0
# and a CPython 3.12.3 venv of the parent's ci/constraints-ci.txt in this lane's scratch.
R=$1; P=$2; J=$3; shift 3
. "$(dirname "$0")/common.sh"
G=$VALIDATION_TOOLS/gtest-1.14.0
PP=$SV:$VC/bin:$VL:$BASE
export HOME=$HOME TMPDIR=$S/tmp/parent-$(basename "$P") SV2V=$SV/sv2v YOSYS=/usr/bin/yosys
export PIP_CONSTRAINT=$P/ci/constraints-ci.txt
export PKG_CONFIG_PATH=$G/lib/pkgconfig CMAKE_PREFIX_PATH=$G LD_LIBRARY_PATH=$G/lib CPLUS_INCLUDE_PATH=$G/include C_INCLUDE_PATH=$G/include LIBRARY_PATH=$G/lib
export MAKEFLAGS="-j$J --no-print-directory"
mkdir -p "$R" "$TMPDIR"
gp() { n=$1; shift; g "$R" "$P" "$PP" "$n" "$@"; }
for gate in "$@"; do
  case $gate in
    rom)
      gp rom_digests ./syn/yosys/ooc.sh --record-rom-digests ;;
    changes)
      gp ci_scope_selftest python3 scripts/ci_scope.py --selftest
      gp ci_scope_classify bash -c 'git diff --no-renames --name-only ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36 HEAD | tee /dev/stderr | python3 scripts/ci_scope.py' ;;
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
    pp_shadow)
      gp pp_shadow make -C tb/verilator/pp_shadow ;;
    nvm_cosim|milan_dp_mclk|milan_dp_render|capture_coherence)
      gp "$gate" make -C "tb/verilator/$gate" ;;
  esac
done
