#!/usr/bin/env bash
# Reviewer probe (R238-5): what the generator does with a tracked page that
# the renderer withholds without refusals() naming it (a text spelling of the
# position attribute through a backslash escape, and one line nested 201
# block quotes deep). Usage: probe_unnamed_withheld_write.sh <python> <tree>
# <workdir>, where <tree> is an export of the head with its index populated.
set -uo pipefail
py=$1; tree=$2; work=$3
rm -rf "$work"; cp -a "$tree" "$work"; cd "$work"
printf "\n<h2 title='\n\nz' data\\\\-sourcepos=1:1-1:1 y\n" >> docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md
printf '\n%s deep\n' "$(printf '>%.0s' $(seq 201))" >> docs/testing/TESTING.md
git add -A
echo "### gen_toc.py --check"; "$py" scripts/gen_toc.py --check 2>&1 | grep -v RuntimeWarning | tail -5
echo "rc=${PIPESTATUS[0]}"
echo "### gen_toc.py --write"; "$py" scripts/gen_toc.py --write 2>&1 | grep -v RuntimeWarning | tail -2
echo "### lines --write removed per page"; git diff --numstat
echo "### Contents headings removed"; git diff | grep -c '^-## Contents'
