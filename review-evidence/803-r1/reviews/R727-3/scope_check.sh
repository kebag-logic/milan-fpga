#!/usr/bin/env bash
# Classify every path that differs between base B, PR-side P, dev-side D and head H.
# Usage: scope_check.sh <repo> <B> <P> <D> <H>
set -u
cd "$1" || exit 2
B=$2 P=$3 D=$4 H=$5
blob() { git rev-parse -q --verify "$1:$2" 2>/dev/null || echo absent; }
{ git diff --name-only "$B" "$P"; git diff --name-only "$B" "$D"; git diff --name-only "$D" "$H"; } | sort -u |
while read -r f; do
  b=$(blob "$B" "$f") p=$(blob "$P" "$f") d=$(blob "$D" "$f") h=$(blob "$H" "$f")
  if [ "$p" = "$b" ] && [ "$d" = "$b" ]; then c="UNEXPECTED(neither side changed, head differs)"; [ "$h" = "$b" ] && c=same
  elif [ "$p" = "$b" ]; then c=dev-only; [ "$h" = "$d" ] || c="DEV-ONLY-BUT-HEAD-DIFFERS"
  elif [ "$d" = "$b" ]; then c=pr-only; [ "$h" = "$p" ] || c="PR-ONLY-BUT-HEAD-DIFFERS"
  else c=both-changed; fi
  [ "$h" = "$d" ] && [ "$c" = both-changed ] && c="both-changed(head=dev)"
  [ "$h" = "$p" ] && [ "$c" = both-changed ] && c="both-changed(head=pr)"
  printf '%s\t%s\n' "$c" "$f"
done
