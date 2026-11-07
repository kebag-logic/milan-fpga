#!/usr/bin/env bash
# Exports the exact head to scratch, runs tb/srp_encoder at the head, against the
# base encoder RTL, and the PV arms through the repository's own campaign driver.
set -u
P=${P:-$REVIEWS/pp214-r779-2-packet}
CLONE=${CLONE:-$REVIEWS/r779-2-pp214}
HEAD=1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa
BASE=a9e84b66
export VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
export TMPDIR=$P/scratch/tmp
S=$P/scratch; R=$P/receipts
rm -rf $S/head $S/base; mkdir -p $S/head $S/base
git -C $CLONE archive $HEAD | tar -x -C $S/head
git -C $CLONE archive $HEAD | tar -x -C $S/base
git -C $CLONE show $BASE:hdl/srp/KL_srp_encoder.sv > $S/base/hdl/srp/KL_srp_encoder.sv
( make -C $S/head/tb/srp_encoder run > $R/head-srp_encoder.log 2>&1; echo $? > $R/head-srp_encoder.rc ) &
( make -C $S/base/tb/srp_encoder run > $R/base-srp_encoder.log 2>&1; echo $? > $R/base-srp_encoder.rc ) &
wait
LABELS=$(python3 - "$S/head" <<'PY'
import re,sys
src=open(sys.argv[1]+'/tb/srp_top/mutants.py').read()
seen=[]
for m in re.finditer(r"\('([a-z0-9-]+)', 'srp_encoder'",src):
    if m.group(1) not in seen: seen.append(m.group(1))
print(','.join(seen))
PY
)
echo "$LABELS" > $R/arms-labels.txt
cd $S/head
python3 tb/srp_top/mutants.py --output $S/arms-out --only "$LABELS" --jobs 8 > $R/arms-campaign.log 2>&1
echo $? > $R/arms-campaign.rc
