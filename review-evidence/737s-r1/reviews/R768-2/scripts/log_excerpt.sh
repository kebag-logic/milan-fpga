#!/bin/sh
# Usage: log_excerpt.sh <job-log>... ; prints each log's sha256 and its cache, verdict and timeout lines.
for f in "$@"; do
  printf '== %s sha256=%s bytes=%s\n' "$(basename "$f")" "$(sha256sum "$f" | cut -d' ' -f1)" "$(wc -c < "$f")"
  grep -aE 'Cache (restored from key|not found for input keys|saved with key)|Unable to reserve|Cache Size|Sent [0-9]+ of [0-9]+ \(100|^[^ ]+ (PASS|FAIL) +test_|exceeded the maximum|The operation was canceled|first_failure|Cancelled runs' "$f" | cut -c1-220
done
