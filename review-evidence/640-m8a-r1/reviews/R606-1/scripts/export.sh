#!/usr/bin/env bash
# Reviewer export (no Vivado): the shipping AX7101 1x1 launch argv from
# `sw/litex/build.sh ax7101 --dry-run`, minus --build, into OUT, from TREE.
# Usage: export.sh TREE OUT LOG [extra milan_soc.py args...]
# Environment: SCRATCH holds venv/ (pinned LiteX + patches), sdk/ (pinned RV32 SDK) and the
# launcher dry-run log; DRY_TREE is the tree path printed in that dry-run log.
set -u
S=${SCRATCH:-$(cd "$(dirname "$0")/../scratch" && pwd)}
TREE=$1 OUT=$2 LOG=$3; shift 3
export PATH=$S/venv/bin:$S/sdk/bin:$PATH PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$S/tmp
export SBT_OPTS="-Dsbt.global.base=$S/sbt/global -Dsbt.boot.directory=$S/sbt/boot -Dsbt.ivy.home=$S/sbt/ivy -Dsbt.coursier.home=$S/sbt/coursier -Xmx4g"
export COURSIER_CACHE=$S/sbt/coursier-cache
mkdir -p $S/tmp
argv=$(grep -o "exec python3 milan_soc.py.*" ${DRY_LOG:-$S/dry-ax7101.log} | head -1 | sed -e 's/^exec python3 milan_soc.py //' -e 's/ --build / /' -e 's/ --output-dir .*$//' -e "s#${DRY_TREE:-/nonexistent}/#$TREE/#g")
cd "$TREE/sw/litex" && python milan_soc.py $argv --output-dir "$OUT" "$@" > "$LOG" 2>&1
echo $? > "$LOG.rc"
