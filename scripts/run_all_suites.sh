#!/usr/bin/env bash
#
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Run the default Verilator sweep, or the separate scheduled physical suite.
#
#   scripts/run_all_suites.sh [outdir] [--wait] [--shard INDEX/TOTAL] [--physical-gptp]
#   scripts/run_all_suites.sh [--shard INDEX/TOTAL] --list
#   scripts/run_all_suites.sh [outdir] [--wait] --preflight-only
#   scripts/run_all_suites.sh [outdir] [--wait] --ci-pieces --no-preflight --shard INDEX/TOTAL
#
# --preflight-only runs the preflight self-tests below, under the same lock,
# log preparation and signal handling, and no suite: exit 0 when every one
# holds, 2 when one fails. --no-preflight skips them, and is accepted only
# with --ci-pieces: the hosted workers' run has a preflight job that runs them
# once for the head, and the verilator-suites aggregate requires that job's
# success for the same SHA (docs/testing/CI_WORKFLOWS.md, "Exhaustive
# validation"). The serial sweep, --physical-gptp and every local run keep
# their preflight. Issue #998; REQ-VER-01 and REQ-VER-04.
#
# Each suite is a directory with its own Makefile; the default target builds
# and runs every shape that suite owns (several own more than one - milan_dp
# runs legacy + N=4 + N=8, csr runs three windows). Per-suite output is written
# to <outdir>/<suite>.log so a failure can be read after the fact; the summary
# is the only thing on stdout.
#
# Exit status:
#   0        every suite passed AND every check count was readable
#   1..89    that many suites FAILED (unchanged - CI can still gate on it). A
#            suite whose make exited 0 while its log reports a failure - a
#            [FAIL] line or a tally counting one - is a FAILED suite here too
#            (scripts/suite_tally.py --verdict), because an assertion that
#            only logs is exactly the false green Rule 6 exists to stop.
#   90       every suite passed, but the CHECK ACCOUNTING is incomplete: some
#            suite's count could not be read, so the printed total is a partial
#            sum and must not be quoted. See scripts/suite_tally.py.
#   91       REFUSED: another sweep is already running in this tree.
#   92       some suite was KILLED BY THE WALL CLOCK. Its result is UNKNOWN -
#            it is not a failure and it is not a pass. Re-run it uncontended.
#   130/143  cancelled by INT/TERM; partial logs, no completed summary.
#   other    the launched process was stopped without cleanup: KILL, or HUP
#            or another fatal signal it does not handle, to it or its group.
#            The caller sees that signal. The sweep shell dies with it: no
#            later suite, no summary, no cleanup. A suite already running may
#            finish and holds the lock until then.
#
# Environment:
#   SUITE_TIMEOUT        explicit wall clock override for every selected suite.
#                        Defaults: 1800 s; capture_coherence gets 2400 s,
#                        milan_dp_mclk 3600 s, milan_dp 4800 s, the
#                        scheduled milan_dp_gptp 6900 s, media_phase
#                        1400 s, and reboot_ctrl, input_loopback and
#                        input_loopback_dp 300 s (suite_timeout below).
#                        See docs/testing/TESTING.md for the physical timer floor.
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
#    contention from parallel lanes a perfectly healthy suite exceeds the wall
#    clock and got reported as a test failure -
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
# STRICT MODE, DECLINED, AND WHY (Rule 13, docs/development/CODE_QUALITY.md).
# This driver keeps `set -u` and takes neither `-e` nor `pipefail`. Errexit
# would END THE SWEEP AT THE FIRST RED SUITE, and continuing past a failing
# step is not an oversight here - it is the product. The loop below runs every
# selected suite, takes `timeout`'s status for each one, and turns the results
# into an exit code that is a COUNT: 1..89 failures, 90 incomplete accounting,
# 92 a wall-clock UNKNOWN. Under `-e` the first suite that exits non-zero -
# or the first one the wall clock kills, which defect 3 above says is not a
# failure at all - aborts the run at that line, and every number in the
# summary is then MISSING rather than wrong, which is the one outcome this
# script exists to prevent. The statuses that matter are already taken on the
# spot (`rc=$?` after each suite, `tally_rc=$?` after the count), and every
# prerequisite is tested with `if ! out=$(...)`, so this script already fails
# when the things it runs fail - which is what Rule 13 is asking for, and
# errexit is not how it gets there. `pipefail` is left out with the rest of
# the trio rather than added for a half-effect: on its own it does not clear
# the finding, and it would change the status of the `printf | sed` that
# indents a masked verdict.
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# A separate owner adopts and reaps the entire command subtree, even children
# that detach or ignore TERM. The launched PID becomes that owner, and it runs
# this shell in its own session; a parent-death signal kills this shell if the
# owner dies without cleanup, so a hard stop never leaves the loop detached.
# Install the shell's terminal traps before any selection, lock wait or
# preflight can start. The private argument is consumed only on re-entry from
# that owner; it is not a supported sweep option.
if [ "${1:-}" != "--owned-sweep" ]; then
  exec python3 "$ROOT/scripts/owned_process.py" -- bash "$0" --owned-sweep "$@"
