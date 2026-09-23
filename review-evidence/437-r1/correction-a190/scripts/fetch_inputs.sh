#!/usr/bin/env bash
# fetch_inputs.sh: recreate inputs/ (the public #437 review evidence this packet
# reads) from the evidence branch commit the reviews were archived at.
set -euo pipefail
LANE=$LANES/437-container-paragraph-scopes
OUT=$REVIEWS/437-a190-packet/inputs
EVIDENCE=de3f66885d255ad1c83cc4f9a7f07834e0dedd0a
git -C "$LANE" fetch -q origin 437-review-evidence
mkdir -p "$OUT"
git -C "$LANE" archive "$EVIDENCE" review-evidence/437-r1/reviews \
    review-evidence/437-r1/correction-a184 review-evidence/437-r1/correction-a172 | tar -x -C "$OUT"
