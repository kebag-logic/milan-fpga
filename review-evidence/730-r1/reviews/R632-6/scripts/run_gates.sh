#!/usr/bin/env bash
# Run the PR's local gates on a disposable export of the head, each in the
# sandbox, concurrently; one log and rc per gate under OUT.
# Usage: run_gates.sh PACKET TREE OUT BASE_CLONE
set -uo pipefail
P=$1; T=$2; O=$3; CLONE=$4
mkdir -p "$O"
SB="$P/scripts/sandbox.sh"
MD=$VALIDATION_TOOLS/md-venv
run() { name=$1; shift; ( "$@" >"$O/$name.log" 2>&1; echo $? >"$O/$name.rc" ) & }
run act-ci-selftest "$SB" "$T" /usr/bin/python3 -I scripts/act_ci.py --selftest
run ci-events-check "$SB" "$T" /usr/bin/python3 scripts/ci_events.py --check
run ci-events-selftest "$SB" "$T" /usr/bin/python3 scripts/ci_events.py --selftest
run slot-proof-selftest "$SB" "$T" bash scripts/act_slot_proof.sh --selftest
run py-idiom "$SB" "$T" /usr/bin/python3 scripts/check_py_idiom.py
run py-idiom-selftest "$SB" "$T" /usr/bin/python3 scripts/check_py_idiom.py --selftest
run baremetal-check "$SB" "$T" /usr/bin/python3 scripts/check_baremetal_only.py --check
run baremetal-selftest "$SB" "$T" /usr/bin/python3 scripts/check_baremetal_only.py --selftest
SANDBOX_RO=$MD run docs-check "$SB" "$T" $MD/bin/python scripts/docs_check.py
SANDBOX_RO=$MD run doc-style "$SB" "$T" $MD/bin/python scripts/check_doc_style.py
SANDBOX_RO=$MD run toc-check "$SB" "$T" $MD/bin/python scripts/gen_toc.py --check
SANDBOX_RO=$MD run toc-anchors "$SB" "$T" $MD/bin/python scripts/gen_toc.py --verify-anchors
SANDBOX_RO=$MD run doc-paths "$SB" "$T" $MD/bin/python scripts/check_doc_paths.py
wait
