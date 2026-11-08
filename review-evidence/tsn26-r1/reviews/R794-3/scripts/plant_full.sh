#!/bin/bash
# SPDX-License-Identifier: MIT
# usage: plant_full.sh HEAD_TREE WORK OUT PLANT PLANTS_JSON JOBS
# Applies one plant to a copy of HEAD_TREE, builds every target (Debug), runs the whole ctest suite, then
# runs scripts/baremetal.py and each smoke ELF under QEMU. Records each return code. Needs TOOLS (gtest).
set -u
src=$1; work=$2; out=$3; plant=$4; plants=$5; jobs=$6; here=$(cd "$(dirname "$0")" && pwd)
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
rm -rf "$work"; mkdir -p "$work"; cp -a "$src" "$work/tree"
python3 -I "$here/apply_plant.py" "$work/tree" "$plant" "$plants" > "$out" || exit 1
cmake -S "$work/tree" -B "$work/build" -DCMAKE_BUILD_TYPE=Debug > "$work/configure.log" 2>&1
cmake --build "$work/build" -j"$jobs" > "$work/build.log" 2>&1; echo "build rc=$?" >> "$out"
ctest --test-dir "$work/build" -j"$jobs" > "$work/ctest.log" 2>&1; echo "ctest rc=$?" >> "$out"
grep -E 'tests passed|tests failed' "$work/ctest.log" >> "$out"
(cd "$work/tree" && python3 scripts/baremetal.py --work "$work/rv32" --jobs "$jobs" > "$work/baremetal.log" 2>&1); line="baremetal rc=$?"
for kind in debug release; do
  elf=$work/rv32/$kind/rv32_smoke.elf
  if [ -f "$elf" ]; then timeout 60 qemu-system-riscv32 -machine virt -nographic -bios none -kernel "$elf" -no-reboot > /dev/null 2>&1; line="$line $kind=$?"; else line="$line $kind=no_elf"; fi
done
echo "$line" >> "$out"
