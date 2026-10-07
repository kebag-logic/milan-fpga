#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Disposable fault probes: each one breaks a scratch copy and records whether
# the corresponding check detects it.  The source checkout is never modified.
# Usage: TERMS_FILE=<terms> CANON=<canonical licence file> probes.sh <repo> <head> <scratch> <logdir>
set -u
repo=$1 head=$2 scr=$3 logs=$4
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$logs"; : > "$logs/probes.txt"
export PYTHONDONTWRITEBYTECODE=1
fresh() { rm -rf "$scr/$1"; git clone -q --no-local "$repo" "$scr/$1"; git -C "$scr/$1" checkout -q --detach "$head"; git -C "$scr/$1" config user.name probe; git -C "$scr/$1" config user.email probe@invalid; }
record() { echo "$1 expected=$2 observed=$3 $( [ "$2" = "$3" ] && echo DETECTED-AS-EXPECTED || echo UNEXPECTED )" | tee -a "$logs/probes.txt"; }

# P1: revert the Leave-interval anchor to the pre-header line; anchor check must fail,
# the existing link checker (bounds only) still passes locally.
fresh p1
sed -i 's|shish_lan/mrp.h#L119)|shish_lan/mrp.h#L118)|' "$scr/p1/doc/integrator.md"
git -C "$scr/p1" commit -qam probe
python3 "$here/anchor_check.py" "$scr/p1" "$(git -C "$repo" rev-parse "$head~1^2")" HEAD > "$logs/p1_anchor.log" 2>&1
record P1-anchor-revert-detected-by-anchor_check 1 $?
(cd "$scr/p1" && python3 doc/tools/check_links.py > "$logs/p1_links.log" 2>&1); grep -q '^FAIL [^h]' "$logs/p1_links.log"
record P1-anchor-revert-local-link-failure 1 $?

# P2: drop the SPDX line from one source file; the SPDX census must fail.
fresh p2
sed -i '1d' "$scr/p2/src/core/mrp_pdu.c"
missing=0
for f in $(git -C "$scr/p2" ls-files); do
  case $f in LICENSE|NOTICE) continue;; esac
  head -n 2 "$scr/p2/$f" | grep -q 'SPDX-License-Identifier: Apache-2.0' || { echo "missing $f" >> "$logs/p2_spdx.log"; missing=1; }
done
record P2-missing-spdx-detected 1 $missing

# P3: one-byte change in LICENSE; the canonical comparison must fail.
fresh p3
sed -i '0,/Apache License/s//Apache Licence/' "$scr/p3/LICENSE"
git -C "$scr/p3" diff --quiet; record P3-mutation-applied 1 $?
cmp -s "$CANON" "$scr/p3/LICENSE"
record P3-license-byte-change-detected 1 $?

# P4: remove NOTICE; the local link check must fail on the notice links.
fresh p4
git -C "$scr/p4" rm -q NOTICE
(cd "$scr/p4" && python3 doc/tools/check_links.py > "$logs/p4_links.log" 2>&1)
grep -q 'NOTICE' "$logs/p4_links.log" && grep -q '^FAIL.*NOTICE' "$logs/p4_links.log"
record P4-missing-notice-detected-by-link-check 0 $?

# P5: positive control for the history scan: a nested file and a commit
# message containing the first term must both be reported.
fresh p5
t=$(head -n 1 "$TERMS_FILE" | tr -d '\\b')
mkdir -p "$scr/p5/a/b"; echo "x $t y" > "$scr/p5/a/b/f.txt"
git -C "$scr/p5" add a; git -C "$scr/p5" commit -qm "probe $t"
git -C "$scr/p5" update-ref refs/heads/probe HEAD
python3 "$here/history_scan.py" "$scr/p5" > "$logs/p5_scan.log" 2>&1
record P5-history-scan-positive-control 1 $?
grep -q '^HIT commit' "$logs/p5_scan.log"; record P5-commit-message-hit 0 $?
grep -q '^HIT blob' "$logs/p5_scan.log"; record P5-blob-hit 0 $?
