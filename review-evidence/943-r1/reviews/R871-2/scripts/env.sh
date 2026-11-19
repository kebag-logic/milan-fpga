# env.sh: pinned tools for this review's probes (sourced). The LiteX venv and RV32 SDK are the runner's, under $HOME.
V=$VALIDATION_TOOLS/pinned-verilator-5.050
export PATH=$HOME/litex-milan/venv/bin:$V:/usr/local/bin:/usr/bin:/bin:$HOME/br-milan-rv32/host/bin
export VERILATOR=$V/verilator
export PYTHONHASHSEED=0 PYTHONUNBUFFERED=1
P=$REVIEWS/943-r871-2-packet
export TMPDIR=$P/scratch/tmp
mkdir -p "$TMPDIR"
