#!/usr/bin/env bash
# Usage: scope.sh <processor-clone> ; prints the base/head scope proof.
set -euo pipefail
cd "$1"
B=09e357fb4bf3d35c8a9deba9a787e13f74d08c83
H=c3864686c0b254bd2d7b7f733078ec302fb9be62
echo "head=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree})"
echo "merge-base=$(git merge-base $B $H)"
for p in hdl syn scripts .github tb/pp_top tb/common Makefile docs/guides docs/diagrams docs/traceability; do
  b=$(git rev-parse $B:$p); h=$(git rev-parse $H:$p)
  printf '%-22s base=%s head=%s %s\n' "$p" "$b" "$h" "$([ "$b" = "$h" ] && echo IDENTICAL || echo DIFFERENT)"
done
echo "--- changed paths (raw, with modes)"
git diff --raw --no-abbrev $B $H
echo "--- RTL/param/port/NVM-framing sources differing from base (expect none)"
git diff --name-only $B $H -- '*.sv' '*.svh' '*.v' '*.vh' '*.tcl' '*.xdc' 'hdl/**' 'syn/**' | sed 's/^/DIFF /' || true
echo "--- DESC_NAME_ENTRIES_P and 0x80 name block at head"
git grep -n 'DESC_NAME_ENTRIES_P = ' $H -- hdl/top/protocol_processor_top.sv
git grep -n '0x80. .. .0xFF.' $H -- docs/architecture/07_memory_maps.md
echo "--- submodules/gitlinks"
git ls-tree -r $H | awk '$1=="160000"' ; echo "gitlinks: $(git ls-tree -r $H | awk '$1=="160000"' | wc -l)"
echo "--- worktree"
git status --porcelain=v1 --ignored | sed 's/^/STATUS /'; echo "status-lines: $(git status --porcelain=v1 | wc -l)"
