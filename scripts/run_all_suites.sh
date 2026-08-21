#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Run every Verilator testbench suite under tb/verilator/ and summarise.
#
#   scripts/run_all_suites.sh [outdir] [--wait] [--shard INDEX/TOTAL]
#   scripts/run_all_suites.sh [--shard INDEX/TOTAL] --list
#
# Each suite is a directory with its own Makefile; the default target builds
# and runs every shape that suite owns (several own more than one - milan_dp
# runs legacy + N=4 + N=8, csr runs three windows). Per-suite output is written
# to <outdir>/<suite>.log so a failure can be read after the fact; the summary
# is the only thing on stdout.
#
# Exit status:
#   0        every suite passed AND every check count was readable
#   1..89    that many suites FAILED (unchanged - CI can still gate on it)
#   90       every suite passed, but the CHECK ACCOUNTING is incomplete: some
#            suite's count could not be read, so the printed total is a partial
#            sum and must not be quoted. See scripts/suite_tally.py.
#   91       REFUSED: another sweep is already running in this tree.
#   92       some suite was KILLED BY THE WALL CLOCK. Its result is UNKNOWN -
#            it is not a failure and it is not a pass. Re-run it uncontended.
#
# Environment:
#   SUITE_TIMEOUT        per-suite wall clock in seconds (default 1800)
#   SUITE_SWEEP_LOCK     lock file path. Defaults to one per repo root, which
#                        is the obj_* collision domain. Point every worktree at
#                        ONE path to serialise sweeps machine-wide instead.
#
# ---------------------------------------------------------------------------
# Three things this script used to get wrong, all of which made it print a
# confident number that was not a measurement:
#
# 1. UNDER-COUNTING.  The total came from `grep -o 'checks: *[0-9]*'`, and the
#    tree emits FIVE different summary shapes: measured on 2026-07-28, that
#    grep saw zero from 29 of the 57 suite logs and only part of two more, a
#    shortfall of 37 784 checks against a figure this project quotes as its
#    evidence that a change is safe. Proven by adding 66 assertions to a suite
#    and watching the printed total not move at all. The tallying now lives in
#    scripts/suite_tally.py, which knows every shape AND FAILS LOUDLY on a
#    count it cannot read, because an unknown must never look like agreement.
#
# 2. CONCURRENT SWEEPS CORRUPTED EACH OTHER.  Every suite builds into a fixed
#    obj_* directory inside its own tb/verilator/<suite>/ (obj_dir, obj_nx,
#    obj_ctx, ...). Two sweeps in the same tree therefore compile and link into
#    the same objects at the same time, and the totals both of them print are
#    contaminated - silently. A whole-sweep lock now makes the second sweep
#    REFUSE instead. Per-invocation build directories would isolate rather than
#    serialise, but the obj_* names are hardcoded in all 57 suite Makefiles, so
#    that is a change to how every suite builds; refusing is the change that
#    only touches the accounting. NOTE the lock covers SWEEPS, not a hand-run
#    `make -C tb/verilator/<suite>` - that still races a sweep in the same tree.
#
# 3. THE WALL CLOCK MANUFACTURED RED RUNS.  Each suite runs under `timeout`,
#    and any non-zero status was recorded as a FAILING SUITE. Under CPU
#    contention from parallel lanes a perfectly healthy suite (hostplane, more
#    than once) exceeds the wall clock and got reported as a test failure -
#    costing someone a hunt for a defect that does not exist. `timeout` exits
#    124 when it is the one that killed the job, so that case is now its own
#    TIMEOUT verdict: not a pass, not a failure, an UNKNOWN, and the sweep says
#    so. Mode 1 makes a green run untrustworthy; mode 3 invented red ones.
#    (The lock cannot prevent mode 3: the contention comes from OTHER
#    worktrees, which have their own roots and so their own locks. What is
#    fixable is the accounting - a suite killed for an unrelated reason must
#    not present itself as a measurement in either direction.)
# ---------------------------------------------------------------------------
#
# NOTE: a run is NOT read-only on the tree. Some suites regenerate their
# `doc/TEST_RESULTS.md` evidence file, which carries a timestamp, so `git
# status` will show those as modified afterwards even when every count is
# unchanged. Commit them when the counts move; revert them when only the
# timestamp did.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

WAIT=0
OUT=""
SHARD="0/1"
LIST=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --wait) WAIT=1; shift ;;
    --list) LIST=1; shift ;;
    --shard)
      [ "$#" -ge 2 ] || { echo "--shard needs INDEX/TOTAL" >&2; exit 2; }
      SHARD="$2"; shift 2 ;;
    --shard=*) SHARD="${1#--shard=}"; shift ;;
    -*)        echo "unknown option: $1" >&2; exit 2 ;;
    *)
      [ -z "$OUT" ] || { echo "more than one output directory" >&2; exit 2; }
      OUT="$1"; shift ;;
  esac
