#!/bin/sh
# mk_tree.sh <clone> <rev> <dest>: an archive copy of <rev>'s tracked files at <dest> (a new directory), the clone's
# initialised submodules linked in (the delta changes no gitlink), and a fresh index holding only <rev>'s gitlinks,
# which the firmware gate's pin checks read; probes never touch the clone.
set -eu
clone=$1; rev=$2; dest=$3
[ ! -e "$dest" ] || { echo "refused: $dest exists" >&2; exit 2; }
mkdir -p "$dest"
git -C "$clone" archive "$rev" | tar -x -C "$dest"
git -C "$dest" init -q
git -C "$clone" ls-tree -r "$rev" | awk '$2=="commit"{print $1, $3, $4}' | while read -r mode sha path; do
  rmdir "$dest/$path" 2>/dev/null || true
  ln -s "$clone/$path" "$dest/$path"
  git -C "$dest" update-index --add --cacheinfo "$mode,$sha,$path"
done
echo "tree $rev at $dest: $(git -C "$clone" rev-parse "$rev^{tree}")"
git -C "$dest" ls-files --stage | awk '$1=="160000"'
