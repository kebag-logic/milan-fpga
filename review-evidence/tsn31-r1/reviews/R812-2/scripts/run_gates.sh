#!/bin/sh
# usage: run_gates.sh CLONE OUT WORK -- the CI's two testing run: steps (validate.py --graphs, baremetal.py) on CLONE,
# concurrently, each with log, rc and time; head/status/diff hash before and after. Build trees under WORK. OUT/done last.
C=$1 O=$2 W=$3
. "$(dirname "$0")/env.sh"
mkdir -p "$O" "$W"; cd "$C" || exit 9
git rev-parse HEAD > "$O/head"; git status --short --ignored > "$O/status-before"; git diff HEAD | sha256sum > "$O/diffsha-before"
{ for t in gcc g++ clang clang++ clang-18 clang-tidy cmake cppcheck riscv64-elf-gcc qemu-system-riscv32 mmdc; do printf '%s: %s | ' "$t" "$(command -v $t)"; $t --version 2>&1 | head -1; done; pkg-config --modversion gtest gmock; } > "$O/tools.txt" 2>&1
( /usr/bin/time -v -o "$O/validate.time" python3 scripts/validate.py --work "$W/val" --jobs 16 --graphs > "$O/validate.log" 2>&1; echo $? > "$O/validate.rc" ) &
( /usr/bin/time -v -o "$O/baremetal.time" python3 scripts/baremetal.py --work "$W/rv32" --jobs 8 > "$O/baremetal.log" 2>&1; echo $? > "$O/baremetal.rc" ) &
wait
rm -rf scripts/__pycache__
git status --short --ignored > "$O/status-after"; git diff HEAD | sha256sum > "$O/diffsha-after"
echo done > "$O/done"
