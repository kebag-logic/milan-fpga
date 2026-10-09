#!/bin/sh
set -eu
source_dir=$1
packet_dir=$2
python3 -m venv --system-site-packages "$packet_dir/scratch/markdown-env"
"$packet_dir/scratch/markdown-env/bin/python" -m pip --disable-pip-version-check install --no-cache-dir --require-hashes -r "$source_dir/tools/markdown/requirements.txt"
