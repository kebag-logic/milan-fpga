#!/usr/bin/env bash
# Run the head's OOC/resource suites, builder bank and docs gates concurrently.
# Usage: run_gates.sh <repo> <packet>; each job writes receipts/<name>.log and .rc
set -u
REPO=$1
PACKET=$2
R=$PACKET/receipts/gates
mkdir -p "$R" "$PACKET/scratch/tmp"
export TMPDIR=$PACKET/scratch/tmp
export PYTHONDONTWRITEBYTECODE=1
export PATH=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
BASE=7c1b52bee26b497080ee22b1c1986109f80a5ee7
cd "$REPO" || exit 9

job() {  # name, command...
  local name=$1; shift
  ( start=$(date +%s); "$@" > "$R/$name.log" 2>&1; rc=$?
    echo "$rc" > "$R/$name.rc"; echo "$name rc=$rc $(( $(date +%s) - start ))s" ) &
}

job baseline_selftest        python3 syn/ooc/pp_baseline.py --selftest
job baseline_mutants         python3 syn/ooc/pp_baseline_mutants.py
job gate_selftest            python3 syn/ooc/pp_resource_gate.py --selftest
job gate_mutants             python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py
job gate_check_baseline      python3 syn/ooc/pp_resource_gate.py check-baseline
job reports_selftest         python3 syn/ooc/pp_baseline_reports_selftest.py
job ooc_tcl_selftest         python3 syn/ooc/ooc_tcl_selftest.py
job dp_srcs                  bash -c 'python3 syn/ooc/dp_srcs.py --selftest && python3 syn/ooc/dp_srcs.py --top milan_datapath >/dev/null && python3 syn/ooc/dp_srcs.py --top KL_pp_shadow >/dev/null'
job pp_srcs                  python3 scripts/pp_srcs.py --check --selftest
job builder_bank             env HOME=$PACKET/scratch/home python3 sw/builder/test_builder.py --require-rv32
job docs_check               python3 scripts/docs_check.py
job docs_style               bash -c 'python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest && python3 scripts/check_doc_paths.py && python3 docs/DOC_MAP.gen.py --check && python3 scripts/check_feature_status.py --self-test && python3 docs/traceability/gen_module_matrix.py --check'
job em_dash                  python3 scripts/check_em_dash.py --base $BASE
job toc                      bash -c 'python3 scripts/gen_toc.py --check && python3 scripts/gen_toc.py --verify-anchors'
job py_idiom                 python3 scripts/check_py_idiom.py
job diff_check               git diff --check $BASE HEAD
wait
echo ALL-DONE
