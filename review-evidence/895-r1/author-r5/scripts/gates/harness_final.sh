#!/bin/bash
# The CPU budget harness at both points on the final head (lane 895), for each leg named: a fresh build of the leg's
# point and arm on a clean clone of HEAD, one sample group run on it, its executable's sha256 against the measurement
# leg's build, the sample's log against the measurement's own (cmp), and every group's measured log regraded on the
# fresh build by the head's graders (run.py --regrade), which refuses a script the head's scenario no longer makes.
# usage: harness_final.sh HEAD SPEC...   SPEC = NAME:POINT:VARIANT:MEASURED_BUILD:MEASURED_RESULTS:SAMPLE_GROUP[:GROUPS]
set -u
H=$1; shift
S=$MANAGEMENT/2026-09-23/895-a775/scripts
T=/data-2/milan/tmp/895-a775
GR=${GATES_ROOT:-$T/r5/gates}
O=$GR/out/harness
mkdir -p "$O"
. "$S/env.sh"
for spec in "$@"; do
  IFS=: read -r n p v m r g sel <<< "$spec"
  W=$GR/harness-wt-$n
  [ -d "$W" ] || bash "$S/clone.sh" "$W" "$H" > "$O/$n-clone.log" 2>&1
  cd "$W" || exit 3
  test "$(git rev-parse HEAD)" = "$H" || exit 4
  export TMPDIR=$GR/tmp/harness-$n; mkdir -p "$TMPDIR"
  b=$T/builds/${BUILD_PREFIX:-F5}-$n
  extra=(); [ "$v" != none ] && extra+=(--variant "$v")
  groups=(); [ -n "${sel:-}" ] && groups+=(--groups "$sel")
  echo "$(date +%T) $n start: point $p variant $v, measured $m/$r, sample $g" >> "$O/summary.txt"
  PYTHONUNBUFFERED=1 python3 -B tb/verilator/ctrl_service_budget/run.py --point "$p" --build-dir "$b" "${extra[@]}" \
    --groups "$g" --record-budget-findings --record-share-findings --jobs 1 > "$O/$n-sample.log" 2>&1
  echo $? > "$O/$n-sample.rc"
  python3 - "$b/build.json" "$T/builds/$m/build.json" > "$O/$n-sha.txt" <<'PY'
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
same = a['executable_sha256'] == b['executable_sha256']
print(f"head build   {a['executable_sha256']}\nmeasured     {b['executable_sha256']}\n"
      f"{'IDENTICAL' if same else 'DIFFERENT'} executables; variant {a.get('variant')} / {b.get('variant')}")
sys.exit(0 if same else 1)
PY
  echo $? > "$O/$n-sha.rc"
  cmp "$b/results/$g.log" "$T/builds/$m/$r/$g.log" > "$O/$n-cmp.txt" 2>&1 && echo "IDENTICAL logs: $g" >> "$O/$n-cmp.txt"
  echo $? > "$O/$n-cmp.rc"
  rm -rf "$b/results-regrade"; mkdir -p "$b/results-regrade"
  cp "$T/builds/$m/$r/"*.txt "$T/builds/$m/$r/"*.log "$b/results-regrade/"
  PYTHONUNBUFFERED=1 python3 -B tb/verilator/ctrl_service_budget/run.py --point "$p" --build-dir "$b" "${extra[@]}" \
    "${groups[@]}" --regrade --out "$b/results-regrade" --record-budget-findings --record-share-findings \
    > "$O/$n-regrade.log" 2>&1
  echo $? > "$O/$n-regrade.rc"
  git status --short --untracked-files=all > "$O/$n-tree-after.txt"
  echo "$(date +%T) $n done: sample rc $(cat $O/$n-sample.rc), sha rc $(cat $O/$n-sha.rc), cmp rc $(cat $O/$n-cmp.rc), regrade rc $(cat $O/$n-regrade.rc)" >> "$O/summary.txt"
done
