#!/usr/bin/env bash
set -euo pipefail
review_root="${1:?pass the review checkout}"
packet_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
mkdir -p "$packet_dir/scratch/tmp"
export TMPDIR="$packet_dir/scratch/tmp"
python3 -m pip install --disable-pip-version-check --no-cache-dir --only-binary=:all: \
  --require-hashes --target "$packet_dir/scratch/markdown" \
  -r "$review_root/tools/markdown/requirements.txt"
