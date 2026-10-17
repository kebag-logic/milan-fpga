#!/usr/bin/env bash
# Reproduce the R638-10 receipts for PR #738 at d7cb1f90af1b8c2f115f58281991f1c9626447f9.
# Usage: reproduce.sh CHECKOUT DEV_REPO OUT
#   CHECKOUT  clean clone at d7cb1f90 with submodules initialised (it is never modified)
#   DEV_REPO  any repository holding dev commits 4a9b5a2a and 1f6f2f57
#   OUT       receipt directory
# Needs: CPython 3.12.3 as PY, PyYAML 6.0.2 importable (PYTHONPATH), the pinned shfmt v3.11.0
# as CI_IMAGE_SHFMT, and GNU Make on PATH for the walker probe.
set -euo pipefail
CHECKOUT=$(realpath "$1"); DEV=$(realpath "$2"); OUT=$(realpath -m "$3")
PY=${PY:-python3}
HERE=$(dirname "$(realpath "$0")")
mkdir -p "$OUT"
test "$(git -C "$CHECKOUT" rev-parse HEAD)" = d7cb1f90af1b8c2f115f58281991f1c9626447f9

# 1. Replay the dev merge and compare it with the committed merge commit.
tree=$(git -C "$CHECKOUT" merge-tree --write-tree 6f86eee604729b80684526fc5b9be720d94f179a \
  4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4 | head -1 || true)
git -C "$CHECKOUT" diff --stat "$tree" 03dcd0c36b9ef1a8aef98f20843f342b5296e357 > "$OUT/merge-replay.txt"

# 2. Generator checks at the head (read-only).
(cd "$CHECKOUT" && "$PY" scripts/ci_tool_inventory.py --check) > "$OUT/inventory-check.log" 2>&1
(cd "$CHECKOUT" && "$PY" scripts/ci_differential.py --check) > "$OUT/differential-check.log" 2>&1
work=$(mktemp -d)
(cd "$CHECKOUT" && "$PY" ci/image/build.py --work "$work" --check-lock) > "$OUT/check-lock.log" 2>&1

# 3. Make walker probes against the host's GNU Make.
(cd "$work" && "$PY" -I "$HERE/probe_make_walker.py" "$CHECKOUT" "$OUT/probe-make-walker.json" \
  "${PROBE_PYLIB:-}") > "$OUT/probe-make-walker.log" 2>&1

# 4. The live-dev candidate: the head plus dev 4a9b5a2a..1f6f2f57, in a disposable copy.
cand="$work/cand"
cp -a "$CHECKOUT" "$cand"
git -C "$cand" update-index -q --refresh
git -C "$DEV" diff --binary 4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4 \
  1f6f2f57177f1dd904654c317009461b43423989 | git -C "$cand" apply --index
(cd "$cand" && "$PY" scripts/ci_tool_inventory.py --check; echo "rc=$?") > "$OUT/candidate-inventory-check.log" 2>&1 || true
echo "receipts in $OUT"
