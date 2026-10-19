#!/bin/sh
# usage: builder_b.sh <tree> <logdir>
# Runs test_baremetal_profile_contract alone (builder leg 0, the parent's own
# measured isolated gate) with the driver's own --receipt.
tree=$1; logdir=$2
mkdir -p "$logdir"
export PATH=<pinned-tools>:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR_ROOT=<pinned-tools>/usr/share/verilator
export TMPDIR=<scratch>/tmpdir
cd "$tree" || exit 2
rm -f "$logdir/receipt-b.json"
s=$(date +%s)
python3 sw/builder/test_builder.py --gates test_baremetal_profile_contract --receipt "$logdir/receipt-b.json" > "$logdir/leg-b.log" 2>&1
echo "b rc=$? secs=$(( $(date +%s) - s ))" > "$logdir/leg-b.rc"
