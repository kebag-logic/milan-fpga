#!/usr/bin/env bash
# Build the pp_shadow run-crf leg from the parent's exact committed bytes with
# the protocol-processor checked out at a chosen revision, then run the named
# regressions. Usage:
#   arm.sh <parent-clone> <label> <processor-rev> <scratch-root> <verilator> [modes...]
# modes: first-probe crf-stop full (default: first-probe crf-stop)
# The parent clone is only read (git archive / clone --shared); nothing in it
# is written.
set -u
src=$1 label=$2 rev=$3 root=$4 vl=$5
shift 5
modes=("$@")
[ ${#modes[@]} -eq 0 ] && modes=(first-probe crf-stop)

tree="$root/$label"
rm -rf "$tree"
mkdir -p "$tree"
parent_head=$(git -C "$src" rev-parse HEAD)
git -C "$src" archive "$parent_head" | tar -x -C "$tree"
rmdir "$tree/protocol-processor" 2>/dev/null || true
git clone -q --shared --no-checkout "$src/.git/modules/protocol-processor" "$tree/protocol-processor"
git -C "$tree/protocol-processor" -c advice.detachedHead=false checkout -q "$rev"
for sub in third_party/verilog-axis gptp-processor; do
    pin=$(git -C "$src" rev-parse "HEAD:$sub")
    mkdir -p "$tree/$sub"
    git -C "$src/$sub" archive "$pin" | tar -x -C "$tree/$sub"
done

echo "label=$label parent=$parent_head processor=$(git -C "$tree/protocol-processor" rev-parse HEAD)"
echo "processor_status=$(git -C "$tree/protocol-processor" status --porcelain | wc -l)"

cd "$tree/tb/verilator/pp_shadow" || exit 2
# Build once (the recipe's own verilate+build line) and run the fast arm.
make -s run-crf VERILATOR="$vl" SIM_ARGS=--first-probe-only > "$root/$label.first-probe.log" 2>&1
echo "make_first_probe_rc=$?"
[ -x obj_crf/Vpp_crf ] || { echo "no binary"; exit 2; }
for m in "${modes[@]}"; do
    case $m in
        first-probe) continue ;;
        crf-stop) ./obj_crf/Vpp_crf --crf-stop-only > "$root/$label.crf-stop.log" 2>&1 ;;
        full) ./obj_crf/Vpp_crf > "$root/$label.full.log" 2>&1 ;;
    esac
    echo "${m}_rc=$?"
done
