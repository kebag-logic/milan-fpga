#!/bin/bash
source $VALIDATION_STORAGE/tsn24-a606/env.sh
trap 'result=$?; echo "$result" > $VALIDATION_STORAGE/tsn24-a606/round2/physical.rc' EXIT
set -e
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/physical_removal.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/physical-0 --plants x-zero-never-expires,dafresh-half-range
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/physical_removal.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/physical-1 --plants dafresh-unanswered-clock,dafresh-expiry-equality
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/physical_removal.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/physical-2 --plants dafresh-inclusive-edge,dafresh-no-renewal
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/physical_removal.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/physical-3 --plants dafresh-listener-needs-probe,dafresh-ignore-address
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/physical_removal.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/physical-4 --plants dafresh-absolute-clock,dafresh-fixed-window
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/physical_removal.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/physical-5 --plants dafresh-refused-answer,dafresh-only-success
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/physical_removal.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/physical-6 --plants dafresh-state-reply-demand,dafresh-wrong-source
python3 $VALIDATION_STORAGE/tsn24-a606/round2/review-scripts/physical_removal.py --tree $VALIDATION_STORAGE/tsn24-a606/round2/tree --work $VALIDATION_STORAGE/tsn24-a606/round2/physical-7 --plants dafresh-wrong-interface,dafresh-reset-retains-demand
