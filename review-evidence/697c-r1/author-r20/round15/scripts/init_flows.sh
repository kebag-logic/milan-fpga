#!/bin/sh
# What each way of initialising the stack submodule writes into the stack's own configuration.
# Usage: init_flows.sh <bare stack repo> <pin> <work dir>
set -eu
src=$1 pin=$2 work=$3
rm -rf "$work"; mkdir -p "$work"; cd "$work"
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@invalid \
  GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@invalid
git --version
git init -q -b dev origin-super
cd origin-super
printf '[submodule "third_party/tsn-c-stack"]\n\tpath = third_party/tsn-c-stack\n\turl = %s\n' "$src" > .gitmodules
git add .gitmodules
git update-index --add --cacheinfo "160000,$pin,third_party/tsn-c-stack"
git commit -q -m super
cd ..
show() { echo "== $1"; git -C "$2" config --list --show-scope; }
git clone -q origin-super a
git -C a -c protocol.file.allow=always submodule update -q --init third_party/tsn-c-stack
show "submodule update --init (the workflows' step)" a/third_party/tsn-c-stack
git -c protocol.file.allow=always clone -q --recurse-submodules origin-super b
show "clone --recurse-submodules" b/third_party/tsn-c-stack
git clone -q --no-hardlinks "$src" ref
git clone -q origin-super c
git -C c -c protocol.file.allow=always submodule update -q --init --reference "$work/ref" third_party/tsn-c-stack
show "submodule update --init --reference" c/third_party/tsn-c-stack
git -c protocol.file.allow=always clone -q --reference "$work/a" --recurse-submodules origin-super d
show "clone --reference --recurse-submodules (superproject)" d/third_party/tsn-c-stack
git clone -q --no-hardlinks a/third_party/tsn-c-stack e
git -C e -c advice.detachedHead=false checkout -q "$pin"
show "the pin controls' clone (clone --no-hardlinks of the submodule)" e
git init -q f
git -C f -c fetch.unpackLimit=1000000 fetch -q --no-tags "$work/e" HEAD
git -C f -c advice.detachedHead=false checkout -q "$pin"
show "the object-store controls' clone (init, fetch)" f
git -C a submodule absorbgitdirs -q 2>/dev/null || true
git -C a worktree add -q --detach ../g 2>/dev/null && git -C g -c protocol.file.allow=always submodule update -q --init third_party/tsn-c-stack && show "a worktree of the superproject, submodule update --init" g/third_party/tsn-c-stack
