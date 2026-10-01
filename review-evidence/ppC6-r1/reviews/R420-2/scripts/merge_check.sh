#!/usr/bin/env bash
# R420-2: does merge a011b14 keep both sides? Usage: merge_check.sh <clone> <workdir>
set -u
C=$1; W=$2; mkdir -p "$W"; cd "$C" || exit 2
LANE=5e806296b73d04ccf095ad00e081cb790fbbaf8d; MAIN=3f3ea56ba61829718a6a288600ab4fdac73aa5ba; M=a011b14
MB=$(git merge-base $LANE $MAIN); echo "merge-base $MB; merge parents: $(git log -1 --format=%P $M)"
git diff --name-only $MB $MAIN | sort > "$W/main.txt"; git diff --name-only $MB $LANE | sort > "$W/lane.txt"
echo "main changed $(wc -l < "$W/main.txt") files, lane changed $(wc -l < "$W/lane.txt")"
n=0; for f in $(comm -23 "$W/main.txt" "$W/lane.txt"); do [ "$(git rev-parse $M:$f 2>/dev/null)" = "$(git rev-parse $MAIN:$f 2>/dev/null)" ] || { echo "MAIN-ONLY DIFFERS $f"; n=$((n+1)); }; done; echo "main-only files differing from main at the merge: $n"
n=0; for f in $(comm -13 "$W/main.txt" "$W/lane.txt"); do [ "$(git rev-parse $M:$f 2>/dev/null)" = "$(git rev-parse $LANE:$f 2>/dev/null)" ] || { echo "LANE-ONLY DIFFERS $f"; n=$((n+1)); }; done; echo "lane-only files differing from the lane at the merge: $n"
for f in $(comm -12 "$W/main.txt" "$W/lane.txt"); do b=$(echo $f | tr / _)
  git show $MB:$f > "$W/$b.base"; git show $LANE:$f > "$W/$b.lane"; git show $MAIN:$f > "$W/$b.main"; git show $M:$f > "$W/$b.merged"
  git merge-file -p "$W/$b.lane" "$W/$b.base" "$W/$b.main" > "$W/$b.re"; rc=$?
  if cmp -s "$W/$b.re" "$W/$b.merged"; then echo "SHARED $f: clean 3-way, merged == reproduction"; else echo "SHARED $f: $rc conflict region(s); resolution inspected by hand"; fi
done
