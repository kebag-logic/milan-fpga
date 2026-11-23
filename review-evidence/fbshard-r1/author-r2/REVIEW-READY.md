[A827] REVIEW READY
Commit: 5392adf989349b68cfbb54d91fd0413c5b745521 (local `pf-fbshard-1`, not yet pushed; remote PR #982 head is still b7b351935f65416c8632c21dd13e08fb2e9c1d9c)
Delta from b7b351935: 2 commits, 7 files, +144/-14

```
20934e179 Escape the watcher's raw skipped-matrix names so a job with no matrix receives them unevaluated, and watch them as the runner delivers them (#980)
5392adf98 Document the escaped skipped-matrix names and the boundary paths' partition of the builders (#980)
```

## Changed

- **Generator** (`scripts/ci_runtime_workflows.py`). The new `literal_json()` writes the watcher's `EXPECTED_JOBS` and `SKIPPED_MATRICES`. It replaces each `${{` with JSON's own escape, `\u0024{{`. The runner then finds no expression to evaluate. `json.loads` decodes the value to the exact raw name, so the consumer is unchanged. The function refuses if any `${{` survives or if the value does not decode back to itself. `generate()` now refuses a workflow where an unexpanded matrix name equals any expanded job name.
- **Consumer** (`scripts/ci_fail_fast.py`). `observe()` refuses the same collision: a skipped-matrix name that is also an expected job name.
- **Regenerated workflows.** `rtl-fast.yml` changes in the `firmware-boundary shard` key. `rtl.yml` changes in the `Verilator shard` and `Yosys shard` keys. Only the `SKIPPED_MATRICES` line changes in each file. `docs.yml` and `elaborate.yml` are byte-identical, because their maps are `{}`.
- **Self-test** (`scripts/ci_fail_fast_selftest.py`).
  - `evaluate_without_matrix()` evaluates an env value the way the runner does in a job with no matrix: each `matrix.<prop>` becomes an empty string. Any other expression is refused.
  - `watcher_runtime_control()` reads each committed `.github/workflows/*.yml`. It first asserts the watcher has no `strategy`. It then evaluates the watcher step's two env values and parses them, and only after that calls the real `watch()` over two reads:
    - **Read 1.** Each raw matrix is completed/skipped with no steps, one ordinary job is `in_progress`, and the rest succeeded. `watch()` must keep waiting.
    - **Read 2.** That job is `failure`. The control requires rc 1, exactly 2 reads, 1 sleep, no `observer_error`, and `first_failure` naming that job.
  - The control then requires:
    - the delivered map equals the raw `skipped_matrices()` of the workflow;
    - no raw name is an expected name;
    - completion over the raw matrices is accepted, and read 1 alone is not complete;
    - cancellation reaches every same-head sibling (`cancellation_control()`).
  - **Plant.** `watcher_runtime_controls()` reruns the control with the round-1 form, the unescaped `json.dumps`. For `rtl` and `rtl-fast` it requires the failure `watcher stopped observing`. For `docs` and `elaborate` it asserts that no plant applies.
  - A further control checks that `observe()` refuses a raw name equal to an expanded one.
- **Docs.** `docs/testing/CI_WORKFLOWS.md` (skipped-matrix paragraph): the evaluation hazard, the escape, the identity refusal and the control. `sw/firmware/ctrl/README.md:171`: R2's sentence, verbatim.

## Finding closure

| Finding | Closure | Evidence |
|---|---|---|
| R897-1-F1 MINOR (Conformance, Robustness, Tests, Docs). The skipped-matrix key was evaluated in the non-matrix watcher. | **Fixed in the generator; workflows regenerated.** The watcher now receives `firmware-boundary shard ${{ matrix.shard }}/${{ matrix.total }}` unevaluated. Expanded and unexpanded identities are refused if equal, in both the generator and the consumer. A raw skipped matrix is accepted, unfinished work is still watched, and a later failure still returns rc 1 with no `observer_error`, which leaves the cancel step's condition true. | `receipts/head-ci_fail_fast_selftest.log`; `receipts/skipped-matrix-receipts.log` (1) and (3); `receipts/reviewer-probe-at-head.log`: the reviewer's unmodified probe now finds the runtime key equal to the raw name, and its `probe no longer reproduces` assertion fires |
| F1: plant the round-1 form | **Caught.** First as the in-memory unescaped form inside the self-test, on every run. Second as the actual `b7b35193` committed `rtl.yml` and `rtl-fast.yml`, both CAUGHT with `observer_error after 1 read(s), rc=0`. | `receipts/head-ci_fail_fast_selftest.log`; `receipts/skipped-matrix-receipts.log` (1) |
| F1: check every other workflow's `SKIPPED_MATRICES` | **One more found, and fixed by the same generator change:** `rtl.yml`, keys `Verilator shard ${{ matrix.shard }}/${{ matrix.total }}` and `Yosys shard ${{ matrix.shard }}/${{ matrix.total }}`. This defect predates #980. The raw names are the ones hosted run 38273578232 reported, so `rtl`'s watcher would have stopped on any run that skipped those matrices unexpanded. `docs` and `elaborate` are `{}`. Across every job with no matrix in all four workflows, the only `${{ matrix.` occurrences at `b7b35193` were these `SKIPPED_MATRICES` keys. At the head there are none. | `receipts/skipped-matrix-receipts.log` (2) |
| R897-1-R2 RESIDUE (Docs). `sw/firmware/ctrl/README.md:171` | **Fixed as written:** "The boundary and Verilator paths partition the builders. Each recorded compile is judged whole; the boundary aggregate judges the shard captures." `CI_WORKFLOWS.md:145` has the phrase "in the job that ran it" too, but it sits under `firmware-verilator`, which builds and judges in one job, so it is still true and was left alone. | the diff; docs gates |
| R897-1-R3 RESIDUE (Docs). The PR body has no role prefix. | **Fixed in `PR-BODY.md`**, for the manager to apply. Its first line is `[A827] Shard the firmware-boundary CI job`, then a blank line and `Closes #980`. The review text says `[A10]`, but this lane's executor is `[A827]` (its TAKEN and REVIEW READY), so `[A10]` would misattribute the body. Only the prefix differs. | `PR-BODY.md` line 1 |

## Validation (all at 5392adf9)

- 28 CI and docs gates, round 1's list, all rc 0 (`receipts/head-ci-and-docs-gates.log`).
- `ci_events.py --check`: OK, 2369 contract items.
- `ci_events.py --selftest`: PASS, 2369 items, 5881 arms.
- `check_wire_accountability.py --self-test`: PASS.
- `ci_gate_workflows.py --check`: rc 0, so the committed workflows equal the generator output.
- **Act replica: not run.** It refuses a candidate that is not the exact remote PR head. The head is local and this round may not push. It is owed after the push.

## Acceptance criteria

- Unchanged from round 1 except F1's skipped-matrix support, which now holds for the new matrix and for `rtl`'s two older ones.
- **Hosted per-shard timing is still open.** It needs a hosted `rtl-fast` run on the pushed head.

## Open risks/questions

- **The evaluation is modelled, not hosted.** The control models the documented rule that an absent matrix property evaluates to an empty string. A hosted docs-only run on the pushed head, where the shard matrix skips unexpanded, would confirm it. The thing to check is that `ci-fail-fast` reports no `observer_error`.
- **Merge candidate.** The base is `dev-soft-core` `854bd723`, while live `dev` is `e275d795`. The merge-candidate composition is unvalidated, as R897-1 noted.
