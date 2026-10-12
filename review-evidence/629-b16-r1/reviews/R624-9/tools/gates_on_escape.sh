#!/usr/bin/env bash
# R624-9: do the repository's own documentation gates stop the email-autolink escape?
# usage: gates_on_escape.sh <repo at the head> <probe case dir> <parser python> <scratch tree dir> <out log>
# Exports the head's tree (git archive, no .git), replaces the findings page and index with the probe's
# altered copies, commits them in a throwaway local repository, and runs the docs gates that need no git base. Offline.
set -u
repo=$1 case_dir=$2 py=$3 tree=$4 log=$5
rm -rf "$tree" && mkdir -p "$tree"
git -C "$repo" archive HEAD | tar -x -C "$tree"
cp "$case_dir/629_MEDIA_CLOCK_FOLLOWING_BENCH.md" "$tree/docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
cp "$case_dir/README.md" "$tree/docs/findings/README.md"
# a throwaway index so the gates that list files with git ls-files can run; never pushed
git -C "$tree" init -q && git -C "$tree" add -A && git -C "$tree" -c user.name=probe -c user.email=probe@invalid commit -q -m probe
: > "$log"
for gate in "scripts/docs_check.py" "scripts/check_doc_style.py" "scripts/gen_toc.py --check" \
            "scripts/gen_toc.py --verify-anchors" "scripts/check_doc_paths.py"; do
  (cd "$tree" && $py -I $gate > "$tree/.gate.out" 2>&1; echo "rc=$? $gate" >> "$log"; tail -n 3 "$tree/.gate.out" | sed 's/^/    /' >> "$log")
done
cat "$log"
