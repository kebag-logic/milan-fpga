#!/usr/bin/env bash
# legs5.sh: both builder legs with the system make, as round 1 ran them, where every SoC-elaborating arm can run, on a clean clone of HEAD2: the LiteX interpreter first on PATH,
# the real HOME (its offline CPU generator caches), and the pinned RV32 SDK named explicitly (MILAN_RV32_CC, its bin on PATH).
set -u
D=<scratch>; G=$D/gates; H=$(cat $G/HEAD2); W=$G/lane-wt8; O=$G/lane5; S=$D/sdk<home-path>/host
$D/tools/snap.sh $W $H >/dev/null || exit 4
cd "$W" && test "$(git rev-parse HEAD)" = "$H" || exit 5
git -C third_party/tsn-c-stack remote set-url origin https://github.com/kebag-logic/tsn-c-stack.git
mkdir -p $O
export HOME=<home> VERILATOR=<tools>/pinned-verilator-5.050/verilator TMPDIR=$D/tmp MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0 TSN_GEN_ROOT=<mgmt>/tools/tsn-gen-deca300c
export MILAN_RV32_CC=$S/bin/riscv32-linux-gcc LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PATH=<litex-env>/venv/bin:$S/bin:<tools>/sv2v-v0.0.12:<tools>/pinned-verilator-5.050:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
for k in 0 1; do
  { echo "# head $H builder leg $k, LiteX interpreter, the pinned RV32 SDK"; python3 scripts/ci_builder_legs.py run $k --receipt $O/builder-leg$k.json -- python3 sw/builder/test_builder.py --require-rv32; } > $O/builder_leg$k.log 2>&1
  echo $? > $O/builder_leg$k.rc
done
git status --porcelain > $O/tree-after-legs.txt
echo done > $O/LEGS_DONE
