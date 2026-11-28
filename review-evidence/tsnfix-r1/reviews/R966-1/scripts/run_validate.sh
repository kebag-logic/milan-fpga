#!/bin/sh
# Run the repository's full validation kit (the quality job's command) at the checked-out head.
# usage: run_validate.sh <clone> <workdir> <jobs>
set -u
here=$(cd "$(dirname "$0")" && pwd)
. "$here/env.sh"
clone=$1; work=$2; jobs=$3
cd "$clone" || exit 2
git rev-parse HEAD > "$work.head"
date -u +%FT%TZ > "$work.start"
python3 scripts/validate.py --work "$work" --jobs "$jobs" --graphs > "$work.stdout" 2>&1
echo $? > "$work.rc"
date -u +%FT%TZ > "$work.end"
