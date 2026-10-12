#!/usr/bin/env bash
# Second pass for gates the first pass could not host: PyYAML gates with the
# system interpreter on the git copy, the Python idiom gate read-only on the
# review clone itself (its pinned submodules are initialized there; git
# alternates bound read-only), and git diff --check with host git.
# Usage: run_gates_r2.sh PACKET CLONE ALTERNATES
set -u
P=$1; CLONE=$2; ALT=$3
COPY=$P/scratch/gitcopy
G=$P/receipts/gates; SB=$P/scripts/sandbox.sh
run() { local name=$1; shift; ( "$SB" "$COPY" "$@" > "$G/$name.log" 2>&1; echo $? > "$G/$name.rc" ) & }
runclone() { local name=$1; shift; ( SANDBOX_TREE_RO=1 SANDBOX_RO="$ALT" "$SB" "$CLONE" "$@" > "$G/$name.log" 2>&1; echo $? > "$G/$name.rc" ) & }
run ci-events-check /usr/bin/python3 scripts/ci_events.py --check
run ci-events-selftest /usr/bin/python3 scripts/ci_events.py --selftest
run baremetal-check /usr/bin/python3 scripts/check_baremetal_only.py --check
run baremetal-selftest /usr/bin/python3 scripts/check_baremetal_only.py --selftest
runclone py-idiom /usr/bin/python3 -B scripts/check_py_idiom.py
runclone py-idiom-selftest /usr/bin/python3 -B scripts/check_py_idiom.py --selftest
( git -C "$CLONE" diff --check dc4d06cb HEAD > "$G/diff-check.log" 2>&1; echo $? > "$G/diff-check.rc" ) &
wait
for f in "$G"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f") | $(tail -1 "${f%.rc}.log" | cut -c1-140)"; done
