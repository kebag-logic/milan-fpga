#!/usr/bin/env bash
# Identity: exact head/tree of the review clone, the pinned simulator (the same
# installation the same-head manager wrapper targets; the prescribed path is
# recorded as found or absent), toolchain versions, and the parent scripts'
# blob ids against the parent tree at 7eb3b0d4.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); C=${CLONE:-$REVIEWS/r334-2-pp120}
echo "clone HEAD: $(git -C $C rev-parse HEAD)"; echo "clone tree: $(git -C $C rev-parse HEAD^{tree})"
R=$HOME/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr
$PK/tools/verilator --version
sha256sum $R/bin/verilator_bin | sed "s#$HOME#\$HOME#"
for p in $VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator $VALIDATION_STORAGE/pp120-manager-83c84b19/pinned-tool-bin/verilator; do
  if [ -e "$p" ]; then echo "$p: present -> $($p --version)"; grep -o 'overlay/[0-9a-f]*' "$p" | head -1; else echo "$p: ABSENT"; fi
done
g++ --version | head -1; python3 --version
echo "parent scripts (git blob ids; parent tree 7eb3b0d4 lists the same ids):"
for f in $PK/scratch/parent-scripts/*.py; do echo "  $(git hash-object $f) $(basename $f)"; done
