#!/usr/bin/env bash
# Run the documentation and resource-policy gate list at a repository head, each with its own log and rc.
# Usage: run_gates.sh <repo> <outdir> <python> <base-sha>
set -u
REPO=$1; OUT=$2; PY=$3; BASE=$4
mkdir -p "$OUT"
cat > "$OUT/commands.tsv" <<TSV
docs_check	$PY scripts/docs_check.py
docs_self	$PY scripts/docs_check.py --selftest
feature_status	$PY scripts/check_feature_status.py
feature_self	$PY scripts/check_feature_status.py --self-test
em_dash	$PY scripts/check_em_dash.py --base $BASE
em_dash_self	$PY scripts/check_em_dash.py --selftest
doc_style	$PY scripts/check_doc_style.py
doc_style_self	$PY scripts/check_doc_style.py --selftest
gptp_docs	$PY scripts/check_gptp_docs.py --with-submodule
gptp_docs_self	$PY scripts/check_gptp_docs.py --selftest
doc_map	$PY docs/DOC_MAP.gen.py --check
doc_map_self	$PY docs/DOC_MAP.gen.py --selftest
timesync	$PY docs/diagrams/timesync_chain.gen.py --check
timesync_self	$PY docs/diagrams/timesync_chain.gen.py --selftest
solution	$PY scripts/check_solution_docs.py
solution_self	$PY scripts/check_solution_docs.py --selftest
submodule_diagram	$PY docs/diagrams/submodule_boundaries.gen.py --check
submodule_diagram_self	$PY docs/diagrams/submodule_boundaries.gen.py --selftest
submodule_docs	$PY scripts/check_submodule_docs.py
submodule_docs_self	$PY scripts/check_submodule_docs.py --selftest
diagram_pngs	$PY scripts/check_diagram_pngs.py
diagram_pngs_self	$PY scripts/check_diagram_pngs.py --selftest
module_matrix	$PY docs/traceability/gen_module_matrix.py --check
baremetal	$PY scripts/check_baremetal_only.py --check
baremetal_self	$PY scripts/check_baremetal_only.py --selftest
doc_paths	$PY scripts/check_doc_paths.py
archive	$PY scripts/check_archive.py
archive_self	$PY scripts/check_archive.py --selftest
toc_self	$PY scripts/gen_toc.py --selftest
toc_anchors	$PY scripts/gen_toc.py --verify-anchors
toc_check	$PY scripts/gen_toc.py --check
todo	$PY scripts/check_todo_ownership.py
hygiene	$PY scripts/check_hygiene.py --check
wire	$PY scripts/check_wire_accountability.py --self-test
resource_baseline	$PY syn/ooc/pp_resource_gate.py check-baseline
resource_self	$PY syn/ooc/pp_resource_gate.py --selftest
resource_mutants	$PY syn/ooc/pp_resource_gate_mutants.py
ci_scope	$PY scripts/ci_scope.py --selftest
ci_events	$PY scripts/ci_events.py --check
wavedrom_self	$PY scripts/gen_wavedrom.py --selftest
wavedrom_axis	$PY scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
wavedrom_cdc	$PY scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
wavedrom_gptp	$PY scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
pp_sources	$PY scripts/pp_srcs.py --check --selftest
docs_nogit	env GIT_DIR=/dev/null $PY scripts/docs_check.py
diff_base	git diff --check $BASE HEAD
diff_tree	git diff --check
TSV
run_one() { name=$1; shift; (cd "$REPO" && bash -c "$*" >"$OUT/$name.log" 2>&1; echo $? >"$OUT/$name.rc"); }
export -f run_one; export REPO OUT
while IFS=$'\t' read -r n c; do printf '%s\0%s\0' "$n" "$c"; done < "$OUT/commands.tsv" | xargs -0 -n2 -P16 bash -c 'run_one "$0" "$1"'
# The gPTP submodule docs build runs alone, after the others.
run_one gptp_make "make -j16 -C gptp-processor docs"
for f in "$OUT"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done > "$OUT/summary.txt"
