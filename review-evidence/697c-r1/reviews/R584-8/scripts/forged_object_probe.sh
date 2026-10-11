#!/bin/sh
# Outside the ruled class (replacement objects, grafts, filters): a corrupted object store.
# The pinned src/ tree's loose object is overwritten with a tree that holds an edited adp.c,
# and the edit is made on disk. Usage: forged_object_probe.sh <milan-fpga checkout> <scratch dir>
set -eu
root=$(cd "$1" && pwd); work=$2
rm -rf "$work"; mkdir -p "$work"
pin=$(git -C "$root" ls-files --stage -- third_party/tsn-c-stack | awk '{print $2}')
git clone --quiet --no-hardlinks "$root/third_party/tsn-c-stack" "$work/clone"
cd "$work/clone"
git -c advice.detachedHead=false checkout --quiet "$pin"
# make every object loose, so a loose object is what git reads
mkdir ../packs; mv .git/objects/pack/* ../packs/
for p in ../packs/*.pack; do git unpack-objects -q < "$p"; done
src=$(git rev-parse "$pin:src")
printf '\n' >> src/adp.c
blob=$(git hash-object -w --no-filters src/adp.c)
forged=$(git ls-tree "$src" | sed "s/[0-9a-f]\{40\}\tadp.c$/$blob\tadp.c/" | git mktree)
obj=.git/objects/$(echo "$src" | cut -c1-2)/$(echo "$src" | cut -c3-)
chmod u+w "$obj"
cp ".git/objects/$(echo "$forged" | cut -c1-2)/$(echo "$forged" | cut -c3-)" "$obj"
echo "pinned src tree $src now holds the bytes of $forged"
echo "git ls-tree of the pin now lists adp.c as: $(GIT_NO_REPLACE_OBJECTS=1 git ls-tree -r "$pin" -- src/adp.c)"
echo "git fsck on the clone: $(git fsck --no-dangling 2>&1 | head -2 | tr '\n' ' ')"
cd "$root"
python3 -I sw/firmware/ctrl/test/ctrl_build.py --stack-pin "$work/clone"; echo "pin check rc=$?"
