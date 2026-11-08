#!/bin/sh
# Usage: run_validate.sh <clone> <workroot> <receipts>; runs the full validation kit with log and rc.
set -u
C=$1; W=$2; R=$3; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$W" "$R"
cd "$C"
python3 scripts/validate.py --work "$W/build-validation" --jobs 16 --graphs > "$R/validate.out" 2>&1; echo $? > "$R/validate.rc"
