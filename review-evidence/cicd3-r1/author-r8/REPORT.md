# [A839] CICD improvement, round 8: round 2's findings on #1003

**Summary.** Three commits on `9c625393` answer both round-2 reviews. The new head is
`b0f2bc1a784d9f006204491c883ac2b1783e970a`, pushed once.

- 37 of 37 local gates pass in a clean clone.
- All four hosted runs at the head succeeded on their first attempt.
- The hosted runs merged into the same base as the previous head's (`e608f8d8`). So for the first time there is a
  hosted comparison at one base, and it is identical: 8 of 8 case suites and 65 of 65 verdict sets.

| # | Item | Commit | Result |
|---:|---|---|---|
| 1 | R924-2-F1: the capture matrix disabled native cancellation | `468c7e47` | `fail-fast: true` in the template, the generated workflow, `FIRMWARE_BOUNDARY_STRATEGY` and its arms. Planted `false` and a removed key are refused |
| 2 | R923-2-F1: follow_ring's fine build was not a recursive make line | `222362ff` | `+` on both lines. `make -n run` is byte-identical to the base's, with 0 jobserver warnings under make 4.4.1 (pipe) and make 4.3 |
| 3 | R924-2-R1, R924-2-R2, R923-2-R1 | `b0f2bc1a` | Applied as written, plus the twin of R2's sentence in CI_WORKFLOWS.md |
| 4 | Gates, self-tests, hosted | — | 37/37. Event self-test 5968 arms. Piece planner 65 parents and 94 units. Hosted 4/4 green, all touched jobs ≤ 25.0 min |

## 1. R924-2-F1: native fail-fast on `firmware-boundary-capture`

**What changed.**

- `.github/ci-templates/rtl-fast.yml`: `fail-fast: true`, with a comment on why. It cites Issue #998, REQ-VER-01
  and REQ-VER-04.
- The generated `.github/workflows/rtl-fast.yml` changes in that one line (`ci_gate_workflows.py`).
- `scripts/ci_events.py`:
  - `FIRMWARE_BOUNDARY_STRATEGY = {"fail-fast": True, …}`.
  - `check_boundary_legs`'s docstring now states the policy.
  - The arm "boundary legs fail-fast", which planted `true` and expected it refused, is now "boundary legs
    cancellation disabled": it plants `false`.
  - A new arm, "boundary legs fail-fast left to the default", removes the key. The contract holds the value
    spelled out, as `rtl.yml`'s two matrices spell it.
  - Arms: 5967 → 5968.
- `docs/testing/CI_WORKFLOWS.md`, the capture legs' paragraph: the matrix keeps `fail-fast: true`, and a failed
  leg cancels the other on every event, a fork's included, with no token. `ci_events.py` pins it.
- Unchanged: the watcher's fork guard (its `if`), the aggregate's list and its `success|skipped` rule, and the
  judge's `needs`.

**Evidence** (`receipts/probe/`).

- `plant.txt`, in a clean clone at the head:
  - (A) `false` in the template, regenerated: `ci_events.py --check` rc 1 with the strategy item.
  - (B) `false` in the generated file alone: `ci_gate_workflows.py --check` rc 1 ("regenerate the gate jobs") and
    `ci_events.py --check` rc 1. Its one finding is the generated jobs' inventory item; the strategy item fires
    when the template carries the change.
  - (C) the key removed, regenerated: rc 1 with the strategy item.
  - The clone was restored, with 0 changed paths.
- `r924-probe-at-b0f2bc1a78.txt`: R924-2's `probe_cancellation.py`, unchanged. It now fails, rc 1, at its
  counterfactual assertion: `true` no longer produces a finding.
- `r8-probe-at-b0f2bc1a78.txt`: my inverse probe (`tools/probe_cancellation_r8.py`). The production matrix is
  `true` and passes the production checker. `false`, and the key removed, are each refused. The watcher's `if`
  still names the same-repository condition, and the judge needs the capture job. The capture job carries no
  `permissions` key.
- The gates' `ci_events_selftest.log`, lines 2866-2872: all seven boundary-leg arms are caught.

