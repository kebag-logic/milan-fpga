#!/usr/bin/env bash
# R632-5: the gates that need a git working tree, run inside scripts/sandbox.sh
# against the exact-head clone bound read-only, concurrently, one log and rc
# per gate. The documentation gates use the pinned Markdown renderer from a
# venv in packet scratch (tools/markdown/requirements.txt, --require-hashes).
# Usage: run_gates_git.sh PACKET CLONE ALTERNATES
set -uo pipefail
packet=$(realpath "$1"); clone=$(realpath "$2"); alternates=$3
venv=$packet/scratch/markdown
cd "$packet"
mkdir -p receipts/gates
hist() {  # name, then the command run inside the read-only clone
  local name=$1; shift
  ( SANDBOX_TREE_RO=1 SANDBOX_RO="$alternates:$venv" scripts/sandbox.sh "$clone" \
      env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0="$clone" \
      PYTHONDONTWRITEBYTECODE=1 "$@" > "receipts/gates/$name.log" 2>&1
    echo $? > "receipts/gates/$name.rc" ) &
}
py=$venv/bin/python
hist head-identity git rev-parse HEAD HEAD^{tree}
hist baremetal-check "$py" -I scripts/check_baremetal_only.py --check
hist doc-paths "$py" -I scripts/check_doc_paths.py
hist py-idiom "$py" -I scripts/check_py_idiom.py
hist py-idiom-selftest "$py" -I scripts/check_py_idiom.py --selftest
hist toc-check "$py" -I scripts/gen_toc.py --check
hist toc-anchors "$py" -I scripts/gen_toc.py --verify-anchors
hist docs-check-pinned "$py" -I scripts/docs_check.py
hist doc-style-git "$py" -I scripts/check_doc_style.py
hist em-dash "$py" -I scripts/check_em_dash.py --base dc4d06cb
hist diff-check git diff --check dc4d06cb ede700b00ef4d79566a6f108b11ce9bd4ad6beaa
wait
for rc in receipts/gates/*.rc; do printf '%s %s\n' "$(cat "$rc")" "$(basename "$rc" .rc)"; done
