#!/usr/bin/env bash
# R580-2 command record (portable). Usage: run_r580_2.sh <clone at d10aee62> <packet> <r580-1 scripts dir> <python 3.12.3>
# Each gate writes receipts/gates/<name>.log and .rc; probes write receipts/probes/.
set -u
CLONE=$1 PACKET=$2 R1=$3 PY3123=$4
export TMPDIR=$PACKET/scratch/tmp PYTHONDONTWRITEBYTECODE=1
G=$PACKET/receipts/gates; Q=$PACKET/receipts/probes; mkdir -p "$G" "$Q" "$TMPDIR"
cd "$CLONE" || exit 9
job() { local n=$1; shift; ( "$@" > "$G/$n.log" 2>&1; echo $? > "$G/$n.rc" ) & }
job baseline_selftest   python3 syn/ooc/pp_baseline.py --selftest
job baseline_mutants    python3 syn/ooc/pp_baseline_mutants.py
job gate_selftest       python3 syn/ooc/pp_resource_gate.py --selftest
job gate_mutants        python3 -X cpu_count=10 syn/ooc/pp_resource_gate_mutants.py
job check_baseline      python3 syn/ooc/pp_resource_gate.py check-baseline
job reports_selftest    python3 syn/ooc/pp_baseline_reports_selftest.py
job ooc_tcl_selftest    python3 syn/ooc/ooc_tcl_selftest.py
wait
# documentation and quality gates use the pinned Markdown venv first on PATH
job docs_check          python3 scripts/docs_check.py
job gen_toc             python3 scripts/gen_toc.py --check
job toc_anchors         python3 scripts/gen_toc.py --verify-anchors
job em_dash             python3 scripts/check_em_dash.py --base 7c1b52bee26b497080ee22b1c1986109f80a5ee7
job py_idiom            python3 scripts/check_py_idiom.py
job pp_srcs             python3 scripts/pp_srcs.py --check --selftest
job docs_style          bash -c 'python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest && python3 scripts/check_doc_paths.py && python3 docs/DOC_MAP.gen.py --check && python3 scripts/check_feature_status.py --self-test && python3 docs/traceability/gen_module_matrix.py --check'
job dp_srcs             bash -c 'python3 syn/ooc/dp_srcs.py --selftest && python3 syn/ooc/dp_srcs.py --top milan_datapath >/dev/null && python3 syn/ooc/dp_srcs.py --top KL_pp_shadow >/dev/null'
for s in check_hygiene measure_fail_fast measure_naming measure_test_evidence; do job $s python3 scripts/$s.py --check; done
git diff --check 7c1b52bee26b497080ee22b1c1986109f80a5ee7 HEAD > "$G/diff_check.log" 2>&1; echo $? > "$G/diff_check.rc"
wait
# prior-round probes, unmodified (sha256 equal to the R580-1 manifest)
python3 -I -B "$R1/probe_mutants.py" "$CLONE" "$PACKET/scratch/p1" 12 > "$Q/P1_probe_mutants.log" 2>&1; echo $? > "$Q/P1_probe_mutants.rc"
python3 -I -B "$R1/probe_parity.py" "$CLONE" 7c1b52bee26b497080ee22b1c1986109f80a5ee7 "$PACKET/scratch/p2" > "$Q/P2_probe_parity.log" 2>&1; echo $? > "$Q/P2_probe_parity.rc"
python3 -I -B "$R1/probe_marker.py" "$CLONE" "$PACKET/scratch/p3" > "$Q/P3_probe_marker.log" 2>&1; echo $? > "$Q/P3_probe_marker.rc"
# this round's probes (see each script's docstring); P4 takes a published post-route hierarchy report
python3 -I -B "$PACKET/scripts/probe_default_population.py" "$CLONE" "$PACKET/scratch/p4" "<route-1x1 baseline_hierarchy.rpt>"
python3 -I -B "$PACKET/scripts/probe_population_mutants.py" "$CLONE" "$PACKET/scratch/p8" 8
# hosted-interpreter reproduction
(cd "$CLONE" && "$PY3123" -B syn/ooc/pp_resource_gate.py --selftest)
(cd "$CLONE" && "$PY3123" -B -X cpu_count=12 syn/ooc/pp_resource_gate_mutants.py)
"$PY3123" -I -B "$PACKET/scripts/probe_cli_order.py" "$CLONE" "$PACKET/scratch/p10"
