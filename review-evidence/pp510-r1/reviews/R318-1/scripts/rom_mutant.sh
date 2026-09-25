#!/bin/sh
# Usage: rom_mutant.sh <built-base-tree> <workdir> <zero-based-word> <new-hex>
# Runs the already-built default pp_top binary against a copy of the
# generated ucode.hex with one word replaced, in <workdir> (never in the
# base tree). Prints the replaced word, the sim output and the exit code.
set -u
BASE=$1; WD=$2; W=$3; NEW=$4
rm -rf "$WD"; mkdir -p "$WD/obj_dir"
cp "$BASE/tb/pp_top/ucode.hex" "$BASE/tb/pp_top/ltn_rom.hex" "$WD/"
L=$((W + 1))
OLD=$(sed -n "${L}p" "$WD/ucode.hex")
sed -i "${L}s/.*/$NEW/" "$WD/ucode.hex"
echo "word $W: $OLD -> $(sed -n "${L}p" "$WD/ucode.hex")"
cmp -l "$BASE/tb/pp_top/ucode.hex" "$WD/ucode.hex" | wc -l | sed 's/^/differing bytes: /'
cd "$WD" && "$BASE/tb/pp_top/obj_dir/Vpp_top_sim"
echo "exit=$?"
