#!/usr/bin/env bash
# launch.sh NAME CMD... - run CMD detached from the review clone with the review's
# toolchain environment; output to receipts/NAME.log, exit status to receipts/NAME.rc.
set -u
P=${PACKET:?export PACKET, this packet directory}
TREE=${TREE:-${CLONE:?export CLONE, the review clone at the exact head}}
name=$1; shift
G=${TOOLS:?export TOOLS, the pinned tools directory}/gtest-1.14.0
VENV=${TOOLS:?export TOOLS, the pinned tools directory}/md-venv-40cdefe08ebd/bin
export PATH=$VENV:${RV32_SDK:?export RV32_SDK, the pinned RV32 SDK host directory}/bin:${TOOLS:?export TOOLS, the pinned tools directory}/pinned-verilator-5.050:$PATH
[ -n "${PIN_GTEST:-}" ] && export PKG_CONFIG_PATH=$G/lib/pkgconfig CMAKE_PREFIX_PATH=$G LD_LIBRARY_PATH=$G/lib
export PYTHONHASHSEED=0
[ -n "${PIN_GTEST:-}" ] && export CPATH=$G/include LIBRARY_PATH=$G/lib
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
rm -f "$P/receipts/$name.rc"
cd "$TREE" && nohup setsid bash -c '"$@" > "'"$P/receipts/$name.log"'" 2>&1; echo $? > "'"$P/receipts/$name.rc"'"' _ "$@" >/dev/null 2>&1 &
