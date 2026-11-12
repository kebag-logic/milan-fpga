#!/bin/bash
# Run the given fleg.sh argument lists side by side in one unit: pair.sh "ARGS1" "ARGS2" ...
for a in "$@"; do bash <scratch>/scripts/fleg.sh $a & done
wait
