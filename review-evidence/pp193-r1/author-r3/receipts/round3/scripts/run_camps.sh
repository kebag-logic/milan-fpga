#!/usr/bin/env bash
# usage: run_camps.sh <processor tree> <log dir> <jobs> [campaign ...]
# Every campaign that builds a changed file, one after another, each driver at
# --jobs <jobs>; <name>.log/.rc/.sec, the driver's outputs under <log dir>/work/<name>.
set -u
tree=$1; out=$2; jobs=$3; shift 3
mkdir -p "$out/work"
. <scratch>/r3/scripts/env.sh
cd "$tree" || exit 2
all=(srp_top acmp notify d3 aecp dispatch ctr gsi name_wr name_state elab_mutants)
[ $# -gt 0 ] && all=("$@")
camp() {
  local name=$1 w="$out/work/$1"
  rm -rf "$w"
  case $name in
    srp_top)      (cd tb/srp_top && python3 mutants.py --output "$w" --jobs "$jobs") ;;
    aecp)         (cd tb/pp_top && python3 aecp_mutants.py --output "$w" --jobs "$jobs") ;;
    dispatch)     (cd tb/pp_top && python3 aecp_dispatch_mutants.py --output "$w" --verilator "$VERILATOR" --jobs "$jobs") ;;
    ctr)          (cd tb/pp_top && python3 ctr_mutants.py --output "$w" --jobs "$jobs") ;;
    acmp)         python3 tb/pp_top/acmp_mutants.py --output "$w" --verilator "$VERILATOR" --jobs "$jobs" ;;
    gsi)          python3 tb/pp_top/gsi_mutants.py --output "$w" --verilator "$VERILATOR" --jobs "$jobs" ;;
    name_wr)      python3 tb/pp_top/name_wr_mutant.py --output "$w" ;;
    notify)       python3 tb/pp_top/notify_mutants.py --output "$w" --verilator "$VERILATOR" --jobs "$jobs" ;;
    name_state)   make -C tb/name_state mutants OUTPUT="$w" VERILATOR="$VERILATOR" ;;
    elab_mutants) make -C tb/elab_guards mutants MUTANT_OUTPUT="$w" VERILATOR="$VERILATOR" JOBS="$jobs" ;;
    d3)           python3 tb/pp_top/d3_mutants.py --output "$w" --verilator "$VERILATOR" --jobs "$jobs" ;;
    *) echo "unknown campaign $name"; return 2 ;;
  esac
}
for c in "${all[@]}"; do
  t0=$(date +%s)
  camp "$c" > "$out/$c.log" 2>&1
  echo $? > "$out/$c.rc"
  echo $(( $(date +%s) - t0 )) > "$out/$c.sec"
done
echo done > "$out/ALL.done"
