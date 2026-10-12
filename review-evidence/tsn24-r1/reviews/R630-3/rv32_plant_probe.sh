#!/bin/sh
# SPDX-License-Identifier: MIT
# Reviewer probe: the RV32 smoke image must fail when the generated freshness
# value or the core's answer record is planted, proving the bare-metal target
# executes the positive DA-freshness path.
# usage: rv32_plant_probe.sh <repo> <rev> <work>
set -u
repo=$1; rev=$2; work=$3
mkdir -p "$work"
run() {
	name=$1; file=$2; old=$3; new=$4
	dir="$work/$name"; rm -rf "$dir"; mkdir -p "$dir/tree"
	git -C "$repo" archive "$rev" | tar -x -C "$dir/tree"
	python3 - "$dir/tree/$file" "$old" "$new" <<'EOF'
import sys
p, old, new = sys.argv[1], sys.argv[2].encode().decode('unicode_escape'), sys.argv[3].encode().decode('unicode_escape')
t = open(p).read()
assert t.count(old) == 1, 'anchor count %d' % t.count(old)
open(p, 'w').write(t.replace(old, new))
EOF
	(cd "$dir/tree" && python3 scripts/baremetal.py --work "$dir/build" --jobs 2 > "$dir/baremetal.log" 2>&1)
	rc=$?
	smoke=$(cat "$dir"/build/*/smoke.log 2>/dev/null | tr '\n' ' ')
	echo "$name baremetal_rc=$rc smoke=[$smoke]"
}
run control src/acmp.c 's->answered = true;' 's->answered = true;'
run rv32-generated-window examples/entities/talker/entity_config.c '.da_fresh_ms = 15000u,' '.da_fresh_ms = 15001u,'
run rv32-answer-not-recorded src/acmp.c '\t\ts->answered = true;\n' ''
