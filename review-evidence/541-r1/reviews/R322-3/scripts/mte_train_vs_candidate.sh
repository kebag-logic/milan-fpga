#!/bin/bash
# Run measure_test_evidence.py --check on the train-only tree (b1b33472) and on
# the candidate (ec9cf454), each with its pinned submodules, and diff the two.
# Usage: mte_train_vs_candidate.sh <candidate-clone> <scratch-dir> <python> <receipt>
set -u
C=$1; S=$2; PY=$3; OUT=$4
TRAIN=b1b334725dcf12e084eaa3bb96b1e6865c052267
if [ ! -d "$S/c508/.git" ]; then
  git clone -q --shared -n "$C" "$S/c508" && git -C "$S/c508" checkout -q "$TRAIN" || exit 2
  for p in gptp-processor protocol-processor third_party/verilog-axis; do
    git -C "$S/c508" submodule init -q "$p"
    git -C "$S/c508" config "submodule.$p.url" "$C/$p"
  done
  git -C "$S/c508" -c protocol.file.allow=always submodule update -q \
      gptp-processor protocol-processor third_party/verilog-axis || exit 2
fi
[ "$(git -C "$S/c508" rev-parse HEAD)" = "$TRAIN" ] || exit 2
(cd "$S/c508" && "$PY" scripts/measure_test_evidence.py --check) > "$S/train-mte.log" 2>&1; trc=$?
(cd "$C" && "$PY" scripts/measure_test_evidence.py --check) > "$S/cand-mte.log" 2>&1; crc=$?
{
  echo "# measure_test_evidence --check: train-only $TRAIN (rc $trc) vs candidate $(git -C "$C" rev-parse HEAD) (rc $crc)"
  echo "# train submodules:"; git -C "$S/c508" submodule status gptp-processor protocol-processor third_party/verilog-axis
  grep -E "RATCHET|lowered" "$S/train-mte.log" | sed 's/^/train: /'
  grep -E "RATCHET|lowered" "$S/cand-mte.log" | sed 's/^/candidate: /'
  echo "# diff train -> candidate (labels only; content lines verbatim)"
  diff -u --label train --label candidate "$S/train-mte.log" "$S/cand-mte.log"; echo "diff rc=$?"
} > "$OUT"
[ $trc -eq 0 ] && [ $crc -eq 0 ]
