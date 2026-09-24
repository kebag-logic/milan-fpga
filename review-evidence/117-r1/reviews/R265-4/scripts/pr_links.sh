#!/usr/bin/env bash
# Every evidence-archive commit or tree a PR commit links, per commit and changed page.
# usage: pr_links.sh <repo>
set -euo pipefail
repo=$1
for c in c3eb95fa9ac86a3f20b45f94057d6c011127db08 0abf147f726721f4a323ee6a32095a02363fe2dc dfe6a587c6dc8e01eaceded4eb8e96d79e68a5ba; do
  echo "== commit $c"
  git -C "$repo" log -1 --format='msg: %s%n%b' "$c"
  for f in docs/findings/117_GPTP_SILICON_EVIDENCE.md docs/design/GM_LOSS_RECOVERY.md docs/findings/README.md; do
    if git -C "$repo" cat-file -e "$c:$f" 2>/dev/null; then
      echo "-- $f blob $(git -C "$repo" rev-parse "$c:$f")"
      git -C "$repo" show "$c:$f" | grep -n -o -E '(tree|commit|blob)/[0-9a-f]{7,40}|117-review-evidence' || true
    fi
  done
done
