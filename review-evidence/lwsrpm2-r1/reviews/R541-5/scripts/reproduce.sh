#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eu
: "${REVIEW_SOURCE:?Set REVIEW_SOURCE to the exact-head checkout}"
REVIEW_PACKET=$(cd "$(dirname "$0")/.." && pwd)
export REVIEW_SOURCE PYTHONDONTWRITEBYTECODE=1
cd "$REVIEW_SOURCE"
git -C "$REVIEW_SOURCE" rev-parse HEAD
mkdir -p "$REVIEW_PACKET/scratch" "$REVIEW_PACKET/receipts"
git clone --quiet --depth 1 --branch 1.7.0 https://github.com/cgreen-devs/cgreen.git "$REVIEW_PACKET/scratch/cgreen"
test "$(git -C "$REVIEW_PACKET/scratch/cgreen" rev-parse HEAD)" = feeb85ed48d163f6b7b0011a6d8e6043951541e4
python3 "$REVIEW_PACKET/scripts/run_common.py"
python3 "$REVIEW_PACKET/scripts/campaign.py" --jobs 2
python3 "$REVIEW_PACKET/scripts/extra_checks.py"
python3 "$REVIEW_PACKET/scripts/final_campaign.py" --jobs 2
python3 "$REVIEW_PACKET/scripts/audit.py"
