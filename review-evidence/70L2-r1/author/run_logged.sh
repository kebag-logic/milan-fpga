#!/bin/bash
# Run one gate detached-safe: run_logged.sh <logdir> <name> <cwd> <command...>
# Writes <logdir>/<name>.log (stdout+stderr), <name>.rc and <name>.meta
# (start, end, seconds, head, command). The pinned Verilator wrapper of the
# manager's consumer bank comes first on PATH.
set -u
LOGDIR=$1 NAME=$2 CWD=$3; shift 3
export PATH=$VALIDATION_STORAGE/pp131-manager-9b4da6b5/pinned-tool-bin:$PATH
mkdir -p "$LOGDIR"
rm -f "$LOGDIR/$NAME.rc"
cd "$CWD" || { echo 97 > "$LOGDIR/$NAME.rc"; exit 97; }
start=$(date +%s)
{
  echo "start $(date -Is)"
  echo "head $(git rev-parse HEAD) dirty=$(git status --porcelain --untracked-files=no | wc -l)"
  echo "cwd $CWD"
  printf 'cmd'; printf ' %q' "$@"; echo
} > "$LOGDIR/$NAME.meta"
"$@" > "$LOGDIR/$NAME.log" 2>&1
rc=$?
end=$(date +%s)
{ echo "end $(date -Is)"; echo "seconds $((end - start))"; echo "rc $rc"; } >> "$LOGDIR/$NAME.meta"
echo $rc > "$LOGDIR/$NAME.rc"
exit $rc
