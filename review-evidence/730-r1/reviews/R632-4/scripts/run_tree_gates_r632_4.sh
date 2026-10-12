#!/usr/bin/env bash
# Run the gates that need git history, initialized submodules or the pinned
# Markdown renderer, each inside sandbox.sh with the review clone bound
# read-only. Usage: run_tree_gates_r632_4.sh PACKET CLONE ALTERNATES MDVENV
# One log and one rc file per gate under PACKET/receipts/gates/.
set -u
P=$1; CLONE=$2; ALT=$3; VENV=$4
G=$P/receipts/gates; mkdir -p "$G"
SB=$P/scripts/sandbox.sh
run() { local name=$1; shift; ( SANDBOX_TREE_RO=1 SANDBOX_RO="$ALT:$VENV" "$SB" "$CLONE" env PATH="$VENV/bin:/usr/bin" "$@" > "$G/$name.log" 2>&1; echo $? > "$G/$name.rc" ) & }
run py-idiom python3 scripts/check_py_idiom.py
run py-idiom-selftest python3 scripts/check_py_idiom.py --selftest
run toc-check python3 scripts/gen_toc.py --check
run toc-anchors python3 scripts/gen_toc.py --verify-anchors
run em-dash python3 scripts/check_em_dash.py --base dc4d06cb
run diff-check git -c safe.directory='*' diff --check dc4d06cb HEAD
run docs-check-pinned python3 scripts/docs_check.py
wait
for f in py-idiom py-idiom-selftest toc-check toc-anchors em-dash diff-check docs-check-pinned; do echo "$f rc=$(cat "$G/$f.rc") | $(tail -1 "$G/$f.log" | cut -c1-160)"; done
