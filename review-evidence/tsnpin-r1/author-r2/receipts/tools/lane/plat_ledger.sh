#!/usr/bin/env bash
# plat_ledger.sh <tree> <out> <runtime> <shape> <interfaces> <csr.csv> <flash-map> [ledgered]: the target platform's split image.
set -u
T=$1; O=$2; R=$3; shape=$4; n=$5; csv=$6; fm=$7; led=${8:-}
mkdir -p "$O"; cd "$T" || exit 3
tag=${shape#endstation_ax7101_}-if$n; extra=(); [ -n "$led" ] && extra=(--ledgered-point "$led")
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/$shape.yaml --interfaces $n "${extra[@]}" --csr-csv "$csv" \
  --flash-map "$fm" --output "$O/$tag" --libc "$R/libc.a" --compiler-runtime "$R/libcompiler_rt.a" > "$O/$tag.log" 2>&1
echo $? > "$O/$tag.rc"
~/br-milan-rv32/host/bin/riscv32-linux-nm -S --size-sort "$O/$tag/ctrl_app.elf" > "$O/$tag.nm" 2>&1
echo "plat $tag rc=$(cat $O/$tag.rc) lshrdi3=$(grep -c ' __lshrdi3$' $O/$tag.nm)"
