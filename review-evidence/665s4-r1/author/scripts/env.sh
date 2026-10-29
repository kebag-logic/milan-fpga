# Lane S4 round 2's gate environment (sourced): the product LiteX venv, the pinned RV32 SDK,
# a scratch bin holding only a link to the system meson ahead of the SDK's shim.
export SDK=$WORKSPACE_HOME/br-milan-rv32/host
export LITEX_PY=$WORKSPACE_HOME/litex-milan/venv/bin
export SCRATCH=$VALIDATION_STORAGE/scratch/665s4-a698b
export GATE_BUILDER_PATH="$LITEX_PY:$SCRATCH/meson-bin:$SDK/bin"
export GATE_HDL_PYTHON=$VALIDATION_STORAGE/scratch/665s4-a698/venv-hdl/bin/python3
export GATE_BEHAVE=$VALIDATION_STORAGE/scratch/665s4-a698/venv-behave/bin/behave
export GATE_SV2V_DIR=$VALIDATION_TOOLS/sv2v-v0.0.12
export MD_PY=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3
export PYTHONHASHSEED=0
export LITEX_ENV_CC_TRIPLE=riscv32-linux
export COURSIER_MODE=offline
export SBT_OPTS=-Dsbt.offline=true
