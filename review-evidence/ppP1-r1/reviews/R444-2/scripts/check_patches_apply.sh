#!/usr/bin/env bash
# git apply --check every tracked mutation patch against a clean worktree of the
# given commit (a disposable clone), recording which patches touch the files
# round 2 changed. Usage: check_patches_apply.sh REPO COMMIT WORKDIR
set -uo pipefail
repo=$1; commit=$2; work=$3
rm -rf "$work"; git clone -q --no-hardlinks "$repo" "$work" && git -C "$work" checkout -q --detach "$commit"
cd "$work" || exit 2
ok=0; bad=0; touch_changed=0
for p in $(git ls-files | grep -E '\.(patch|diff)$'); do
  if git apply --check "$p" 2>/dev/null; then ok=$((ok+1)); else
    # some drivers apply patches from the suite directory: try that too
    d=$(dirname "$(dirname "$p")")
    if (cd "$d" && git apply --check "$(basename "$(dirname "$p")")/$(basename "$p")" 2>/dev/null); then ok=$((ok+1));
    else echo "DOES NOT APPLY: $p"; bad=$((bad+1)); fi
  fi
  grep -qE '^\+\+\+ .*(protocol_processor_top|KL_aecp_engine|KL_aecp_nvm_writer)\.sv' "$p" && touch_changed=$((touch_changed+1))
done
echo "commit $commit: $ok apply, $bad do not, of $((ok+bad)); $touch_changed patch(es) target a file round 2 changed"
[ "$bad" -eq 0 ]
