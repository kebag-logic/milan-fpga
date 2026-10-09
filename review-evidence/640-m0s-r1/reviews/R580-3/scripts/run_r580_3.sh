#!/usr/bin/env bash
# R580-3 command record (portable).
# Usage: run_r580_3.sh <clone at 6904af6b> <packet> <r580-1 scripts> <r580-2 scripts> <python 3.12.3> <route-1x1 hierarchy report> <stage>
# Each command writes receipts/gates/<name>.log and .rc; stages run in order, jobs inside a stage concurrently (<= 16).
set -u
CLONE=$1 PACKET=$2 R1=$3 R2=$4 PY312=$5 REPORT=$6 STAGE=$7
PYH=$(command -v python3)
export TMPDIR=$PACKET/scratch/tmp PYTHONDONTWRITEBYTECODE=1
G=$PACKET/receipts/gates; mkdir -p "$G" "$TMPDIR"
cd "$CLONE" || exit 9
job() { local n=$1; shift; ( "$@" > "$G/$n.log" 2>&1; echo $? > "$G/$n.rc" ) & }
case $STAGE in
1)
  for tag in py3123 host; do
    PY=$PY312; [ $tag = host ] && PY=$PYH
    job gate_selftest_$tag          "$PY" -B syn/ooc/pp_resource_gate.py --selftest
    job check_baseline_$tag         "$PY" -B syn/ooc/pp_resource_gate.py check-baseline
    job baseline_selftest_$tag      "$PY" -B syn/ooc/pp_baseline.py --selftest
    job reports_selftest_$tag       "$PY" -B syn/ooc/pp_baseline_reports_selftest.py
    job ooc_tcl_selftest_$tag       "$PY" -B syn/ooc/ooc_tcl_selftest.py
    job dp_srcs_$tag bash -c "'$PY' -B syn/ooc/dp_srcs.py --selftest && '$PY' -B syn/ooc/dp_srcs.py --top milan_datapath >/dev/null && '$PY' -B syn/ooc/dp_srcs.py --top KL_pp_shadow >/dev/null"
    job P4_default_population_$tag  "$PY" -I -B "$R2/probe_default_population.py" "$CLONE" "$PACKET/scratch/p4_$tag" "$REPORT"
    job P10_cli_order_$tag          "$PY" -I -B "$R2/probe_cli_order.py" "$CLONE" "$PACKET/scratch/p10_$tag"
  done; wait ;;
2) job gate_mutants_py3123 "$PY312" -B syn/ooc/pp_resource_gate_mutants.py; wait ;;
3) job gate_mutants_host "$PYH" -B -X cpu_count=16 syn/ooc/pp_resource_gate_mutants.py; wait ;;
4)
  job baseline_mutants_py3123 "$PY312" -B syn/ooc/pp_baseline_mutants.py
  job baseline_mutants_host   "$PYH" -B syn/ooc/pp_baseline_mutants.py
  job P1_probe_mutants_py3123 "$PY312" -I -B "$R1/probe_mutants.py" "$CLONE" "$PACKET/scratch/p1_py3123" 6
  job P1_probe_mutants_host   "$PYH" -I -B "$R1/probe_mutants.py" "$CLONE" "$PACKET/scratch/p1_host" 6
  wait ;;
5)
  job P11_order_plants_py3123 "$PY312" -I -B "$PACKET/scripts/probe_order_plants.py" "$CLONE" "$PACKET/scratch/p11_py3123" "$PY312" 6
  job P11_order_plants_host   "$PYH" -I -B "$PACKET/scripts/probe_order_plants.py" "$CLONE" "$PACKET/scratch/p11_host" "$PYH" 6
  # documentation and quality gates (host interpreter; the pinned Markdown environment first on PATH when present)
  job docs_check   python3 scripts/docs_check.py
  job gen_toc      python3 scripts/gen_toc.py --check
  job toc_anchors  python3 scripts/gen_toc.py --verify-anchors
  job em_dash      python3 scripts/check_em_dash.py --base 7c1b52bee26b497080ee22b1c1986109f80a5ee7
  job py_idiom     python3 scripts/check_py_idiom.py
  for s in check_hygiene measure_fail_fast measure_naming measure_test_evidence; do job $s python3 scripts/$s.py --check; done
  git diff --check 7c1b52bee26b497080ee22b1c1986109f80a5ee7 HEAD > "$G/diff_check.log" 2>&1; echo $? > "$G/diff_check.rc"
  wait ;;
esac
