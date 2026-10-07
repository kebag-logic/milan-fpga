#!/bin/sh
# usage: run.sh REPO WORK [RV32_CC]  -- host semantics run, plus RV32 compile-only and symbol check
set -eu
R=$1; W=$2; RC=${3:-}
mkdir -p "$W"; H=$(dirname "$0")
INC=$(gcc -print-file-name=include)
gcc -std=c11 -pedantic -Wall -Wextra -Werror -O2 -nostdinc -isystem "$INC" -I "$R/sw/firmware/gtest/rv32_include" -c "$H/probe.c" -o "$W/probe.o"
gcc -std=c11 -O2 -c "$H/main.c" -o "$W/main.o"
gcc "$W/probe.o" "$W/main.o" -o "$W/probe"
"$W/probe"
if [ -n "$RC" ]; then
  RINC=$("$RC" -print-file-name=include)
  for nd in "" "-DNDEBUG"; do
    for src in probe ndebug; do
      [ "$src" = probe ] && [ -n "$nd" ] && continue   # probe.c sets NDEBUG itself
      "$RC" -march=rv32i -mabi=ilp32 -ffreestanding -Os -std=c11 -pedantic -Wall -Wextra -Werror $nd -nostdinc -isystem "$RINC" \
        -I "$R/sw/firmware/gtest/rv32_include" -c "$H/$src.c" -o "$W/$src-rv32$nd.o"
      echo "rv32 $src ${nd:-debug} undefined: [$(${RC%gcc}nm -u "$W/$src-rv32$nd.o" | awk '{print $NF}' | tr '\n' ' ')]"
    done
  done
fi
