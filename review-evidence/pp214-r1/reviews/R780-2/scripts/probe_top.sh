#!/bin/bash
# Usage: probe_top.sh CLONE WORKDIR NAME 'old' 'new' RECEIPT
# One disposable arm through the whole tb/srp_top suite in a scratch copy.
set -u
clone=$1; work=$2; name=$3; old=$4; new=$5; receipt=$6
rm -rf "$work/$name"; mkdir -p "$work/$name/tb"
cp -a "$clone/hdl" "$work/$name/hdl"
for s in common srp_top; do cp -a "$clone/tb/$s" "$work/$name/tb/$s"; done
if [ "$old" != "NONE" ]; then
  OLD="$old" NEW="$new" F="$work/$name/hdl/srp/KL_srp_encoder.sv" python3 -I -c '
import os
f=os.environ["F"]; t=open(f).read(); o=os.environ["OLD"].encode().decode("unicode_escape")
n=os.environ["NEW"].encode().decode("unicode_escape")
assert t.count(o)==1, "drift"
open(f,"w").write(t.replace(o,n))'
fi
make -C "$work/$name/tb/srp_top" > "$receipt" 2>&1
echo $? > "$receipt.rc"
