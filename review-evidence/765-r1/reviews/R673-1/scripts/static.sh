#!/bin/bash
# static.sh TREE OUTDIR : the repository's lightweight static/docs gates on a clean tree at the head
T=$1; O=$2; mkdir -p "$O"; : > "$O/gates.tsv"
cd "$T" || exit 99
while read -r name args; do
  timeout 300 python3 scripts/$name.py $args > "$O/$name.log" 2>&1
  printf '%s\t%s\tpython3 scripts/%s.py %s\n' "$name" "$?" "$name" "$args" >> "$O/gates.tsv"
done <<'L'
lint_rtl --check
docs_check
check_doc_paths
measure_test_evidence --check
check_cpp_idiom
check_py_idiom
check_sv_idiom
check_port_contracts
check_em_dash --base 78ca9bdf1
L
cat "$O/gates.tsv"
