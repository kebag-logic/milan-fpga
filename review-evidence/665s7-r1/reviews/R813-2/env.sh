# environment for the R813-2 gate runs (portable: set V to a Verilator 5.050 install directory)
V=${V:-$VALIDATION_TOOLS/pinned-verilator-5.050}
export VERILATOR=$V/verilator PATH=$V:$VALIDATION_TOOLS/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin
export TMPDIR=${TMPDIR:-$REVIEWS/665s7-r813-2-packet/scratch/tmp}
