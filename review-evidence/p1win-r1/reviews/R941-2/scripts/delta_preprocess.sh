#!/bin/sh
# Show that the one commit 85569e241..079c4fa15 changes no token a compiler sees: extract
# sw/firmware/ctrl_nvm at both commits, strip comments with the preprocessor keeping line markers,
# and compare. Usage: delta_preprocess.sh <repo> <workdir>
set -eu
repo=$1; work=$2
rm -rf "$work"; mkdir -p "$work/head" "$work/prev"
git -C "$repo" archive 079c4fa1514be460949ddc28ae3277ea1873cb48 sw/firmware/ctrl_nvm | tar -x -C "$work/head"
git -C "$repo" archive 85569e241625d8e4176aae7d77c524783dff30cd sw/firmware/ctrl_nvm | tar -x -C "$work/prev"
for t in head prev; do
	(cd "$work/$t" && gcc -fpreprocessed -dD -E sw/firmware/ctrl_nvm/nvm_store.h > "$work/$t-stripped.txt")
done
git -C "$repo" diff --stat 85569e241625d8e4176aae7d77c524783dff30cd 079c4fa1514be460949ddc28ae3277ea1873cb48
wc -l "$work/head/sw/firmware/ctrl_nvm/nvm_store.h" "$work/prev/sw/firmware/ctrl_nvm/nvm_store.h"
cmp "$work/head-stripped.txt" "$work/prev-stripped.txt" && echo "RESULT: identical after comment removal"
