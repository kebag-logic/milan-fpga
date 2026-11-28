#!/bin/sh
# Usage: run_validate.sh <clone> <work> <jobs> <log> <rcfile>
. "$(dirname "$0")/env.sh"
cd "$1" || exit 2
python3 scripts/validate.py --work "$2" --jobs "$3" > "$4" 2>&1
echo $? > "$5"
