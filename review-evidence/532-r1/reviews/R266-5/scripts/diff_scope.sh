#!/usr/bin/env bash
# Candidate composition scope: PR delta on the train parent vs the source PR delta,
# and every PR file a predecessor (dev + train) also changed.
set -euo pipefail
cd "$1"
B=7ddbbdc9be73728b239718c8976261c7e0ad0563   # candidate first parent (dev + queued train)
S=022290e4c94a23b9ee97852b6c1c2ee2c1f25352   # reviewed source head
H=b74fb11162fba8f019110d9f2c21492300857da2   # candidate
MB=$(git merge-base "$S" "$B")
echo "parents of H: $(git rev-parse "$H^1") $(git rev-parse "$H^2")"
echo "source merge-base with train parent: $MB"
echo "PR files on candidate (B..H):"; git diff --name-only "$B" "$H"
echo "PR files at source (MB..S):"; git diff --name-only "$MB" "$S"
echo "patch-id MB..S: $(git diff "$MB" "$S" | git patch-id --stable | cut -d' ' -f1)"
echo "patch-id B..H:  $(git diff "$B" "$H" | git patch-id --stable | cut -d' ' -f1)"
echo "PR files a predecessor also changed (MB..B):"
git diff --name-only "$MB" "$B" -- $(git diff --name-only "$B" "$H")
echo "predecessor commits on those files:"; git log --oneline "$MB..$B" -- $(git diff --name-only "$B" "$H")
echo "hunk headers, PR on candidate:"; git diff -U0 "$B" "$H" -- docs/testing/CI_WORKFLOWS.md | grep '^@@'
echo "hunk headers, predecessors:"; git diff -U0 "$MB" "$B" -- docs/testing/CI_WORKFLOWS.md | grep '^@@'
echo "predecessor gate/workflow files changed (MB..B):"; git diff --stat=150 "$MB" "$B" -- scripts .github tools CONTRIBUTING.md AGENTS.md | cat
