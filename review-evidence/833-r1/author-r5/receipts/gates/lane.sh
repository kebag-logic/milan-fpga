#!/usr/bin/env bash
# The lane's own gates, one log and one rc per gate, never piped, on a clean clone of the head.
set -u
H=a67eaf66c99b6b07c7ef206ad3489cb9555e00ca; W=$VALIDATION_STORAGE/833-a726e/gates/lane-wt; O=$VALIDATION_STORAGE/833-a726e/gates/lane-out
[ -d "$W" ] || $VALIDATION_STORAGE/833-a726e/tools/clone_at.sh $LANES/833-owned-process "$H" "$W" || exit 2
mkdir -p "$O" $VALIDATION_STORAGE/833-a726e/gates/tmp; cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=$VALIDATION_STORAGE/833-a726e/gates/home VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$VALIDATION_STORAGE/833-a726e/gates/tmp MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
export PATH=$VALIDATION_STORAGE/scratch/a662/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$O/$id.log" 2>&1; rc=$?; echo $rc > "$O/$id.rc"; echo "$id rc=$rc"; }
for g in "$@"; do
  case $g in
    diffcheck) run diffcheck "git diff --check 1f29f189279f9fc0132f4918e47342b87d22f33a HEAD" ;;
    suite) run test_suite_cancellation "python3 scripts/test_suite_cancellation.py" ;;
    lifecycle) run lifecycle "make --no-print-directory -C tb/verilator/gptp_shadow lifecycle" ;;
    behave) PATH=$VALIDATION_STORAGE/sync-a723b/venv-docs/bin:$PATH run behave "cd tests && behave --no-capture -f plain" ;;
  esac
done
git status --short --ignored > "$O/tree-after.txt"
