preflight() {
  local name="$1"
  shift
  "$@" > "$OUT/preflight/$name.log" 2>&1
  local status=$?
  cat "$OUT/preflight/$name.log"
  return "$status"
}
prepare_logs() {
  mkdir -p "$OUT/preflight" || exit 2
  rm -f "$OUT"/*.log "$OUT/preflight"/*.log || exit 2
  LOGS_READY=1
}
run_preflight_gates() {
  if ! selftest_out=$(preflight test_suite_cancellation python3 "$ROOT/scripts/test_suite_cancellation.py" 2>&1); then
    echo "$selftest_out" >&2
    echo "ABORTING: sweep cancellation controls failed." >&2
    exit 2
  fi
  # The tallying tool gets its own gate, run BEFORE the 40-minute sweep rather
  # than after: if the thing that turns logs into the headline number is broken,
  # the number it would print is worthless and there is no point measuring.
  if ! selftest_out=$(preflight suite_tally python3 "$ROOT/scripts/suite_tally.py" --selftest 2>&1); then
    echo "$selftest_out" >&2
    echo "ABORTING: scripts/suite_tally.py fails its own self-test, so any check" >&2
    echo "total this sweep printed would be unreliable." >&2
    exit 2
  fi

  if ! selftest_out=$(preflight suite_shards python3 "$ROOT/scripts/suite_shards.py" --selftest 2>&1); then
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
  #
  # Exit 3 is not a failing self-test (#438): every arm passed and only a
  # temporary tree it built could not be removed. Nothing the arms measured is
  # in doubt, so the sweep prints the leftover and goes on; aborting there once
  # stranded a required context on a change that never touched the checker.
  # Every other non-zero status still aborts.
  selftest_out=$(cd "$ROOT" && \
          preflight check_merge_containment python3 "$ROOT/scripts/check_merge_containment.py" --selftest 2>&1)
  selftest_rc=$?
  case "$selftest_rc" in
    0) ;;
    3) echo "$selftest_out" >&2
       echo "CLEANUP: scripts/check_merge_containment.py passed every self-test arm" >&2
       echo "but left a temporary tree behind; its verdicts stand, the sweep goes on." >&2 ;;
    *) echo "$selftest_out" >&2
       echo "ABORTING: scripts/check_merge_containment.py fails its own self-test," >&2
       echo "so its 'contained' verdicts cannot be trusted either." >&2
       exit 2 ;;
  esac

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
          preflight check_results_fresh python3 "$ROOT/scripts/check_results_fresh.py" --self-test 2>&1); then
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
  if ! selftest_out=$(cd "$ROOT" && preflight check_list_hermetic bash "$ROOT/syn/yosys/check_list_hermetic.sh" 2>&1); then
    echo "$selftest_out" >&2
    echo "ABORTING: syn/yosys/check_list_hermetic.sh fails: run.sh --list no" >&2
    echo "longer stands alone, so the portability aggregate could redden on a" >&2
    echo "submodule-free checkout again (#190)." >&2
    exit 2
  fi

  # Fifth of the family: xvlog_gate.py is a Vivado front-end parse gate whose
  # LIVE detection needs xvlog and so only runs on a bench box, but its parser,
  # its dedup and its ratchet diff are pure Python and rot the same way the tally
  # does. --selftest exercises those arms and skips the xvlog one cleanly, so the
  # gate cannot rot into a green between the bench runs that use it (#132).
  if ! selftest_out=$(cd "$ROOT" && \
          preflight xvlog_gate python3 "$ROOT/scripts/xvlog_gate.py" --selftest 2>&1); then
    echo "$selftest_out" >&2
    echo "ABORTING: scripts/xvlog_gate.py fails its own self-test, so its" >&2
    echo "front-end findings cannot be trusted either." >&2
    exit 2
  fi

  # Sixth of the family: check_merge_review_integrity.py reports a PR that merged
  # against a NEGATIVE review or left its linked Issue open. The scan itself is a
  # post-merge act over the GitHub window and cannot run from here, but its
  # --selftest drives the pure assess_pr core over fixtures - including the
  # negative control and a vacuity arm - so the detector cannot rot into a green
  # that means nothing (#180), exactly as the containment self-test above.
  if ! selftest_out=$(cd "$ROOT" && \
          preflight check_merge_review_integrity python3 "$ROOT/scripts/check_merge_review_integrity.py" --selftest 2>&1); then
    echo "$selftest_out" >&2
    echo "ABORTING: scripts/check_merge_review_integrity.py fails its own" >&2
    echo "self-test, so its review-integrity findings cannot be trusted." >&2
    exit 2
  fi
}
