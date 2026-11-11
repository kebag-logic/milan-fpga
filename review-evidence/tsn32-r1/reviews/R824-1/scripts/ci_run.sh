#!/bin/bash
# The stack's two testing run: steps (quality.yml) on a clean clone of COMMIT. usage: ci_run.sh REPO COMMIT OUT
set -u
REPO=$1 C=$2 O=$3
S=$(cd "$(dirname "$0")/.." && pwd)/scratch; . "$(dirname "$0")/env.sh"
rm -rf "$O"; mkdir -p "$O"
git clone -q --no-local "$REPO" "$O/src" && git -C "$O/src" checkout -q --detach "$C" || exit 3
cd "$O/src" || exit 3
{ git rev-parse HEAD; git status --porcelain --untracked-files=all | wc -l; clang --version | head -1; clang-tidy --version | grep -m1 version; pkg-config --modversion gtest; gcc --version | head -1; riscv64-elf-gcc --version 2>/dev/null | head -1; } > "$O/before.txt"
s=$(date +%s); python3 scripts/validate.py --work "$O/build-validation" --jobs 16 --graphs > "$O/validate.log" 2>&1; echo $? > "$O/validate.rc"; echo "validate $(( $(date +%s) - s ))s" >> "$O/times.txt"
s=$(date +%s); python3 scripts/baremetal.py --work "$O/build-rv32" --jobs 16 > "$O/baremetal.log" 2>&1; echo $? > "$O/baremetal.rc"; echo "baremetal $(( $(date +%s) - s ))s" >> "$O/times.txt"
{ git rev-parse HEAD; git status --porcelain --untracked-files=all | wc -l; } > "$O/after.txt"
echo done > "$O/DONE"
