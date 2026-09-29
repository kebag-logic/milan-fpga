#!/bin/sh
# Run Verilator suites on the composed candidate the way scripts/run_all_suites.sh
# does (`make -C tb/verilator/<suite>` under timeout), bounded to 8 CPUs.
# Usage: run_suites.sh <repo> <receipt-dir> <verilator-bin-dir> <timeout-s> <target-spec>...
#   target-spec is <suite> or <suite>:<make-target>
set -u
REPO=$1; OUT=$2; VBIN=$3; TMO=$4; shift 4
mkdir -p "$OUT"
export PATH="$VBIN:$PATH"
cd "$REPO" || exit 2
for spec in "$@"; do
  suite=${spec%%:*}; tgt=
  [ "$suite" != "$spec" ] && tgt=${spec#*:}
  tag=$suite${tgt:+_$tgt}
  log="$OUT/suite_$tag.log"
  {
    echo "\$ taskset -c 0-7 timeout $TMO make -C tb/verilator/$suite $tgt"
    echo "head: $(git rev-parse HEAD) tree: $(git rev-parse 'HEAD^{tree}')"
    echo "verilator: $(verilator --version)"
    echo "start: $(date -u +%FT%TZ)"
  } > "$log"
  t0=$(date +%s)
  taskset -c 0-7 timeout "$TMO" make -C "tb/verilator/$suite" $tgt >> "$log" 2>&1
  rc=$?
  t1=$(date +%s)
  echo "end: $(date -u +%FT%TZ) wall_s=$((t1 - t0)) rc=$rc" >> "$log"
  printf '%-40s rc=%s wall_s=%s\n' "$tag" "$rc" "$((t1 - t0))" | tee -a "$OUT/suites_summary.txt"
done
