#!/usr/bin/env bash
# Does the MAAP README's literal selector prefix pick the compiler it names?
# Usage: selector_probe.sh <repo> <competing-compiler-dir>
# Case 1: competing default on PATH (riscv32-linux-gcc), README prefix names riscv64-elf-gcc.
# Case 2: retired CTRL_RV32_CC prefix, same PATH (control: must NOT select riscv64-elf-gcc).
# Case 3: no default candidate on PATH except the named one via MILAN_RV32_CC.
set -u
repo=$1; comp=$2
line=$(grep -n 'RV32_CC=riscv64-elf-gcc python3 sw/firmware/ctrl/test/test_ctrl_firmware.py' "$repo/sw/firmware/ctrl/maap/README.md")
echo "README line: $line"
prefix=$(echo "$line" | sed -E 's/^[0-9]+:([A-Z0-9_]+)=riscv64-elf-gcc .*/\1/')
echo "README selector variable: $prefix"
py="import sys; sys.path[:0]=['$repo/sw/firmware/gtest','$repo/scripts']; import fw_rv32; print(fw_rv32.compiler())"
echo "case1 README prefix, competing default: $(env -u MILAN_RV32_CC PATH="$comp:/usr/bin:/bin" HOME=/nonexistent "$prefix=riscv64-elf-gcc" python3 -c "$py")"
echo "case2 retired CTRL_RV32_CC, competing default: $(env -u MILAN_RV32_CC PATH="$comp:/usr/bin:/bin" HOME=/nonexistent CTRL_RV32_CC=riscv64-elf-gcc python3 -c "$py")"
echo "case3 README prefix, no competing default: $(env -u MILAN_RV32_CC PATH="/usr/bin:/bin" HOME=/nonexistent "$prefix=riscv64-elf-gcc" python3 -c "$py")"
echo "grep CTRL_RV32_CC sw docs scripts:"; (cd "$repo" && grep -rn CTRL_RV32_CC sw docs scripts); echo "grep rc=$? (1 = no match)"