done
OUT="${OUT:-$ROOT/.suite-logs}"

# Selection is delegated to a self-tested helper. Its default 0/1 result is
# exactly the old lexical glob order, so local callers remain an unsharded
# full sweep. --list is intentionally read-only and takes no sweep lock.
if [ "$LIST" = 1 ]; then
  exec python3 "$ROOT/scripts/suite_shards.py" \
    --suite-root "$ROOT/tb/verilator" --shard "$SHARD"
fi

if ! selected_out=$(python3 "$ROOT/scripts/suite_shards.py" \
      --suite-root "$ROOT/tb/verilator" --shard "$SHARD" 2>&1); then
  echo "$selected_out" >&2
  exit 2
fi
mapfile -t suites < <(printf '%s' "$selected_out")
if [ "${#suites[@]}" -eq 0 ]; then
  echo "shard $SHARD owns no suites; choose fewer workers" >&2
  exit 2
fi

# --- concurrency guard -------------------------------------------------------
# Scope is the repo root, which is exactly the collision domain: the obj_* dirs
# live under this root's tb/verilator/. Separate worktrees have separate roots
# and so do not block each other.
LOCK="${SUITE_SWEEP_LOCK:-$ROOT/.run_all_suites.lock}"
LOCK_OWNER="$LOCK.owner"
TMO="${SUITE_TIMEOUT:-1800}"

refuse() {
  echo "REFUSING TO RUN: another sweep is already running in this tree." >&2
  echo "  tree: $ROOT" >&2
  if [ -r "$LOCK_OWNER" ]; then
    echo "  holder:" >&2
    sed 's/^/    /' "$LOCK_OWNER" >&2
  fi
  echo "  Concurrent sweeps share the per-suite obj_* build directories and" >&2
  echo "  corrupt each other's results, so the totals would be meaningless." >&2
  echo "  Wait for it, or re-run with --wait to queue behind it." >&2
  exit 91
}

if command -v flock >/dev/null 2>&1; then
  exec 9>>"$LOCK" || { echo "cannot open $LOCK" >&2; exit 2; }
  if [ "$WAIT" = 1 ]; then
    flock 9 || { echo "cannot lock $LOCK" >&2; exit 2; }
  else
    flock -n 9 || refuse
  fi
  cleanup() { rm -f "$LOCK_OWNER"; }
else
  # Portable fallback: mkdir is atomic. Staleness is checked against the
  # recorded pid so a crashed sweep cannot wedge the tree forever.
  LOCKDIR="$LOCK.d"
  while ! mkdir "$LOCKDIR" 2>/dev/null; do
    stale_pid=$(sed -n 's/^pid \([0-9]*\).*/\1/p' "$LOCK_OWNER" 2>/dev/null)
    if [ -n "$stale_pid" ] && ! kill -0 "$stale_pid" 2>/dev/null; then
      rm -rf "$LOCKDIR" "$LOCK_OWNER"; continue
    fi
    [ "$WAIT" = 1 ] || refuse
    sleep 20
  done
  cleanup() { rm -rf "$LOCKDIR" "$LOCK_OWNER"; }
fi
trap cleanup EXIT INT TERM
printf 'pid %s  host %s  started %s\n  outdir %s\n' \
       "$$" "$(uname -n)" "$(date -Is 2>/dev/null || date)" "$OUT" > "$LOCK_OWNER"

# The tallying tool gets its own gate, run BEFORE the 40-minute sweep rather
# than after: if the thing that turns logs into the headline number is broken,
# the number it would print is worthless and there is no point measuring.
if ! selftest_out=$(python3 "$ROOT/scripts/suite_tally.py" --selftest 2>&1); then
  echo "$selftest_out" >&2
  echo "ABORTING: scripts/suite_tally.py fails its own self-test, so any check" >&2
  echo "total this sweep printed would be unreliable." >&2
  exit 2
fi

if ! selftest_out=$(python3 "$ROOT/scripts/suite_shards.py" --selftest 2>&1); then
  echo "$selftest_out" >&2
  echo "ABORTING: scripts/suite_shards.py fails its own self-test, so the" >&2
  echo "selected workers cannot be trusted to cover every suite once." >&2
  exit 2
fi

