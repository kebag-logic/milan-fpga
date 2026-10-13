#!/bin/bash
python3 $WORK/prepare_shipping.py $WORK/candidate $WORK/shipping-candidate > $WORK/prepare-candidate.log 2>&1
r=$?
echo "$r" > $WORK/prepare-candidate.rc
if [ "$r" -eq 0 ]; then python3 $WORK/resource_bank.py; r=$?; fi
echo "$r" > $WORK/resource-bank.rc
