#!/bin/sh
# Usage: derive_equal.sh <clone> <scratchdir> <make>
# Prints sha256 of the derived DP_SRCS and DP_FLAGS for the b9b38961 and HEAD integration.mk
# (plain context, VERILATOR_JOBS=0 on the command line), and diffs them.
set -u
C=$1; S=$2; m=$3; M=$C/tb/verilator/maap; mkdir -p "$S"
printf '\nshow:\n\t@echo "$(DP_SRCS)" > $(OUT).srcs\n\t@echo '"'"'$(DP_FLAGS)'"'"' > $(OUT).flags\n' > "$S/tail.mk"
git -C "$C" show b9b389611:tb/verilator/maap/integration.mk | cat - "$S/tail.mk" > "$S/A.mk"; cat "$M/integration.mk" "$S/tail.mk" > "$S/B.mk"
for v in A B; do (cd "$M" && env -u MAKEFLAGS -u VERILATOR_JOBS "$m" -s -f "$S/$v.mk" show OUT="$S/$v" VERILATOR_JOBS=0); done
sha256sum "$S/A.srcs" "$S/B.srcs" "$S/A.flags" "$S/B.flags" | sed "s|$S/||"
cmp -s "$S/A.srcs" "$S/B.srcs" && echo "DP_SRCS identical ($(wc -w < "$S/B.srcs") words)"
cmp -s "$S/A.flags" "$S/B.flags" && echo "DP_FLAGS identical ($(wc -w < "$S/B.flags") words, $(grep -o -- '--build -j [0-9]*' "$S/B.flags"))"
