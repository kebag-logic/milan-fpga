#!/bin/sh
# Whole-tree sweep for pending/trigger/composition statements at a revision.
# Usage: sweep.sh <clone> <out-dir>
set -eu
clone=$1; out=$2
cd "$clone"
git grep -n -I -E 'pend_i *=|D2 sticky|D2 bit|aecp_mark_pend|sticky (live-name/map |pending )?bit|every commit beat|conservative duplicate|class-6/7|class-6|class-7|mark-based|late-mark|mark trigger|marks? (as|are) (the )?pending|NVM_MARK.*pend|pend.*NVM_MARK|amap_edit_req_o *(&&|AND|and) |phase-5 export|phase 5 export' \
  -- . ':!protocol-processor' ':!gptp-processor' ':!third_party' ':!external' > "$out/tree_grep_head.txt" || true
git grep -n -I -i -P '(\bpend(ing|_i|_r|_w|_o)?\b|nvm_pend|durable)' \
  -- . ':!protocol-processor' ':!gptp-processor' ':!third_party' ':!external' ':!docs/history' \
  | grep -i -P '\bname|\bmaps?\b|mapping|\bmarks?\b|live.?wr|\bD2\b|amap' \
  | grep -v -E '^docs/design/SAVED_STATE_(MATERIALIZATION|SNAPSHOT_OWNERSHIP)\.md' > "$out/tree_grep_namemap_pending.txt" || true
wc -l "$out/tree_grep_head.txt" "$out/tree_grep_namemap_pending.txt"
