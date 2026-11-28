#!/bin/bash
set -eu
export PATH=$VALIDATION_STORAGE/usbnet-a855/round7/bin:$WORKSPACE_HOME/litex-milan/venv/bin:$PATH
export PYTHONPATH=$VALIDATION_STORAGE/usbnet-a855/round7/audit${PYTHONPATH:+:$PYTHONPATH}
export CCACHE_DIR=$VALIDATION_STORAGE/ccache CCACHE_TEMPDIR=$VALIDATION_STORAGE/usbnet-a855/ccache-tmp
export OBJCACHE=ccache VERILATOR_CCACHE=ccache MAKEFLAGS='--eval=.SECONDARY:'
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export TMPDIR=$VALIDATION_STORAGE/usbnet-a855/round7/work-tmp
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
exec "$@"
