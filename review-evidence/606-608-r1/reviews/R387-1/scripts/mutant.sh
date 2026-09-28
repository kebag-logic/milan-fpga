#!/usr/bin/env bash
# Plant one named defect in a disposable copy of an arm tree built by arm.sh,
# rebuild the run-crf leg and run one regression mode.
# Usage: mutant.sh <arm-tree> <scratch-root> <verilator> <name> <file> <sed-expr> <sim-arg>
set -u
base=$1 root=$2 vl=$3 name=$4 file=$5 expr=$6 arg=$7
tree="$root/mut-$name"
rm -rf "$tree"
cp -a "$base" "$tree"
rm -rf "$tree/tb/verilator/pp_shadow/obj_crf"
before=$(sha256sum < "$tree/$file")
sed -i -e "$expr" "$tree/$file"
after=$(sha256sum < "$tree/$file")
if [ "$before" = "$after" ]; then echo "mutant=$name NOT-APPLIED"; exit 3; fi
echo "mutant=$name file=$file planted"
diff <(cd "$base" && cat "$file") "$tree/$file"
cd "$tree/tb/verilator/pp_shadow" || exit 2
make -s run-crf VERILATOR="$vl" SIM_ARGS="$arg" > "$root/mut-$name.log" 2>&1
echo "mutant=$name make_rc=$?"
grep -cE "^pp_shadow: [0-9]+ checks" "$root/mut-$name.log" | sed 's/^/completed_runs=/'
grep -E "FAIL\]|^pp_shadow:|RESULT|%Error" "$root/mut-$name.log"
