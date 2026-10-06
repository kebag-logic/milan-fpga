#!/bin/sh
# Run from the candidate checkout. All disposable state stays in the packet.
set -eu
review_packet=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
mkdir -p "$review_packet/scratch/tmp" "$review_packet/scratch/raw"
export TMPDIR="$review_packet/scratch/tmp"
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/ci_rv32_sdk.py --destination "$review_packet/scratch/sdk"
python3 -m venv --system-site-packages "$review_packet/scratch/docs-venv"
"$review_packet/scratch/docs-venv/bin/python" -m pip install --no-cache-dir --require-hashes --only-binary=:all: -r tools/markdown/requirements.txt
