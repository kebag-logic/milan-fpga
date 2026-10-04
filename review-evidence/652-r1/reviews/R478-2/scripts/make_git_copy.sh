#!/bin/sh
# Turn a copy of an exported tree into throwaway local git repositories (the
# top and each pinned submodule dir), so gates that list tracked files with
# git can run in it. Usage: make_git_copy.sh <export> <dest>
set -eu
rm -rf "$2"; cp -a "$1" "$2"
for d in third_party/verilog-axis protocol-processor gptp-processor .; do
  (cd "$2/$d" && git init -q && git add -A && git -c user.name=probe -c user.email=probe@invalid commit -q -m probe)
done
echo "git copy ready: $2"
