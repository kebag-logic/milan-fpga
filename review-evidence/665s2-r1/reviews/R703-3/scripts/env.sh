# Review environment: product LiteX venv and RV32 SDK on PATH, pinned Verilator 5.050, an sbt shim
# that refuses netlist generation, and a make shim capping make's parallelism, in $P/scratch/shim.
P=$REVIEWS/665s2-r703-3-packet
export PATH=$P/scratch/shim:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:/usr/bin:/bin
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export TMPDIR=$P/scratch/tmp
mkdir -p $TMPDIR
