#!/usr/bin/env bash
# Replay of the reviewer's new-suite walkthrough (#727 round 3) at one head.
# Usage: new_suite_walkthrough.sh CHECKOUT HEAD_SHA STEPS_DIFF WORKDIR
# Clones CHECKOUT at HEAD_SHA into WORKDIR/clone, plants tb/verilator/zz_new_suite,
# applies STEPS_DIFF (the docstring's steps 1 and 2 as the reviewer applied
# them), and runs the selector self-test, the six --list outputs, ci_events
# --check/--selftest and the serial sweep's preflight (driver copy ending at
# run_preflight_gates, so no suite runs). CHECKOUT is only read.
set -u
checkout=$1 head=$2 diff=$3 work=$4
rm -rf "$work/clone"
mkdir -p "$work"
git clone -q --no-hardlinks "$checkout" "$work/clone" || exit 2
cd "$work/clone" || exit 2
git checkout -q "$head" || exit 2
mkdir tb/verilator/zz_new_suite
printf 'all:\n\t@echo zz_new_suite ok\n' > tb/verilator/zz_new_suite/Makefile
echo "== stage 0 (planted, no figure)"
python3 -I scripts/suite_shards.py --selftest > /dev/null 2>&1; echo "selftest rc=$?"
scripts/run_all_suites.sh --shard 0/5 --list > /dev/null 2>&1; echo "--shard 0/5 --list rc=$?"
git apply "$diff" || exit 2
echo "== after steps 1 and 2"
python3 -I scripts/suite_shards.py --selftest > "$work/selftest.txt" 2>&1; echo "selftest rc=$?"
grep -E 'head worker|provisional figures|specialized owners' "$work/selftest.txt"
for i in 0 1 2 3 4 5; do scripts/run_all_suites.sh --shard "$i/6" --list; done | sort > "$work/union.txt"
scripts/run_all_suites.sh --list | sort > "$work/inventory.txt"
cmp -s "$work/union.txt" "$work/inventory.txt" && echo "six lists: union == inventory, no duplicates ($(wc -l < "$work/inventory.txt") suites)"
echo "worker 5/6: $(scripts/run_all_suites.sh --shard 5/6 --list | tr '\n' ' ')"
python3 scripts/ci_events.py --check > "$work/ci_check.txt" 2>&1; echo "ci_events --check rc=$? :: $(tail -1 "$work/ci_check.txt")"
python3 scripts/ci_events.py --selftest > "$work/ci_selftest.txt" 2>&1; echo "ci_events --selftest rc=$? :: $(tail -1 "$work/ci_selftest.txt")"
python3 - <<'EOF'
t = open("scripts/run_all_suites.sh").read()
o = "  run_preflight_gates\n  run_suites\n  summarise\n}\n\nmain \"$@\"\n"
assert t.count(o) == 1
open("scripts/zz_preflight_only.sh", "w").write(
    t.replace(o, "  run_preflight_gates\n  echo PREFLIGHT_DONE\n}\n\nmain \"$@\"\n"))
EOF
chmod +x scripts/zz_preflight_only.sh
scripts/zz_preflight_only.sh "$work/preflight-out" > "$work/preflight.txt" 2>&1
echo "serial preflight rc=$? :: $(tail -1 "$work/preflight.txt")"
