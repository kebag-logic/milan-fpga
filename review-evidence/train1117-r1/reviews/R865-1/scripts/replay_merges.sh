#!/bin/bash
# Replay each first-parent merge of the train with git merge-tree (no checkout, no ref change) and report, per merge:
# the files git leaves conflicted, the files both sides changed from the merge base (auto-merged or conflicted),
# which of those are RTL (hdl/, *.sv, *.v) or firmware C, and the files where the recorded merge differs from the
# replayed clean side (its resolution). usage: replay_merges.sh <repo> <base> <head>
repo=$1; base=$2; head=$3
cd "$repo" || exit 99
for m in $(git rev-list --merges --first-parent --reverse "$head" ^"$base"); do
  p1=$(git rev-parse "$m^1"); p2=$(git rev-parse "$m^2"); mb=$(git merge-base "$p1" "$p2")
  out=$(git merge-tree --write-tree --name-only --no-messages "$p1" "$p2")
  tree=$(echo "$out" | head -1); conflicted=$(echo "$out" | tail -n +2 | grep -v '^$' | sort -u)
  both=$(comm -12 <(git diff --name-only "$mb" "$p1" | sort) <(git diff --name-only "$mb" "$p2" | sort))
  resolved=$(git diff --name-only "$tree" "$m" | sort -u)
  echo "== $(git log -1 --format='%h %s' "$m" | cut -c1-90)"
  echo "   parents ${p1:0:8} ${p2:0:8} base ${mb:0:8}; conflicted $(echo "$conflicted" | grep -c .); both-sides $(echo "$both" | grep -c .); recorded differs from replay in $(echo "$resolved" | grep -c .)"
  echo "$both" | grep -E '(^hdl/|\.sv$|\.v$)' | sed 's/^/   both-sides RTL: /'
  echo "$conflicted" | grep -E '(^hdl/|\.sv$|\.v$|\.c$|\.h$)' | sed 's/^/   conflicted RTL\/C: /'
  comm -13 <(echo "$conflicted") <(echo "$resolved") | grep . | sed 's/^/   resolved without a conflict: /'
done
