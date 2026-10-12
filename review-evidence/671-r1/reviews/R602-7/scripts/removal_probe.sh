#!/bin/sh
# Remove one term from the firmware's refused-read comparison in a disposable
# copy of the head and run the ordinary writer gate on the 8x8 shape.
# Usage: removal_probe.sh <disposable-tree> trailer|prefix <log>
# The tree must be a git-backed export of the head with its submodule trees.
# Expected: rc 1 and exactly 32 findings "which differ only in their <term>".
set -u
tree=$1; term=$2; log=$3
f=sw/firmware/milan_baremetal/milan_baremetal.c
case "$term" in
  trailer) sed -i 's/^\t       a\.tail == b\.tail;$/\t       1;/' "$tree/$f" ;;
  prefix)  sed -i 's/a\.digest == b\.digest \&\&$/1 \&\&/' "$tree/$f" ;;
  *) echo "unknown term $term"; exit 2 ;;
esac
cd "$tree" || exit 2
PYTHONHASHSEED=0 python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py \
  --config configs/endstation_ax7101_8x8.yaml --jobs 7 > "$log" 2>&1
echo "rc=$?" >> "$log"
grep -o "which differ only in their [a-zA-Z ]*:" "$log" | sort | uniq -c
