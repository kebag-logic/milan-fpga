#!/usr/bin/env bash
# Usage: check_patches.sh REPO PATCH_DIR WORK
# For each of the eight parent patches: (a) applies alone at base d77a8afd;
# (b) its commit's diff is byte-identical (modulo index lines) to the patch's diff;
# (c) applying all eight in commit order to the base yields the head's bytes.
set -u
REPO=$1; PD=$2; W=$3; BASE=d77a8afdbc960d70d1ceeee9af1163624f102b16; HEAD=a97aea01449492b1f640924f5a34726f602cabed
FILES="scripts/measure_test_evidence_readers.py tb/verilator/milan_dp/sim_nxn.cpp hdl/milan/KL_pp_shadow.sv tb/verilator/milan_dp/README.md tb/verilator/gptp_shadow/sim_main.cpp tb/verilator/milan_dp/sim_ax1x1gptp.cpp tb/verilator/milan_dp/sim_gptp.cpp"
ORDER="8144d2885:parent-evidence-classification 2dc612fbd:parent-adoption-milan_dp-67 c6afca8ce:parent-scratch-tspec-every-slot 300911eaf:parent-adoption-milan_dp-gsi-g9 1e305876b:parent-adoption-gptp_shadow-85 d255806ce:parent-adoption-milan_dp-85 7d9d730c6:parent-adoption-milan_dp-82 0e4d10b25:parent-adoption-milan_dp_gptp-84"
rm -rf "$W"; mkdir -p "$W"
extract() { # rev dir
  mkdir -p "$2"; git -C "$REPO" archive "$1" $FILES | tar -x -C "$2"; }
strip() { grep -vE '^(index |From |Date: |Subject: |commit |Author: )' | sed -n '/^diff --git/,$p'; }
rc=0
for e in $ORDER; do c=${e%%:*}; p=$PD/${e#*:}.patch
  d=$W/alone_${e#*:}; extract $BASE $d
  if (cd $d && git apply --check -p1 "$p" 2>/dev/null); then a=ALONE_OK; else a=ALONE_FAIL; rc=1; fi
  d2=$W/parent_${e#*:}; extract $c^ $d2
  if (cd $d2 && git apply -p1 "$p" 2>/dev/null); then
     extract $c $W/commit_${e#*:}
     if diff -r $d2 $W/commit_${e#*:} >/dev/null; then b=COMMIT_EQUALS_PATCH_ON_PARENT; else b=COMMIT_DIFFERS; rc=1; fi
  else b=NOT_APPLY_ON_COMMIT_PARENT; rc=1; fi
  echo "$c ${e#*:} $a $b"
done
seq=$W/sequence; extract $BASE $seq
for e in $ORDER; do p=$PD/${e#*:}.patch; (cd $seq && git apply -p1 "$p") || { echo "SEQ_FAIL ${e#*:}"; rc=1; }; done
extract $HEAD $W/head
if diff -r $seq $W/head >/dev/null; then echo "SEQUENCE_EQUALS_HEAD for: $FILES"; else echo SEQUENCE_DIFFERS_FROM_HEAD; diff -r $seq $W/head | head -20; rc=1; fi
exit $rc
