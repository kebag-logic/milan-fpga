#!/usr/bin/env bash
# Fault probe for the one code file both a predecessor and PR #557 change.
# Usage: probe_overlap_census.sh <disposable-candidate-git-clone>
# Plants a mis-resolved merge of sw/builder/test_builder.py (the census stub
# keeps the pre-#501 MILAN_NVM_MAP{IN,OUT}_CLUSTERS_k names while the firmware
# uses *_ENTRIES_k), runs only test_baremetal_profile_contract, requires it to
# fail with the compiled-census build refusal whose GCC diagnostic names the
# stale CLUSTERS stub, then restores the exact blob and checks it. (Run 1 of
# this probe required an ENTRIES spelling in the log; the gate prints only the
# tail of GCC's diagnostic, a nearest-name note on the stale stub.)
set -u
cd "$1" || exit 2
f=sw/builder/test_builder.py
want=$(git rev-parse HEAD:$f)
sed -i 's/MILAN_NVM_MAPIN_ENTRIES_{k}/MILAN_NVM_MAPIN_CLUSTERS_{k}/; s/MILAN_NVM_MAPOUT_ENTRIES_{k}/MILAN_NVM_MAPOUT_CLUSTERS_{k}/' $f
git diff --stat -- $f
python3 -c "
import sys; sys.path.insert(0,'sw/builder'); sys.argv=['test_builder.py','--require-rv32']
import test_builder as t
t.test_baremetal_profile_contract()
print('PROBE: planted test RETURNED OK')
" > probe.log 2>&1
rc=$?
git checkout -- $f
got=$(git hash-object $f)
echo "planted rc=$rc"
grep -m3 -nE 'MAP(IN|OUT)_(ENTRIES|CLUSTERS)|AssertionError' probe.log | cut -c1-300
[ "$got" = "$want" ] && echo "restored blob $got" || { echo "RESTORE MISMATCH"; exit 3; }
if [ $rc -ne 0 ] && grep -q 'compiled census could not build the firmware' probe.log \
   && grep -qE 'MILAN_NVM_MAP(IN|OUT)_CLUSTERS_' probe.log; then
  echo "RESULT: mis-resolved overlap caught"; exit 0
fi
echo "RESULT: NOT caught"; exit 1
