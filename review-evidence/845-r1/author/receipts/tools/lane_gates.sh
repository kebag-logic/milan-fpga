#!/usr/bin/env bash
# lane_gates.sh <head> <group> <clone> <logdir>: the parent gates this adoption touches, on a clean clone of <head>.
# Each gate's whole output goes to <logdir>/<id>.log and its exit status to <logdir>/<id>.rc; every gate runs
# whatever the previous one returned, and none is piped. The commands are the rtl-fast workflow's run steps at this
# head plus the assignment's named gates, with CI's pins: Verilator 5.050, Yosys 0.66, sv2v v0.0.12, GoogleTest
# 1.14.0 (its headers and libraries ahead of the system's), the Bootlin RV32 SDK that scripts/ci_rv32_sdk.py
# installed into the scratch HOME, and a CPython 3.12.3 venv of ci/constraints-ci.txt (LiteX pins only for the
# firmware-boundary gate, as CI installs them only there).
set -u
H=$1; GROUP=$2; W=$3; G=$4
S=<scratch>
BASE=cc204c6fd2349b543d73f15c97162a2c4434c86e
J=8
GT=<toolchain>/gtest-1.14.0
mkdir -p "$G" "$S/tmp/$GROUP"
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=$S/home TMPDIR=$S/tmp/$GROUP PYTHONHASHSEED=0
export VERILATOR=<toolchain>/pinned-verilator-5.050/verilator TSN_GEN_ROOT=<mgmt-root>/tools/tsn-gen-deca300c
export PKG_CONFIG_PATH=$GT/lib/pkgconfig CMAKE_PREFIX_PATH=$GT LD_LIBRARY_PATH=$GT/lib CPLUS_INCLUDE_PATH=$GT/include C_INCLUDE_PATH=$GT/include LIBRARY_PATH=$GT/lib
export MAKEFLAGS="-j16 --no-print-directory"
TOOLS=<toolchain>/pinned-verilator-5.050:<toolchain>/sv2v-v0.0.12:<make-4.3>/bin:/usr/local/bin:/usr/bin:/bin
CI=$S/venv-ci/bin
LX=$S/venv-docs/bin
P=$CI:$TOOLS
g() { id=$1; shift; { echo "# head $H gate $id: $*"; PATH=$P bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc $(date -Iseconds)" >> "$G/progress.txt"; }
case $GROUP in
  rtl)
    g diffcheck "git diff --check $BASE HEAD"
    g ci_scope_selftest "python3 scripts/ci_scope.py --selftest"
    g ci_scope_classify "git diff --no-renames --name-only $BASE HEAD > $TMPDIR/changed-files && cat $TMPDIR/changed-files && python3 scripts/ci_scope.py < $TMPDIR/changed-files"
    g lint_rtl "python3 scripts/lint_rtl.py --check --self-test --jobs $J"
    g pp_srcs "python3 scripts/pp_srcs.py --check --selftest"
    g behave "cd tests && behave --no-capture -f plain"
    g yosys_elaborate "syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow"
    g ooc_read_sets "set -euo pipefail; python3 syn/ooc/dp_srcs.py --selftest; python3 syn/ooc/ooc_tcl_selftest.py; python3 syn/ooc/pp_baseline.py --selftest; python3 syn/ooc/pp_baseline_mutants.py; python3 syn/ooc/pp_baseline_reports_selftest.py; python3 syn/ooc/pp_resource_gate.py --selftest; python3 syn/ooc/pp_resource_gate_mutants.py; python3 syn/ooc/pp_resource_gate.py check-baseline; python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null; python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null"
    g ooc_selftest "python3 syn/yosys/ooc_selftest.py"
    g guard_selftest "python3 syn/yosys/guard_selftest.py"
    g cache_selftest "python3 syn/yosys/cache_selftest.py"
    g publication_census "python3 sw/mailbox/publication_census.py --check --selftest --jobs $J"
    g cpp_idiom "python3 scripts/check_cpp_idiom.py"
    g cpp_idiom_list "python3 scripts/check_cpp_idiom.py --list"
    g cpp_idiom_selftest "python3 scripts/check_cpp_idiom.py --selftest"
    g xvlog_gate "XVLOG=<home>/Xilinx/2026.1/Vivado/bin/xvlog python3 scripts/xvlog_gate.py --check"
    g docs_inventory "python3 scripts/docs_inventory.py --check"
    g rom_digests_check "./syn/yosys/ooc.sh --record-rom-digests && git diff --exit-code -- syn/yosys/rom_digests.tsv"
    ;;
  fw)
    g fw_tally_selftest "python3 sw/firmware/gtest/tally_selftest.py"
    g fw_rv32_selftest "python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32"
    g fw_shard0 "python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 0/4"
    g fw_ctrl_nvm "python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs $J"
    g fw_coverage_selftest "python3 sw/firmware/gtest/fw_coverage.py --selftest"
    g fw_coverage "python3 sw/firmware/gtest/fw_coverage.py --check --jobs $J"
    g fw_shard1_control "python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 1/4"
    g fw_shard2_aecp "python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 2/4"
    g fw_shard3_srp "python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs $J --shard 3/4"
    P=$LX:$TOOLS g fw_boundary "python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator"
    g fw_verilator "python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator"
    ;;
  builder)
    g builder "python3 sw/builder/test_builder.py --require-rv32"
    ;;
  builder-litex)
    g builder_litex "MILAN_LITEX_PYTHON=<litex>/venv/bin/python3 python3 sw/builder/test_builder.py --require-rv32"
    ;;
esac
git status --porcelain --untracked-files=no > "$G/tree-after.txt"
echo done > "$G/DONE"
