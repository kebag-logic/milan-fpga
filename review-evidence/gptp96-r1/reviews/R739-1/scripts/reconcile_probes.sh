#!/usr/bin/env bash
# Reproduce the prior public findings' gate escapes in disposable copies.
# Usage: reconcile_probes.sh <clone> <scratch-dir>
set -u
SRC=$1; WORK=$2; mkdir -p "$WORK"
fresh() { rm -rf "$WORK/t"; mkdir -p "$WORK/t"; git -C "$SRC" archive HEAD | tar -x -C "$WORK/t"; }
run() { local out rc; out=$(cd "$WORK/t" && python3 -B scripts/check_docs.py 2>&1); rc=$?
  printf '%-34s rc=%s | %s\n' "$1" "$rc" "$(printf '%s' "$out" | tail -1)"; }
fresh; run control
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | **376** |/' "$WORK/t/docs/INTEGRATION.md"; run bold_stale_constant
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | -1 |/' "$WORK/t/docs/INTEGRATION.md"; run negative_stale_constant
fresh; sed -i 's/| `SYNC_RTO_MS_C` | 375 |/| `SYNC_RTO_MS_C` | 376 ms |/' "$WORK/t/docs/INTEGRATION.md"; run unit_stale_constant
fresh; sed -i 's/^| Link-up | 20 us | 20 us |/| Link-up | 21 us | 21 us |/' "$WORK/t/docs/INTEGRATION.md"; run drifted_duplicate_threshold_table
fresh; sed -i 's/^Timer slot 4 is the 375 ms/Timer slot 4 is the 376 ms/' "$WORK/t/docs/HDL_DEVELOPER.md"; run drifted_prose_copy
rm -rf "$WORK/t"
