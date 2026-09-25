#!/bin/sh
# [R316] R316-1 reproduction. Run from the root of a clean checkout of
# b068763c849a18096b0f46cf9b18e0f904e4d708 (tree dd5e37ec...).
#   SDK      = a pinned RV32 SDK install that scripts/ci_rv32_sdk.py verifies
#   VERILATOR_DIR = directory holding the pinned Verilator 5.050 entry point
#   PACKET   = this packet
set -eu
: "${SDK:?}" "${VERILATOR_DIR:?}" "${PACKET:?}"
BASE=ffcbd33de70278ae34b533dcbadde0b36c8cba13
R=$PACKET/receipts
S=$PACKET/scratch/tmp
mkdir -p "$R" "$S"
export TMPDIR="$S"

# Hostile/benign variants through the real assert_boot_contract, at head and base,
# and with each new check disconnected.
python3 "$PACKET/scripts/probe.py" sdk --sdk "$SDK" --out "$R/probe-head-sdk.json" --scratch "$S" > "$R/probe-head-sdk.log" 2>&1
python3 "$PACKET/scripts/probe.py" absent --out "$R/probe-head-absent.json" --scratch "$S" > "$R/probe-head-absent.log" 2>&1
python3 "$PACKET/scripts/probe.py" sdk --sdk "$SDK" --base "$BASE" --out "$R/probe-base-sdk.json" --scratch "$S" > "$R/probe-base-sdk.log" 2>&1
python3 "$PACKET/scripts/probe.py" absent --base "$BASE" --out "$R/probe-base-absent.json" --scratch "$S" > "$R/probe-base-absent.log" 2>&1
python3 "$PACKET/scripts/probe.py" sdk --sdk "$SDK" --disable assert_preprocessed_identity_sample --out "$R/probe-head-sdk-disabled.json" --scratch "$S" > "$R/probe-head-sdk-disabled.log" 2>&1
python3 "$PACKET/scripts/probe.py" absent --disable assert_identity_macro_free --out "$R/probe-head-absent-disabled.json" --scratch "$S" > "$R/probe-head-absent-disabled.log" 2>&1
python3 "$PACKET/scripts/matrix.py" "$R" > "$R/probe-matrix.md"

# What the accepted hostile spellings compile to on the pinned SDK.
for v in 0 8 10; do
  "$SDK/bin/riscv32-linux-gcc" -std=gnu99 -O2 -Wall -Wextra -DVARIANT=$v -S \
    -o "$S/v$v.s" "$PACKET/scripts/forge_semantics.c"
done

# Gate 1b alone (not the builder bank), both compiler modes, pinned Verilator.
PATH="$VERILATOR_DIR:$PATH" python3 sw/builder/test_firmware_compiler.py \
  --sdk-destination "$SDK" --audit "$R/gate1b-sdk-v5050.argv.jsonl" > "$R/gate1b-sdk-v5050.log" 2>&1
PATH="$VERILATOR_DIR:$PATH" python3 sw/builder/test_firmware_compiler.py \
  --absent --audit "$R/gate1b-absent-v5050.argv.jsonl" > "$R/gate1b-absent-v5050.log" 2>&1
