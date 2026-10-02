#!/usr/bin/env bash
# Run every plant of one reviewer plant script against <head-tree>, JOBS at a time.
# Usage: run_plants.sh <plant-script> <head-tree> <work-dir> <jobs> > receipt
set -u
script=$1 head=$2 work=$3 jobs=$4
mkdir -p "$work"
python3 - "$script" <<'EOF' | xargs -P "$jobs" -I{} python3 -B "$script" "$head" "$work" {}
import re, sys
for name in re.findall(r'^ "([^"]+)":', open(sys.argv[1]).read(), re.M):
    print(name)
EOF
