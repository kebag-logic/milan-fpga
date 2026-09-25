#!/usr/bin/env bash
# R289-2 fault probes for the round-2 anchor fix, on disposable exports of HEAD.
# Each probe runs the repository link gate and the offline mode of
# github_anchor_check.py over the changed files, and prints both return codes.
# Usage: probe-anchors.sh CLONE PACKET
set -u
C=$1; PK=$2; S=$PK/scratch/probe-anchors; H=9cde1c19dbfd859257be8e012d4455856fcfce3b
OLD1=331-realization-the-image-lives-in-main-memory-not-on-chip
OLD2=332-the-other-main-memory-region-the-aecp-response-buffer
GH1=331-realization--the-image-lives-in-main-memory-not-on-chip
GH2=332-the-other-main-memory-region--the-aecp-response-buffer
run() { # name expected_links expected_anchor mutation...
  local name=$1 el=$2 ea=$3; shift 3
  rm -rf "$S/$name"; mkdir -p "$S/$name"; git -C "$C" archive $H | tar -x -C "$S/$name"
  ( cd "$S/$name" && git init -q && git add -A && eval "$@" )
  ( cd "$S/$name" && python3 scripts/check-links.py > ../$name.links.log 2>&1 ); lr=$?
  python3 "$PK/github_anchor_check.py" "$S/$name" --files docs/guides/integrator.md docs/architecture/07_memory_maps.md docs/architecture/09_verification.md > "$S/$name.anchors.log" 2>&1; ar=$?
  printf '%-28s links rc=%s (expect %s)  anchors rc=%s (expect %s)  %s\n' "$name" $lr $el $ar $ea \
    "$([ $lr = $el ] && [ $ar = $ea ] && echo AS-EXPECTED || echo UNEXPECTED)"
  grep -h -m3 -E 'DEAD|broken|FAIL|missing' "$S/$name.links.log" "$S/$name.anchors.log" | sed 's/^/    /' | cut -c1-200
}
run baseline-head 0 0 true
run typo-resp-fragment 1 1 "sed -i 's/#sec-resp-memory)/#sec-resp-memoryX)/' docs/guides/integrator.md"
run drop-resp-anchor 1 1 "sed -i '/^<a id=\"sec-resp-memory\"><\\/a>\$/d' docs/architecture/07_memory_maps.md"
run drop-desc-anchor 1 1 "sed -i '/^<a id=\"sec-desc-memory\"><\\/a>\$/d' docs/architecture/07_memory_maps.md"
run revert-to-round1-slugs 0 1 "sed -i -e 's/07_memory_maps.md#sec-desc-memory)/07_memory_maps.md#$OLD1)/' -e 's/07_memory_maps.md#sec-resp-memory)/07_memory_maps.md#$OLD2)/' docs/guides/integrator.md"
run github-double-hyphen-slugs 1 0 "sed -i -e 's/07_memory_maps.md#sec-desc-memory)/07_memory_maps.md#$GH1)/' -e 's/07_memory_maps.md#sec-resp-memory)/07_memory_maps.md#$GH2)/' docs/guides/integrator.md"
