#!/usr/bin/env bash
# In a disposable clone at the exact head, regenerate the submodule diagram
# (drawio, SVG, PNG and PNG_MANIFEST.json) with the repository generator in
# write mode, then require every generated file to be byte-identical to the
# committed blob (git status must stay clean and hashes must match HEAD).
set -eu
cd "${1:?disposable clone}"
F="docs/diagrams/submodule_boundaries.drawio docs/diagrams/submodule_boundaries.svg docs/diagrams/submodule_boundaries.png docs/diagrams/PNG_MANIFEST.json"
for f in $F; do echo "before $(sha256sum "$f")"; done
rm -f docs/diagrams/submodule_boundaries.drawio docs/diagrams/submodule_boundaries.svg docs/diagrams/submodule_boundaries.png
python3 docs/diagrams/submodule_boundaries.gen.py
for f in $F; do echo "after  $(sha256sum "$f")  head_blob=$(git rev-parse HEAD:$f) worktree_blob=$(git hash-object "$f")"; done
st=$(git status --porcelain -- docs/diagrams)
echo "status: ${st:-clean}"
[ -z "$st" ]
