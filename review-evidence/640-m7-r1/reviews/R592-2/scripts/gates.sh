#!/bin/sh
# gates.sh REPO LOGDIR MDPY PY VERILATOR_BIN BASE
# Runs the documentation, source and lint gates the M7 diff touches, one log
# and one rc line per gate (LOGDIR/gates.tsv); nothing is piped.
REPO=$1; LOGDIR=$2; MDPY=$3; PY=$4; VBIN=$5; BASE=$6
VDIR=$(dirname "$VBIN")
cd "$REPO" || exit 2
out="$LOGDIR/gates.tsv"; : > "$out"
g() { name=$1; shift; "$@" > "$LOGDIR/gate_$name.log" 2>&1; printf '%s\t%s\t%s\n' "$name" "$?" "$*" >> "$out"; }
g docs_check        "$MDPY" scripts/docs_check.py
g docs_nogit        env GIT_DIR=/dev/null "$MDPY" scripts/docs_check.py
g em_dash           "$MDPY" scripts/check_em_dash.py --base "$BASE"
g doc_style         "$MDPY" scripts/check_doc_style.py
g toc_check         "$MDPY" scripts/gen_toc.py --check
g toc_anchors       "$MDPY" scripts/gen_toc.py --verify-anchors
g doc_paths         "$MDPY" scripts/check_doc_paths.py
g doc_map           "$MDPY" docs/DOC_MAP.gen.py --check
g module_matrix     "$MDPY" docs/traceability/gen_module_matrix.py --check
g gptp_docs         "$MDPY" scripts/check_gptp_docs.py
g gptp_docs_sub     "$MDPY" scripts/check_gptp_docs.py --with-submodule
g gptp_docs_self    "$MDPY" scripts/check_gptp_docs.py --selftest
g submodule_docs    "$MDPY" scripts/check_submodule_docs.py
g submodule_diagram "$MDPY" docs/diagrams/submodule_boundaries.gen.py --check
g timesync          "$MDPY" docs/diagrams/timesync_chain.gen.py --check
g diagram_pngs      "$MDPY" scripts/check_diagram_pngs.py
g feature_status    "$MDPY" scripts/check_feature_status.py
g sv_idiom          "$PY" scripts/check_sv_idiom.py
g cpp_idiom         "$PY" scripts/check_cpp_idiom.py
g py_idiom          "$PY" scripts/check_py_idiom.py
g hygiene           "$PY" scripts/check_hygiene.py --check
g test_evidence     "$PY" scripts/measure_test_evidence.py --check
g naming            "$PY" scripts/measure_naming.py --check
g fail_fast         "$PY" scripts/measure_fail_fast.py --check
g todo              "$PY" scripts/check_todo_ownership.py
g rtl_source_lists  "$PY" scripts/check_rtl_source_lists.py
g port_contracts    "$PY" scripts/check_port_contracts.py
g resource_baseline "$PY" syn/ooc/pp_resource_gate.py check-baseline
g lint              env PATH="$VDIR:$PATH" "$PY" scripts/lint_rtl.py --check
g gp_contract       env PATH="$VDIR:$PATH" make -C gptp-processor contract
g gp_lint           env PATH="$VDIR:$PATH" make -C gptp-processor lint
g diff_base         git diff --check "$BASE" HEAD
