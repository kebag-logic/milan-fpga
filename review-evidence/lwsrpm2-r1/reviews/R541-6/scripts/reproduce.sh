#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -eu
: "${REVIEW_SOURCE:?Set REVIEW_SOURCE to the exact-head checkout}"
REVIEW_PACKET=$(cd "$(dirname "$0")/.." && pwd)
export REVIEW_SOURCE PYTHONDONTWRITEBYTECODE=1
cd "$REVIEW_SOURCE"
mkdir -p "$REVIEW_PACKET/scratch" "$REVIEW_PACKET/receipts"
git clone --quiet --depth 1 --branch 1.7.0 https://github.com/cgreen-devs/cgreen.git "$REVIEW_PACKET/scratch/cgreen"
python3 "$REVIEW_PACKET/scripts/baseline.py" --jobs 2
python3 "$REVIEW_PACKET/scripts/campaign.py" --jobs 2
python3 "$REVIEW_PACKET/scripts/storage.py" --jobs 2
python3 "$REVIEW_PACKET/scripts/own_mutations.py" --jobs 2
python3 "$REVIEW_PACKET/scripts/suggestions.py" --jobs 2
python3 "$REVIEW_PACKET/scripts/boundary.py"
python3 "$REVIEW_PACKET/scripts/docs.py" --jobs 4
python3 "$REVIEW_PACKET/scripts/audit.py"
