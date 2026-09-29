#!/usr/bin/env bash
# [A447] Round 3 of PR #622: literal diff of every Markdown table line (a line
# starting with '|') on both findings pages at the round-2 and round-3 heads,
# and in the round-2 PR body against the proposed round-3 body.
# Usage: table_lines_diff_b2r3.sh <clone> <old-rev> <new-rev> <old-body.md> <new-body.md> <scratch-dir>
set -u
clone=$1; old=$2; new=$3; oldbody=$4; newbody=$5; s=$6
mkdir -p "$s"
worst=0
for p in docs/findings/606_FIRST_BIND_MEASUREMENT.md docs/findings/608_75_WITHDRAWAL_AND_RESTART.md; do
  n=$(basename "$p" .md)
  git -C "$clone" show "$old:$p" > "$s/$n.old.md"
  git -C "$clone" show "$new:$p" > "$s/$n.new.md"
  grep '^|' "$s/$n.old.md" > "$s/$n.old.tables"
  grep '^|' "$s/$n.new.md" > "$s/$n.new.tables"
  diff "$s/$n.old.tables" "$s/$n.new.tables" > "$s/$n.tables.diff"; rc=$?
  [ $rc -gt $worst ] && worst=$rc
  echo "$p: $(wc -l < "$s/$n.old.tables") table lines at old, $(wc -l < "$s/$n.new.tables") at new," \
       "sha256 old $(sha256sum < "$s/$n.old.tables" | cut -d' ' -f1) new $(sha256sum < "$s/$n.new.tables" | cut -d' ' -f1)," \
       "diff rc=$rc, diff lines $(wc -l < "$s/$n.tables.diff")"
done
tr -d '\r' < "$oldbody" | grep '^|' > "$s/body.old.tables"
tr -d '\r' < "$newbody" | grep '^|' > "$s/body.new.tables"
diff "$s/body.old.tables" "$s/body.new.tables" > "$s/body.tables.diff"; rc=$?
[ $rc -gt $worst ] && worst=$rc
echo "PR body: $(wc -l < "$s/body.old.tables") table lines in the round-2 body, $(wc -l < "$s/body.new.tables") in the round-3 body," \
     "sha256 old $(sha256sum < "$s/body.old.tables" | cut -d' ' -f1) new $(sha256sum < "$s/body.new.tables" | cut -d' ' -f1)," \
     "diff rc=$rc, diff lines $(wc -l < "$s/body.tables.diff")"
echo "page diff (all lines, old..new), for reference:"
for p in docs/findings/606_FIRST_BIND_MEASUREMENT.md docs/findings/608_75_WITHDRAWAL_AND_RESTART.md; do
  git -C "$clone" diff --numstat "$old" "$new" -- "$p"
  echo "  changed lines starting with '|': $(git -C "$clone" diff -U0 "$old" "$new" -- "$p" | grep -c '^[-+]|')"
done
echo "worst rc=$worst"
exit $worst
