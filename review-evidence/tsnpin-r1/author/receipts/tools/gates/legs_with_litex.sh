#!/usr/bin/env bash
# Both builder legs where every SoC-elaborating arm can run: the LiteX interpreter first on PATH and the real HOME, on a clean clone of the head.
set -u
G=<scratch>/gates; H=$(cat $G/HEAD); W=$G/lane-wt4; O=$G/lane
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=<home> VERILATOR=<tools>/pinned-verilator-5.050/verilator TMPDIR=<scratch>/tmp MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0 TSN_GEN_ROOT=<mgmt>/tools/tsn-gen-deca300c
export PATH=<litex-env>/venv/bin:<rv32-sdk>/host/bin:<tools>/sv2v-v0.0.12:<tools>/pinned-verilator-5.050:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
for k in 0 1; do
  { echo "# head $H builder leg $k, LiteX interpreter and HOME"; python3 scripts/ci_builder_legs.py run $k --receipt $O/builder-leg$k-litex.json -- python3 sw/builder/test_builder.py --require-rv32; } > $O/builder_leg${k}_litex.log 2>&1
  echo $? > $O/builder_leg${k}_litex.rc
done
git status --porcelain > $O/tree-after-legs.txt
echo done > $O/LEGS_DONE
