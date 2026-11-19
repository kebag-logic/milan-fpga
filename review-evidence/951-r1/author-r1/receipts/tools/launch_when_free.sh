#!/bin/bash
# launch_when_free.sh NAME CWD CMD...: wait (up to 280 s) for a free CPU range, then bgunit.sh NAME CWD CMD...
S=<scratch>
timeout 280 bash -c 'until python3 <mgmt>/2026-09-23/cpu_ranges.py pick >/dev/null 2>&1; do sleep 10; done' || { echo "still no free range"; exit 75; }
exec $S/bin/bgunit.sh "$@"
