#!/usr/bin/env bash
# Reproduce the R725-3 delta checks at exact head 4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020.
# Usage: delta_checks.sh <clone-at-head> <receipts-dir>
# Needs: python3 with pyyaml, Yosys 0.66 on PATH, SV2V pointing at sv2v v0.0.12
# (the rtl-fast pin), MDPY pointing at the pinned Markdown renderer's python, gh (read-only).
set -euo pipefail
C=${1:?clone}; R=${2:?receipts}; mkdir -p "$R"; cd "$C"
HEAD=4f3ebffbbb195bcee8f54bd0c57b40e0dbd4d020; PREV=f87da064d7d03063d8eb0b95a6559463a1bd2a3f
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "clone not at $HEAD" >&2; exit 2; }
: "${SV2V:?set SV2V to sv2v v0.0.12}"; : "${MDPY:=python3}"
export SV2V
g(){ n=$1; shift; ( "$@" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" ) & }
g census_check python3 sw/mailbox/publication_census.py --check --jobs 12
g gen_mailbox_check sh -c 'python3 sw/mailbox/gen_mailbox.py --check; echo "check rc=$?"; python3 sw/mailbox/gen_mailbox.py --crosscheck; echo "crosscheck rc=$?"'
g doc_style python3 scripts/check_doc_style.py
g doc_paths python3 scripts/check_doc_paths.py
g hygiene python3 scripts/check_hygiene.py --check
g doc_map python3 docs/DOC_MAP.gen.py --check
g todo_owner python3 scripts/check_todo_ownership.py
g em_dash "$MDPY" scripts/check_em_dash.py --base "$PREV"
wait
python3 sw/mailbox/publication_census.py --list --jobs 12 > "$R/census_list.log" 2>&1; echo $? > "$R/census_list.rc"
# Reads by kind: the last column is "processor", "status [field]" or "field <REG.FIELD>".
awk '/-> .*reaches/{k=($NF=="processor")?"processor":(($(NF-1)=="field")?"field":(($NF=="status"||$(NF-1)=="status")?"status":"other")); c[k]++; t++}
     END{for(k in c) print k, c[k]; print "total", t}' "$R/census_list.log" | sort > "$R/kind_counts.txt"
python3 -I -c "import ast;t=ast.parse(open('sw/mailbox/census_rules.py').read());print('rules',[len(n.value.keys) for n in t.body if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='RULES'][0])" > "$R/rule_count.txt"
# Comment lines over 79 columns in the contract source.
awk '/^#/ && length($0)>79 {print FILENAME":"NR": "length($0)}' sw/mailbox/mailbox.yaml > "$R/yaml_long_comment_lines.txt"
# Comment-rule scan of the delta's added lines.
git diff -U0 "$PREV"..HEAD | grep '^+[^+]' | grep -nE '\b[A-Z][0-9]{1,3}(-[0-9a-z]+)?\b|comment [0-9]{6,}|issuecomment|\[R[0-9]|\[A[0-9]|round' > "$R/comment_rule_scan.txt" || true
git diff "$PREV"..HEAD > "$R/delta.diff"
gh api --paginate "repos/kebag-logic/milan-fpga/commits/$HEAD/check-runs?per_page=100" \
  --jq '.check_runs[]|[.name,.status,(.conclusion//"-")]|@tsv' | sort > "$R/hosted_checks_4f3ebffb.tsv"
date -u +%FT%TZ >> "$R/hosted_checks_4f3ebffb.tsv"
for n in census_check census_list doc_style doc_paths hygiene doc_map todo_owner em_dash; do echo "$n rc=$(cat "$R/$n.rc")"; done
