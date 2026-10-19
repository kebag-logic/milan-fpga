#!/bin/sh
# usage: builder_rest.sh <limit-secs> <tree>:<logdir> [<tree>:<logdir> ...]
# Runs every builder gate except test_baremetal_profile_contract (which ran
# as its own leg) as ONE leg per tree, trees in parallel, each leg writing
# the driver's own --receipt. One tree never runs two legs at once.
limit=$1; shift
export PATH=<pinned-tools>:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR_ROOT=<pinned-tools>/usr/share/verilator
export TMPDIR=<scratch>/tmpdir
for pair in "$@"; do
  tree=${pair%%:*}; logdir=${pair#*:}
  mkdir -p "$logdir"
  (
    cd "$tree" || exit 2
    python3 sw/builder/test_builder.py --list > "$logdir/inventory.json"
    gates=$(python3 -I -c 'import json,sys; print(",".join(n for n in json.load(open(sys.argv[1])) if n != "test_baremetal_profile_contract"))' "$logdir/inventory.json")
    rm -f "$logdir/receipt-r.json"
    s=$(date +%s)
    timeout "$limit" python3 sw/builder/test_builder.py --gates "$gates" --receipt "$logdir/receipt-r.json" > "$logdir/leg-r.log" 2>&1
    echo "r rc=$? secs=$(( $(date +%s) - s ))" > "$logdir/leg-r.rc"
  ) &
done
wait
for pair in "$@"; do echo "${pair#*:}: $(cat "${pair#*:}/leg-r.rc")"; done
