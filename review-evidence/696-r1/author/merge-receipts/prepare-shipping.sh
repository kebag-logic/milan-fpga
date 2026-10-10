#!/bin/bash
export TMPDIR=<scratch>
export PYTHONDONTWRITEBYTECODE=1
python3 "$TMPDIR/prepare_shipping.py" <validation-tree> "$TMPDIR/shipping" > "$TMPDIR/prepare-shipping.log" 2>&1
rc=$?
echo "$rc" > "$TMPDIR/prepare-shipping.rc"
exit "$rc"
