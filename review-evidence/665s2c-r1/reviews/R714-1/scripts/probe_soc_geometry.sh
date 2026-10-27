#!/bin/sh
# Planted-defect probe for sw/builder/test_soc_options.py at the reviewed head.
# Usage: probe_soc_geometry.sh <extracted head tree> <receipt dir>
# Each probe copies the tree, rewrites one line of sw/litex/milan_soc.py and
# runs the option test; rc 0 means the planted defect SURVIVED.
set -u
tree=$1
out=$2
probe() {
    label=$1; old=$2; new=$3
    dir=$(mktemp -d "${tree%/}.XXXX")
    cp -a "$tree/." "$dir/"
    python3 -I - "$dir/sw/litex/milan_soc.py" "$old" "$new" <<'EOF'
import sys
from pathlib import Path
p, old, new = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
s = p.read_text()
assert s.count(old) == 1, old
p.write_text(s.replace(old, new))
EOF
    python3 -B "$dir/sw/builder/test_soc_options.py" > "$out/probe-$label.log" 2>&1
    rc=$?
    echo "$label rc=$rc" | tee -a "$out/probe-soc-summary.txt"
    rm -rf "$dir"
}
: > "$out/probe-soc-summary.txt"
probe control "#: The split placement" "#: The split placement"
probe sets128 'CTRL_FETCH_L1 = (64, 1)' 'CTRL_FETCH_L1 = (128, 1)'
probe ways2 'CTRL_FETCH_L1 = (64, 1)' 'CTRL_FETCH_L1 = (64, 2)'
probe sets32 'CTRL_FETCH_L1 = (64, 1)' 'CTRL_FETCH_L1 = (32, 1)'
