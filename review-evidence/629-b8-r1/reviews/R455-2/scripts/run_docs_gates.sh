#!/usr/bin/env bash
# usage: run_docs_gates.sh REPO OUTDIR BASE VENV_PYTHON
# Runs the docs gates concurrently; each writes OUTDIR/<gate>.log and .rc.
set -u
R=$1; G=$2; B=$3; VP=$4
mkdir -p "$G"; cd "$R" || exit 2
run() { n=$1; shift; "$@" > "$G/$n.log" 2>&1; echo $? > "$G/$n.rc"; }
run docs_check python3 scripts/docs_check.py &
run check_doc_style python3 scripts/check_doc_style.py &
run check_doc_paths python3 scripts/check_doc_paths.py &
run check_em_dash python3 scripts/check_em_dash.py --base "$B" &
run gen_toc_check "$VP" scripts/gen_toc.py --check &
run check_feature_status python3 scripts/check_feature_status.py &
run diff_check git diff --check "$B"..HEAD &
wait
for f in "$G"/*.rc; do n=$(basename "$f" .rc); echo "$n rc=$(cat "$f") :: $(tail -1 "$G/$n.log" | cut -c1-160)"; done
