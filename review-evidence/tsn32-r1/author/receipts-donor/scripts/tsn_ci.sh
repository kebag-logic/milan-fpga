#!/bin/bash
# The TSN stack's two testing run: steps on a clean clone of a commit (quality.yml), one log and rc each.
# usage: tsn_ci.sh COMMIT OUT
set -u
C=$1 O=$2
. <scratch>/scripts/tsn_env.sh
rm -rf "$O"; mkdir -p "$O"
git clone -q --no-local <lanes>/tsn-c-stack-32-walk "$O/src" && git -C "$O/src" checkout -q --detach "$C"
cd "$O/src" || exit 3
{ git rev-parse HEAD; git status --porcelain --untracked-files=all | wc -l; } > "$O/before.txt"
start=$(date +%s)
python3 scripts/validate.py --work "$O/build-validation" --jobs 12 --graphs > "$O/validate.log" 2>&1; echo $? > "$O/validate.rc"
echo "validate elapsed=$(( $(date +%s) - start ))s" >> "$O/times.txt"
start=$(date +%s)
python3 scripts/baremetal.py --work "$O/build-rv32" --jobs 12 > "$O/baremetal.log" 2>&1; echo $? > "$O/baremetal.rc"
echo "baremetal elapsed=$(( $(date +%s) - start ))s" >> "$O/times.txt"
{ git rev-parse HEAD; git status --porcelain --untracked-files=all | wc -l; } > "$O/after.txt"
