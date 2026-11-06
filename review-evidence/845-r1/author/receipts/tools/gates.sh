#!/usr/bin/env bash
# gates.sh <head> <clone> <logdir> <gate-id>=<command> ...: each gate's whole output into <logdir>/<id>.log and its
# exit status into <logdir>/<id>.rc, run one after the other in <clone>, never piped; DONE when all have run.
set -u
H=$1; W=$2; G=$3; shift 3
mkdir -p "$G"
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export PATH=<toolchain>/pinned-verilator-5.050:<toolchain>/sv2v-v0.0.12:<make-4.3>/bin:${EXTRA_PATH:+$EXTRA_PATH:}/usr/local/bin:/usr/bin:/bin
export VERILATOR=<toolchain>/pinned-verilator-5.050/verilator TSN_GEN_ROOT=<mgmt-root>/tools/tsn-gen-deca300c PYTHONHASHSEED=0
export TMPDIR=${GATE_TMPDIR:-<scratch>/tmp}
for spec in "$@"; do
  id=${spec%%=*}; cmd=${spec#*=}
  { echo "# head $H gate $id: $cmd"; bash -c "$cmd"; } > "$G/$id.log" 2>&1
  rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc $(date -Iseconds)" >> "$G/progress.txt"
done
git status --porcelain --untracked-files=no > "$G/tree-after.txt"
echo done > "$G/DONE"
