# env.sh: the pinned tools for this review's runs (paths are this host's)
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator SV2V=$VALIDATION_TOOLS/sv2v-v0.0.12/sv2v
export PYTHONHASHSEED=0
