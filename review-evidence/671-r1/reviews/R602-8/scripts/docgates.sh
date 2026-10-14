#!/bin/sh
# Usage: docgates.sh <repo-root> <receipt-dir>
# Doc and hygiene gates relevant to a doc + receipt delta, run concurrently.
set -u
REPO=$1; OUT=$2
mkdir -p "$OUT"
cd "$REPO" || exit 2
job() { name=$1; shift; ( "$@" >"$OUT/$name.log" 2>&1; echo $? >"$OUT/$name.rc" ) & }
job docs_check python3 scripts/docs_check.py
job doc_style python3 scripts/check_doc_style.py
job doc_paths python3 scripts/check_doc_paths.py
job em_dash python3 scripts/check_em_dash.py --base fa8209889411e8ca95757174c981f720dbcd95a2
job gen_toc_check python3 scripts/gen_toc.py --check
job hygiene python3 scripts/check_hygiene.py
job diffcheck_base sh -c 'git diff --check e8454e2751d05b02ee8e5a571857589ab358ab86 HEAD'
job diffcheck_dev sh -c 'git diff --check fa8209889411e8ca95757174c981f720dbcd95a2 HEAD'
job diffcheck_merge sh -c 'git diff --check f3bb2014d065141930ae1a473c966b419d1040aa HEAD'
wait
for f in "$OUT"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
