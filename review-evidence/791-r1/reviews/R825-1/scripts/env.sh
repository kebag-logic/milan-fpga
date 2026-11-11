# Source me. Review environment: pinned Verilator 5.050 first, RV32 SDK, offline generator, and an sbt stub
# that refuses so no CPU netlist is ever generated into the shared generator cache (reuse of cached netlists only).
P=${P:-$REVIEWS/791-r825-1-packet}
export PY=$HOME/litex-milan/venv/bin/python3
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0
export PATH=$P/scratch/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$HOME/br-milan-rv32/host/bin:$PATH
