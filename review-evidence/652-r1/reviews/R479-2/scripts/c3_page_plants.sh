#!/bin/sh
# Campaign 3: edits planted in a disposable copy's section 4.2 table; the real
# record-space gate (check 14) is run on each, then the copy is restored.
# Usage: c3_page_plants.sh <tree copy> <receipt dir>
T=$1; R=$2; mkdir -p "$R"
cd "$T" || exit 9
P=docs/design/SAVED_STATE_FASTCONNECT.md
git checkout -q -- . && test -z "$(git status --porcelain)" || exit 8
sed -n '/^| ids | group | block | index | 1x1 | 8x8 |$/,/^$/p' $P > "$R/c3_table_at_head.txt"
plant() { # id python-edit
  git checkout -q -- "$P"
  python3 - "$P" "$2" <<'EOF'
import sys
p, edit = sys.argv[1], sys.argv[2]
t = open(p).read()
head = "| ids | group | block | index | 1x1 | 8x8 |"
lines = t.split("\n")
i = lines.index(head) + 2
rows = {}
j = i
while lines[j].startswith("|"):
    rows[j] = lines[j]
    j += 1
def find(sub):
    hits = [k for k, v in rows.items() if sub in v]
    assert len(hits) == 1, (sub, hits)
    return hits[0]
exec(edit)
open(p, "w").write("\n".join(lines))
EOF
  { echo "plant $1: $2"; git diff -U0 -- "$P" | grep '^[-+]|'
    python3 scripts/check_nvm_record_space.py > .c3.log 2>&1; echo "check_nvm_record_space rc=$?"
    grep -E 'section 4.2' .c3.log | cut -c1-220; grep -c Traceback .c3.log | sed 's/^/tracebacks=/'
    echo; } >> "$R/c3_plants.txt"
  rm -f .c3.log
}
: > "$R/c3_plants.txt"
# p1 the R479-1 F1 reproduction: the user-name row loses its 8x8 figure
plant p1_short_user_name 'k=find("user name"); lines[k]=lines[k].rsplit("|",2)[0]+"|"'
# p2 the user-name row carries an extra cell past 8x8
plant p2_long_user_name 'k=find("user name"); lines[k]=lines[k]+" 107 |"'
# p3 the records row loses its 8x8 figure
plant p3_short_records 'k=find("records"); lines[k]=lines[k].rsplit("|",2)[0]+"|"'
# p4 the highest-id row loses its 1x1 figure (an interior cell, 8x8 shifts left)
plant p4_short_highest_1x1 'k=find("highest id"); c=lines[k].split("|"); del c[5]; lines[k]="|".join(c)'
# p5 a group row whose 8x8 cell is emptied (cell kept, figure gone)
plant p5_empty_8x8 'k=find("user name"); c=lines[k].split("|"); c[-2]="  "; lines[k]="|".join(c)'
# p6 the records row deleted outright (a total the table stops stating)
plant p6_records_row_deleted 'k=find("records"); del lines[k]'
# p7 a group row deleted outright
plant p7_user_name_row_deleted 'k=find("user name"); del lines[k]'
# p8 the block column dropped from the user-name row (figures shift left one)
plant p8_short_block 'k=find("user name"); c=lines[k].split("|"); del c[3]; lines[k]="|".join(c)'
git checkout -q -- . && test -z "$(git status --porcelain)" && echo "restored clean" >> "$R/c3_plants.txt"
echo done > "$R/c3.done"
