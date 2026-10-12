#!/usr/bin/env bash
# R585-14: the superproject a partial clone with a sparse index, a sparse directory's tree object absent, its promisor
# remote's upload-pack a recorder; the gitlink read as the pin proof reads it (ctrl_build.stack_gitlink), on the Git
# PATH names. Prints the gitlink read (or the refusal) and how many times the recorder ran.
# usage: r585_14_superproject_sparse.sh <superproject-checkout-at-head> <scratch-dir>
set -u
TOP=$(cd "$1" && pwd); D=$2; rm -rf "$D"; mkdir -p "$D"
PIN=$(git -C "$TOP" ls-files --stage -- third_party/tsn-c-stack | awk '{print $2}')
printf '#!/bin/sh\necho "$0 $*" >> "%s/ran"\nexit 1\n' "$D" > "$D/rec"; chmod +x "$D/rec"
git init -q "$D/origin"; mkdir -p "$D/origin/elsewhere"; echo x > "$D/origin/elsewhere/f"
git -C "$D/origin" add elsewhere/f; git -C "$D/origin" update-index --add --cacheinfo "160000,$PIN,third_party/tsn-c-stack"
git -C "$D/origin" -c user.name=r -c user.email=r@x commit -q -m s
git -C "$D/origin" config uploadpack.allowFilter true
git -c protocol.file.allow=always clone -q --no-local --filter=tree:0 --no-checkout "file://$D/origin" "$D/sp" 2>&1 | tail -1
git -C "$D/sp" sparse-checkout init --cone --sparse-index; git -C "$D/sp" sparse-checkout set third_party 2>&1 | tail -1
git -C "$D/sp" checkout -q 2>&1 | tail -1
echo "index entries (sparse dirs end in /):"; git -C "$D/sp" ls-files --sparse --stage | sed 's/^/  /'
t=$(git -C "$D/origin" rev-parse HEAD:elsewhere); f="$D/sp/.git/objects/${t:0:2}/${t:2}"
mkdir -p "$D/packs"; mv "$D/sp/.git/objects/pack/"* "$D/packs/"
for pk in "$D/packs/"*.pack; do git -C "$D/sp" unpack-objects -q < "$pk"; done
rm -f "$f"; { [ -f "$f" ] || ls "$D/sp/.git/objects/pack/" | grep -q .; } && echo "  (elsewhere/ tree may be held: $t)" || echo "  elsewhere/ tree $t absent (no loose file, no pack)"
git -C "$D/sp" config remote.origin.uploadpack "$D/rec"
echo "superproject config:"; git -C "$D/sp" config --list --local | sed 's/^/  /'
cd "$TOP/sw/firmware/ctrl/test" && timeout 60 python3 -I -c '
import sys; sys.path.insert(0, ".")
from pathlib import Path
import ctrl_build
try:
    print("gitlink", ctrl_build.stack_gitlink(Path(sys.argv[1])))
except ctrl_build.Refusal as exc:
    print("REFUSED", exc)' "$D/sp" 2>&1 | tail -2
echo "git $(git --version | cut -d" " -f3): superproject sparse RAN=$( [ -f "$D/ran" ] && wc -l < "$D/ran" || echo 0)"
