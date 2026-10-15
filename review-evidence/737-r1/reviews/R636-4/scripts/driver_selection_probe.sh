#!/bin/sh
# Exercise the builder driver's --list/--gates refusals before any gate runs.
# Usage: driver_selection_probe.sh <tree>   (prints one line per case: label rc first-stderr-line)
set -u
tree=$1
cd "$tree" || exit 2
D="python3 sw/builder/test_builder.py"
first=$($D --list | python3 -c 'import json,sys; n=json.load(sys.stdin); print(len(n), n[0], n[1], n[-1])')
set -- $first
count=$1; a=$2; b=$3; last=$4
echo "inventory $count first=$a second=$b last=$last"
probe() {
    label=$1; shift
    out=$(timeout 120 "$@" 2>&1 >/dev/null </dev/null); rc=$?
    echo "$label rc=$rc :: $(printf '%s' "$out" | tail -1 | cut -c1-160)"
}
probe unknown        $D --gates test_no_such_gate
probe repeated       $D --gates "$a,$a"
probe out-of-order   $D --gates "$b,$a"
probe empty          $D --gates ""
probe missing-value  $D --gates
probe flag-as-value  $D --gates --receipt x.json
probe known-and-unknown $D --gates "$a,test_no_such_gate"
