#!/bin/bash
# The docs workflow's CI-tooling self-tests (docs_ci_selftests.sh) at the lane head, into a work log; the
# summary (status lines) goes to receipts, the full log is recorded by size and sha256.
set -u
O=$MANAGEMENT/2026-09-23/665s1-a680l
W=$VALIDATION_STORAGE/scratch/665s1-a680l-work
export TMPDIR=$W/tmp
git -C $LANES/665-s1-faces rev-parse HEAD > "$O/receipts/gates/docs-ci-selftests.txt.head"
bash "$O/probes/docs_ci_selftests.sh" $LANES/665-s1-faces > "$W/docs-ci-selftests.txt" 2>&1
rc=$?
echo "rc=$rc" >> "$W/docs-ci-selftests.txt"
grep -E '^\[rc=|^docs CI self-tests:|^rc=' "$W/docs-ci-selftests.txt" > "$O/receipts/gates/docs-ci-selftests-summary.txt"
(cd "$W" && stat -c '%s bytes' docs-ci-selftests.txt && sha256sum docs-ci-selftests.txt) > "$O/receipts/gates/docs-ci-selftests-large.txt"
exit $rc
