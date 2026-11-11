#!/usr/bin/env bash
# run_compare.sh: the all-fabric compare, base against the final head, its rc beside its log.
S=/data-2/milan/tmp/791-a765; F=$S/final; T=$MANAGEMENT/2026-09-23/791-a765/tools
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0
cd "$S" || exit 2
$WORKSPACE_HOME/litex-milan/venv/bin/python3 "$T/allfabric_compare.py" "$S/clones/base" "$S/clones/final-af" "$S/allfabric" \
  "$F/allfabric-receipt" > "$F/allfabric.log" 2>&1
echo $? > "$F/allfabric.rc"
