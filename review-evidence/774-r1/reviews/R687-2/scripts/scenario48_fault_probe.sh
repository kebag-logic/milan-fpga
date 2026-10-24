#!/usr/bin/env bash
# Plant two frame-size faults in KL_crf_tx.sv on a DISPOSABLE copy and show the
# unchanged scenario features/crf_sr_class_a.feature:48 fails on each, then
# restore the file. usage: scenario48_fault_probe.sh <disposable-copy>
set -u
cd "$1" || exit 2
f=hdl/ieee1722/crf/KL_crf_tx.sv
probe() {
  echo "== probe: $1"
  sed -i "$2" "$f"; git diff --stat | cat
  (cd tests && behave --no-capture -f plain features/crf_sr_class_a.feature 2>&1 | grep -E 'resize|ASSERT|scenarios')
  git checkout -q -- "$f"
}
probe "CRF_DLEN_C 16'd8 -> 16'd12 (frame grows to 64)" \
  "s/localparam \[15:0\] CRF_DLEN_C   = 16'd8;/localparam [15:0] CRF_DLEN_C   = 16'd12;/"
probe "CRF_PDU_C gains 4 octets (the tag grows the frame)" \
  "s/  localparam int CRF_PDU_C   = CRF_HDR_C + 32'(CRF_DLEN_C);/  localparam int CRF_PDU_C   = CRF_HDR_C + 32'(CRF_DLEN_C) + 4;/"
echo "== restored: $(git status --porcelain | wc -l) dirty"
