#!/bin/sh
# Copy a log into the packet with host-specific prefixes replaced by neutral labels.
# Usage: sanitize.sh <in> <out> <scratch-dir>
sed -e "s|/home/[^ ]*/overlay/[0-9a-f]*/diff/usr|<verilator-root>/usr|g" \
    -e "s|$3|<scratch>|g" -e "s|/tmp/maap-mutants-[a-z0-9_]*|<tmp>/maap-mutants|g" "$1" > "$2"
