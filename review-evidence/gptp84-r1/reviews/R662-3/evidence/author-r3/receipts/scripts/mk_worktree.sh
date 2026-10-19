#!/bin/sh
# usage: mk_worktree.sh <name> <parent-commit>
# Adds a scratch parent worktree <scratch>/<name> at <parent-commit>, with its
# submodules initialised from the local scratch parent's module checkouts
# (no network), the gptp-processor gitlink's commit fetched from the lane,
# and tsn-c-stack's origin set back to its canonical URL (the parent's
# receipt identity check reads it). Never pushes anything.
set -e
S=<scratch>
name=$1; commit=$2
git -C "$S/parent" worktree add -q --detach "$S/$name" "$commit"
cd "$S/$name"
test "$(git rev-parse --show-toplevel)" = "$S/$name"
git -c protocol.file.allow=always submodule update -q --init 2>/dev/null || true
gl=$(git ls-tree HEAD gptp-processor | awk '{print $3}')
test "$(git -C gptp-processor rev-parse --show-toplevel)" = "$S/$name/gptp-processor"
git -C gptp-processor -c protocol.file.allow=always fetch -q <lane> 84-85-tu-pathtrace
git -C gptp-processor checkout -q "$gl"
git -c protocol.file.allow=always submodule update -q --init
test "$(git -C third_party/tsn-c-stack rev-parse --show-toplevel)" = "$S/$name/third_party/tsn-c-stack"
git -C third_party/tsn-c-stack remote set-url origin https://github.com/kebag-logic/tsn-c-stack.git
# The first update stops at the missing gptp-processor commit and can leave a
# freshly cloned submodule with an unpopulated index; reset each one to its
# recorded commit (each is new and checked to be its own top level).
for p in $(git config -f .gitmodules --get-regexp '\.path$' | awk '{print $2}'); do
  test "$(git -C "$p" rev-parse --show-toplevel)" = "$S/$name/$p"
  git -C "$p" reset -q --hard
done
git submodule status
test -z "$(git status --porcelain)"
echo "worktree $name at $(git rev-parse HEAD)"
