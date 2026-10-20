#!/bin/bash
# Builder bank at the lane head: both measured legs with --require-elaboration --require-rv32, then their union.
export PATH=<scratch>/venv/bin:<tools>/sv2v-v0.0.12:$PATH
export MILAN_LITEX_PYTHON=<home>/litex-milan/venv/bin/python3
export TMPDIR=<scratch>/round1c/tmp
O=<scratch>/round1c/builder; mkdir -p $O
cd <scratch>/round1c/cloneB
echo "head $(git rev-parse HEAD) python $(python3 --version 2>&1)" > $O/HEAD.txt
for leg in 0 1; do
  date -Is > $O/leg-$leg.start
  python3 scripts/ci_builder_legs.py run $leg --receipt $O/leg-$leg.json -- \
    python3 sw/builder/test_builder.py --require-elaboration --require-rv32 > $O/leg-$leg.log 2>&1
  echo "rc=$?" > $O/leg-$leg.rc
  date -Is > $O/leg-$leg.end
done
python3 scripts/ci_builder_legs.py union --workflow elaborate \
  --head "$(git rev-parse HEAD)" --tree "$(git rev-parse 'HEAD^{tree}')" \
  $O/leg-0.json $O/leg-1.json > $O/union.log 2>&1
echo "rc=$?" > $O/union.rc
echo done > $O/DONE
