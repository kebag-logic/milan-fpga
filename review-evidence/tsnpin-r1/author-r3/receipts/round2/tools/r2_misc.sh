#!/usr/bin/env bash
# r2_misc.sh: on a clean clone of the head, the sweep's mbx suite (it builds acmp_mbx.c) and S2's harness self-test.
set -u
D=<scratch>; W=$D/gates/lane-wt5; H=$(cat $D/gates/HEAD2)
$D/tools/snap.sh $W $H >/dev/null || exit 4
cd $W && test "$(git rev-parse HEAD)" = "$H" || exit 5
export PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<tools-scratch>/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=<tools>/pinned-verilator-5.050/verilator TSN_GEN_ROOT=<mgmt>/tools/tsn-gen-deca300c
export TMPDIR=$D/tmp MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0
{ echo "# head $H: make -C tb/verilator/mbx"; timeout 1800 make -C tb/verilator/mbx; } > $D/logs/mbx-suite-r2.log 2>&1; echo $? > $D/logs/mbx-suite-r2.rc
python3 scripts/suite_tally.py --help >/dev/null 2>&1 && python3 scripts/suite_tally.py $D/logs/mbx-suite-r2.log > $D/logs/mbx-suite-r2.tally 2>&1
export MILAN_RV32_CC=$D/sdk<home-path>/host/bin/riscv32-linux-gcc PATH=$D/sdk<home-path>/host/bin:$PATH LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
{ echo "# head $H: run.py --self-test"; <litex-env>/venv/bin/python3 -B tb/verilator/ctrl_service_budget/run.py --self-test; } > $D/logs/s2-selftest-r2.log 2>&1; echo $? > $D/logs/s2-selftest-r2.rc
git status --porcelain > $D/logs/r2-misc-tree-after.txt
