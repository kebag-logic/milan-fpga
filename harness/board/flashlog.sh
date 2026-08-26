#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# flashlog.sh <mount> <tag> <one-line message>
#
# OPTIONAL board-side durable log. It exists for exactly ONE case the host
# cannot observe: a fault where the board dies or hangs before it can report.
# Everything else belongs in the host log, which is the primary record and is
# complete on its own.
#
# IT DOES NOTHING TODAY, ON PURPOSE. No deployed image carries an mtd
# node and no mtd driver is known to bind to this flash controller in this
# kernel configuration, so the writable area this would use does not exist.
# The falsifier is `cat /proc/mtd` after a flash and boot; when a partition
# appears and is mounted, this script starts working with no code change and
# the harness picks it up automatically.
#
# Degrades SILENTLY to a no-op (exit 0, one `#FLASHLOG=` line saying why) so a
# missing mount can never fail a step. It is a logging path, not a test result.

MOUNT="${1:-/user}"
TAG="${2:-run}"
shift 2 2>/dev/null
MSG="$*"

# Report what the falsifier says, so the run record carries the evidence.
if [ -r /proc/mtd ]; then
    echo "#PROC_MTD_PRESENT=1"
else
    echo "#PROC_MTD_PRESENT=0"
fi

if [ -z "$MOUNT" ] || [ ! -d "$MOUNT" ]; then
    echo "#FLASHLOG=absent ($MOUNT is not a directory) - host-only logging"
    exit 0
fi
if ! touch "$MOUNT/.mh-probe" 2>/dev/null; then
    echo "#FLASHLOG=readonly ($MOUNT is not writable) - host-only logging"
    exit 0
fi
rm -f "$MOUNT/.mh-probe"

# Bounded: one file per tag, capped, oldest lines dropped. A board-side log
# must never be the reason a partition fills.
F="$MOUNT/mh-$TAG.log"
LIMIT=200
printf '%s %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || echo unknown)" "$MSG" >> "$F"
LINES=$(wc -l < "$F" 2>/dev/null)
if [ -n "$LINES" ] && [ "$LINES" -gt "$LIMIT" ]; then
    tail -n "$LIMIT" "$F" > "$F.new" && mv "$F.new" "$F"
fi
echo "#FLASHLOG=written ($F)"
exit 0
