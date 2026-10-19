#!/usr/bin/env bash
# usage: run_camps.sh <processor tree> <log dir> <parallel> [campaign ...]
# Every campaign that builds a changed file; <name>.log/.rc/.sec, scratch
# outputs under <log dir>/work/<name>.
set -u
tree=$1; out=$2; par=$3; shift 3
mkdir -p "$out/work"
. <scratch>/scripts/env.sh
cd "$tree" || exit 2
all=(srp_top srp_admission maap adp aecp dispatch ctr acmp gsi name_wr notify name_state elab_mutants d3)
[ $# -gt 0 ] && all=("$@")
camp() {
  local name=$1 w="$out/work/$1"
  rm -rf "$w"
  case $name in
    srp_top)       make -C tb/srp_top mutants MUTANT_OUTPUT="$w" ;;
    srp_admission) python3 tb/srp_admission/mutants.py --output "$w" ;;
    maap)          make -C tb/maap mutants MUTANT_OUTPUT="$w" ;;
    adp)           make -C tb/adp_engine mutants MUTANT_OUTPUT="$w" ;;
    aecp)          make -C tb/pp_top aecp-mutants MUTANT_OUTPUT="$w" ;;
    dispatch)      make -C tb/pp_top aecp-dispatch-mutants AECP_DISPATCH_MUTANT_OUTPUT="$w" VERILATOR="$VERILATOR" ;;
    ctr)           make -C tb/pp_top ctr-mutants CTR_MUTANT_OUTPUT="$w" ;;
    acmp)          python3 tb/pp_top/acmp_mutants.py --output "$w" --verilator "$VERILATOR" ;;
    gsi)           python3 tb/pp_top/gsi_mutants.py --output "$w" --verilator "$VERILATOR" ;;
    name_wr)       python3 tb/pp_top/name_wr_mutant.py --output "$w" ;;
    notify)        python3 tb/pp_top/notify_mutants.py --output "$w" --verilator "$VERILATOR" ;;
    name_state)    make -C tb/name_state mutants OUTPUT="$w" VERILATOR="$VERILATOR" ;;
    elab_mutants)  make -C tb/elab_guards mutants MUTANT_OUTPUT="$w" VERILATOR="$VERILATOR" ;;
    d3)            python3 tb/pp_top/d3_mutants.py --output "$w" --verilator "$VERILATOR" ;;
    *) echo "unknown campaign $name"; return 2 ;;
  esac
}
runone() {
  local name=$1 t0=$(date +%s)
  camp "$name" > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
  echo $(( $(date +%s) - t0 )) > "$out/$name.sec"
}
for c in "${all[@]}"; do
  while [ "$(jobs -rp | wc -l)" -ge "$par" ]; do wait -n; done
  runone "$c" &
done
wait
echo done > "$out/ALL.done"
