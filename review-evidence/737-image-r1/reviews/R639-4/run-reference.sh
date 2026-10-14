#!/bin/sh
set -eu
packet=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PYTHONHOME="$packet/scratch/reference/usr"
export PYTHONPATH="$packet/scratch/reference/site"
export LD_LIBRARY_PATH="$packet/scratch/reference/usr/lib/x86_64-linux-gnu"
export PYTHONDONTWRITEBYTECODE=1
export REVIEW_RECEIPT_PREFIX=reference-
"$PYTHONHOME/bin/python3.12" -c 'import sys; assert sys.version_info[:3] == (3,12,3); print(sys.version)'
"$PYTHONHOME/bin/python3.12" "$packet/run-focused.py" "$1"
"$PYTHONHOME/bin/python3.12" "$packet/probe-traversal.py" "$1" > "$packet/reference-traversal-probes.log"
