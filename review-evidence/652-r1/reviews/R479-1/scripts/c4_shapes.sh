#!/bin/sh
# Campaign 4: the resmap `shapes` step on the real plan at the head, and with
# one expect mark removed (must fail), in a disposable tree copy.
# Usage: c4_shapes.sh <head tree> <receipt dir> <work root>
H=$1; R=$2; W=$3; mkdir -p "$R"; rm -rf "$W"; mkdir -p "$W"
cd "$H" || exit 9
python3 syn/resmap/yosys_sweep.py --work "$W/real" shapes > "$R/c4_shapes_real.log" 2>&1; echo $? > "$R/c4_shapes_real.rc"
cp "$W/real/shapes/outcomes.json" "$R/c4_outcomes_real.json" 2>/dev/null
# probe: the 2ch 235-name variant not marked: the step must fail on it
python3 - "$W" <<'EOF' > "$R/c4_shapes_unmarked.log" 2>&1
import sys, json, pathlib
sys.path.insert(0, 'syn/resmap')
import yosys_sweep as y
work = pathlib.Path(sys.argv[1])
p = json.load(open('syn/resmap/sweep_plan.json'))
del p['variants']['rm_ax7101_8x8_tdm8_2ch']['expect']
(work / 'plan_unmarked.json').write_text(json.dumps(p, indent=1))
plan = y.load_plan(work / 'plan_unmarked.json')
rc = y.command_shapes(work / 'unmarked', plan)
print('command_shapes rc', rc)
sys.exit(rc)
EOF
echo $? > "$R/c4_shapes_unmarked.rc"
git status --porcelain > "$R/c4_status_after.txt"
echo done > "$R/c4.done"
