[A614] REVIEW READY

Commit: `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe`
Branch: `737-ci-30min`, from round-six head `47fd0d3c`. The worktree is clean. Not pushed: origin holds `47fd0d3c`.

Round 7 ([6190383901](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6190383901)) is complete. Delta for review: `47fd0d3c..fe2e2a54`, two commits.

**1. Runner self-test on small hosts (R636-6-F1)** (`2db6c0f9d`).
- `selftest_main_entry_probe` (`scripts/act_ci.py:12168-12178`) now adds `mock.patch.object(os, "cpu_count", return_value=512)` to its existing patch context, as the other main-path probes do (`:13675`, `:14675`). The diff is six lines in that one self-test function: two comment lines and the one context. No production code path changed.
- Runner SHA-256 for the repin: `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c` -> `7ff18c6a89aeb40c54d44411ffc6ff766fe6aa0f29baf595ba1e2aa833a446fd`. The evidence-helper pin block is unchanged.
- New committed control, `scripts/act_ci_small_host_selftest.py`, run as `python3 -I scripts/act_ci_small_host_selftest.py`:
  - It installs the runner read-only and runs its self-test in an isolated child whose `os.cpu_count()` reports 4 (`--cpus` takes 1 to 63).
  - It then runs the same self-test on a copy whose `main` returns `execute_pr_run()` without the cleanup-signal wrapper.
  - The clean run must pass. The planted run must fail the main-entry probe, and must do so without the CPU refusal on stderr, so it has to reach the lookup.
  - The isolated child skips only the flat-install launcher, a fresh interpreter the forced count cannot reach. Every other arm runs under the forced count.
- Results, in an image like the hosted runner (CPython 3.12.3 with PyYAML, no network or Docker socket, read-only source, fresh clone at the head):
  - Control at 4 CPUs: rc 0, 69 s. The clean run passes. The planted copy fails the main-entry probe alone, with detail `recorded=(...) runner_status=-15 group_absent=False`: the lookup was reached, the runner died on the signal and the stub's process group survived.
  - Control at 1 CPU: rc 0, same outcomes.
  - Control against the `47fd0d3c` runner: rc 1. It reproduces the hosted failure, "CPU range 0-15 exceeds this host's 4 CPUs". Its planted run fails only by that refusal, and the control rejects that.
  - The docs `Local act runner contract gate` step, both invocations as written: rc 0, 102.6 s.
- `docs/testing/CI_WORKFLOWS.md:1748-1767` documents the control. It is a local command and not a CI step, because the hosted gate already runs on four CPUs.

**2. R1, R2, S1, S2** (`fe2e2a543`).
- R1 and R2: the PR body in the handoff carries the exact texts. The round-6 status now ends "The coordinating role published this head."
- S1: `ci_gate_workflows_selftest.py:444-451` requires that the workers owning a builder leg are exactly `BUILDER_WORKERS`, and that exactly those workers upload `builder-leg-*.json`.
- S2: `ci_gate_workflows_selftest.py:93-114` plants two templates each for docs and elaborate. One runs the driver in a preparation line. In the other, the last line is not the driver. Each plant breaks one condition alone, and the generator must refuse each.
- Mutation battery, each mutation regenerated so the generator's `--check` passes under it:
  - Receipts kept for elaboration only (R636-6's probe): rc 0 at `47fd0d3c`, rc 1 at the head.
  - Receipts kept on every worker: rc 1 at the head.
  - Preparation-line refusal removed (R636-6's probe): rc 0 at `47fd0d3c`, rc 1 at the head.
  - Last-line refusal removed: rc 1 at the head.
  - The pristine self-test passes before and after the battery.

**Verification at this head.**
- The docs `CI scheduling and evidence controls` step (14 commands) passes in a fresh clone, rc 0.
- `ci_events.py --check` and `--selftest` pass, rc 0: 2,187 items, 5,215 arms.
- 17 host gates pass on the clean head, rc 0. They include docs-check, the em-dash check against `47fd0d3c`, the generator check, the gate self-test, evidence pins, the runtime evidence self-test, the bare-metal check and self-test, Python idiom, hygiene and `git diff --check`.
- No workflow template or generated workflow changed. The round-6 banks and projections stand.

Acceptance criteria: round-7 items 1 and 2 are met, with the evidence above.

Open risks/questions:
- The exact check for F1 is the hosted docs run at this head after the repin. It belongs to the coordinating role.
- The non-isolated first invocation's flat child cannot be forced below the host count. The control covers its arm set through the isolated run, and the hosted runner covers the launcher itself.
- This is an author handoff, not a review verdict.
