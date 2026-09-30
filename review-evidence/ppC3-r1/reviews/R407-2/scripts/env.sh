# Source before any run. Pinned Verilator 5.050 wrapper (identity in receipts/tool_identity.txt).
# Override PINNED_BIN to point at another host's 5.050 wrapper directory.
export PINNED_BIN="${PINNED_BIN:-$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin}"
export PATH="$PINNED_BIN:$PATH"
export CLONE="${CLONE:-$REVIEWS/r407-2-ppC3}"
export PKT="${PKT:-$REVIEWS/ppC3-r407-2-packet}"
# at most 8 CPUs for every job (parallelism cap)
export CAP="taskset -c 0-7"
