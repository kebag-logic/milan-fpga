#!/usr/bin/env bash
# R300-4 focused simulation evidence at the exact head.
# Usage: run_sims.sh <clone> <packet> <verilator-bin-dir> <stream: A|B>
#   A (CPUs 0-3): mmcm_servo default (unit, rails, step, slew), slew-mutants, crf_rx
#   B (CPUs 4-7): milan_dp aclk (#443 render CSR leg), render-csr-controls,
#                 gmstep-mutants (the connected gmstep leg, then all controls),
#                 gmstep_mutants.py --slew
# Each step writes <packet>/receipts/sim/<stream>_<n>_<name>.log ending in rc=<n>
# and elapsed seconds. Stream completion writes <packet>/receipts/sim/<stream>.done.
set -u
CLONE=${1:?clone}; PKT=${2:?packet}; VBIN=${3:?verilator bin dir}; S=${4:?stream}
OUT="$PKT/receipts/sim"; mkdir -p "$OUT" "$PKT/scratch/tmp"
export PATH="$VBIN:$PATH" TMPDIR="$PKT/scratch/tmp"
case $S in A) CPUS=0-3 ;; B) CPUS=4-7 ;; *) exit 2 ;; esac
n=0
step() {
  local dir=$1 name=$2; shift 2
  n=$((n + 1))
  local log="$OUT/${S}_${n}_${name}.log"
  local t0; t0=$(date +%s.%N)
  {
    echo "\$ (cd $dir && taskset -c $CPUS $*)"
    echo "verilator: $(command -v verilator) $(verilator --version)"
    ( cd "$CLONE/$dir" && taskset -c "$CPUS" "$@" )
    local rc=$?
    echo "rc=$rc elapsed_s=$(echo "$(date +%s.%N) - $t0" | bc)"
  } > "$log" 2>&1
}
rm -f "$OUT/$S.done"
if [ "$S" = A ]; then
  step tb/verilator/mmcm_servo servo_clean make clean
  step tb/verilator/mmcm_servo servo_default make VERILATOR=verilator
  step tb/verilator/mmcm_servo servo_slew_mutants make slew-mutants VERILATOR=verilator
  step tb/verilator/crf_rx crf_rx_default make VERILATOR=verilator
else
  step tb/verilator/milan_dp dp_aclk make aclk VERILATOR=verilator VERILATOR_JOBS=4
  step tb/verilator/milan_dp dp_render_csr_controls make render-csr-controls VERILATOR=verilator VERILATOR_JOBS=4
  step tb/verilator/milan_dp dp_gmstep_mutants_all make gmstep-mutants VERILATOR=verilator VERILATOR_JOBS=4
  step tb/verilator/milan_dp dp_gmstep_mutants_slew python3 gmstep_mutants.py --slew
fi
date -u +%FT%TZ > "$OUT/$S.done"
