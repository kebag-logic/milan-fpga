#!/usr/bin/env bash
# rtl-fast static gates and a few repository checks from the clean candidate clone; one log and rc per gate.
set -u
root=$SCRATCH
out=$root/static
rm -rf "$out"; mkdir -p "$out"
export PATH=$root/bin5050:$root/venv312/bin:$PATH TMPDIR=$root/tmp PYTHONDONTWRITEBYTECODE=1
cd $root/cand || exit 2
n=0
gate() {
  n=$((n + 1)); local name; name=$(printf '%02d' $n)
  echo "== $*" > "$out/$name.log"
  local t0=$SECONDS
  timeout 3600 bash -c "$*" >> "$out/$name.log" 2>&1
  printf '%s\trc=%s\t%ss\t%s\n' "$name" "$?" "$((SECONDS - t0))" "$*" >> "$out/summary.tsv"
}
: > "$out/summary.tsv"
gate git diff --check e8454e2751d05b02ee8e5a571857589ab358ab86 HEAD
gate 'python3 scripts/ci_scope.py $(git diff --no-renames --name-only e8454e2751d05b02ee8e5a571857589ab358ab86 HEAD)'
gate python3 scripts/ci_scope.py --selftest
gate verilator --version
gate python3 scripts/lint_rtl.py --check --self-test
gate python3 scripts/pp_srcs.py --check --selftest
gate syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
gate python3 syn/ooc/dp_srcs.py --selftest
gate python3 syn/ooc/ooc_tcl_selftest.py
gate python3 syn/ooc/pp_baseline.py --selftest
gate python3 syn/ooc/pp_baseline_mutants.py
gate python3 syn/ooc/pp_baseline_reports_selftest.py
gate python3 syn/ooc/pp_resource_gate.py --selftest
gate python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py
gate python3 syn/ooc/pp_resource_gate.py check-baseline
gate 'python3 syn/ooc/dp_srcs.py --top milan_datapath > /dev/null'
gate 'python3 syn/ooc/dp_srcs.py --top KL_pp_shadow > /dev/null'
gate python3 scripts/check_em_dash.py --selftest
gate python3 scripts/check_merge_review_integrity.py --selftest
echo "clean=$(git status --porcelain --untracked-files=all | wc -l)" >> "$out/summary.tsv"
echo done >> "$out/summary.tsv"
