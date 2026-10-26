# Review environment: product LiteX venv and RV32 SDK first on PATH, pinned Verilator 5.050,
# and an sbt shim that refuses netlist generation (no writes into the shared LiteX tree).
P=$REVIEWS/665s2-r703-1-packet
export PATH=$P/scratch/shim:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:/usr/bin:/bin
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export TMPDIR=$P/scratch/tmp
mkdir -p $TMPDIR