**How a failed leg cancels its sibling on a fork** (stated in the PR body's own section).

- `strategy.fail-fast` is applied by the Actions service. On a failed matrix job, it cancels that matrix's
  queued and running jobs. No step and no token is involved, so a fork's read-only token is irrelevant.
- The write-token watcher stays same-repository only.
- The matrix result is `failure`, so `firmware-boundary` is skipped and the `rtl-fast` aggregate fails.
- **Not shown:** a hosted injected failure. That would need a failing commit pushed from a fork, which this round
  did not do.

## 2. R923-2-F1: follow_ring's recursive recipe lines

**What changed.** In `tb/verilator/follow_ring/Makefile`, `small-pullin` now runs
`+$(if $(LEG_BUILD),$(FINE_BUILD))` and `build-pullin-small` runs `+$(FINE_BUILD)`. The leg-build comment says
why the `+` is there. GNU make marks a line recursive only by a leading `+`, or by `$(MAKE)` in the line itself.

**Evidence** (`receipts/probe/`).

- I used R923-2's `follow_ring_make_probe.sh`.
  - The reviewer's copy is `tools/follow_ring_make_probe.reviewer-original.sh`, with sha256 `7f72a73f…`, equal
    to its packet manifest.
  - My copy reads the head list from `PROBE_REVS` and is otherwise byte-identical. Its diff is one line.
  - The make 4.3 variant drops `--jobserver-style=pipe`, which 4.3 lacks: its only jobserver is the pipe one.

| Tree | make 4.4.1, pipe: head warnings | make 4.3: head warnings | `make -n run` |
|---|---:|---:|---|
| `9c625393` (before) | 1 | 1 | DIFFERS (both versions) |
| `222362ff` (the fix) | 0 | 0 | IDENTICAL (both) |
| `b0f2bc1a` (the head) | 0 | 0 | IDENTICAL (both), sha256 `f5c44c63…` for both trees |

- The base gives 0 warnings in every row.
- The make 4.3 rows execute what the review could only infer: 4.3 warns at the old head and not at the fix.
- The full `small-pullin` transcripts (base against head) differ only in the stub run's traceback line numbers
  and the Makefile's line numbers. The probe sets `VERILATOR=true`, so `small_pulls.py` fails on purpose there.
- `make -n exec-pullin-small` builds nothing: `LEG_BUILD=` empty, so the `+` line expands to nothing.
  `make -n build-pullin-small` builds both models. `make -s ci-list` lists `b8`, `pullin-small` and
  `bind-settle`.
- **Both CI pieces, locally** (`receipts/local/`). The unit `milan-cicd-a839j-frpiece` ran on CPUs 48-55, booked
  through `cpu_ranges.py pick`, with the shared ccache, in a clean clone each.
  - It ran `ci_make_cases.py --suite follow_ring --shard L/2 --jobs 2`, the piece command.
  - At `b0f2bc1a`: 350.7 s and 464.9 s, both rc 0.
  - At `9c625393`: 351.4 s and 472.1 s, both rc 0.
  - The three case receipts (`b8`, `bind-settle`, `pullin-small`) are equal in both trees and equal to hosted run
    45528738040's (`follow_ring-receipts.txt`).
  - Piece 1's log shows two Verilator builds, both before execution. The exec phase built nothing.
- The serial `run` was not executed for real: the `-n` and jobserver probes are the requested evidence.

## 3. Residues

- **R924-2-R1.** `Issue #998; REQ-VER-01 and REQ-VER-04.` is added to each listed block:
  - `follow_ring/Makefile`'s leg-build block;
  - `small_pulls.py`'s and `settle_control.py`'s print-order comments. The trailing `, #998` in their parentheses
    is dropped, since the sentence now carries it;
  - the template's capture-job block;
  - `ctrl_boundary.py`'s THE CAPTURE paragraph;
  - `ctrl_configs.py`'s known-set block;
  - `ctrl_runs.py`'s THE LEGS paragraph;
  - `ci_events.py`'s six blocks: `GATE_LEGS`, `FIRMWARE_BOUNDARY_CAPTURE_JOB`, `FIRMWARE_BOUNDARY_SETUP`, the
    capture job's inventory comment, `check_boundary_legs` and `_boundary_leg_arms`.
- **R924-2-R2.** In `sw/firmware/ctrl/README.md`, the sentence is the reviewer's, word for word, without code
  formatting. The leg and argument explanation follows as its own sentence.
- **Beyond the residue list.** CI_WORKFLOWS.md had the same overbroad phrase: "`firmware-boundary` needs both
  legs and runs no builder itself". It now reads "runs none of their builders itself". This is disclosed in the
  PR body.
- **R923-2-R1.** CI_WORKFLOWS.md now reads "is in PR #1003's description (its derivation table)", as written.
- **R923-2-S1 to S4**, and the suggestions retained from round 1: not adopted. They are optional, and no defect is
  claimed.

## 4. Gates and hosted

**Local gates** (`receipts/gates/summary`, one log each). The unit `milan-cicd-a839j-gates` ran in the session pool
on CPUs 80-95, because `cpu_ranges.py show` had no free range left after the piece booking. It used a clean clone
at `b0f2bc1a`.

- 37 of 37 commands rc 0.
- Counts that moved: `ci_events --selftest` 5968 arms (5967 before); `check_em_dash` 208 added lines.
- `check_doc_paths` reports "2 allowlisted" in the clean clone. The lane checkout reports 1, at the old head too.
  That is the lane's working tree, not the change.

**Hosted** (`receipts/hosted/`). The push was at 05:58 CET.

| Run | Workflow | Result |
|---|---|---|
| 45550366428 | rtl-full | success, attempt 1, 47 jobs (the nightly physical job skipped) |
| 45550366444 | rtl-fast | success, attempt 1, 19 jobs |
| 45550366332 | elaborate | success, attempt 1 |
| 45550366343 | docs | success, attempt 1 |

- **Same base.** Merge `c5327b25` has parents `e608f8d8` and `b0f2bc1a` (`merge-c5327b25.txt`). The previous
  head's run tested `241f036e` = `9c625393` into `e608f8d8`. I checked this first, as the memory note from round 7
  says to.
- **Comparison** (`compare-45528738040-vs-45550366428.txt`, round 5's `hosted_compare5.py`): case tables 8/8
  identical, `milan_dp` 26 cases included; verdict sets 65/65 identical; problems 0.
- **Minutes** (`minutes-b0f2bc1a.tsv`). Factors are against 64 earlier runs (round 6's 60 plus the previous
  head's 4).

Touched jobs:

- `firmware-boundary-capture (0)` 15.3 and `(1)` 11.0 minutes.
- `firmware-boundary` 5.0, with the same verdict line as at `9c625393` (`judge-45550366444-verdict.txt`).
- Aggregate 0.3. Preflight 1.9 (117 s against its slowest 116).
- Workers at most 25.0 (shard 2/26), 397.6 job-minutes in all. Leg A 14.1. Unions and the two required
  aggregates at most 0.5.
- `workers-vs-projection.txt`: job over projection is 0.42-1.21. The deal is unchanged, so the projections are
  round 5's.

Slower, and why:

- **Seven workers built Verilator on a cache miss**, 278-405 s each (`verilator-cache-miss.txt`). The key hashes
  `.github/workflows/*.yml`, and this push changed `rtl-fast.yml`. rtl-full's "Prepare pinned Yosys" built Yosys:
  1024 s, within its slowest earlier window.
- **Shard 9/26.** Its suites (`aes3`, `media_nco`, `milan_dp_gm_steps`, `pair_fill`, `ptp_ts`) are unchanged
  since `9c625393`. Its suite step took 1436 s against 947 s there. That is runner speed.

Untouched, over 30 minutes (#1008):

- `publication-census` 36.7.
- `firmware-srp-mutants` 30.5: 1.33 × its slowest. Its campaign step took 1789 s here and 1233 s at `9c625393`,
  whose inputs differ only in comments.
- `firmware-control-mutants` 30.1.

The PR body states that "no job got slower" does not hold at this head, and why.

## Said plainly

- **Removal logging went wrong twice; both entries are marked LATE.** Removals are logged in
  `2026-09-23/disk-cleanup.log`.
  - My first command wrote a review comment to a stray path, `/data-2/milan/tmp/cicd-a839/r8-R924.md`, and the
    same command removed it before any log entry.
  - I also removed my own two-line note, `r8/rm-log.txt`, in the same command as its log line.
  - Every other removal was logged before it ran. These were the probe's re-extractions and the `make clean`
    runs in my fresh clones, including the restart after I re-targeted the piece clone.
- **I stopped the first piece unit** about five minutes in, at `222362ff`, and re-ran both trees at the final head,
  because commit 3 touched follow_ring files. Its partial logs were overwritten.
- **No trailer was added to commits.** The user's rule ("no trailers") overrides the attribution reminder. The
  first commit was amended within seconds, before any push, to drop one.
- Scratch `r8` is 1.1 GB. `/data-2` is at 95 %.
- **Not run:** the act replay, the full serial sweep, a real serial `follow_ring` run, and a hosted injected leg
  failure. The `ctrl_boundary.py` legs and judge ran hosted at the head and passed. They were not re-run locally,
  since the delta touches only their comments.
- Nothing was posted.
