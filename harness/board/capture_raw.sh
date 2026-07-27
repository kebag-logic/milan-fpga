#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# capture_raw.sh <device> <channels> <rate> <seconds> <outfile>
#
# Capture PCM for THD+N. The card accepts **S32_BE only** and it CANNOT go in a
# WAV container - so this is `-t raw`, and the host-side analysis is told the
# format explicitly rather than sniffing a header that does not exist.
#
# The capture is coherently sampled (the pilot tone is exact-period: 48 samples
# = 1 kHz at 48 kHz), which is what lets the host FFT it with NO window. That
# only holds if the capture is not resampled anywhere, hence the fixed -f/-r.
#
# Emits `#CAPTURE_BYTES=` / `#CAPTURE_FILE=` so the host can verify the length
# it got matches the length it asked for before trusting a THD+N number.

DEV="${1:-hw:0,0}"
CH="${2:-2}"
RATE="${3:-48000}"
SECS="${4:-10}"
OUT="${5:-/tmp/mh-capture.raw}"

command -v arecord > /dev/null 2>&1 || { echo "#ERROR=no-arecord"; exit 2; }

rm -f "$OUT"
arecord -D "$DEV" -t raw -f S32_BE -c "$CH" -r "$RATE" -d "$SECS" "$OUT" \
    > /dev/null 2>&1
rc=$?

BYTES=$(wc -c < "$OUT" 2>/dev/null)
[ -n "$BYTES" ] || BYTES=0
WANT=$((CH * 4 * RATE * SECS))

echo "#CAPTURE_FILE=$OUT"
echo "#CAPTURE_BYTES=$BYTES"
echo "#CAPTURE_EXPECT=$WANT"
echo "#CAPTURE_RC=$rc"
[ "$rc" -eq 0 ] || exit "$rc"
# A short capture is a measurement error, not a distortion result.
[ "$BYTES" -ge $((WANT * 9 / 10)) ] || { echo "#ERROR=short-capture"; exit 3; }
exit 0
