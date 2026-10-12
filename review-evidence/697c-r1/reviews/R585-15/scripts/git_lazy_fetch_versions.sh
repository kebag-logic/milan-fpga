#!/bin/sh
# Which Git sources and Ubuntu 24.04 git packages read GIT_NO_LAZY_FETCH.
# usage: git_lazy_fetch_versions.sh WORK   (needs gh, curl, ar, tar; reads only; executes nothing it downloads)
W=$1; mkdir -p "$W"
echo "## upstream git/git tags: occurrences of NO_LAZY_FETCH in environment.h, cache.h, promisor-remote.c"
for t in v2.39.4 v2.42.2 v2.43.0 v2.43.4 v2.44.0 v2.44.1 v2.45.0; do n=0
  for f in environment.h cache.h promisor-remote.c; do
    c=$(gh api "repos/git/git/contents/$f?ref=$t" -q .content 2>/dev/null | base64 -d 2>/dev/null | grep -c NO_LAZY_FETCH); n=$((n+${c:-0}))
  done; echo "$t $n"; done
echo "## Ubuntu noble git packages: GIT_NO_LAZY_FETCH strings in /usr/bin/git"
for v in 7 7.3; do d="$W/u$v"; rm -rf "$d"; mkdir -p "$d"; ( cd "$d" && curl -fsSO "http://archive.ubuntu.com/ubuntu/pool/main/g/git/git_2.43.0-1ubuntu${v}_amd64.deb" && ar x "git_2.43.0-1ubuntu${v}_amd64.deb" && tar -xf data.tar.* ./usr/bin/git && echo "git_2.43.0-1ubuntu${v}_amd64.deb sha256 $(sha256sum git_2.43.0-1ubuntu${v}_amd64.deb | cut -c1-64) strings $(grep -c -a GIT_NO_LAZY_FETCH usr/bin/git)" ); done
