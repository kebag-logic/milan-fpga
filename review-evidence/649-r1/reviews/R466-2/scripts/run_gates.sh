#!/bin/sh
# R466-2: the resmap self-tests and the docs gates the diff touches, each with its own log
# and rc file. Usage: run_gates.sh <clone at the head> <out dir> <python with the pinned renderer>
set -u
cd "$1" || exit 2
OUT=$2; VPY=$3
mkdir -p "$OUT"
gate() { name=$1; shift; "$@" >"$OUT/$name.log" 2>&1; echo $? >"$OUT/$name.rc"; }
gate map-selftest python3 syn/resmap/resmap_map.py --selftest &
gate sweep-selftest python3 syn/resmap/yosys_sweep.py --selftest &
gate soc-selftest python3 syn/resmap/soc_sweep.py --selftest &
gate models-selftest python3 syn/resmap/resmap_models.py --selftest &
gate tables-selftest python3 syn/resmap/resmap_tables.py --selftest &
gate docs-check python3 scripts/docs_check.py &
gate doc-paths python3 scripts/check_doc_paths.py &
gate toc-check "$VPY" scripts/gen_toc.py --check &
gate toc-anchors "$VPY" scripts/gen_toc.py --verify-anchors &
gate em-dash-base "$VPY" scripts/check_em_dash.py --base 241f91845230ae410506dffb16b71937127fd175 &
gate em-dash-dev "$VPY" scripts/check_em_dash.py --base fea346e76c2a57ed5cd131af8fc68dfeff57f877 &
gate py-idiom python3 scripts/check_py_idiom.py &
gate diff-check-base git diff --check 241f91845230ae410506dffb16b71937127fd175 HEAD &
gate diff-check-dev git diff --check fea346e76c2a57ed5cd131af8fc68dfeff57f877 HEAD &
wait
for f in "$OUT"/*.rc; do printf '%s rc=%s | %s\n' "$(basename "$f" .rc)" "$(cat "$f")" "$(tail -n 1 "${f%.rc}.log")"; done
