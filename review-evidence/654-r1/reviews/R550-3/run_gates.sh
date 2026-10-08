#!/usr/bin/env bash
# Run the composition-relevant gates on a candidate checkout, in parallel.
#   run_gates.sh <repo> <outdir> <docs-python> <litex-python> <gates-file> [jobs]
# gates-file: one gate per line, "<name>|<D or L>|<command words>"; D runs the
# command with <docs-python>, L with <litex-python>, S as a shell command.
# Each gate writes <outdir>/<name>.log and <outdir>/<name>.rc.
set -u
REPO=$1 OUT=$2 DPY=$3 LPY=$4 GATES=$5 JOBS=${6:-16}
mkdir -p "$OUT"
export REPO OUT DPY LPY PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
run_one() {
    IFS='|' read -r name kind cmd <<<"$1"
    cd "$REPO" || exit 1
    case $kind in
        D) set -- "$DPY" $cmd ;;
        L) set -- "$LPY" $cmd ;;
        S) set -- bash -c "$cmd" ;;
    esac
    start=$(date +%s)
    { echo "# cmd: $*"; echo "# head: $(git rev-parse HEAD)"; } >"$OUT/$name.log"
    timeout 3000 "$@" >>"$OUT/$name.log" 2>&1
    rc=$?
    echo "# rc=$rc seconds=$(( $(date +%s) - start ))" >>"$OUT/$name.log"
    echo "$rc" >"$OUT/$name.rc"
    echo "$name rc=$rc"
}
export -f run_one
grep -v '^\s*#' "$GATES" | grep -v '^\s*$' | tr '\n' '\0' |
    xargs -0 -P "$JOBS" -I{} bash -c 'run_one "$1"' _ {}
