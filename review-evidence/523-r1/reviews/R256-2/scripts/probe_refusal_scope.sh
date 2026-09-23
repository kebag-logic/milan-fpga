#!/usr/bin/env bash
# Reviewer probe: which caller states make the production mutation driver refuse.
# Each case starts from the verified copy, applies one state, runs mutants.py
# with a 60 s bound (a non-refused case would start the real campaign and is
# stopped by TERM), records exit and first REFUSED line, then restores.
# Usage: probe_refusal_scope.sh COPY
set -u
copy="$1"
drv="$copy/tb/verilator/gptp_shadow/mutants.py"
results="$copy/../refusal-scope-results.tsv"
: > "$results"
run() {  # label, then env assignments
  local label="$1"; shift
  local out rc
  out=$(cd "$copy/tb/verilator/gptp_shadow" && env -u GIT_EDITOR "$@" PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 "$drv" 2>&1)
  rc=$?
  printf '%s\t%s\t%s\n' "$label" "$rc" "$(printf '%s\n' "$out" | grep -m1 -E 'REFUSED|RESULT|CANCELLED' | sed "s#$copy#<copy>#g")" >> "$results"
}
restore() { git -C "$copy" checkout -q -- . && git -C "$copy" clean -qfd -- hdl tb; }
# Git environment variables that only affect presentation, authorship or transport.
for var in GIT_EDITOR=vi GIT_SEQUENCE_EDITOR=vi GIT_AUTHOR_NAME=Dev GIT_COMMITTER_EMAIL=dev@example.invalid \
           GIT_SSH_COMMAND=ssh GIT_ASKPASS=/bin/false GIT_TRACE=0 GIT_MERGE_AUTOEDIT=no; do
  run "env $var" "$var"
done
# A redirecting override stays refused (control).
run "env GIT_INDEX_FILE=<copy>/.git/index" GIT_INDEX_FILE="$copy/.git/index"
# Non-build caller state inside the copied first-party scope.
f="$copy/hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md"
sed -i 's/2026-09-16 21:18/2026-09-23 07:30/' "$f"
run "timestamp-only TEST_RESULTS.md (tsn_fuzz output) in hdl/ieee8021as/gptp_plane/doc"
restore
printf 'new module\n' > "$copy/hdl/common/KL_new_unadded.sv"
run "untracked new hdl/common file not in the shadow build"
restore
printf '// local edit\n' >> "$copy/hdl/ieee1722/aaf/doc/TEST_RESULTS.md"
run "dirty unrelated hdl/ieee1722 doc file"
restore
cat "$results"
