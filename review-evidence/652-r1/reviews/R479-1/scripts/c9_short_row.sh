#!/bin/sh
# Finding F1 receipt: drop the 8x8 figure from section 4.2's user-name row in a
# disposable copy of the head; record check_nvm_record_space (check 14) and the
# docs gates, then restore the copy.
# Usage: c9_short_row.sh <tree copy> <receipt file> <python with the pinned Markdown renderer>
T=$1; OUT=$2; PY=$3
cd "$T" || exit 9
git checkout -q -- . && test -z "$(git status --porcelain)" || exit 8
python3 - <<'EOF'
p = 'docs/design/SAVED_STATE_FASTCONNECT.md'
t = open(p).read()
row = "| `0x80` .. `0xFF` | user name | 128 | name ordinal | 39 | **107** |"
assert t.count(row) == 1
open(p, 'w').write(t.replace(row, "| `0x80` .. `0xFF` | user name | 128 | name ordinal | 39 |"))
EOF
{
  echo "head $(git rev-parse HEAD)"; git diff
  python3 scripts/check_nvm_record_space.py > .r.log 2>&1; echo "check_nvm_record_space rc=$?"; grep -E "section 4.2|finding\(s\)" .r.log | cut -c1-200
  for g in docs_check.py check_doc_style.py "gen_toc.py --check"; do
    $PY scripts/$g > .r.log 2>&1; echo "$g rc=$?"; grep -v RuntimeWarning .r.log | tail -1
  done
  rm -f .r.log
} > "$OUT" 2>&1
git checkout -q -- . && test -z "$(git status --porcelain)" && echo "restored" >> "$OUT"
