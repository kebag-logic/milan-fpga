#!/usr/bin/env bash
# Compare linked RV32 image hashes: ctrl_image.py at the head (and its --base aef7ac66 build) against the
# round-2b head's own harness and the prior round's receipt; ctrl_srp_image.py at head against round-2b head.
# Usage: image_hashes.sh <scratch> <prior ctrl_image receipt>
S=$1; PRIOR=$2
for s in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_4x4 endstation_arty_8ch endstation_arty_current; do
  h=$(sha256sum < $S/img-head/head/$s/ctrl_app.elf | cut -c1-64); b=$(sha256sum < $S/img-head/base/$s/ctrl_app.elf | cut -c1-64)
  r=$(sha256sum < $S/img-r2b/head/$s/ctrl_app.elf | cut -c1-64); p=$(grep "^$s " $PRIOR | sed 's/.* head=\([0-9a-f]*\).*/\1/')
  [ "$h" = "$b" ] && [ "$h" = "$r" ] && [ "$h" = "$p" ] && v=IDENTICAL || v=DIFFERENT
  echo "ctrl_image $s head=$h base-aef7ac66=$b r2b-386b8e69=$r prior-round=$p $v"
done
for d in $S/srp-head/*/; do n=$(basename $d)
  h=$(sha256sum < $d/ctrl_app.elf | cut -c1-64); r=$(sha256sum < $S/srp-r2b/$n/ctrl_app.elf | cut -c1-64)
  echo "ctrl_srp_image $n head=$h r2b-386b8e69=$r $([ "$h" = "$r" ] && echo IDENTICAL || echo DIFFERENT)"; done
