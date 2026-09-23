#!/bin/sh
# Actual gPTP processor PR61/PR62 verdicts and the decision's patch hashes.
# A disposable bare repository under ../scratch borrows the lane submodule's
# objects read-only through objects/info/alternates; no checkout is made.
# Usage: actual_history.sh <label> <checker> [<checker> ...]
set -eu
here=$(cd "$(dirname "$0")" && pwd)
packet=$(dirname "$here")
label=$1
shift
objects=$LANES/423-retained-redundant-replay/.git/modules/gptp-processor/objects
work=$packet/scratch/actual-$label
rm -rf "$work"
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
git init -q --bare "$work"
printf '%s\n' "$objects" > "$work/objects/info/alternates"
cd "$work"
git update-ref refs/heads/pr62 3db86812096830fada2f5f276fa5f4d9f37d1d14
git update-ref refs/heads/pr61 9790ac736e6d10301ad814ffdf73dbe37b59768b
git update-ref refs/heads/target-f0f1c055 f0f1c055ee5226f08e656c27cb1bf4c355be11ae
git update-ref refs/heads/target-c1b61743 c1b617435824929a790739ea8585c3fe1a328cc0
echo "## patch hashes: git diff --no-ext-diff --no-textconv --no-renames <parent> <commit> | sha256sum"
for pair in 7fa64e99490b4648797374d3fdb1fedf08145e91:9790ac736e6d10301ad814ffdf73dbe37b59768b \
            7fa64e99490b4648797374d3fdb1fedf08145e91:20927af74752620b2ad0f973e8be3203994b5547 \
            f27b45500cb02a5277b5cb32cef408658c1f914e:3db86812096830fada2f5f276fa5f4d9f37d1d14 \
            377b8c428b226a796adde099fe07152151fd6c5d:5602e70bb4cf70c2e0e39e846e26925e27659e32; do
  parent=${pair%%:*}
  commit=${pair##*:}
  printf '%s %s ' "$parent" "$commit"
  git diff --no-ext-diff --no-textconv --no-renames "$parent" "$commit" | sha256sum
done
for checker in "$@"; do
  for branch in pr62 pr61; do
    for target in target-f0f1c055 target-c1b61743; do
      echo "## $checker --no-fetch --base $target $branch"
      set +e
      python3 -B "$checker" --no-fetch --base "$target" "$branch"
      echo "rc=$?"
      set -e
    done
  done
done
cd "$packet"
rm -rf "$work"
