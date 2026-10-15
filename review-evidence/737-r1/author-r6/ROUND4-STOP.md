[A614] STOP
Head: 6ab22bca61a76c989ad9fbb94b9cde2639d38ca9 (branch `737-ci-30min`, from `84ee9ea1`; not pushed)

Round 4 ([6180908502](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6180908502)) is done except the S3 worker. Each item was committed after its gates passed.

- **1. R636-3-F1** `cadd00137`. A production collector control: `runs/1` recovers on its third read, after 480 s, and the jobs page never recovers. Collection stops at 480 s, within `RETRY_BUDGET_SECONDS` (600). The same reads through `API` without a shared deadline take 960 s. Mutation `i3-no-shared-budget` makes `ci_runtime_evidence_selftest.py` return 1 (`collector reads took 960.0s`).
- **S1** `6c36e98f0`. A planted `if:` and a planted `continue-on-error` preparation in each of the 13 reader jobs; all 26 are refused. Mutation `i1-conditional-prep-accepted` makes the self-test return 1.
- **S2** `81a55f1f4`. One classifier (`ci_fail_fast.transient`) serves the retry loop, the watcher and the collector:
  - observer-only: 403, 429, 5xx, timeouts, and transport errors that outlast the retries;
  - genuine: 400, 401 and 404 make one request, write no observer output and fail with rc 1, so the cancel step and the tail still act.
  - Controls cover each side in both the watcher and the collector. Six mutations across the two sides each make their self-test fail.
- **S4** `80bdcd690`. `--parallel "$CI_TOOL_BUILD_JOBS"`. The contract line is replaced by the bounded one (equal or stronger), and the unbounded form gives 2 `ci_events --check` findings. The generated step ran once in the shipping image: rc 0, 17.4 s, `CI_TOOL_BUILD_JOBS=8`, peak 0.84 GB, zero memory events.
- **R1** `4f7c281e7`: the exact text. **R2**: the PR body sentence is replaced.
- **S3 projection** `6ab22bca6`. From hosted run 38495894212, by the docs worker-zero method:
  - `elaborate-gates-0` = 2144 − 593 − 3 + 60 = 1608 s;
  - `elaborate-gates-1` = 763 s;
  - workflow = 1608 + 270 = 1878 s (31.3 min), over 30 min.

**STOP: the S3 worker needs a test-driver change.**
- **No step can move.** Worker zero's gate is one command, `python3 sw/builder/test_builder.py --require-elaboration --require-rv32` (hosted 1441 s). A further worker needs the driver's `__main__` to run a selected subset of its 103 gate functions.
- **The rulings require a decision.** Round 1 says to STOP "if a test cannot be sharded without changing it". Ruling 6160937413 allowed driver refactoring for `milan_dp` and `milan_dp_mclk` only.
- **Verdict semantics would change.** `SKIPPED`, the NOT RUN ledger and `--require-elaboration` are evaluated per process. A leg with no elaboration row passes `--require-elaboration` vacuously.
- **Measurement.** The unchanged command ran in the shipping image (16 CPUs, 8 GiB) at `4f7c281e`, whose source differs from the head only in `CI_WORKFLOWS.md`:
  - rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (the same two recorded arms), peak 3.72 GB;
  - 1292.7 s over 103 gates;
  - `test_baremetal_profile_contract` alone takes 945.2 s, and the other 102 take 347.1 s.
- **What a split would give.** Scaled to the hosted window, a two-leg split at that boundary puts worker zero at about 1221 s and the workflow at about 1491 s (24.9 min). A function-level split is enough.

**Decision requested.** May this lane refactor `test_builder.py`'s `__main__` to expose its ordered gate list as an inventory and run a selected subset? The conditions would be those of 6160937413:
- an inventory taken from the driver;
- a union proof;
- per-gate verdicts and the NOT RUN ledger equal to the unsharded run;
- planted controls caught in the owning leg;
- nothing else changes;
- plus a union check that the elaboration arms ran in some leg.

The alternative is to keep one elaboration worker and let hosted readback decide the 31.3-minute projection; that is an owner-level choice.

**Validation at `6ab22bca`.** Fresh clones, the shipping image, one 8 GiB container without network:
- Docs-check: every step except the untouched builder gate, 39 steps, all rc 0, including the CI-event contract (5,209 arms, 226.6 s).
- docs-check-no-git: rc 0.
- Runner contract gate: rc 0 in 103.1 s with a read-only candidate. `act_ci.py` SHA-256 is unchanged (`f968f676…`).
- Mutations: 9/9 killed; 4/4 pristine copies return 0.
- rtl-fast: no step is touched.

No test assertion, case, arm, timeout, firmware behaviour or linked image changed. HANDOFF.md and PR-BODY.md carry the Round 4 sections.
