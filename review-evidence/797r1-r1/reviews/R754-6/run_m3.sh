#!/bin/sh
# Extra mutant at head 2c500d0a: the write-answer clear of srp_fresh_r deleted
# (milan_csr.sv:3115), as opposed to m2's set-instead-of-clear. Want rc 1.
# Usage: run_m3.sh <packet-dir>   (scratch/t/head is a `git archive` of the head)
set -u
P=$1; S=$P/scratch; R=$P/receipts
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
rm -rf "$S/t/m3"; cp -r "$S/t/head" "$S/t/m3"
(cd "$S/t/m3" && patch -p1 < "$R/patches/m3.rtl.diff")
python3 -I "$S/t/m3/scripts/register_read_sweep.py" --work "$S/w/m3" > "$R/sweep_m3.log" 2>&1; echo $? > "$R/sweep_m3.rc"
