#!/bin/sh
# usage: run_ci_steps.sh CLEAN_CLONE OUT  -- runs the two testing run: steps of .github/workflows/quality.yml concurrently.
C=$1 O=$2
. "$(dirname "$0")/env.sh"
mkdir -p "$O"; export TMPDIR=$O/tmp; mkdir -p "$TMPDIR"
cd "$C" || exit 9
git rev-parse HEAD > $O/head; git status --porcelain > $O/status-before; git diff | sha256sum > $O/diffsha-before
{ which clang-18 clang clang++ gcc g++ clang-tidy cppcheck cmake mmdc riscv64-elf-gcc qemu-system-riscv32; clang-18 --version | head -1; clang --version | head -1; gcc --version | head -1; clang-tidy --version | sed -n 2p; pkg-config --modversion gtest gmock; mmdc --version; } > $O/toolchain.txt 2>&1
( python3 scripts/validate.py --work $O/val --jobs 8 --graphs > $O/validate.log 2>&1; echo $? > $O/validate.rc ) &
( python3 scripts/baremetal.py --work $O/rv32 --jobs 8 > $O/baremetal.log 2>&1; echo $? > $O/baremetal.rc ) &
wait
rm -rf scripts/__pycache__
git status --porcelain > $O/status-after; git diff | sha256sum > $O/diffsha-after
echo done > $O/done
