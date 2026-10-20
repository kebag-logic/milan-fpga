#!/bin/bash
# Copy round-2 logs into receipts/r2-* with host paths replaced (collect.py), then regenerate the index.
R=<scratch>/r2; S=$R/scripts
C="<scratch>/venv/bin/python3 -I <scratch>/collect.py"
put() { for f in "$@"; do [ -f "$f" ] && $C "$f" "$DEST/$(basename "$f")" > /dev/null; done; }
DEST=r2-regen; put $R/regen/*
DEST=r2-worktree-rxmon; put $R/wt-rxmon/*
for d in rxmon tsnfuzz static builder; do DEST=r2-$d; put $R/$d/*; done
for d in rxmon tsnfuzz static builder; do DEST=r2-superseded-11119970/$d; put $R/$d-11119970/*; done
DEST=r2-superseded-11119970/builder; put $R/builder-11119970-stopped/*
DEST=r2-tsn-gen-build; put $R/tsngen-submodule.log $R/tsngen-cmake.log $R/tsngen-build.log
DEST=r2-clones; put $R/cloneH.log $R/cloneS.log $R/cloneB.log
DEST=r2-scripts; put $S/* <scratch>/collect.py <scratch>/gen_index.py
<scratch>/venv/bin/python3 -I <scratch>/gen_index.py
echo collected
