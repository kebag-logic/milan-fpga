# Environment for lane 951's firmware, image and harness runs (sourced): the product LiteX venv, the pinned RV32 SDK,
# the pinned Verilator, sv2v and make, the hash seed, offline CPU generator.
V=<tools>/pinned-verilator-5.050
export PATH=<litex>/venv/bin:<sdk>/host/bin:$V:<tools>/sv2v-v0.0.12:<tools>/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=$V/verilator PYTHONHASHSEED=0 PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export TMPDIR=<scratch>/tmp HOME=<scratch>/home
[ -e "$HOME/br-milan-rv32" ] || ln -s <sdk> "$HOME/br-milan-rv32"