fi
shift

# Every build and every mutant rebuild compiles the same Verilator runtime
# (verilated.cpp alone is most of a small model's compile) and, for a mutant,
# the same testbench. verilated.mk prefixes each compile with $(OBJCACHE), so
# where ccache is installed the sweep uses it: crf_rx's 23 mutants take 47 %
# less CPU on a cold cache, with byte-identical results. A caller's OBJCACHE,
# empty included, is kept; with no ccache nothing changes.
if [ -z "${OBJCACHE+set}" ] && command -v ccache > /dev/null 2>&1; then
  export OBJCACHE=ccache
fi
LOGS_READY=0
cancelled() {
  echo "CANCELLED: $1; no completed sweep result" >&2
  if [ "$LOGS_READY" = 1 ]; then
    echo "partial logs: $OUT" >&2
  else
    echo "logs were not prepared for this invocation" >&2
  fi
  exit "$2"
}
trap 'cancelled INT 130' INT
trap 'cancelled TERM 143' TERM

WAIT=0
OUT=""
SHARD="0/1"
LIST=0
PHYSICAL_GPTP=0
CI_PIECES=0
PREFLIGHT_ONLY=0
NO_PREFLIGHT=0
SHARD_GIVEN=0

#! the command line: [outdir] [--wait] [--shard INDEX/TOTAL] [--list]
parse_args() {
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --wait) WAIT=1; shift ;;
      --list) LIST=1; shift ;;
      --physical-gptp) PHYSICAL_GPTP=1; shift ;;
      --ci-pieces) CI_PIECES=1; shift ;;
      --preflight-only) PREFLIGHT_ONLY=1; shift ;;
      --no-preflight) NO_PREFLIGHT=1; shift ;;
      --shard)
        [ "$#" -ge 2 ] || { echo "--shard needs INDEX/TOTAL" >&2; exit 2; }
        SHARD="$2"; SHARD_GIVEN=1; shift 2 ;;
      --shard=*) SHARD="${1#--shard=}"; SHARD_GIVEN=1; shift ;;
      -*)        echo "unknown option: $1" >&2; exit 2 ;;
      *)
        [ -z "$OUT" ] || { echo "more than one output directory" >&2; exit 2; }
        OUT="$1"; shift ;;
    esac
  done
  if [ "$PREFLIGHT_ONLY" = 1 ] && \
     [ "$LIST$PHYSICAL_GPTP$CI_PIECES$NO_PREFLIGHT$SHARD_GIVEN" != 00000 ]; then
    echo "--preflight-only selects no suite: it takes only [outdir] and --wait" >&2
    exit 2
  fi
  if [ "$NO_PREFLIGHT" = 1 ] && [ "$CI_PIECES" != 1 ]; then
    echo "--no-preflight is only for --ci-pieces workers, whose run's preflight job" >&2
    echo "runs the self-tests once for the head; every other sweep keeps them" >&2
    exit 2
  fi
  OUT="${OUT:-$ROOT/.suite-logs}"
  # Prerequisites may change directory. Keep every log in the caller's OUT.
  case "$OUT" in
    /*) ;;
    *) OUT="$PWD/$OUT" ;;
  esac
}

#! the suites this invocation owns, into `suites` (or --list and out)
select_suites() {
  # Selection is delegated to a self-tested helper. Its default 0/1 result is
  # the default inventory in lexical order. The physical leg has its own
  # explicit selection. --list is read-only and takes no sweep lock.
  selector=(python3 "$ROOT/scripts/suite_shards.py"
    --suite-root "$ROOT/tb/verilator" --shard "$SHARD")
  [ "$PHYSICAL_GPTP" = 1 ] && selector+=(--physical-gptp)
  [ "$CI_PIECES" = 1 ] && selector+=(--ci-pieces)
  if [ "$LIST" = 1 ]; then
    exec "${selector[@]}"
  fi

  if ! selected_out=$("${selector[@]}" 2>&1); then
    echo "$selected_out" >&2
    exit 2
  fi
  mapfile -t suites < <(printf '%s' "$selected_out")
  if [ "${#suites[@]}" -eq 0 ]; then
    echo "shard $SHARD owns no suites; choose fewer workers" >&2
    exit 2
  fi
}

# --- concurrency guard -------------------------------------------------------
# Scope is the repo root, which is exactly the collision domain: the obj_* dirs
# live under this root's tb/verilator/. Separate worktrees have separate roots
# and so do not block each other.
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

#! serialise sweeps in this tree, and record who holds it
acquire_lock() {
  LOCK="${SUITE_SWEEP_LOCK:-$ROOT/.run_all_suites.lock}"
  LOCK_OWNER="$LOCK.owner"

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
  trap cleanup EXIT
  printf 'pid %s  host %s  started %s\n  outdir %s\n' \
         "$$" "$(uname -n)" "$(date -Is 2>/dev/null || date)" "$OUT" > "$LOCK_OWNER"
}

#! Declared per-suite defaults; an explicit caller override retains its meaning.
#! The CI runner contract pins every budget and each named suite.
#! #673, decision 6015726285: capture_coherence passed in 1642.280 s,
#! milan_dp in 3509.562 s; milan_dp_mclk timed out at 1800.008 s.
#! The new limits leave >=10% in each hosted shard's measured job envelope.
#! CI_WORKFLOWS.md records the samples and per-shard arithmetic.
#! #781: media_phase timed out at 900 s on hosted. 1400 s leaves more than
#! 10% over its projected hosted window (at most about 1240 s). Its own
#! hosted run then passed it in 582 s, and 1400 s is kept for that variance.
#! #803: FPGA-gPTP #90's fifth lost response lengthens the scheduled
#! milan_dp_gptp scenario to 899637137 cycles; its README projects the hosted
#! suite at 5347 to 5484 s, and 6900 s keeps that worst case at 79.5%.
suite_timeout() {
  case "$1" in
    capture_coherence) printf '%s\n' "${SUITE_TIMEOUT:-2400}" ;;
    input_loopback)    printf '%s\n' "${SUITE_TIMEOUT:-300}" ;;
    input_loopback_dp) printf '%s\n' "${SUITE_TIMEOUT:-300}" ;;
    milan_dp)          printf '%s\n' "${SUITE_TIMEOUT:-4800}" ;;
    milan_dp_gptp)     printf '%s\n' "${SUITE_TIMEOUT:-6900}" ;;
    milan_dp_mclk)     printf '%s\n' "${SUITE_TIMEOUT:-3600}" ;;
    media_phase)       printf '%s\n' "${SUITE_TIMEOUT:-1400}" ;;
    reboot_ctrl)       printf '%s\n' "${SUITE_TIMEOUT:-300}" ;;
    usbaudio)          printf '%s\n' "${SUITE_TIMEOUT:-900}" ;;
