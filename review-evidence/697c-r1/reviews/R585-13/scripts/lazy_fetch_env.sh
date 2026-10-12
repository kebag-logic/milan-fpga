#!/usr/bin/env bash
# Whether Git, given exactly the pin proof's environment and arguments, starts the transport program a partial
# clone's own configuration names when an object of the pin is missing; and whether GIT_NO_LAZY_FETCH=1 stops it.
# usage: lazy_fetch_env.sh <stack checkout at the pin> <work dir>
set -u
SRC=$(realpath "$1"); W=$(realpath -m "$2"); rm -rf "$W"; mkdir -p "$W"; cd "$W" || exit 3
PIN=$(git -C "$SRC" rev-parse HEAD)
git init -q s; git -C s -c fetch.unpackLimit=1000000 fetch -q --no-tags "$SRC" "$PIN"
git -C s -c advice.detachedHead=false checkout -q "$PIN"
T=$(git -C s rev-parse "$PIN:src"); rm -f "s/.git/objects/${T:0:2}/${T:2}"
printf '#!/bin/sh\necho ran >> %s/lazy.log\nexit 1\n' "$W" > rec; chmod +x rec
git -C s config core.repositoryformatversion 1; git -C s config extensions.partialClone probe
git -C s config remote.probe.url ssh://probe.invalid/x; git -C s config remote.probe.promisor true
git -C s config core.sshCommand "$W/rec"
GIT=$(command -v git); echo "git: $("$GIT" --version)"
count() { [ -f lazy.log ] && wc -l < lazy.log || echo 0; }
env -i GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null/no-grafts GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null \
  "$GIT" -c core.fsmonitor=false -C s cat-file tree "$T" > /dev/null 2>&1
echo "the proof's environment and arguments: transport program runs $(count)"
rm -f lazy.log
env -i GIT_NO_REPLACE_OBJECTS=1 GIT_GRAFT_FILE=/dev/null/no-grafts GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null \
  GIT_NO_LAZY_FETCH=1 "$GIT" -c core.fsmonitor=false -C s cat-file tree "$T" > /dev/null 2>&1
echo "the same with GIT_NO_LAZY_FETCH=1: transport program runs $(count)"
