#!/usr/bin/env bash
# Run the read-only checks of the docs workflow at a tree and print one rc
# line per check. usage: docs_gate_sweep.sh <tree> <python> <logdir>
set -u
tree=$1 py=$2 logs=$3
mkdir -p "$logs"
cd "$tree" || exit 2
while read -r name args; do
    [ -z "$name" ] && continue
    timeout 900 "$py" "scripts/$name" $args > "$logs/${name%.py}${args:+-${args//[^a-z]/}}.log" 2>&1
    echo "$name $args rc=$?"
done <<'EOF'
docs_inventory.py --check
check_py_idiom.py
check_cpp_idiom.py
check_sv_idiom.py
check_sh_idiom.py
check_feature_status.py
gen_register_reference.py --check
check_port_contracts.py
check_rtl_source_lists.py
check_hygiene.py --check
check_todo_ownership.py
check_solution_docs.py
check_doc_paths.py
check_submodule_docs.py
check_soc_sources.py
check_baremetal_only.py --check
check_archive.py
check_gptp_docs.py
check_diagram_pngs.py
ci_events.py --check
ci_gate_workflows.py --check
generate_ci_evidence_pins.py --check
EOF
