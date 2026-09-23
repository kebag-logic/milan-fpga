#!/bin/sh
# Simulator identity: the pinned wrapper, the binary it execs, and the version.
. $REVIEWS/gptp68-a199-packet/scripts/env.sh
W=$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator
echo "# date: $(date -Is)"
echo "# wrapper: $W"
sha256sum "$W"
cat "$W"; echo
D=$(sed -n 's/.*VERILATOR_ROOT=\([^ ]*\)\/share\/verilator .*/\1/p' "$W")
sha256sum "$D/bin/verilator_bin" "$D/bin/verilator"
echo "# verilator on PATH: $(command -v verilator)"
verilator --version
echo "# system verilator (NOT used): $(/usr/bin/verilator --version 2>&1)"
echo "# python3: $(python3 --version 2>&1); make: $(make --version | head -1)"
echo "# host nproc: $(nproc)"
