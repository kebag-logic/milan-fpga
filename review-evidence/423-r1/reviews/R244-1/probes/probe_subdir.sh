#!/bin/sh
# Probe: does running the checker from a subdirectory change verdicts?
# Usage: probe_subdir.sh <checker.py> <workdir>
set -eu
CHECKER=$1; W=$2
rm -rf "$W"; mkdir -p "$W"; cd "$W"
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
g() { git -c user.name=F -c user.email=f@example.invalid -c commit.gpgsign=false "$@"; }
g init -q -b main
mkdir sub; printf 'sub\n' > sub/f; printf 'top\n' > top.txt
g add -A; g commit -qm base
g checkout -qb pr
printf 'top changed by pr\n' > top.txt
g commit -qam 'pr edits top'
g checkout -q main
printf 'unrelated\n' > other.txt; g add -A; g commit -qm 'unrelated main work'
echo "== linear stranded, from root"
python3 "$CHECKER" --no-fetch --base main pr && echo rc=0 || echo "rc=$?"
echo "== linear stranded, from sub/"
(cd sub && python3 "$CHECKER" --no-fetch --base main pr && echo rc=0 || echo "rc=$?")
