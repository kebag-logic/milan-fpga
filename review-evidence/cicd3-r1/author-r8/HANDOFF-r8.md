# [A839] CICD improvement — round 8 handoff

Status (2026-11-25 07:05 CET): DONE, review ready at `b0f2bc1a`. ETA: none; nothing of mine is running (all
`milan-cicd-a839j-*` units finished). Pushed once; nothing posted.

**Head**

- milan-fpga `cicd-3` = `b0f2bc1a784d9f006204491c883ac2b1783e970a`. Remote and lane are equal; the lane is clean.
- Three commits on `9c625393`. Each has a one-line subject and no trailer:
  - `468c7e47` R924-2-F1: the capture matrix keeps `fail-fast: true`. The template, the generated workflow, the
    contract constant and its arms changed together.
  - `222362ff` R923-2-F1: follow_ring's two fine-build lines start with `+`.
  - `b0f2bc1a` residues: R924-2-R1, R924-2-R2 and R923-2-R1, as written. CI_WORKFLOWS.md's twin of the R2 sentence is
    corrected too, and disclosed.

**Evidence**

- 37 of 37 local gates rc 0 in a clean clone at the head, including:
  - the event self-test (5968 arms; the planted `false` and the removed key are caught);
  - the piece planner self-test (65 parents, 94 units).
- A planted `fail-fast: false` is refused in all three forms by `ci_events.py --check` and/or
  `ci_gate_workflows.py --check`.
- R923-2's make probe at the head: `make -n run` IDENTICAL and 0 jobserver warnings, under make 4.4.1 (pipe) and
  under make 4.3. Both versions reproduce the warning at `9c625393`.
- follow_ring's two CI pieces pass at the head. Their case receipts are equal to `9c625393`'s and to the previous
  hosted run's.
- **Hosted at the head:** rtl-full 45550366428, rtl-fast 45550366444, elaborate 45550366332, docs 45550366343, all
  success on attempt 1, so no re-run was needed.
  - **Same base as the previous head's runs (`e608f8d8`).** This is the hosted same-base comparison round 7 asked
    about: all 8 case suites' receipts and all 65 verdict sets are identical, `milan_dp`'s gPTP cases included.
  - Touched jobs: capture legs 15.3 and 11.0, judge 5.0 (`PASS`, same counts), preflight 1.9, workers at most 25.0.

**For the manager**

- At this head, three things ran slower than their earlier windows. The PR body states each, and none is from the
  change:
  - the untouched `firmware-srp-mutants`, 30.5 minutes, 1.33 × its slowest;
  - shard 9's unchanged suites, 1.52 ×;
  - seven workers' one-time Verilator rebuild after the workflow change.
- `publication-census` 36.7, `firmware-srp-mutants` 30.5 and `firmware-control-mutants` 30.1 are over 30 minutes.
  They are untouched jobs, tracked in #1008.
- The fork cancellation is explained in the PR body's new section. No hosted failure was injected.

**Said plainly**

- Two removals were logged late, and both are marked LATE in `disk-cleanup.log`:
  - a stray copy of a review comment that my own first command wrote one directory too high;
  - my own two-line note file.
- I stopped and restarted the piece unit once, to run it at the final head.
- `/data-2` is at 95 %. Scratch `r8` is 1.1 GB.
- Not run: the act replay, the full serial sweep, and a real serial `follow_ring` run.

**Written:**

- `REPORT.md`
- `PR-BODY-1003.md`: a full replacement, not posted.
- `REVIEW-READY.md`: not posted.
- `receipts/INDEX.md`

REVIEW READY b0f2bc1a784d9f006204491c883ac2b1783e970a
