#!/bin/sh
# [R316] R316-2 reproduction. Run from the root of a clean checkout of
# 77e9ca5ea9e04a7618c577ab511baec63b39dc05 (tree 2748915e...).
#   SDK           = a pinned RV32 SDK install that scripts/ci_rv32_sdk.py verifies
#   VERILATOR_DIR = directory holding the pinned Verilator 5.050 entry point
#   LITEX_INIT_H  = LiteX litex/soc/software/bios/init.h (machine-level check only)
#   PACKET        = this packet
set -eu
: "${SDK:?}" "${VERILATOR_DIR:?}" "${LITEX_INIT_H:?}" "${PACKET:?}"
BASE=ffcbd33de70278ae34b533dcbadde0b36c8cba13
R=$PACKET/receipts
S=$PACKET/scratch/tmp
mkdir -p "$R" "$S"
export TMPDIR="$S"

# 1. The unchanged R316-1 probe set, six configurations.
P1=$PACKET/scripts/r316-1-unchanged/probe.py
python3 "$P1" sdk --sdk "$SDK" --out "$R/r1set-head-sdk.json" --scratch "$S" > "$R/r1set-head-sdk.log" 2>&1
python3 "$P1" absent --out "$R/r1set-head-absent.json" --scratch "$S" > "$R/r1set-head-absent.log" 2>&1
python3 "$P1" sdk --sdk "$SDK" --base "$BASE" --out "$R/r1set-base-sdk.json" --scratch "$S" > "$R/r1set-base-sdk.log" 2>&1
python3 "$P1" absent --base "$BASE" --out "$R/r1set-base-absent.json" --scratch "$S" > "$R/r1set-base-absent.log" 2>&1
python3 "$P1" sdk --sdk "$SDK" --disable assert_preprocessed_identity_sample --out "$R/r1set-head-sdk-disabled.json" --scratch "$S" > "$R/r1set-head-sdk-disabled.log" 2>&1
python3 "$P1" absent --disable assert_identity_macro_free --out "$R/r1set-head-absent-disabled.json" --scratch "$S" > "$R/r1set-head-absent-disabled.log" 2>&1

# 2. New R316-2 cases (N near misses, E escapes, W writes naming nothing, A plain forms).
P2=$PACKET/scripts/r316-2/probe2.py
python3 "$P2" sdk --sdk "$SDK" --out "$R/r2set-head-sdk.json" --scratch "$S" > "$R/r2set-head-sdk.log" 2>&1
python3 "$P2" absent --out "$R/r2set-head-absent.json" --scratch "$S" > "$R/r2set-head-absent.log" 2>&1
python3 "$P2" sdk --sdk "$SDK" --base "$BASE" --out "$R/r2set-base-sdk.json" --scratch "$S" > "$R/r2set-base-sdk.log" 2>&1
python3 "$P2" absent --base "$BASE" --out "$R/r2set-base-absent.json" --scratch "$S" > "$R/r2set-base-absent.log" 2>&1
python3 "$P2" sdk --sdk "$SDK" --disable assert_preprocessed_identity_sample --out "$R/r2set-head-sdk-disabled.json" --scratch "$S" > "$R/r2set-head-sdk-disabled.log" 2>&1
python3 "$P2" absent --disable assert_identity_macro_free --out "$R/r2set-head-absent-disabled.json" --scratch "$S" > "$R/r2set-head-absent-disabled.log" 2>&1

# 3. Sub-rule necessity: one sub-rule mutated in memory (the checkout is not edited).
P3=$PACKET/scripts/r316-2/probe3.py
python3 "$P3" sdk --sdk "$SDK" --out "$R/r2sub-none.json" --scratch "$S" > "$R/r2sub-none.log" 2>&1
for m in nested asm extblank register storage; do
  python3 "$P3" sdk --sdk "$SDK" --disable "mut:$m" --out "$R/r2sub-$m.json" --scratch "$S" > "$R/r2sub-$m.log" 2>&1
done
T=$PACKET/scripts/r316-2/tabulate.py
python3 "$T" "$R" r1set base-sdk head-sdk head-sdk-disabled base-absent head-absent head-absent-disabled > "$R/r1set-matrix.md"
python3 "$T" "$R" r2set base-sdk head-sdk head-sdk-disabled base-absent head-absent head-absent-disabled > "$R/r2set-matrix.md"
python3 "$T" "$R" r2sub none nested asm extblank register storage > "$R/r2sub-matrix.md"

# 4. Machine level: W01-W04 and production at the LiteX optimisation flags.
W=$PACKET/scratch/wdump
python3 "$PACKET/scripts/r316-2/dump_w.py" sdk --sdk "$SDK" --out "$W.json" --scratch "$S" > "$W.log" 2>&1
cp "$LITEX_INIT_H" "$W/init.h"
for v in production W01 W02 W03 W04; do
  "$SDK/bin/riscv32-linux-gcc" -std=gnu99 -Os -g0 -fomit-frame-pointer -fno-builtin \
    -fno-stack-protector -Wall -I"$W" -S -o "$W/$v.s" "$W/$v.c"
done
# Read milan_init up to `bne s0,a5` and the helper bodies (receipts/w-machine.txt).

# 5. Gate 1b alone (not the builder bank), both compiler modes, pinned Verilator.
PATH="$VERILATOR_DIR:$PATH" python3 sw/builder/test_firmware_compiler.py \
  --sdk-destination "$SDK" --audit "$R/gate1b-sdk.argv.jsonl" > "$R/gate1b-sdk.log" 2>&1
PATH="$VERILATOR_DIR:$PATH" python3 sw/builder/test_firmware_compiler.py \
  --absent --audit "$R/gate1b-absent.argv.jsonl" > "$R/gate1b-absent.log" 2>&1
