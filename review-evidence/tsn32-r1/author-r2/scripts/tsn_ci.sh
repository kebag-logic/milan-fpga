#!/bin/bash
# The stack's two testing run: steps (quality.yml) on a clean clone of COMMIT, concurrently, one log and rc each.
# usage: tsn_ci.sh COMMIT OUT
set -u
C=$1 O=$2
. <scratch>/scripts/env.sh
rm -rf "$O"; mkdir -p "$O"
git clone -q --no-local <lanes>/tsn-c-stack-32-walk "$O/src" && git -C "$O/src" checkout -q --detach "$C" || exit 3
cd "$O/src" || exit 3
{ git rev-parse HEAD; git rev-parse HEAD^{tree}; git status --porcelain --untracked-files=all --ignored | wc -l; } > "$O/before.txt"
{ gcc --version | head -1; g++ --version | head -1; clang --version | head -1; clang-18 --version | head -1; clang-tidy --version | grep -m1 version; cppcheck --version; pkg-config --modversion gtest gmock; cmake --version | head -1; python3 --version; mmdc --version; riscv64-elf-gcc --version | head -1; qemu-system-riscv32 --version | head -1; } > "$O/tools.txt" 2>&1
s=$(date +%s); ( python3 scripts/validate.py --work "$O/build-validation" --jobs 16 --graphs > "$O/validate.log" 2>&1; echo $? > "$O/validate.rc"; echo "validate $(( $(date +%s) - s ))s" >> "$O/times.txt" ) &
( python3 scripts/baremetal.py --work "$O/build-rv32" --jobs 16 > "$O/baremetal.log" 2>&1; echo $? > "$O/baremetal.rc"; echo "baremetal $(( $(date +%s) - s ))s" >> "$O/times.txt" ) &
wait
{ git rev-parse HEAD; git rev-parse HEAD^{tree}; git status --porcelain --untracked-files=all | wc -l; git status --porcelain --untracked-files=all --ignored | wc -l; } > "$O/after.txt"
echo done > "$O/DONE"
