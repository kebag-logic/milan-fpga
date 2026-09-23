#!/usr/bin/env bash
# The repository's own documentation gates, run read-only at the reviewed head.
# usage: gates.sh CLONE_AT_HEAD OUTDIR BASE_SHA
set -uo pipefail
export PYTHONDONTWRITEBYTECODE=1
clone=$1 out=$(mkdir -p "$2" && cd "$2" && pwd) base=$3
cd "$clone"
: > "$out/SUMMARY.txt"
{ git --version; python3 --version; python3 -c 'import yaml;print("pyyaml",yaml.__version__)'; } >> "$out/SUMMARY.txt" 2>&1
run() { n=$1; shift; timeout 600 "$@" > "$out/$n.log" 2>&1; echo "$n rc=$?" >> "$out/SUMMARY.txt"; }
run docs_check python3 scripts/docs_check.py
run em_dash python3 scripts/check_em_dash.py --base "$base"
run baremetal_check python3 scripts/check_baremetal_only.py --check
run doc_style python3 scripts/check_doc_style.py
run gptp_docs python3 scripts/check_gptp_docs.py
run feature_status python3 scripts/check_feature_status.py
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run toc_check python3 scripts/gen_toc.py --check
cat "$out/SUMMARY.txt"
