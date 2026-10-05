#!/bin/sh
# Delta checks for 356c1bba..80b3c1b2 in the review clone CLONE; disposable work in SCRATCH.
# Usage: delta_identity.sh CLONE SCRATCH
set -u
C=$1 S=$2
OLD=356c1bbad2e9838659b433736040acf0cc4abf3e NEW=80b3c1b223aaad05f428164cd56595a4c1187509
BED=bed5f47785839800bb640d7c747f5435f84ab5a3
PATCH=tb/pp_top/ctr_mutations/ctr-notify-one-window.patch
NOTIFY=hdl/aecp/KL_aecp_notify.sv
g() { git -C "$C" "$@"; }
echo "== head, tree, parent"
g rev-parse $NEW $NEW^{tree} $NEW^@
echo "== files changed $OLD..$NEW (raw, numstat)"
g diff --raw $OLD $NEW; g diff --numstat $OLD $NEW
echo "== git diff --check"; g diff --check $OLD $NEW && echo clean
echo "== blob of the patch: base, bed5f477, 356c1bba, head"
for r in 07b1469ddf1e2a54e4a42cac06c41f084ecffd6c $BED $OLD $NEW; do echo "$r $(g rev-parse $r:$PATCH)"; done
echo "== blob of $NOTIFY: bed5f477, 356c1bba, head"
for r in $BED $OLD $NEW; do echo "$r $(g rev-parse $r:$NOTIFY)"; done
rm -rf "$S/delta"; mkdir -p "$S/delta"
g show $BED:$PATCH > "$S/delta/old.patch"; g show $NEW:$PATCH > "$S/delta/new.patch"
echo "== the patch's -/+ lines, old vs new (must be identical)"
grep -E '^[-+][^-+]|^[-+]$' "$S/delta/old.patch" > "$S/delta/old.pm"
grep -E '^[-+][^-+]|^[-+]$' "$S/delta/new.patch" > "$S/delta/new.pm"
cmp "$S/delta/old.pm" "$S/delta/new.pm" && echo "identical: $(wc -l < "$S/delta/new.pm") lines"
echo "== hunk header arithmetic of the new patch"
awk '/^@@/{h=$0; next} /^(---|\+\+\+) /{next} /^ /{o++; n++} /^-/{o++} /^\+/{n++} END{print h; print "old lines " o ", new lines " n}' "$S/delta/new.patch"
echo "== CR bytes / final newline in the new patch"
printf 'CR bytes: %s\n' "$(tr -cd '\r' < "$S/delta/new.patch" | wc -c)"; tail -c1 "$S/delta/new.patch" | od -An -c
echo "== plant both: old patch at bed5f477, new patch at head (outside any work tree)"
for side in bed:$BED:old head:$NEW:new; do
  name=${side%%:*}; rest=${side#*:}; rev=${rest%%:*}; p=${rest#*:}
  mkdir -p "$S/delta/$name"; g show $rev:$NOTIFY > "$S/delta/$name/orig.sv"
  mkdir -p "$S/delta/$name/t/hdl/aecp"; cp "$S/delta/$name/orig.sv" "$S/delta/$name/t/$NOTIFY"
  (cd "$S/delta/$name/t" && git apply -v "$S/delta/$p.patch") 2>&1
  echo "rc=$?"; sha256sum "$S/delta/$name/t/$NOTIFY"
done
echo "== planted(bed5f477) vs planted(head) must differ exactly as the unplanted files do"
diff "$S/delta/bed/t/$NOTIFY" "$S/delta/head/t/$NOTIFY" > "$S/delta/planted.diff"
diff "$S/delta/bed/orig.sv" "$S/delta/head/orig.sv" > "$S/delta/orig.diff"
sed 's/^[0-9,]*c[0-9,]*$/HUNK/' "$S/delta/planted.diff" > "$S/delta/planted.n"
sed 's/^[0-9,]*c[0-9,]*$/HUNK/' "$S/delta/orig.diff" > "$S/delta/orig.n"
cat "$S/delta/orig.diff"
cmp "$S/delta/planted.n" "$S/delta/orig.n" && echo "same change, modulo hunk line numbers"
echo "== planted head file, comment-stripped, equals planted bed5f477 file, comment-stripped"
for name in bed head; do sed -e 's#//.*$##' -e 's/[[:space:]]*$//' "$S/delta/$name/t/$NOTIFY" | grep -v '^$' > "$S/delta/$name.stripped"; done
cmp "$S/delta/bed.stripped" "$S/delta/head.stripped" && echo identical
echo "== the patch's hunk, located at the head"
grep -n "Provisional stamp: it keeps the window shut" "$S/delta/head/orig.sv"
