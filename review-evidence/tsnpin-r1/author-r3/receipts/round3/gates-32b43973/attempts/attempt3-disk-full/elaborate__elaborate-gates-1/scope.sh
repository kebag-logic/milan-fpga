set -euo pipefail
# ci_scope.py arrives with PR #176. Until that lands this file may
# not exist, and the safe answer to "is this change RTL relevant"
# when the classifier is absent is yes.
if [ ! -f scripts/ci_scope.py ]; then
  echo "rtl=true" >> "$GITHUB_OUTPUT"
  echo "no scripts/ci_scope.py yet: elaborating unconditionally"
  exit 0
fi
python3 scripts/ci_scope.py --selftest
if [ "$EVENT_NAME" != pull_request ]; then
  echo "rtl=true" >> "$GITHUB_OUTPUT"
  exit 0
fi
if [ "${ACT:-false}" = true ]; then
  # Replay uses the live base fetched and verified by the runner.
  base="$(git merge-base --all "refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA")"
  git cat-file -e "$base^{commit}"
  merged="$(git merge-tree --write-tree "refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA")"
  git diff --no-renames --name-only "refs/remotes/origin/$PR_BASE_REF" "$merged" \
    > "$RUNNER_TEMP/changed"
else
  git diff --no-renames --name-only "$GITHUB_SHA^1" "$GITHUB_SHA" \
    > "$RUNNER_TEMP/changed"
fi
echo "rtl=$(python3 scripts/ci_scope.py < "$RUNNER_TEMP/changed")" >> "$GITHUB_OUTPUT"
