# Product environment for the service-budget harness, as the harness README describes.
export PRODUCT_PYTHON="$HOME/litex-milan/venv/bin/python"
export PYTHON="$PRODUCT_PYTHON"
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin"
