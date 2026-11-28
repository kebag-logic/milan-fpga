#!/bin/bash
set -eu
export CCACHE_DIR=$VALIDATION_STORAGE/ccache
export CCACHE_TEMPDIR=$VALIDATION_STORAGE/arty4x4-a863/ccache-tmp
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export TMPDIR=$VALIDATION_STORAGE/arty4x4-a863/work-tmp
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$PATH
exec nice -n 19 "$@"
