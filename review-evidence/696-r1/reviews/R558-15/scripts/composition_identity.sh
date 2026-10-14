#!/usr/bin/env bash
# Prove the candidate is the clean composition of dev and the PR source head.
# Usage: composition_identity.sh REPO DEV PR CAND
# Prints one line per changed path naming the side whose blob and mode the
# candidate carries; exits 1 on any path that equals neither side.
set -euo pipefail
REPO=$1 DEV=$2 PR=$3 CAND=$4
g() { git -C "$REPO" "$@"; }
MB=$(g merge-base "$DEV" "$PR")
echo "merge-base $MB"
echo "merge-tree $(g merge-tree --write-tree "$DEV" "$PR" | head -n 1)"
echo "cand-tree  $(g rev-parse "$CAND^{tree}")"
echo "parents    $(g rev-parse "$CAND^1") $(g rev-parse "$CAND^2")"
entry() { g ls-tree "$1" -- "$2" | awk '{print $1, $3}'; }
rc=0
for p in $( { g diff --name-only "$MB" "$DEV"; g diff --name-only "$MB" "$PR"; } | sort -u); do
  c=$(entry "$CAND" "$p"); d=$(entry "$DEV" "$p"); s=$(entry "$PR" "$p"); b=$(entry "$MB" "$p")
  side=neither
  if [ "$c" = "$d" ] && [ "$c" = "$s" ]; then side=both
  elif [ "$c" = "$d" ] && [ "$s" = "$b" ]; then side=dev
  elif [ "$c" = "$s" ] && [ "$d" = "$b" ]; then side=pr
  elif [ "$d" != "$b" ] && [ "$s" != "$b" ]; then side=both-changed
  fi
  printf '%-14s %s %s\n' "$side" "${c:-absent}" "$p"
  case $side in neither) rc=1;; esac
done
exit $rc