# Same argument, different gate: check_merge_containment.py decides whether a
# merge left work behind, and a review pointed out it was wired into nothing at
# all -- its only caller was a sentence in CONTRIBUTING.md telling a human to
# run it. The CHECK itself is a post-merge act nobody can schedule from here,
# but its self-test can be gated exactly like the tally's, so the tool cannot
# rot into a green that means nothing between merges.
if ! selftest_out=$(cd "$ROOT" && \
        python3 "$ROOT/scripts/check_merge_containment.py" --selftest 2>&1); then
  echo "$selftest_out" >&2
  echo "ABORTING: scripts/check_merge_containment.py fails its own self-test," >&2
  echo "so its 'contained' verdicts cannot be trusted either." >&2
  exit 2
fi

# Third gate of the same family: check_results_fresh.py decides whether a
# committed TEST_RESULTS.md still says what its campaign produces. It runs
# inside the tsn_fuzz suite, where tsn-gen is, but its self-test belongs here
# with the others - twelve of its seventeen arms assert a REFUSAL rather than a
# pass (a stale copy, a leftover file, a silent log, a skipped campaign, a
# sections table that does not add up, a stamp stripped off the wrong line), and
# every one of them is a place a careless version would return a green it did
# not earn. A gate that lost those arms would go on passing without saying
# anything.
#
# Both numbers are derived, not typed: seventeen is the tally the tool prints on
# every run, and twelve is how many of its arms expect a verdict other than OK.
# A reader who doubts this line can settle it in nine seconds:
#   python3 scripts/check_results_fresh.py --self-test
if ! selftest_out=$(cd "$ROOT" && \
        python3 "$ROOT/scripts/check_results_fresh.py" --self-test 2>&1); then
  echo "$selftest_out" >&2
  echo "ABORTING: scripts/check_results_fresh.py fails its own self-test, so" >&2
  echo "its 'fresh' verdicts on generated evidence cannot be trusted." >&2
  exit 2
fi

# Fourth of the family: syn/yosys/check_list_hermetic.sh proves `run.sh --list`
# needs only itself and scripts/yosys_shards.py - not a submodule, not
# pp_srcs.py - which is the property the yosys-portability aggregate depends on
# and the one #190 broke. It builds a submodule-free tree and its own negative
# control, needs no yosys or sv2v, and is the durable check #191 deferred (#192).
if ! selftest_out=$(cd "$ROOT" && bash "$ROOT/syn/yosys/check_list_hermetic.sh" 2>&1); then
  echo "$selftest_out" >&2
  echo "ABORTING: syn/yosys/check_list_hermetic.sh fails: run.sh --list no" >&2
  echo "longer stands alone, so the portability aggregate could redden on a" >&2
  echo "submodule-free checkout again (#190)." >&2
  exit 2
fi

mkdir -p "$OUT"
rm -f "$OUT"/*.log            # a stale log from a previous sweep is not evidence

pass=0; fail=0; tmo=0; failed=""; timedout=""
echo "shard: $SHARD   selected suites: ${#suites[@]}"
for suite in "${suites[@]}"; do
  d="$ROOT/tb/verilator/$suite"
  timeout "$TMO" make -C "$d" > "$OUT/$suite.log" 2>&1
  rc=$?
  case $rc in
    0)   pass=$((pass + 1)); printf 'PASS     %s\n' "$suite" ;;
    # 124: timeout(1) killed it. 137: SIGKILL, i.e. timeout's -k follow-up or
    # the OOM killer - either way the suite did not get to render a verdict.
    124|137)
         tmo=$((tmo + 1)); timedout="$timedout $suite"
         printf 'TIMEOUT  %s   (%ss wall clock - result UNKNOWN, not a failure)\n' \
                "$suite" "$TMO" ;;
    *)   fail=$((fail + 1)); failed="$failed $suite"; printf 'FAIL     %s\n' "$suite" ;;
  esac
done

echo "----------------------------------------------------------------"
echo "suites: $((pass + fail + tmo))   passed: $pass   failed: $fail   timed out: $tmo"

# The check total and the in-suite failure total both come from here, so the
# two halves of the headline can never be derived by different rules.
python3 "$ROOT/scripts/suite_tally.py" "$OUT" --quiet
tally_rc=$?

[ -n "$failed" ] && echo "failing suites:$failed"
if [ -n "$timedout" ]; then
  echo "TIMED OUT (result unknown, NOT a failure):$timedout"
  echo "  A suite killed by the wall clock proves nothing either way. This is"
  echo "  usually CPU contention from a parallel sweep in another worktree -"
  echo "  re-run those suites uncontended, or raise SUITE_TIMEOUT."
fi
echo "logs: $OUT"

[ "$fail" -gt 0 ] && exit $fail
[ "$tmo"  -gt 0 ] && exit 92
[ "$tally_rc" -ne 0 ] && exit 90
exit 0
