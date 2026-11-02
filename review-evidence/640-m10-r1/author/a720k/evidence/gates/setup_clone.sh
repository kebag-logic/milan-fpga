#!/usr/bin/env bash
# Clean clone of the lane head with the four submodules the docs jobs fetch.
set -euo pipefail
G=$VALIDATION_STORAGE/640-a720k/gates
SRC=$VALIDATION_STORAGE/640-a720j/gates/wt
LANE=$LANES/640-mark2-charter
rm -rf "$G/wt"
git clone -q --no-hardlinks "$LANE" "$G/wt"
cd "$G/wt"
git checkout -q 640-charter-followup
git remote set-url origin https://github.com/kebag-logic/milan-fpga.git
git rev-parse HEAD
for p in gptp-processor protocol-processor third_party/tsn-c-stack third_party/verilog-axis; do
  name=$(git config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk -v p="$p" '$2==p{sub(/^submodule\./,"",$1); sub(/\.path$/,"",$1); print $1}')
  url=$(git config -f .gitmodules submodule."$name".url)
  git config submodule."$name".url "file://$SRC/.git/modules/$p"
  git -c protocol.file.allow=always submodule update -q --init --depth 1 -- "$p"
  test -e "$p/.git"
  git -C "$p" remote set-url origin "$url"
  git config --unset submodule."$name".url
  git config submodule."$name".url "$url"
  printf '%s\t%s\t%s\n' "$p" "$(git -C "$p" rev-parse HEAD)" "$(git -C "$p" remote get-url origin)"
done
git status --short | head
git submodule status
