#!/usr/bin/env bash
# #817: the Verilator suites that compile hdl/ieee1722/crf/KL_mmcm_drp_servo.sv (directly or through
# milan_datapath), run as scripts/run_all_suites.sh runs each one: `timeout <its wall clock> make -C <suite>`,
# then scripts/suite_tally.py --verdict on the log (a make that exits 0 over a failing log is a FAIL).
# One worker per clone, its suites in order. Writes <out>/<suite>.log and <out>/<suite>.rc ("<rc> <seconds>s").
# usage: suites.sh <clone> <out> <suite> ...
set -u
clone=$1; out=$2; shift 2
here=$(cd "$(dirname "$0")" && pwd)
source "$here/env.sh"; source "$here/fw_env.sh"
mkdir -p "$out"
timeout_of() {
  case "$1" in
    capture_coherence) echo 2400 ;; milan_dp_mclk) echo 3600 ;; milan_dp) echo 4800 ;;
    media_phase) echo 1400 ;; *) echo 1800 ;;
  esac
}
for suite in "$@"; do
  s=$(date +%s)
  timeout "$(timeout_of "$suite")" make -C "$clone/tb/verilator/$suite" > "$out/$suite.log" 2>&1
  rc=$?
  if [ "$rc" -eq 0 ] && ! python3 "$clone/scripts/suite_tally.py" --verdict "$out/$suite.log" > "$out/$suite.verdict" 2>&1; then
    rc=93
  fi
  echo "$rc $(( $(date +%s) - s ))s" > "$out/$suite.rc"
  echo "$(date -u +%T) $suite rc=$rc $(( $(date +%s) - s ))s"
done
echo WORKER-DONE
