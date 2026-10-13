#!/usr/bin/env bash
# R632-5: the repository gates for the files PR #731 touches, at the exact head,
# each inside scripts/sandbox.sh, concurrently, one log and rc per gate.
# Usage: run_gates.sh PACKET CLONE ALTERNATES
#   PACKET/scratch/pristine holds `git archive` of the exact head (tree gates);
#   CLONE is the exact-head clone (history gates, bound read-only);
#   ALTERNATES is the clone's alternate object store (bound read-only).
set -uo pipefail
packet=$(realpath "$1"); clone=$(realpath "$2"); alternates=$3
cd "$packet"
mkdir -p receipts/gates scratch/gates
rm -rf scratch/gates/tree; cp -r scratch/pristine scratch/gates/tree
tree=scratch/gates/tree
gate() {  # name, then the command run inside the tree
  local name=$1; shift
  ( scripts/sandbox.sh "$tree" "$@" > "receipts/gates/$name.log" 2>&1
    echo $? > "receipts/gates/$name.rc" ) &
}
hist() {  # name, then the command run inside the read-only clone
  local name=$1; shift
  ( SANDBOX_TREE_RO=1 SANDBOX_RO="$alternates" scripts/sandbox.sh "$clone" \
      env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0="$clone" "$@" \
      > "receipts/gates/$name.log" 2>&1
    echo $? > "receipts/gates/$name.rc" ) &
}
gate ci-events-check python3 -I scripts/ci_events.py --check
gate ci-events-selftest python3 -I scripts/ci_events.py --selftest
gate slot-proof-selftest bash scripts/act_slot_proof.sh --selftest
gate py-idiom python3 -I scripts/check_py_idiom.py
gate py-idiom-selftest python3 -I scripts/check_py_idiom.py --selftest
gate baremetal-check python3 -I scripts/check_baremetal_only.py --check
gate baremetal-selftest python3 -I scripts/check_baremetal_only.py --selftest
gate docs-check python3 -I scripts/docs_check.py
gate doc-style python3 -I scripts/check_doc_style.py
gate toc-check python3 -I scripts/gen_toc.py --check
gate toc-anchors python3 -I scripts/gen_toc.py --verify-anchors
gate doc-paths python3 -I scripts/check_doc_paths.py
hist em-dash python3 -I scripts/check_em_dash.py --base dc4d06cb
hist diff-check git diff --check dc4d06cb ede700b00ef4d79566a6f108b11ce9bd4ad6beaa
wait
for rc in receipts/gates/*.rc; do printf '%s %s\n' "$(cat "$rc")" "$(basename "$rc" .rc)"; done
