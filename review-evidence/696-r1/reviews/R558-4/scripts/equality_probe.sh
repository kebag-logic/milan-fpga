#!/bin/sh
# Usage: equality_probe.sh <clone> <scratchdir> <make-binary-dir>
# The head integration.mk's DP_SRCS and DP_FLAGS (VERILATOR_JOBS=5 on the outer command
# line, outer MAKEFLAGS=w) must equal the datapath suite's own print-srcs and
# print-dp-vflags (VERILATOR_JOBS=5) byte for byte: the delta changes how the lists
# are captured, not what they contain. (Values are written with $(file) so quoting survives.)
set -u
C=$1; S=$2; MB=$3; M=$C/tb/verilator/maap; export PATH="$MB:$PATH"; mkdir -p "$S"
{ cat "$M/integration.mk"; printf '\nprobe-print:\n\t@:$(file >%s/srcs.mk.txt,$(DP_SRCS))$(file >%s/flags.mk.txt,$(DP_FLAGS))\n' "$S" "$S"; } > "$S/eq.mk"
(cd "$M" && env MAKEFLAGS=w make -s -f "$S/eq.mk" probe-print VERILATOR_JOBS=5) || echo "probe rc=$?"
(cd "$C/tb/verilator/milan_dp" && env -u MAKEFLAGS make -s --no-print-directory print-srcs) > "$S/srcs.dp.txt"
(cd "$C/tb/verilator/milan_dp" && env -u MAKEFLAGS make -s --no-print-directory print-dp-vflags VERILATOR_JOBS=5) > "$S/flags.dp.txt"
echo "make=$(make --version | head -1)"
cmp "$S/srcs.mk.txt" "$S/srcs.dp.txt" && echo "srcs identical ($(wc -w < "$S/srcs.dp.txt") words)"
cmp "$S/flags.mk.txt" "$S/flags.dp.txt" && echo "flags identical ($(wc -w < "$S/flags.dp.txt") words; $(grep -o -- '--build -j [0-9]*' "$S/flags.dp.txt"))"
