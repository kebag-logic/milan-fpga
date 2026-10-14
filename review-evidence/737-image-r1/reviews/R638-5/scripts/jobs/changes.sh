. /jobs/lib.sh
step "Classify the change (ACT pull_request path vs live dev)" 'python3 scripts/ci_scope.py --selftest
PR_BASE_REF=dev; PR_HEAD_SHA=4391f353690972f4844cb641b1e77fa94f38cdf4
base="$(git merge-base --all "refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA")"
git cat-file -e "$base^{commit}"
merged="$(git -c user.name=r -c user.email=r@invalid merge-tree --write-tree "refs/remotes/origin/$PR_BASE_REF" "$PR_HEAD_SHA")"
git diff --no-renames --name-only "refs/remotes/origin/$PR_BASE_REF" "$merged" > "$RUNNER_TEMP/changed-files"
sed "s/^/  /" "$RUNNER_TEMP/changed-files"
rtl="$(python3 scripts/ci_scope.py < "$RUNNER_TEMP/changed-files")"
echo "RTL/tooling relevant: $rtl"'
