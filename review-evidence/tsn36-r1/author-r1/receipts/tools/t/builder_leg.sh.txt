#!/bin/bash
# builder_leg.sh CLONE LEG OUT: docs.yml's end-station builder gate, leg LEG of 2, on CLONE, its receipt in OUT.
cd "$1" || exit 3
echo "HEAD $(git rev-parse --short=8 HEAD) dirty $(git status --porcelain --untracked-files=no | wc -l) leg $2 start $(date +%T)"
python3 scripts/ci_builder_legs.py run "$2" --receipt "$3/builder-leg-$2.json" -- python3 sw/builder/test_builder.py --require-rv32
rc=$?; echo "END rc=$rc $(date +%T)"; exit $rc
