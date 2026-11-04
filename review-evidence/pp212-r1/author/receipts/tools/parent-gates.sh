#!/usr/bin/env bash
# parent-gates.sh <runs> <parent> <jobs> <gate>...: run the named consumer gates of the scratch parent, in
# order, each with its cmd/log/rc/start/end under <runs>; every gate runs whatever the previous one's rc.
# The commands are the rtl-fast workflow's run steps (plus milan_dp), with CI's pinned Verilator 5.050,
# Yosys 0.66, sv2v v0.0.12, GoogleTest 1.14.0 (its headers on the system include path, as the distribution package installs them) and a CPython 3.12.3 venv of ci/constraints-ci.txt.
R=$1; P=$2; J=$3; shift 3
T=<scratch>
G=<toolchain>/gtest-1.14.0
export PATH=<toolchain>/sv2v-v0.0.12:$T/venv-ci/bin:<toolchain>/verilator-v5.050/bin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export HOME=<home> TMPDIR=$T<tmp>/parent SV2V=<toolchain>/sv2v-v0.0.12/sv2v YOSYS=/usr/bin/yosys
export PKG_CONFIG_PATH=$G/lib/pkgconfig CMAKE_PREFIX_PATH=$G LD_LIBRARY_PATH=$G/lib CPLUS_INCLUDE_PATH=$G/include C_INCLUDE_PATH=$G/include LIBRARY_PATH=$G/lib
export MAKEFLAGS="-j$J --no-print-directory"
mkdir -p $R $TMPDIR
g() { n=$1; shift; echo "$*" > $R/$n.cmd; date +%s > $R/$n.start; (cd $P && "$@") > $R/$n.log 2>&1; echo $? > $R/$n.rc; date +%s > $R/$n.end; }
for gate in "$@"; do
  case $gate in
    changes)
      g ci_scope_selftest python3 scripts/ci_scope.py --selftest
      g ci_scope_classify bash -c 'git diff --no-renames --name-only 604899c08ff1cd1830e1dd08b733109ef852400c HEAD | tee /dev/stderr | python3 scripts/ci_scope.py' ;;
    lint)
      g lint_rtl python3 scripts/lint_rtl.py --check --self-test --jobs $J
      g pp_srcs python3 scripts/pp_srcs.py --check --selftest ;;
    bdd)
      g behave bash -c 'cd tests && behave --no-capture -f plain' ;;
    yosys)
      g yosys_elaborate syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
      g ooc_read_sets bash -c 'set -euo pipefail; python3 syn/ooc/dp_srcs.py --selftest; python3 syn/ooc/ooc_tcl_selftest.py; python3 syn/ooc/pp_baseline.py --selftest; python3 syn/ooc/pp_baseline_mutants.py; python3 syn/ooc/pp_baseline_reports_selftest.py; python3 syn/ooc/pp_resource_gate.py --selftest; python3 syn/ooc/pp_resource_gate_mutants.py; python3 syn/ooc/pp_resource_gate.py check-baseline; python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null; python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null'
      g ooc_selftest python3 syn/yosys/ooc_selftest.py
      g guard_selftest python3 syn/yosys/guard_selftest.py
      g cache_selftest python3 syn/yosys/cache_selftest.py ;;
    census)
      g publication_census python3 sw/mailbox/publication_census.py --check --selftest --jobs $J ;;
    fw-unit)
      g fw_tally_selftest python3 sw/firmware/gtest/tally_selftest.py
      g fw_rv32_selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
      g fw_shard0 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 0/4
      g fw_ctrl_nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs $J
      g fw_coverage_selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
      g fw_coverage python3 sw/firmware/gtest/fw_coverage.py --check --jobs $J ;;
    fw-control)
      g fw_shard1 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 1/4 ;;
    fw-aecp)
      g fw_shard2 python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 2/4 ;;
    fw-srp)
      g fw_shard3_srp python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 3/4 ;;
    fw-boundary)
      g fw_boundary python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator ;;
    fw-verilator)
      g fw_verilator python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator ;;
    milan_dp)
      g milan_dp make -C tb/verilator/milan_dp SIM_JOBS=2 ;;
  esac
done
