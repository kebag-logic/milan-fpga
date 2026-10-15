#!/usr/bin/env bash
# R636-5 generator mismatch plants. Usage: probe_generator.sh <extracted-head-tree>
# Each arm edits a fresh copy of .github/ci-templates/rtl.yml (or the generated
# workflow), runs the generator's --check (template arms) and the CI-event
# contract check, prints the outcome, and restores the original bytes.
set -u
S=${1:?tree}
cd "$S" || exit 2
T=.github/ci-templates/rtl.yml
W=.github/workflows/rtl.yml
cp "$T" /tmp/r636-5-template.orig
cp "$W" /tmp/r636-5-workflow.orig
gen() { python3 scripts/ci_gate_workflows.py --check >/tmp/r636-5-gen.out 2>&1; echo $?; }
evt() { python3 scripts/ci_events.py --check >/tmp/r636-5-evt.out 2>&1; echo $?; }
arm() {
  name=$1; shift
  cp /tmp/r636-5-template.orig "$T"; cp /tmp/r636-5-workflow.orig "$W"
  "$@"
  g=$(gen); e=$(evt)
  gm=$(grep -m1 -o 'ValueError: .*\|regenerate the gate jobs' /tmp/r636-5-gen.out)
  echo "$name | generator_rc=$g ($gm) | ci_events_rc=$e"
}
arm "control: head bytes" true
arm "stale arm index (total 6, arm 4)" sed -i 's/^            5) test "\$(cat "\$RUNNER_TEMP\/owned-suites")" = milan_dp ;;/            4) test "$(cat "$RUNNER_TEMP\/owned-suites")" = milan_dp ;;/' "$T"
arm "arm deleted" sed -i '/^            5) test "\$(cat "\$RUNNER_TEMP\/owned-suites")" = milan_dp ;;/d' "$T"
arm "expect mismatched (--expect 5)" sed -i 's/--require-target-sha --expect 6 /--require-target-sha --expect 5 /' "$T"
arm "total 7 without arm/expect" sed -i 's/^        total: \[6\]/        total: [7]/' "$T"
arm "consistent recount (total 7, shard 0-6, arm 6, --expect 7)" sed -i -e 's/^        shard: \[0, 1, 2, 3, 4, 5\]/        shard: [0, 1, 2, 3, 4, 5, 6]/' -e 's/^        total: \[6\]/        total: [7]/' -e 's/^            5) test "\$(cat/            6) test "$(cat/' -e 's/--require-target-sha --expect 6 /--require-target-sha --expect 7 /' "$T"
arm "duplicate arm (arm 5 twice)" sed -i 's/^\(            5) test "\$(cat "\$RUNNER_TEMP\/owned-suites")" = milan_dp ;;\)$/\1\n\1/' "$T"
arm "extra stale arm 4 beside arm 5" sed -i 's/^\(            5\)\() test "\$(cat "\$RUNNER_TEMP\/owned-suites")" = milan_dp ;;\)$/            4\2\n\1\2/' "$T"
arm "hand-edited generated workflow (--expect 15)" sed -i 's/--require-target-sha --expect 16 /--require-target-sha --expect 15 /' "$W"
cp /tmp/r636-5-template.orig "$T"; cp /tmp/r636-5-workflow.orig "$W"
echo "restored: generator_rc=$(gen) ci_events_rc=$(evt)"
