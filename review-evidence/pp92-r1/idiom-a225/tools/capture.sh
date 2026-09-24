#!/usr/bin/env bash
# capture.sh TAG — clean-build the four touched suites (and the acmp_nvm
# pinned control), keep each make log, then re-run every built binary and keep
# its stdout+stderr alone, so a before/after diff compares only what the
# benches print. Also greps every compile for a compiler warning.
set -uo pipefail
tag=${1:?tag}
export PATH=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin:$PATH
lane=$LANES/pp92-93-boot-restore
out=$REVIEWS/pp92-a225-packet/logs/$tag
mkdir -p "$out"
cd "$lane" || exit 1
git rev-parse HEAD > "$out/head.txt"
git status --short >> "$out/head.txt"

run_suite() {   # dir target binary...
  local d=$1 t=$2; shift 2
  make -C "tb/$d" clean > /dev/null 2>&1
  make -C "tb/$d" "$t" > "$out/make-$d-$t.log" 2>&1
  echo "make $d $t rc=$?" >> "$out/rc.txt"
  for b in "$@"; do
    (cd "tb/$d" && "./$b") > "$out/out-$d-$(basename "$b").txt" 2>&1
    echo "run $d $b rc=$?" >> "$out/rc.txt"
  done
}

: > "$out/rc.txt"
run_suite lsn_admit run obj_dir/Vlsn_admit_sim
run_suite nvm_port run obj_dir/Vnvm_port_sim
run_suite pp_top run obj_dir/Vpp_top_sim obj_vid/Vpp_top_vid
run_suite acmp_nvm pinned obj_pinned/Vacmp_nvm_pinned
# `run` after `pinned` without a clean in between would keep obj_pinned; the
# clean inside run_suite removes it, so the pinned binary is re-run above first.
run_suite acmp_nvm run obj_dir/Vacmp_nvm_sim
grep -H "warning:" "$out"/make-*.log > "$out/compiler-warnings.txt"
echo "compiler warnings: $(wc -l < "$out/compiler-warnings.txt")" >> "$out/rc.txt"
cat "$out/rc.txt"
