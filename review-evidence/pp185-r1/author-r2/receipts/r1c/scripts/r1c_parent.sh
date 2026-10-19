#!/usr/bin/env bash
# usage: r1c_parent.sh <pass> <submodule-sha> <wait-file...>   round 1c parent pass on the
# committed local scratch parent: wait for every file, check the gitlink is committed at
# the sha and the submodule checked out there, clean both trees' ignored products, record
# the parent's commits and the two patches, run the consumer gates
S=<data>/tmp/pp185-a647; P="$S/parent"; PP="$P/protocol-processor"
M=<home>/milan-fpga-management/2026-09-23
pass="$1"; sha="$2"; R="$S/r1c/parent-$pass"; mkdir -p "$R"
shift 2; for f in "$@"; do while [ ! -e "$f" ]; do timeout 30 tail -f /dev/null; done; done
[ "$(git -C "$PP" rev-parse --show-toplevel)" = "$PP" ] || { echo "submodule toplevel mismatch"; exit 1; }
[ "$(git -C "$PP" rev-parse HEAD)" = "$sha" ] || { echo "submodule not at $sha"; exit 1; }
[ "$(git -C "$P" rev-parse --show-toplevel)" = "$P" ] || { echo "parent toplevel mismatch"; exit 1; }
[ "$(git -C "$P" rev-parse HEAD:protocol-processor)" = "$sha" ] || { echo "gitlink not committed at $sha"; exit 1; }
git -C "$PP" clean -fdXq
[ "$(git -C "$P" rev-parse --show-toplevel)" = "$P" ] || exit 1
git -C "$P" clean -fdXq
git -C "$P" status --short > "$R/parent-status-before.txt"
git -C "$P" log --oneline e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f..HEAD > "$R/parent-log.txt"
git -C "$P" diff --stat e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f HEAD > "$R/parent-diff-stat-vs-dev.txt"
{ for p in "$M/pp178-a634/parent-evidence-classification.patch" "$M/pp176-a629/parent-adoption-milan_dp-67.patch"; do
    sha256sum "$p" | sed 's#  .*/#  #'
    git -C "$P" apply --check -R "$p" && echo "applied (apply --check -R passes)"
  done; } > "$R/parent-patches.txt" 2>&1
"$S/scripts/parent_gates.sh" "$R"
