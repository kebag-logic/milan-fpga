set -euo pipefail
python3 scripts/ci_scope.py --selftest

if [ "$EVENT_NAME" = pull_request ]; then
  if [ "${ACT:-false}" = true ]; then
    # Replay uses the live base fetched and verified by the runner.
    base="$(git merge-base --all "refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA")"
    git cat-file -e "$base^{commit}"
    merged="$(git merge-tree --write-tree "refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA")"
    git diff --no-renames --name-only "refs/remotes/origin/$PR_BASE_REF" "$merged" \
      > "$RUNNER_TEMP/changed-files"
  else
    git diff --no-renames --name-only "$GITHUB_SHA^1" "$GITHUB_SHA" \
      > "$RUNNER_TEMP/changed-files"
  fi
else
  base="$PUSH_BEFORE_SHA"
  if [ -n "$base" ] \
     && [ "$base" != 0000000000000000000000000000000000000000 ] \
     && git cat-file -e "$base^{commit}" 2>/dev/null; then
    git diff --no-renames --name-only "$base" "$GITHUB_SHA" \
      > "$RUNNER_TEMP/changed-files"
  else
    # An unknown base must never turn a real change into docs-only.
    git ls-files > "$RUNNER_TEMP/changed-files"
  fi
fi

echo "Changed files:"
sed 's/^/  /' "$RUNNER_TEMP/changed-files"
rtl="$(python3 scripts/ci_scope.py < "$RUNNER_TEMP/changed-files")"
echo "rtl=$rtl" >> "$GITHUB_OUTPUT"
echo "RTL/tooling relevant: $rtl"
