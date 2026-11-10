#!/bin/bash
# Real-toolchain probe sized for one foreground call on a loaded host:
# the control and one generator mutant (sub1_*.py from make_variants.py).
# usage: real1_probes.sh <tree> <receipts_dir> <verilator_dir> <cpu_list>
#   R1H: the jobs comparison test (--jobs 1 and --jobs 4) on the head driver
#   R1B: the base commit's serial driver on the same subset
# Both run concurrently in the foreground, each capped at 560 s (rc 124 =
# the cap was reached, not a verdict).
set -u
TREE=$1; OUT=$2; VDIR=$3; CPUS=$4
HERE=$(cd "$(dirname "$0")" && pwd)
ENG=$TREE/tb/verilator/engine
mkdir -p "$OUT"
export PATH="$VDIR:$PATH"
"$VDIR/verilator" --version > "$OUT/verilator-version.txt"
for n in R1H R1B; do rm -rf "$TREE/../tmp-real1/$n"; mkdir -p "$TREE/../tmp-real1/$n"; done
"$HERE/job.sh" R1H "$OUT" "$ENG" "$TREE/../tmp-real1/R1H" "$CPUS" \
  timeout 560 python3 -I ../../mutation_jobs_test.py sub1_none.py --out "$OUT/R1H-out" &
"$HERE/job.sh" R1B "$OUT" "$ENG" "$TREE/../tmp-real1/R1B" "$CPUS" \
  timeout 560 sh -c 'python3 -I sub1_base.py > "$0/R1B.stdout"' "$OUT" &
wait
for n in R1H R1B; do echo "$n rc=$(cat "$OUT/$n.rc")"; done
