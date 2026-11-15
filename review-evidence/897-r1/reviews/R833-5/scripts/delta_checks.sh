#!/usr/bin/env bash
# Delta checks of PR #898 round 5: the sync merge's conflict resolutions, the ledger commit against #901's, and the
# lane's own product-firmware hunks against round 3's.
# usage: delta_checks.sh CLONE OUTDIR
set -u
cd "$1" || exit 2
out=$2; mkdir -p "$out"
git show --remerge-diff --format='%H %s' b58a5430 > "$out/remerge-b58a5430.diff"
grep '^remerge CONFLICT' "$out/remerge-b58a5430.diff" > "$out/remerge-conflicts.txt"
grep -c '^-[<=>]\{7\}' "$out/remerge-b58a5430.diff" | sed 's/^/conflict-marker lines removed by the resolution (expected >0): /' >> "$out/remerge-conflicts.txt"
grep -c '^+[<=>]\{7\}' "$out/remerge-b58a5430.diff" | sed 's/^/conflict markers left in the resolution (expected 0): /' >> "$out/remerge-conflicts.txt"
{
  for f in sw/litex/ctrl_memory_ledger.py sw/litex/test_ctrl_memory.py sw/litex/ctrl_memory.py docs/design/SPLIT_CONTROL_MEMORY.md sw/firmware/ctrl/plat/README.md; do
    a=$(git diff 8238156d^ 8238156d -- "$f" | grep '^[-+][^-+]' | sha256sum | cut -c1-16)
    b=$(git diff 2170b22e^ 2170b22e -- "$f" | grep '^[-+][^-+]' | sha256sum | cut -c1-16)
    echo "$f: 8238156d own hunks $a, 2170b22e own hunks $b, $([ "$a" = "$b" ] && echo identical || echo differ)"
  done
  echo "ctrl_memory_ledger.py at 8238156d vs head:"; git diff 8238156d HEAD -- sw/litex/ctrl_memory_ledger.py | grep '^[-+][^-+]'
  echo "test_ctrl_memory.py at 8238156d vs head: $(git diff 8238156d HEAD -- sw/litex/test_ctrl_memory.py | wc -l) diff lines"
} > "$out/ledger-vs-8238156d.txt"
base=$(git merge-base f098f893 234bc149)
{
  echo "own-side hunks of the lane's product firmware, round 3 (${base:0:8}..f098f893) vs this head (234bc149..HEAD)"
  for f in $(git diff --name-only "$base" f098f893 -- sw/firmware hdl); do
    a=$(git diff "$base" f098f893 -- "$f" | grep '^[-+][^-+]' | sha256sum | cut -c1-16)
    b=$(git diff 234bc149 HEAD -- "$f" | grep '^[-+][^-+]' | sha256sum | cut -c1-16)
    echo "$f: $a $b $([ "$a" = "$b" ] && echo same || echo DIFFER)"
  done
  echo "hdl/ changed by the lane since 234bc149: $(git diff --name-only 234bc149 HEAD -- hdl | wc -l) file(s)"
} > "$out/own-side-firmware.txt"
git diff b58a5430 HEAD -- '*.py' '*.c' '*.h' '*.cpp' '*.sv' | grep '^+' | grep -v '^+++' \
  | grep -n -E "round [0-9]|round-[0-9]|\bR[0-9]{3}\b|issuecomment|[0-9]{10}|\blane\b|\bB[0-9]{2}\b|\bA[0-9]{3}\b|reviewer" \
  > "$out/comment-rule-scan.txt"; echo "comment-rule matches in added source lines since b58a5430: $(wc -l < "$out/comment-rule-scan.txt")" >> "$out/comment-rule-scan.txt"
cat "$out/remerge-conflicts.txt" "$out/ledger-vs-8238156d.txt" "$out/own-side-firmware.txt" | cut -c1-200
tail -1 "$out/comment-rule-scan.txt"
