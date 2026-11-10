#!/bin/sh
# The donor probes, as run (shell, from the probe directory, with the pinned toolchain's env.sh sourced):
# 1. R807-1's mask probe (a copy of its acmp_mask_probe.sh and .cpp, unchanged) at 33 sinks against the donor head's
#    clean clone, against main ea4af6f and against the parent's pin 70936b77:
#      GTEST=$TOOLS/gtest-1.14.0 bash acmp_mask_probe.sh <tree> <out> 33
# 2. The new 33-sink test (tests/test_acmp_wide.cpp at the donor head) built against main's src/acmp.c at 33 sinks,
#    first with -fno-sanitize-recover=shift,undefined, then recovering (to show the alias):
G=$TOOLS/gtest-1.14.0; T=<donor clone>; M=<main export>
for mode in norecover recover; do
  F="-fsanitize=shift,undefined"; [ $mode = norecover ] && F="$F -fno-sanitize-recover=shift,undefined"
  gcc -std=c11 -O0 -g $F -DACMP_MAX_SINKS=33u -DNDEBUG -DCTRL_REENTRY_ASSERT -I$M/include -c $M/src/acmp.c -o main-$mode.o
  g++ -std=c++20 -O0 -g $F -DACMP_MAX_SINKS=33u -I$M/include -I$T/tests -I$G/include -c $T/tests/test_acmp_wide.cpp -o wide-$mode.o
  g++ -std=c++20 -c $T/tests/main.cpp -I$G/include -o tmain.o
  g++ main-$mode.o wide-$mode.o tmain.o $F $G/lib/libgmock.a $G/lib/libgtest.a -lpthread -o wide-on-main-$mode
  ./wide-on-main-$mode
done
# 3. The build-time refusal: the donor head's tree with the mask planted back to one word (uint32_t release[1]),
#    compiled at 32 and at 33 sinks; then the donor head as committed at 16, 33, 64 and 65 sinks:
#      gcc -std=c11 -Wall -Wextra -Werror -DACMP_MAX_SINKS=<n>u -I<tree>/include -c <tree>/src/acmp.c -o /dev/null
# 4. wide_plants_at16.py: each acmp-wide-* plant in the 16-sink acmp_tests binary.
# 5. RV32 sizes: riscv64-elf-size of baremetal.py's Release and Debug acmp.c.obj and rv32_smoke.elf at main and at
#    the donor head, and riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc
#    -DNDEBUG -DCTRL_REENTRY_ASSERT at -Os and -O2 (the parent firmware compiles the stack at -Os).
