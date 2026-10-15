#!/bin/sh
set -eu
# Usage: PYTHON312=/path/to/python3.12.3 ./replay.sh /path/to/checkout
# This uses an existing reference interpreter and a local PyYAML directory.
CHECKOUT=$(cd "$1" && pwd)
export CHECKOUT
PACKET=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$PACKET/scratch"
export TMPDIR="$PACKET/scratch" PYTHONDONTWRITEBYTECODE=1
: "${PYTHON312:?Set PYTHON312 to an existing CPython 3.12.3 with pip}"
: "${PYTHONPATH:?Set PYTHONPATH to a readable PyYAML package directory}"
export CI_IMAGE_SHFMT="$PACKET/scratch/shfmt"
curl -fsSL https://github.com/mvdan/sh/releases/download/v3.11.0/shfmt_v3.11.0_linux_amd64 -o "$CI_IMAGE_SHFMT"
printf '%s  %s\n' 1904ec6bac715c1d05cd7f6612eec8f67a625c3749cb327e5bfb4127d09035ff "$CI_IMAGE_SHFMT" | sha256sum -c -
chmod +x "$CI_IMAGE_SHFMT"
python3 "$PACKET/reference_bash.py"
PATH="$PACKET/scratch/reference-bash/bin:$PACKET/scratch/reference-bash/usr/bin:$PATH"
export PATH
cd "$CHECKOUT"
"$PYTHON312" "$PACKET/probe_walk.py" > "$PACKET/walker-probes-reference.json"
"$PYTHON312" "$PACKET/probe_audit.py" > "$PACKET/scratch/audit-probe-run.log" 2>&1
"$PYTHON312" "$PACKET/run_controls.py"
python3 "$PACKET/verify_tree.py"
