#!/bin/bash
# Build the disposable head, work and base copies under <scratch>: git archive of
# the superproject plus the checked-out submodule trees, then a private local git
# snapshot in each copy and submodule (the SoC path runs `git ls-files` there).
# Usage: 01_prepare_copies.sh <clone> <scratch>
set -eu
C=${1:?clone}; S=${2:?scratch}
HEAD_SHA=77998f14b16bf7605956332d0f0ac8af0cecab5a; BASE_SHA=9e9954e96bf55181edb9949ae94c9abd4ab6aaf5
mk() {
  mkdir -p "$S/$1"; git -C "$C" archive "$2" | tar -x -C "$S/$1"
  for sm in gptp-processor protocol-processor third_party/verilog-axis; do
    mkdir -p "$S/$1/$sm"; git -C "$C/$sm" archive HEAD | tar -x -C "$S/$1/$sm"; done
}
mk head "$HEAD_SHA"; cp -a "$S/head" "$S/work"; mk base "$BASE_SHA"
for t in work base; do
  for d in "$S/$t/protocol-processor" "$S/$t/gptp-processor" "$S/$t/third_party/verilog-axis" "$S/$t"; do
    (cd "$d" && git init -q && git add -A && git -c user.name=reviewer -c user.email=reviewer@invalid commit -qm snapshot --no-verify)
  done
done
