#!/bin/sh
# [R383] Documentation/static gates at the review head (read-only on the clone).
# Usage: docs_gates.sh <clone> <python with the pinned markdown renderer>
cd "$1" || exit 2; md=$2
run() { out=$("$@" 2>&1); rc=$?; echo "rc=$rc $(echo "$out" | tail -1 | cut -c1-200) :: $*" | sed "s|$md|md-venv/python3|"; }
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_doc_paths.py
run "$md" -B scripts/gen_toc.py --check
run "$md" -B scripts/gen_toc.py --verify-anchors
run "$md" -B scripts/check_em_dash.py --base 54ce877371ee6e8878cf67294e86c2a8481b62f6
run python3 -B scripts/check_doc_style.py
run python3 -B scripts/check_baremetal_only.py --check
run python3 -B scripts/check_py_idiom.py
