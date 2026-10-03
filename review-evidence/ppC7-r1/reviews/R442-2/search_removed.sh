#!/bin/sh
# Search the named documents for any removed class-B adapter op, removed class-C
# event, adapter wording, or an in-processor counter block. Run from the repo root.
# Usage: search_removed.sh [rev]   (default: working tree)
REV=${1:-}
FILES="docs/architecture/01_overview.md docs/architecture/03_packet_engine.md docs/architecture/05_acmp_engine.md docs/architecture/06_aecp_engine.md docs/guides/README.md docs/README.md"
OPS='INPUT_CONFIGURE|INPUT_ENABLE|INPUT_START|INPUT_STOP|INPUT_DISABLE|OUTPUT_STATUS|OUTPUT_SET_PT_OFFSET|SET_INPUT_FORMAT|SET_OUTPUT_FORMAT|READ_AS_PATH|GET_MCR_DEFAULTS|MC_LOCKED|MC_UNLOCKED|FRAMES_RX_TICK|FRAMES_TX_TICK|AS_CAPABLE_CHANGE|PATH_CHANGE|mclk\.|avtp\.|gptp\.|INPUT_DISABLE'
ADP='adapter'
CTR='counter bank|counters? block|ctrs\b|counter RAM|counters RAM|bank sizes|counter-mask (table|ROM)|mask ROM|accumulat|-> *ctrs|--> *ctrs|to counters|counters,'
for f in $FILES; do
  if [ -n "$REV" ]; then git show "$REV:$f"; else cat "$f"; fi | \
    grep -n -i -E "$OPS|$ADP|$CTR" | sed "s|^|$f:|"
done
