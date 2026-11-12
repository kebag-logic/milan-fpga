#!/usr/bin/env bash
# leg0_pinned.sh: builder leg 0 on a clean clone of HEAD2 with HOME at the pinned RV32 SDK's parent, so the builder's
# home-relative compiler (Path.home()/br-milan-rv32/host/bin/riscv32-linux-gcc, gate 1b) is the pinned SDK; the LiteX
# interpreter named by MILAN_LITEX_PYTHON and first on PATH; the system make. The SDK is verified in the same run.
set -u
D=<scratch>; G=$D/gates; H=$(cat $G/HEAD2); W=$G/lane-wt9; O=$G/lane6
SDKHOME=$D/sdk/home; S=$SDKHOME/br-milan-rv32/host
rm -rf $W; $D/tools/snap.sh $W $H >/dev/null || exit 4
cd "$W" && test "$(git rev-parse HEAD)" = "$H" || exit 5
git -C third_party/tsn-c-stack remote set-url origin https://github.com/kebag-logic/tsn-c-stack.git
mkdir -p $O
python3 -I scripts/ci_rv32_sdk.py --verify-only --destination $S > $O/sdk-verify-only.log 2>&1; echo $? > $O/sdk-verify-only.rc
export HOME=$SDKHOME VERILATOR=<tools>/pinned-verilator-5.050/verilator TMPDIR=$D/tmp MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0 TSN_GEN_ROOT=<mgmt>/tools/tsn-gen-deca300c
export MILAN_LITEX_PYTHON=<litex-env>/venv/bin/python3 LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PATH=<litex-env>/venv/bin:<tools>/sv2v-v0.0.12:<tools>/pinned-verilator-5.050:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
{ echo "# head $H builder leg 0, LiteX interpreter, HOME at the pinned RV32 SDK's parent: $($S/bin/riscv32-linux-gcc --version | head -1)"; python3 scripts/ci_builder_legs.py run 0 --receipt $O/builder-leg0.json -- python3 sw/builder/test_builder.py --require-rv32; } > $O/builder_leg0.log 2>&1
echo $? > $O/builder_leg0.rc
git status --porcelain > $O/tree-after-leg0.txt
echo done > $O/LEG0_DONE
