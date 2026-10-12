#!/usr/bin/env bash
# Two routes inside the pin proof's stated threat model (Git's object store; the repository's configuration),
# probed against a tree's shared pin check (ctrl_build.py --stack-pin DIR) on disposable stack clones.
# usage: model_routes.sh <tree> <stack repository to clone from> <work>
set -uo pipefail
tree=$1 src=$2 work=$3
pin=$(git -C "$tree" ls-tree HEAD third_party/tsn-c-stack | awk '{print $3}')
check() { python3 -I "$tree/sw/firmware/ctrl/test/ctrl_build.py" --stack-pin "$1" 2>&1 | tail -2; echo "exit ${PIPESTATUS[0]}"; }
fresh() {
  rm -rf "$1"; git clone -q --no-local --no-checkout "$src" "$1"; git -C "$1" checkout -q --detach "$pin"
  # every object loose, so one can be overwritten in place
  mkdir -p "$1.packs"; mv "$1"/.git/objects/pack/* "$1.packs/" 2>/dev/null
  for p in "$1.packs"/*.pack; do git -C "$1" unpack-objects -q < "$p"; done; rm -rf "$1.packs"
}
echo "pin $pin"
echo "## control: the pinned clone, unmodified"; fresh "$work/clean"; check "$work/clean"
echo "## control: src/adp.c edited on disk only"; fresh "$work/edit"; echo "/* probe */" >> "$work/edit/src/adp.c"; check "$work/edit"

echo "## route 1: src/adp.c edited, and the pinned src/ tree's loose object overwritten by a tree holding the edit"
d=$work/forged; fresh "$d"
old_tree=$(git -C "$d" rev-parse "$pin:src")
echo "/* probe */" >> "$d/src/adp.c"
blob=$(git -C "$d" hash-object -w src/adp.c)
new_tree=$(git -C "$d" ls-tree "$pin:src" | sed "s/[0-9a-f]\{40\}\(\tadp\.c\)$/$blob\1/" | git -C "$d" mktree)
obj="$d/.git/objects/${old_tree:0:2}/${old_tree:2}"
chmod u+w "$obj"; cp "$d/.git/objects/${new_tree:0:2}/${new_tree:2}" "$obj"
echo "old src tree $old_tree now holds $(git -C "$d" cat-file -p "$old_tree" | grep -c "$blob") entry for the edited blob"
check "$d"
echo "git fsck says: $(git -C "$d" fsck 2>&1 | grep -i 'hash mismatch\|sha1 mismatch\|corrupt' | head -1)"

echo "## route 2: the clone's own .git/config names core.fsmonitor"
d=$work/fsmon; fresh "$d"
rec=$work/fsmon-recorder.sh; log=$work/fsmon-ran.log; rm -f "$log"
printf '#!/bin/sh\necho "fsmonitor ran: $*" >> %s\nexit 1\n' "$log" > "$rec"; chmod +x "$rec"
git -C "$d" config core.fsmonitor "$rec"
check "$d"
echo "recorder lines: $( [ -f "$log" ] && wc -l < "$log" || echo 0)"
