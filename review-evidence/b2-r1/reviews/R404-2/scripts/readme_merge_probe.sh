#!/usr/bin/env bash
# Trial three-way merge of docs/findings/README.md: base 13eda870, ours = PR head,
# theirs = live dev. Usage: readme_merge_probe.sh <clone> <live-dev-sha> <workdir>
set -u; c=$1; dev=$2; w=$3; mkdir -p "$w"
git -C "$c" show 13eda870d1a6cf3f946fc228a98862366b08d102:docs/findings/README.md > "$w/base.md"
git -C "$c" show HEAD:docs/findings/README.md > "$w/ours.md"
gh api "repos/kebag-logic/milan-fpga/contents/docs/findings/README.md?ref=$dev" --jq .content | base64 -d > "$w/theirs.md"
sha256sum "$w/base.md" "$w/ours.md" "$w/theirs.md" | sed "s#$w/##"
git merge-file -p "$w/ours.md" "$w/base.md" "$w/theirs.md" > "$w/merged.md"; echo "merge-file conflicts: $?"
grep -n '^<<<<<<<\|^=======\|^>>>>>>>' "$w/merged.md" | sed 's/ .*//'
diff "$w/base.md" "$w/theirs.md" | grep '^[<>]' | cut -c1-80
