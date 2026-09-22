#!/usr/bin/env bash
# Build isolated scratch copies from the review clone's object store only (no
# network, no hardlinks, no worktree registration in the review clone).
#   git-nosub : Git clone at the head, NO submodule initialized
#   nogit     : `git archive` extraction of the head, no .git at all
#   git-sub   : Git clone at the head, the three required submodules
#               initialized at their gitlinks from the review clone's
#               submodule repositories
#   base-sub  : same as git-sub at the current base 88e9276b
set -euo pipefail
R=$VALIDATION_STORAGE/reviews/r222-478-r2
S=${SCRATCH:-/tmp/r222-478-r2-scratch}
HEAD_C=1496558d82cf35fc98dda0e781b2a1be643c301a
BASE_NOW=88e9276b2a220c716f64a843f7e1eb8f9265e896
REQ=(third_party/verilog-axis protocol-processor gptp-processor)
rm -rf "$S"; mkdir -p "$S"

clone_at() { # <dir> <commit>
  git clone --quiet --no-hardlinks --no-checkout "$R" "$1"
  git -C "$1" checkout --quiet --detach "$2"
}
init_subs() { # <dir>  (scratch-local config only; the review clone is read)
  git -C "$1" submodule init -- "${REQ[@]}"
  for p in "${REQ[@]}"; do
    git -C "$1" config "submodule.$p.url" "$R/.git/modules/$p"
  done
  git -C "$1" -c protocol.file.allow=always submodule update --no-fetch --quiet -- "${REQ[@]}" \
    || git -C "$1" -c protocol.file.allow=always submodule update --quiet -- "${REQ[@]}"
}
report() { # <dir>
  echo "HEAD=$(git -C "$1" rev-parse HEAD) tree=$(git -C "$1" rev-parse 'HEAD^{tree}')"
  echo "status-lines=$(git -C "$1" status --porcelain --untracked-files=all | wc -l)"
  git -C "$1" submodule status
}

clone_at "$S/git-nosub" "$HEAD_C"
echo "== git-nosub"; report "$S/git-nosub"
for p in external "${REQ[@]}"; do
  printf '%s entries=%s\n' "$p" "$(find "$S/git-nosub/$p" -mindepth 1 2>/dev/null | wc -l)"
done

mkdir -p "$S/nogit"
git -C "$R" archive --format=tar "$HEAD_C" | tar -x -C "$S/nogit"
echo "== nogit"
echo ".git present: $([ -e "$S/nogit/.git" ] && echo yes || echo no)"
for p in external "${REQ[@]}"; do
  printf '%s exists=%s entries=%s\n' "$p" "$([ -e "$S/nogit/$p" ] && echo yes || echo no)" \
    "$(find "$S/nogit/$p" -mindepth 1 2>/dev/null | wc -l)"
done
# Every archived regular file must equal its head blob.
( cd "$S/nogit" && git -C "$R" ls-tree -r "$HEAD_C" | awk '$2=="blob"' | while read -r mode _ sha path; do
    got=$(git hash-object --no-filters -- "$path"); [ "$got" = "$sha" ] || echo "MISMATCH $path"
    if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE $path"; fi
  done; echo "archive blob check done" )

clone_at "$S/git-sub" "$HEAD_C"; init_subs "$S/git-sub"
echo "== git-sub"; report "$S/git-sub"

clone_at "$S/base-sub" "$BASE_NOW"; init_subs "$S/base-sub"
echo "== base-sub"; report "$S/base-sub"
