#!/usr/bin/env bash
# usage: PY312=<CPython 3.12.3> V312=<3.12.3 with PyYAML> item3.sh LANE HEAD COPY EVIDENCE
# Follows the selector docstring's new-suite steps in a disposable clone.
# COPY and EVIDENCE are removed and recreated; LANE is only cloned.
set -u
LANE="$1"; HEAD="$2"; C="$3"; E="$4"
PY312="${PY312:-python3}"
V312="${V312:-python3}"
TOOLS="$(cd "$(dirname "$0")" && pwd)"
rm -rf "$C" "$E"; mkdir -p "$E"
git clone -q --no-hardlinks "$LANE" "$C" || exit 1
git -C "$C" checkout -q --detach "$HEAD" || exit 1
echo "copy $(git -C "$C" rev-parse HEAD) toplevel $(git -C "$C" rev-parse --show-toplevel)"
cd "$C" || exit 1
step() { local name="$1"; shift; "$@" > "$E/$name.txt" 2>&1; echo "rc=$? $name"; }
# The planted suite.
mkdir tb/verilator/zz_new_suite
printf 'all:\n\t@echo "zz_new_suite: planted for the new-suite steps; never run here"\n' \
  > tb/verilator/zz_new_suite/Makefile
# The serial preflight on its own: the driver's bytes with main's last two
# calls (run_suites, summarise) left out. Untracked, in the copy only.
head -n -1 scripts/run_all_suites.sh > scripts/run_preflight_only.sh
printf '%s\n' "# Verification only: main's steps up to and including the preflight." \
  'parse_args "$@"' select_suites acquire_lock prepare_logs run_preflight_gates \
  'echo "PREFLIGHT PASSED: every gate before the first suite exited 0"' \
  >> scripts/run_preflight_only.sh
chmod +x scripts/run_preflight_only.sh
diff scripts/run_all_suites.sh scripts/run_preflight_only.sh > "$E/preflight-only.diff"
echo "== planted, no figure"
step 0-selftest $PY312 scripts/suite_shards.py --selftest
step 0-list-shard0of5 scripts/run_all_suites.sh --shard 0/5 --list
step 0-serial-sweep timeout 300 scripts/run_all_suites.sh "$E/0-serial-sweep-out"
step 0-preflight-only timeout 300 scripts/run_preflight_only.sh "$E/0-preflight-out"
echo "== step 1"
sed -n '/^suite_timeout() {/,/^}/p' scripts/run_all_suites.sh > "$E/1-suite_timeout.txt"
step 1-edits $PY312 -I "$TOOLS/new_suite_steps.py" "$C" step1
step 1-selftest $PY312 scripts/suite_shards.py --selftest
echo "== step 2"
step 2-edits $PY312 -I "$TOOLS/new_suite_steps.py" "$C" step2
git diff > "$E/steps-1-2.diff"
git diff --stat > "$E/steps-1-2.stat"
step 2-selftest-3.12.3 $PY312 scripts/suite_shards.py --selftest
step 2-selftest-host python3 scripts/suite_shards.py --selftest
step 2-ci_events-check $V312 scripts/ci_events.py --check
step 2-ci_events-selftest $V312 scripts/ci_events.py --selftest
for i in 0 1 2 3 4 5; do step "2-list-$i-of-6" scripts/run_all_suites.sh --shard "$i/6" --list; done
step 2-list-serial scripts/run_all_suites.sh --list
cat "$E"/2-list-[0-5]-of-6.txt | sort > "$E/2-union.txt"
sort -u "$E/2-union.txt" | cmp -s - "$E/2-union.txt"; echo "rc=$? no suite on two workers ($(wc -l < "$E/2-union.txt") listed)"
sort "$E/2-list-serial.txt" | cmp -s - "$E/2-union.txt"; echo "rc=$? union equals the serial inventory ($(wc -l < "$E/2-list-serial.txt") suites)"
test "$(cat "$E/2-list-5-of-6.txt")" = milan_dp; echo "rc=$? 5/6 is milan_dp alone"
grep -qFx tsn_fuzz "$E/2-list-1-of-6.txt"; echo "rc=$? tsn_fuzz on 1/6"
grep -qFx chmap_capture "$E/2-list-3-of-6.txt"; echo "rc=$? chmap_capture on 3/6"
echo "zz_new_suite on: $(grep -lFx zz_new_suite "$E"/2-list-[0-5]-of-6.txt | xargs -n1 basename)"
start=$(date +%s)
step 2-preflight-only timeout 540 scripts/run_preflight_only.sh "$E/2-preflight-out"
echo "   preflight took $(( $(date +%s) - start )) s; logs: $(ls "$E/2-preflight-out/preflight" | tr '\n' ' ')"
