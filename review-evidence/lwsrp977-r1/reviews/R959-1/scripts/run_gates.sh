#!/usr/bin/env bash
# Start the lwSRP gates concurrently, each with its own log and rc file.
# Usage: run_gates.sh <checkout> <packet-dir> <cgreen-prefix>
set -u
src=$1; pk=$2; cg=$3
r=$pk/receipts/gates; w=$pk/scratch/work
mkdir -p "$r" "$w"
export LD_LIBRARY_PATH="$cg/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export CMAKE_PREFIX_PATH="$cg"
start() { # name, command...
  local name=$1; shift
  ( cd "$src" && "$@" > "$r/$name.log" 2>&1; echo $? > "$r/$name.rc" ) &
}
for m in OFF ON; do
  start diff-$m python3 -I "$src/tests/check_differential.py" --work-dir "$w/diff-$m" --milan $m --sanitize-memory clang
done
for m in OFF ON; do for s in OFF ON; do
  start rev-m$m-s$s python3 -I "$src/tests/check_reversals.py" --work-dir "$w/rev-m$m-s$s" --prefix "$cg" --milan $m --scale $s
done; done
for cfg in "default:-DLWSRP_MILAN=OFF" "milan:-DLWSRP_MILAN=ON" "scale:-DLWSRP_MILAN=OFF -DLWSRP_SCALE=ON" "milan-scale:-DLWSRP_MILAN=ON -DLWSRP_SCALE=ON"; do
  name=${cfg%%:*}; flags=${cfg#*:}
  start unit-$name bash -c "cmake -S '$src' -B '$w/unit-$name' -DCMAKE_BUILD_TYPE=Debug $flags && cmake --build '$w/unit-$name' -j4 && '$w/unit-$name/unit_tests' && ctest --test-dir '$w/unit-$name' --output-on-failure"
done
wait
echo ALL-DONE > "$r/ALL.done"
