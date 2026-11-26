#!/bin/bash
# delta_check.sh CLONE OLD NEW: read-only checks of a one-commit delta.
# Prints the raw diff, proves every changed line in the C++ file is a whole-line
# comment, lists gitlinks at both heads, and lists any non-ASCII added byte.
set -u
C=$1; OLD=$2; NEW=$3
g() { git -C "$C" "$@"; }
echo "# delta $OLD..$NEW in $(g rev-parse --show-toplevel | sed 's|.*/||')"
echo "== commits"; g log --format='%H %P%n  subject: %s%n  body-lines: %b' "$OLD..$NEW" | sed 's/body-lines: $/body-lines: (none)/'
echo "== raw diff"; g diff --raw "$OLD" "$NEW"
echo "== changed C++ lines that are not whole-line // comments (must be empty)"
g diff -U0 "$OLD" "$NEW" -- '*.cpp' '*.h' '*.sv' '*.py' | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' | grep -vE '^[+-][[:space:]]*//' || echo "(none)"
echo "== comment-stripped C++ files identical at both heads"
for f in $(g diff --name-only "$OLD" "$NEW" -- '*.cpp'); do
  a=$(g show "$OLD:$f" | sed -E 's#^[[:space:]]*//.*$##' | sha256sum | cut -c1-16)
  b=$(g show "$NEW:$f" | sed -E 's#^[[:space:]]*//.*$##' | grep -v '^$' | sha256sum | cut -c1-16)
  a2=$(g show "$OLD:$f" | sed -E 's#^[[:space:]]*//.*$##' | grep -v '^$' | sha256sum | cut -c1-16)
  echo "$f old=$a2 new=$b $([ "$a2" = "$b" ] && echo EQUAL || echo DIFFERENT)"
done
echo "== gitlinks"
for r in "$OLD" "$NEW"; do echo "-- $r"; g ls-tree -r "$r" | awk '$2=="commit"{print $3, $4}'; done
echo "== non-ASCII bytes in added lines (must be empty)"
g diff "$OLD" "$NEW" | grep '^+' | grep -v '^+++' | LC_ALL=C grep -nP '[^\x00-\x7F]' || echo "(none)"
echo "== image-input paths touched (must be empty)"
g diff --name-only "$OLD" "$NEW" -- hdl syn sw configs constraints avdecc gptp-processor protocol-processor external third_party || true
echo "(end)"
