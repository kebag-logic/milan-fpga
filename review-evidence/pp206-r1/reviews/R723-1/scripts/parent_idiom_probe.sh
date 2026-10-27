#!/usr/bin/env bash
# Reviewer probe: the parent's Python and C++ idiom scanners over a scratch
# parent at dev 97aab1d0 (WITHOUT the #202 wiring patch, which is not public)
# with the processor gitlink set to each given pin. It isolates what the
# processor submodule contributes; it is not the author's patched gate.
# Usage: parent_idiom_probe.sh <scratch parent> <receipt dir> <pin>...
set -u
parent=$1 out=$2; shift 2
for pin in "$@"; do
  d="$out/$pin"; mkdir -p "$d"
  git -C "$parent" update-index --cacheinfo "160000,$pin,protocol-processor"
  git -C "$parent/protocol-processor" checkout -q --detach "$pin"
  git -C "$parent" rev-parse HEAD > "$d/PARENT-HEAD.txt"
  git -C "$parent" submodule status -- protocol-processor gptp-processor \
    > "$d/SUBMODULES.txt"
  git -C "$parent" status --porcelain > "$d/PARENT-STATUS.txt"
  for c in "check_py_idiom.py" "check_py_idiom.py --list" \
           "check_cpp_idiom.py" "check_cpp_idiom.py --list"; do
    n=$(echo "$c" | tr ' ' '_' | tr -d '-')
    (cd "$parent" && python3 scripts/$c) > "$d/$n.log" 2>&1
    echo $? > "$d/$n.rc"
  done
done
