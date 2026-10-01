#!/usr/bin/env bash
# R426-3: run the page's two reproduction commands in a fresh clone, as the page
# instructs. Usage: reproduce.sh <local-source-repo> <work-dir> <page-head>
# The clone is taken from a local repo for speed; origin is then pointed at the
# public repository so `git fetch origin b6-review-evidence` runs as written.
# The only deviation from the page: /tmp/ outputs go to <work-dir>/out/.
set -u
src=$1; work=$2; head=$3
rm -rf "$work"; mkdir -p "$work/out"
git clone -q --no-checkout "$src" "$work/clone"
cd "$work/clone"
git remote set-url origin https://github.com/kebag-logic/milan-fpga.git
git checkout -q --detach "$head"
echo "clone head: $(git rev-parse HEAD)"
echo "python: $(python3 --version 2>&1), numpy: $(python3 -c 'import numpy; print(numpy.__version__)')"
# Commands as on the page (lines extracted from the page itself)
cmds=$(awk '/^```sh$/{f=1;next} /^```$/{f=0} f' docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md | sed "s#/tmp/#$work/out/#g")
printf '%s\n' "--- commands as run:" "$cmds" "---"
bash -c "set -e; $cmds"
rc=$?
echo "commands rc=$rc"
echo "staged after checkout: $(git diff --cached --name-only | wc -l) paths (the page's warning)"
page_hash=$(grep -o 'Tone loop (`b6_tone.py`) | [0-9,]* | `[0-9a-f]*`' docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md | grep -o '[0-9a-f]\{64\}')
got=$(sha256sum "$work/out/b6-loop.bin" | cut -d' ' -f1)
echo "page tone hash:  $page_hash"
echo "regenerated:     $got  bytes $(stat -c %s "$work/out/b6-loop.bin")"
[ "$page_hash" = "$got" ] && echo "TONE MATCH" || { echo "TONE MISMATCH"; rc=1; }
cmp "$work/out/b6-controls.json" review-evidence/b6-r1/author/controls/controls.json && echo "CONTROLS BYTE-IDENTICAL ($(sha256sum "$work/out/b6-controls.json" | cut -d' ' -f1))" || rc=1
echo "RESULT rc=$rc"
exit $rc
