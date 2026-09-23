#!/usr/bin/env bash
# Record the composition facts of a merge-train candidate.
# Usage: composition_facts.sh <repo> <receipt-dir> [<candidate> [<merge-base>]]
# Defaults: candidate 18271beb..., whose first parent is live dev and second
# parent the PR head. Writes 01-06 and 10 receipts; read-only on <repo>.
set -euo pipefail
repo=$1
out=$2
cand=${3:-18271bebbd1a4abf2e32e7783477573114e2a5fa}
mkdir -p "$out"
g() { git -C "$repo" -c core.pager=cat -c color.ui=never "$@"; }
p1=$(g rev-parse "$cand^1")
p2=$(g rev-parse "$cand^2")
mb=${4:-$(g merge-base "$p1" "$p2")}

{
  echo "## topology"
  echo "candidate=$(g rev-parse "$cand") tree=$(g rev-parse "$cand^{tree}")"
  echo "P1(dev)=$p1 P2(pr)=$p2"
  echo "merge-base(P1,P2)=$mb"
  echo "all merge-bases:"; g merge-base --all "$p1" "$p2"
  echo "## dev commits not in PR (first-parent)"; g log --no-decorate --oneline --first-parent "$mb..$p1"
  echo "## PR commits not in dev"; g log --no-decorate --oneline "$mb..$p2"
} > "$out/01_topology.txt"

{
  echo "## PR side files (MB..P2)"; g diff --no-ext-diff --no-renames --name-status "$mb" "$p2"
  echo; echo "## dev side files (MB..P1)"; g diff --no-ext-diff --no-renames --name-status "$mb" "$p1"
  echo; echo "## per dev first-parent merge"
  for c in $(g rev-list --first-parent --reverse "$mb..$p1"); do
    echo "### $(g log -1 --no-decorate --oneline "$c")"
    g diff --no-ext-diff --no-renames --name-status "$c^1" "$c"
  done
  echo; echo "## intersection (paths changed on both sides)"
  comm -12 <(g diff --no-renames --name-only "$mb" "$p2" | sort) \
           <(g diff --no-renames --name-only "$mb" "$p1" | sort)
} > "$out/02_file_sets.txt"

{
  g --version 2>/dev/null || git --version
  echo "## ort merge-tree recomputation of P1+P2"
  mt=$(g merge-tree --write-tree --messages "$p1" "$p2")
  echo "$mt"
  echo "candidate tree: $(g rev-parse "$cand^{tree}")"
  if [ "$(echo "$mt" | head -1)" = "$(g rev-parse "$cand^{tree}")" ]; then
    echo "RESULT: candidate tree equals the conflict-free ort merge of its parents"
  else
    echo "RESULT: candidate tree DIFFERS from the ort merge"
  fi
} > "$out/03_merge_recompute.txt"

{
  echo "## CONTRIBUTING.md blobs"
  for r in "$mb" "$p1" "$p2" "$cand"; do echo "$r $(g rev-parse "$r:CONTRIBUTING.md")"; done
  echo "## PR side (MB..P2) CONTRIBUTING.md"; g diff --no-ext-diff "$mb" "$p2" -- CONTRIBUTING.md
  echo "## dev side (MB..P1) CONTRIBUTING.md"; g diff --no-ext-diff "$mb" "$p1" -- CONTRIBUTING.md
} > "$out/05_contributing_threeway.txt"

{
  echo "## patch-id per side for CONTRIBUTING.md (equal pairs = each side's change applied intact)"
  echo "MB->P2   $(g diff --no-ext-diff "$mb" "$p2" -- CONTRIBUTING.md | git patch-id --stable | cut -d' ' -f1)"
  echo "P1->cand $(g diff --no-ext-diff "$p1" "$cand" -- CONTRIBUTING.md | git patch-id --stable | cut -d' ' -f1)"
  echo "MB->P1   $(g diff --no-ext-diff "$mb" "$p1" -- CONTRIBUTING.md | git patch-id --stable | cut -d' ' -f1)"
  echo "P2->cand $(g diff --no-ext-diff "$p2" "$cand" -- CONTRIBUTING.md | git patch-id --stable | cut -d' ' -f1)"
  echo "## every other path equals its only changing side"
  for f in $(g diff --name-only "$mb" "$p2"); do
    [ "$f" = CONTRIBUTING.md ] && continue
    [ "$(g rev-parse "$cand:$f")" = "$(g rev-parse "$p2:$f")" ] && echo "OK PR-side $f" || echo "DIFF PR-side $f"
  done
  for f in $(g diff --name-only "$mb" "$p1"); do
    [ "$f" = CONTRIBUTING.md ] && continue
    [ "$(g rev-parse "$cand:$f")" = "$(g rev-parse "$p1:$f")" ] && echo "OK dev-side $f" || echo "DIFF dev-side $f"
  done
  echo "## candidate vs P1 paths"; g diff --name-only "$p1" "$cand"
  echo "## candidate vs P2 paths"; g diff --name-only "$p2" "$cand"
} > "$out/06_merge_equivalence.txt"

{
  echo "## gitlinks (mode oid path) at P1, P2 and candidate"
  for r in "$p1" "$p2" "$cand"; do
    echo "$r:"; g ls-tree -r "$r" | awk '$1=="160000"'
  done
} > "$out/10_gitlinks.txt"
echo "composition facts written to $out"
