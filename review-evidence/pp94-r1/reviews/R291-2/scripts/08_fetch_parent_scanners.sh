#!/usr/bin/env bash
# Fetch the parent dev 9d328810 Rule 11/12 scanners used by 07_idiom_scan.py (read-only API).
source "$(dirname "$0")/00_env.sh"
D=$PKT/scratch/parent; mkdir -p "$D"
for f in check_cpp_idiom.py check_py_idiom.py code_quality_scope.py; do
  gh api "repos/kebag-logic/milan-fpga/contents/scripts/$f?ref=9d3288107edc97fe13d894874a6ca6c7e00de1ba" \
     -H 'Accept: application/vnd.github.raw' > "$D/$f"
done
sha256sum "$D"/check_cpp_idiom.py "$D"/check_py_idiom.py "$D"/code_quality_scope.py | sed "s|$D/||"
