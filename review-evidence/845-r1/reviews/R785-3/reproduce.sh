#!/bin/sh
# Re-run the R785-3 delta checks. Usage: reproduce.sh <clone-at-43410ce1> <out-dir>
set -eu
R=$1; O=$2; mkdir -p "$O"; H=$(cd "$(dirname "$0")" && pwd)
cd "$R"
MB=$(git merge-base 853ca25a 697e17a4)
git diff --name-only "$MB" 697e17a4 | sort > "$O/side849_paths.txt"
git diff --name-only 87e9d03a 853ca25a | sort > "$O/pr847_paths.txt"
git diff --name-only 853ca25a 43410ce1 | sort > "$O/delta_paths.txt"
echo "delta outside #849 side:"; comm -23 "$O/delta_paths.txt" "$O/side849_paths.txt"
echo "#847 files in delta:"; comm -12 "$O/delta_paths.txt" "$O/pr847_paths.txt"
while read f; do
  [ "$(git rev-parse -q --verify 43410ce1:"$f")" = "$(git rev-parse -q --verify 697e17a4:"$f")" ] && echo "EQ849 $f" || echo "DIFF849 $f"
done < "$O/delta_paths.txt" > "$O/path_blob_check.txt"
f=tb/verilator/milan_dp/README.md
git show 853ca25a:$f > "$O/o"; git show 87e9d03a:$f > "$O/b"; git show 697e17a4:$f > "$O/t"
git merge-file -p "$O/o" "$O/b" "$O/t" > "$O/m"; git show 43410ce1:$f | cmp - "$O/m" && echo README_CLEAN_3WAY_EQUAL
python3 -I "$H/check_changelog.py" "$R" 43410ce1 853ca25a 697e17a4
python3 -I scripts/docs_inventory.py --check
