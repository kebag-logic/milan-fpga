[A839] REVIEW READY (round 3)
Commit: 13e6d869d842fc06155ef5dae9b0347596d6d4df (branch cicd-3, local, not pushed; three commits on PR #1001's
head fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f, which is untouched, as is cicd-verilator-perf)
  66b092e124479b3f30ebeb1d521ea53267a61686  preflight once per head
  f6c11a2502b9377cbeced2a78011a6f52c196242  stable mutant staging
  13e6d869d842fc06155ef5dae9b0347596d6d4df  longest case first

Changed:
- scripts/run_all_suites.sh: --preflight-only; --no-preflight (refused without --ci-pieces).
- scripts/ci_suite_workflows.py + regenerated .github/workflows/rtl.yml: the verilator-preflight job; the workers
  run --no-preflight; verilator-suites requires the job's success and its SHA record.
- scripts/suite_preflight_controls.py (new), scripts/test_suite_cancellation.py (stays at its 1000-line ratchet):
  controls for both modes.
- scripts/ci_suite_pieces_selftest.py: six executable binding controls.
- scripts/mutant_stage.py (new): 38 mutation drivers' staging; gptp_shadow/test_mutant_lifecycle.py's fixtures and
  scratch check.
- scripts/ci_events.py and .github/ci-templates/docs.yml (+ generated docs.yml): `mutant_stage.py --selftest` in
  the pinned "CI scheduling and evidence controls" step.
- scripts/ci_make_cases.py: CASE_SECONDS, start_order(), execute_all(); scripts/ci_make_cases_selftest.py.
- docs/testing/CI_WORKFLOWS.md, docs/testing/TESTING.md.

Validation (exact commands in REPORT and PR-BODY; logs in receipts/gates/, run at 13e6d869 in a clean clone):
- ci_gate_workflows --check, ci_events --check (2287 items), ci_events --selftest (5755 arms): PASS
- every "CI scheduling and evidence controls" command (14 self-tests and checks + mutant_stage --selftest): exit 0
- suite_shards --selftest, test_suite_cancellation.py, gptp_shadow test_mutant_lifecycle.py: PASS
- check_py_idiom, check_sh_idiom, check_hygiene, measure_naming, measure_fail_fast, measure_test_evidence,
  check_todo_ownership, check_doc_paths, check_doc_style, docs_check, check_archive, docs_inventory, gen_toc
  --check/--verify-anchors, check_em_dash --base fcbc31f3: exit 0
- Contract mutation self-test (ci_events --selftest) PASS at 13e6d869, 413 s; 36 gates in receipts/gates/summary, all rc=0
- Measurements (REPORT 1.3, 2.3, 3.3): shard 9/19 replica with and without preflight, logs and receipts
  IDENTICAL; milan_dp__0 list order vs longest first, receipts IDENTICAL; five mutation drivers cold/warm/second
  checkout, logs IDENTICAL.

Acceptance criteria (the round-3 task list):
- 1 Preflight once per head: met. One job runs it. The shards consume its result for the same SHA through
  verilator-suites (round 2 §5: a shard cannot read a parallel job), and fail-fast cancels on its failure.
  Required contexts are unchanged and fork safety is kept. Shard time drop measured: +535 s → +2 s to the first
  suite, −134 CPU-s. A failing preflight fails the run, shown by executing the generated step.
- 2 Longest case first: met. milan_dp__0 through its driver 3411.9 s → 2711.8 s wall (−20.5 %) at the same instructions; receipts identical.
- 3 Stable mutant staging: met. The warm-cache hit rate rises (crf_rx 79/115 → 115/115), and every mutant is
  still killed by the same named check. Finding 3: same cause, fixed.
- 4 SMT patch: written and not applied; measured before/after on shard 8. No gain today; the reason is measured
  and named in the patch.
- 5 FPGA-gPTP branch: ready, not pushed; PR-BODY-fpgagptp.md.
- 6 PROPOSAL-hosted-ccache.md: written; nothing in ci/image was edited and no cache was deleted.

Open risks/questions:
- Not run: an act replay (needs a pushed head) and the full serial sweep. A hosted run must confirm the
  per-worker drop and re-measure WORKER_OVERHEAD_SECONDS.
- The CI tool inventory stays red, as at the base.
- f6c11a25 is b01326c5 amended: the helper's `dir` parameter renamed `parent`, no behaviour change. The mutant
  measurement ran b01326c5, and the gates ran f6c11a25. 13e6d869 is 0572488b amended with aclk's and
  render-mutants' final costs, which changed no start order; the piece measurement ran 0572488b.
