# SPDX-License-Identifier: CERN-OHL-W-2.0
# Common environment: packet and scratch locations, and $S/bin first on PATH,
# where `verilator` must be a link to the pinned Verilator 5.050 wrapper
# (identity checked by its --version and the wrapper's SHA-256, README.md).
P=${P:?set P to the packet directory}
S=$P/scratch
export PATH=$S/bin:$PATH
HEAD=9160f7d7f005050887cab942710940b91e34fc65
