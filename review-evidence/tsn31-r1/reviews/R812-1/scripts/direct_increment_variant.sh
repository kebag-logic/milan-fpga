#!/bin/bash
# SUGGESTION measurement only (not proposed source): transmit increments the one released sink's change_owed
# directly instead of looping over every sink. RV32I text at 16 sinks, then acmp_tests (16) and acmp_wide (33).
# usage: direct_increment_variant.sh <packet> <head tree> <scratch work dir>
P=$1 H=$2 W=$3; . "$P/scripts/env.sh" "$P"
rm -rf "$W"; mkdir -p "$W"; cp -r "$H/src" "$H/include" "$W/"
python3 -I - "$W/src/acmp.c" <<'PY'
import sys
p = sys.argv[1]; t = open(p).read()
old_set = "\t\to->release[(release - 1u) / 32u] = 1u << ((release - 1u) % 32u);\n\t}\n"
new_set = "\t\to->release[(release - 1u) / 32u] = 1u << ((release - 1u) % 32u);\n\t\ta->sinks[release - 1u].change_owed++;\n\t}\n"
old_loop = ("\tfor (unsigned k = 0; k < a->cfg.n_sinks; ++k) {\n\t\ta->sinks[k].change_owed = (uint8_t)(a->sinks[k].change_owed + "
            "((o->release[k / 32u] >> (k % 32u)) & 1u));\n\t}\n")
assert t.count(old_set) == 1 and t.count(old_loop) == 1
open(p, "w").write(t.replace(old_set, new_set).replace(old_loop, ""))
PY
I="-isystem $(riscv64-elf-gcc -print-file-name=include) -I$H/examples/rv32/include"
for o in Os O2 O3; do
  riscv64-elf-gcc -march=rv32i -mabi=ilp32 -ffreestanding -fno-builtin -nostdinc $I -std=c11 -Wall -Wextra -Werror -$o \
    -DNDEBUG -DCTRL_REENTRY_ASSERT -I"$W/include" -c "$W/src/acmp.c" -o "$W/v-$o.o" && echo "-$o variant text=$(riscv64-elf-size "$W/v-$o.o" | awk 'NR==2{print $1}')"
done
GT=$(pkg-config --cflags gmock gtest); GL=$(pkg-config --libs gmock gtest); g++ -std=c++20 $GT -c "$H/tests/main.cpp" -o "$W/m.o"
gcc -std=c11 -O0 -g -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT -I"$W/include" -c "$W/src/acmp.c" -o "$W/a16.o"
g++ -std=c++20 -O0 $GT -I"$W/include" -I"$H/tests" -I"$H/examples" -c "$H/tests/test_acmp.cpp" -o "$W/t16.o" && g++ "$W/a16.o" "$W/t16.o" "$W/m.o" $GL -o "$W/acmp16"
"$W/acmp16" 2>&1 | grep -E "^\[  (PASSED|FAILED) " | head -3
F="-DACMP_MAX_SINKS=33u -fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined"
gcc -std=c11 -O0 -g -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT $F -I"$W/include" -c "$W/src/acmp.c" -o "$W/a33.o"
g++ -std=c++20 -O0 $F $GT -I"$W/include" -I"$H/tests" -c "$H/tests/test_acmp_wide.cpp" -o "$W/t33.o" && g++ "$W/a33.o" "$W/t33.o" "$W/m.o" -fsanitize=shift,undefined $GL -o "$W/wide33"
"$W/wide33" 2>&1 | grep -E "^\[  (PASSED|FAILED) |runtime error" | head -3
