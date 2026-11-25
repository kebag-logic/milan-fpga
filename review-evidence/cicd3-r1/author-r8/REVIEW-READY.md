[A839] REVIEW READY
Commit: b0f2bc1a784d9f006204491c883ac2b1783e970a
Changed: three commits on `9c625393`, answering round 2's reviews.
- `468c7e47`: `firmware-boundary-capture`'s matrix keeps GitHub's own `fail-fast: true` (R924-2-F1). The change is in the template, the generated `rtl-fast.yml`, `ci_events.py`'s `FIRMWARE_BOUNDARY_STRATEGY` and its arms (`false` refused, the key removed refused), and CI_WORKFLOWS.md.
- `222362ff`: follow_ring's two fine-build recipe lines start with `+`, so make treats them as recursive again (R923-2-F1).
- `b0f2bc1a`: wording. R924-2-R1 adds `Issue #998; REQ-VER-01 and REQ-VER-04.` to every listed block. R924-2-R2 and R923-2-R1 are applied as written. The twin of R924-2-R2's sentence in CI_WORKFLOWS.md is corrected too.
No RTL, firmware, test expectation, graded figure or deal changed.
Validation:
- Local gates: 37 of 37 commands rc 0 at the head in a clean clone. Among them:
  - `python3 scripts/ci_events.py --selftest`: 2378 items, 5968 arms, including "boundary legs cancellation disabled" and "boundary legs fail-fast left to the default", both caught.
  - `python3 scripts/ci_suite_pieces_selftest.py`: 65 parents, 94 units.
  - `python3 scripts/ci_workflow_plan_selftest.py`, `python3 scripts/ci_fail_fast_selftest.py` (fork zero-write), `python3 scripts/suite_shards.py --selftest`, `python3 scripts/ci_gate_workflows.py --check`, `python3 scripts/check_py_idiom.py`.
- Planted in a clean clone, each refused:
  - `fail-fast: false` in the template, regenerated: `ci_events.py --check` rc 1, the strategy item.
  - The key removed, regenerated: rc 1, the strategy item.
  - `false` in the generated file alone: `ci_gate_workflows.py --check` rc 1 and `ci_events.py --check` rc 1.
  - R924-2's `probe_cancellation.py`, unchanged, now fails at its assertion that `false` is production. Its inverse passes.
- R923-2's `follow_ring_make_probe.sh`, with `b0f2bc1a` in its head list, against `13e6d869`:
  - make 4.4.1 `--jobserver-style=pipe`: base 0 and head 0 jobserver warnings.
  - make 4.3, whose only jobserver is the pipe: base 0 and head 0.
  - `make -n run`: IDENTICAL under both (sha256 `f5c44c63…`).
  - At `9c625393` the same probe gives head 1 warning and DIFFERS, under both versions.
- `make -n exec-pullin-small` builds nothing. `make -s ci-list` gives `b8 pullin-small bind-settle`.
- Both follow_ring CI pieces (`ci_make_cases.py --suite follow_ring --shard L/2 --jobs 2`) pass at `b0f2bc1a` and at `9c625393`. Their case receipts are equal to each other and to hosted run 45528738040's.
- Hosted at the head: rtl-full 45550366428, rtl-fast 45550366444, elaborate 45550366332 and docs 45550366343, all success on attempt 1.
  - All four ran on `e608f8d8` (merge `c5327b25`), the base of the previous head's runs.
  - Against rtl-full 45528738040: all 8 case suites' receipts and all 65 suites' verdict lines are identical, `milan_dp`'s `gptp`/`gptp-lat` included.
  - Touched jobs' minutes:
    - `firmware-boundary-capture` legs 15.3 and 11.0, `firmware-boundary` 5.0 (`PASS`, 4032 of 4325, 0 findings, 112/192/4 controls), aggregate 0.3.
    - Preflight 1.9. Verilator workers at most 25.0 (shard 2/26, with a 405 s Verilator rebuild on a cache miss), 397.6 job-minutes in all. Leg A 14.1.
    - Unions and `verilator-suites` at most 0.5.
Acceptance criteria:
- #998 acceptance 1 (byte-identical against the base): met, and now shown hosted at one base.
- #998 acceptance 2 (as ruled for this PR): every touched job is within 30 minutes, and leg A is stated (#737).
  - "No job slower" held at `9c625393`. At `b0f2bc1a`, three things are slower, none caused by the change:
    - the untouched `firmware-srp-mutants` (1.33 × its slowest window);
    - Verilator shard 9's unchanged suites (1.52 × the previous head's window);
    - seven workers' one-time Verilator rebuild after the workflow change.
  - `publication-census` 36.7, `firmware-srp-mutants` 30.5 and `firmware-control-mutants` 30.1 minutes are untouched jobs, tracked in #1008.
Open risks/questions:
- No hosted failure of a capture leg was injected. Fork cancellation rests on GitHub's matrix `fail-fast`, the exact contract check and the unchanged watcher guard; the PR body explains the mechanism.
- R923-2-S1 to S4 and the retained optional suggestions are not adopted.
- Not run: the act replay and the full serial sweep.
- `ci/image/tool-inventory.json` and `exec-audit-receipt.json` still name `firmware-boundary`'s old step indices (the image work's).
