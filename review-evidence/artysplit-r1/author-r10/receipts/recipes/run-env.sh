#!/bin/bash
set -eu
export CCACHE_DIR=$SHARED_STORAGE/ccache
export CCACHE_TEMPDIR=$VALIDATION_STORAGE/r10/ccache-tmp
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
export TMPDIR=$VALIDATION_STORAGE/r10/work-tmp
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export PATH=$TOOLCHAIN/venv/bin:$PATH
exec "$@"
