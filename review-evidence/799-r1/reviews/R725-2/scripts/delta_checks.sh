#!/usr/bin/env bash
# Reproduce the R725-2 delta checks at a checkout of the reviewed head.
# Usage: delta_checks.sh <checkout> <receipt-dir>
# Needs sv2v v0.0.12 in $SV2V and Yosys 0.66 in $YOSYS (the rtl-fast pins),
# and a Python with the pinned Markdown renderer in $MD_PYTHON for the em-dash gate.
set -euo pipefail
repo=$(cd "$1" && pwd)
out=$(mkdir -p "$2" && cd "$2" && pwd)
cd "$repo"
: "${SV2V:?set SV2V to the pinned sv2v}" "${YOSYS:?set YOSYS to the pinned yosys}"
export SV2V YOSYS
run() { local n=$1; shift; ( set +e; "$@" > "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" ) & }
run census_check python3 -I sw/mailbox/publication_census.py --check --jobs 6
run census_list python3 -I sw/mailbox/publication_census.py --list
run gen_mailbox_check python3 -I sw/mailbox/gen_mailbox.py --check
run doc_style python3 -I scripts/check_doc_style.py
run doc_paths python3 -I scripts/check_doc_paths.py
run hygiene python3 -I scripts/check_hygiene.py --check
run doc_map python3 -I docs/DOC_MAP.gen.py --check
run todo_owner python3 -I scripts/check_todo_ownership.py
if [ -n "${MD_PYTHON:-}" ]; then run em_dash "$MD_PYTHON" -I scripts/check_em_dash.py --base ca39dc1b; fi
wait
# The census listing's reads by kind (the page states 11 field, 14 status, 16 processor).
python3 -I - "$out/census_list.log" > "$out/kind_counts.txt" <<'EOF'
import collections, re, sys
c = collections.Counter()
for line in open(sys.argv[1]):
    m = re.match(r'^(pp_\w+)\s+->\s+(\S+)\s+reaches\s+([a-z, ]+?)\s{2,}(field|status|processor)\b', line)
    if m:
        c[m.group(4)] += 1
print(dict(c), sum(c.values()))
EOF
# Rules and plants the page states (31 rules; 116 plants plus 2 table plants).
python3 -I -c "import sys; sys.path.insert(0, 'sw/mailbox'); import census_rules as r, census_plants as p; print('rules', len(r.RULES), 'plants', len(p.PLANTS))" > "$out/rule_plant_counts.txt"
for f in "$out"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
cat "$out/kind_counts.txt" "$out/rule_plant_counts.txt"
