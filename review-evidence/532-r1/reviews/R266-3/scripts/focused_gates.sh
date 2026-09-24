#!/usr/bin/env bash
# focused_gates.sh: the docs, scope and idiom gates this round ran at the head, one line each.
# Run from the review clone; no gate here executes scripts/act_ci.py.
set -uo pipefail
run() { local rc=0; "$@" >"$OUT/$(echo "$*" | tr -c 'A-Za-z0-9._-' '_' | cut -c1-90).log" 2>&1 || rc=$?; echo "rc=$rc $*"; }
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_baremetal_only.py --selftest
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9
run python3 scripts/check_em_dash.py --base ede8d48ecd7c7f589a14b957951f040d92c99c70
run python3 scripts/check_py_idiom.py
run python3 scripts/check_sh_idiom.py
run python3 scripts/gen_toc.py --check
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/check_doc_paths.py
run python3 scripts/check_doc_style.py
run python3 scripts/ci_events.py --check
run python3 scripts/check_feature_status.py
run git diff --check 759da623072358afdb0e9d570a7b4b6a788492c9..HEAD
run git diff --check f5497170a2c444e01175683606310dbe7fbb2816..HEAD
run bash -n scripts/act_slot_proof.sh
