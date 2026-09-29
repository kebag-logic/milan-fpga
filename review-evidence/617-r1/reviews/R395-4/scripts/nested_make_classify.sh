#!/usr/bin/env bash
# Classify the nested `$(shell $(MAKE) -s -C ../milan_dp print-srcs)` pattern
# in pp_shadow and milan_dp_render (and capture_coherence for reference) under
# GNU make 4.3: print the first words of the parse-time list (a) at a top-level
# parse (`make -C <suite>`, what scripts/run_all_suites.sh does) and (b) in a
# child make that inherited MAKEFLAGS=w (what a recipe-launched script's
# `make -s -C <suite> <target>` gets under 4.3).
# Usage: nested_make_classify.sh <repo>   (make 4.3 first on PATH)
set -u
R=$1
show() { # suite var
  printf '%-18s %-10s top-level make -C : ' "$1" "$2"
  env -u MAKEFLAGS make -C "$R/tb/verilator/$1" --no-print-directory --eval "zz_show: ; @echo '[\$(wordlist 1,4,\$($2))]'" zz_show 2>&1 | tail -1
  printf '%-18s %-10s inherited MAKEFLAGS=w: ' "$1" "$2"
  MAKEFLAGS=w make -s -C "$R/tb/verilator/$1" --no-print-directory --eval "zz_show: ; @echo '[\$(wordlist 1,4,\$($2))]'" zz_show 2>&1 | tail -1
}
make --version | head -1
show pp_shadow DP_SRCS
show milan_dp_render SRCS
show milan_dp_render DP_VFLAGS
show capture_coherence DP_SRCS
show capture_coherence DP_VFLAGS
echo "-- pp_shadow/pending_mutant.py listing call, as a recipe-launched child would run it:"
( cd "$R/tb/verilator/pp_shadow" && MAKEFLAGS=w make -s -C ../milan_dp print-srcs 2>&1 | head -c 160; echo )
