#!/usr/bin/env bash
# R222-3: candidate identity, merge-tree reproduction, patch identity, disjointness.
# Runs in the scratch candidate clone (merge-tree writes objects there, never
# into the review clone). Usage: 01_history_identity.sh <scratch-cand> <out>
set -euo pipefail
d=$1; out=$2
export GIT_NO_REPLACE_OBJECTS=1
C=72e16c6172db723734317b105cff6c6e9168571a
D=52711029f374650dc93830d5ea28e81cb5c8f410
P=1496558d82cf35fc98dda0e781b2a1be643c301a
MB_EXPECT=88e9276b2a220c716f64a843f7e1eb8f9265e896
g() { git -C "$d" "$@"; }
{
  echo "candidate: $(g rev-parse $C) tree $(g rev-parse $C^{tree})"
  echo "candidate parents: $(g rev-parse $C^1) $(g rev-parse $C^2)"
  echo "candidate message lines: $(g log -1 --format=%B $C | sed '/^$/d' | wc -l)"
  echo "candidate subject: $(g log -1 --format=%s $C)"
  echo "candidate trailers: [$(g log -1 --format='%(trailers:only,unfold)' $C | tr -d '\n')]"
  mb=$(g merge-base $D $P)
  echo "merge-base(dev,source): $mb expect $MB_EXPECT $([ "$mb" = "$MB_EXPECT" ] && echo OK || echo MISMATCH)"
  mt=$(g merge-tree --write-tree $D $P | head -1)
  echo "merge-tree --write-tree dev source: $mt vs candidate tree $(g rev-parse $C^{tree}) $([ "$mt" = "$(g rev-parse $C^{tree})" ] && echo EQUAL || echo DIFFERENT)"
  echo "--- issue side: merge-base..source (name-status)"
  g diff --name-status $mb $P
  echo "--- #513 side: merge-base..dev (name-status)"
  g diff --name-status $mb $D
  comm -12 <(g diff --name-only $mb $P | sort) <(g diff --name-only $mb $D | sort) > /tmp/r222-478-r3-inter.txt
  echo "--- path intersection count: $(wc -l < /tmp/r222-478-r3-inter.txt)"
  echo "--- candidate vs source (should be exactly #513 paths)"
  g diff --name-status $P $C
  echo "--- candidate vs dev (should be exactly issue paths)"
  g diff --name-status $D $C
  echo "--- patch identity"
  a=$(g diff --full-index --binary $mb $P | sha256sum | cut -d' ' -f1)
  b=$(g diff --full-index --binary $D $C | sha256sum | cut -d' ' -f1)
  echo "issue patch sha256 (mb..source): $a"
  echo "issue patch sha256 (dev..cand):  $b  $([ "$a" = "$b" ] && echo BYTE-EQUAL || echo DIFFERENT)"
  pa=$(g diff $mb $P | git patch-id --verbatim | cut -d' ' -f1)
  pb=$(g diff $D $C | git patch-id --verbatim | cut -d' ' -f1)
  echo "issue patch-id --verbatim: $pa / $pb $([ "$pa" = "$pb" ] && echo EQUAL || echo DIFFERENT)"
  c=$(g diff --full-index --binary $mb $D | sha256sum | cut -d' ' -f1)
  e=$(g diff --full-index --binary $P $C | sha256sum | cut -d' ' -f1)
  echo "#513 patch sha256 (mb..dev):   $c"
  echo "#513 patch sha256 (source..cand): $e  $([ "$c" = "$e" ] && echo BYTE-EQUAL || echo DIFFERENT)"
  echo "--- blob identity per changed path"
  for f in $(g diff --name-only $mb $P); do
    echo "issue  $f src=$(g rev-parse $P:$f) cand=$(g rev-parse $C:$f) dev=$(g rev-parse $D:$f) mb=$(g rev-parse $mb:$f)"
  done
  for f in $(g diff --name-only $mb $D); do
    echo "#513   $f dev=$(g rev-parse $D:$f) cand=$(g rev-parse $C:$f) src=$(g rev-parse $P:$f) mb=$(g rev-parse $mb:$f)"
  done
  echo "--- modes of changed paths at candidate"
  g ls-tree $C -- $(g diff --name-only $mb $P) $(g diff --name-only $mb $D)
  echo "--- gitlinks and .gitmodules across mb/dev/source/candidate"
  for r in $mb $D $P $C; do
    echo "$r gitmodules=$(g rev-parse $r:.gitmodules) $(g ls-tree $r external gptp-processor protocol-processor third_party/verilog-axis | awk '{printf "%s=%s ", $4, $3}')"
  done
  echo "--- source-issue patch vs author 099e1911 + correction 2b200948 (issue files only)"
  AU=099e191137dd2797407fb8345a452bcc7a965608
  AB=b17580b91deb11f3441dfc5d7f9fafe539d929b8
  for f in docs/ENDSTATION_BUILDER.md sw/builder/endstation_builder.py sw/builder/test_builder.py; do
    echo "$f author-base->author: $(g diff $AB $AU -- $f | git patch-id --verbatim | cut -d' ' -f1) ; mb->source: $(g diff $mb $P -- $f | git patch-id --verbatim | cut -d' ' -f1)"
  done
} > "$out" 2>&1
cat "$out"
