#!/bin/sh
# Tree-wide search at a commit for CTLR_DIAG / 0x6F4 / departing-controller statements.
# Usage: tree_search.sh <repo> <commit>
C=$1; H=$2
git -C "$C" grep -n -i -E "ctlr_diag|0x0*6f4\b|'h6f4|\b6f4\b|departing.controller|evictions?\[|probes sent|replies seen|controllers shed" "$H" -- . ':!docs/history' | sed "s/^$H://"
echo "## docs/history (frozen) hit counts"
git -C "$C" grep -c -i -E "ctlr_diag|0x0*6f4\b" "$H" -- docs/history | sed "s/^$H://"
