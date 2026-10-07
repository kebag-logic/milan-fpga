#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Disposable probes on exported copies of <rev>; the source clone is never edited.
# Usage: licence_probes.sh <repo> <rev> <base-rev> <scratch-dir>
#  control : exported head tree, local doc checks must pass.
#  oldlic  : LICENSE replaced by the base blob (SPDX line restored); checks must
#            report the same results, so none reads or requires the SPDX line.
#  nolic   : LICENSE removed; the link checker must fail (the link is required).
set -u
repo=$1; rev=$2; base=$3; s=$4
mkdir -p "$s"
s=$(cd "$s" && pwd -P)
export PYTHONDONTWRITEBYTECODE=1
for v in control oldlic nolic; do
    d=$s/probe-$v
    rm -rf "$d"; mkdir -p "$d"
    git -C "$repo" archive "$rev" | tar -x -C "$d"
    case $v in
        oldlic) git -C "$repo" show "$base:LICENSE" > "$d/LICENSE" ;;
        nolic) rm "$d/LICENSE" ;;
    esac
    echo "=== $v LICENSE sha256: $( [ -f "$d/LICENSE" ] && sha256sum < "$d/LICENSE" | cut -c1-64 || echo absent)"
    for c in "check_links.py --local-only" "check_sentences.py" "check_references.py"; do
        ( cd "$d" && python3 doc/tools/$c > "$s/probe-$v.$(echo "$c" | cut -d. -f1).log" 2>&1 )
        rc=$?
        echo "$v $c rc=$rc :: $(grep -E 'Local links|Sentences/fragments|Unlinked references' "$s/probe-$v.$(echo "$c" | cut -d. -f1).log" | tail -1)"
        grep -E '^FAIL' "$s/probe-$v.$(echo "$c" | cut -d. -f1).log" | head -5
    done
done
