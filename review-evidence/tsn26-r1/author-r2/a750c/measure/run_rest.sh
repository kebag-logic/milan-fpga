#!/bin/sh
S=$VALIDATION_STORAGE/tsn26-a750c
. $S/env.sh
cd $S/clone || exit 9
rm -rf $S/val-rest
git rev-parse HEAD > $S/gates-rest.head
git status --short > $S/gates-rest.status
python3 -I $S/scripts/validate_minus_privacy.py $S/clone --work $S/val-rest --jobs 16 --graphs > $S/val-rest.log 2>&1; echo $? > $S/val-rest.rc
git status --short > $S/gates-rest.status-after
echo done > $S/gates-rest.done
