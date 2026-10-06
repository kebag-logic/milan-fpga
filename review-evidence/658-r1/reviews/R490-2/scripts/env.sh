# Environment for the R490-2 receipts: the pinned Verilator 5.050 wrapper first on PATH.
export PINNED_VERILATOR_DIR=${PINNED_VERILATOR_DIR:-$VALIDATION_TOOLS/pinned-verilator-5.050}
export PATH="$PINNED_VERILATOR_DIR:$PATH"
export VERILATOR="$PINNED_VERILATOR_DIR/verilator"
export REPO=${REPO:-$REVIEWS/r490-2-658}
export PKT=${PKT:-$REVIEWS/658-r490-2-packet}
