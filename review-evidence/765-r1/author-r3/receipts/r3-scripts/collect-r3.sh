#!/bin/bash
# Copy round-3 logs into receipts/r3-* with host paths replaced (collect.py), then regenerate the index.
R=<scratch>/r3; S=$R/scripts
C="<scratch>/venv/bin/python3 -I <scratch>/collect.py"
put() { for f in "$@"; do [ -f "$f" ] && $C "$f" "$DEST/$(basename "$f")" > /dev/null; done; }
for d in regen rxmon tsnfuzz aaf static probe misc; do DEST=r3-$d; put $R/$d/*; done
DEST=r3-clones; put $R/cloneH.log $R/cloneS.log
DEST=r3-scripts; put $S/* <scratch>/collect.py <scratch>/gen_index.py
<scratch>/venv/bin/python3 -I <scratch>/gen_index.py
echo collected
