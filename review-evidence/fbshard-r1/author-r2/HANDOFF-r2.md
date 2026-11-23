# HANDOFF r2: #980 firmware-boundary shards ([A827])

**Status:** REVIEW READY at `5392adf989349b68cfbb54d91fd0413c5b745521`. Two new local commits on `pf-fbshard-1`, on top of round 1's `b7b35193`. Not pushed; the remote branch and PR #982 head are still `b7b35193`.
**Answers:** R897-1, which was NEGATIVE: F1 MINOR and residues R2 and R3. All are closed; see `REVIEW-READY.md`.

**Posted on #980:** [A827] REVIEW READY, https://github.com/kebag-logic/milan-fpga/issues/980#issuecomment-7097237511. I edited it once to restore a literal `\u0024` that a file write had decoded to `$`. The readback is in `receipts/`.

## Commits

```
5392adf98 Document the escaped skipped-matrix names and the boundary paths' partition of the builders (#980)
20934e179 Escape the watcher's raw skipped-matrix names so a job with no matrix receives them unevaluated, and watch them as the runner delivers them (#980)
```

7 files, +144/-14.

## F1 fix in one paragraph

The runner evaluates `${{ }}` inside env values, and the watcher has no matrix, so the raw matrix name reached the watcher as `firmware-boundary shard /`. The generator's new `literal_json()` writes the watcher's two job lists with each `${{` as `\u0024{{`. That is valid JSON, it contains no expression, and `json.loads` decodes it to the exact raw name, so the consumer is unchanged. The generator and `observe()` both refuse an unexpanded name equal to an expanded one. Regenerating also fixed `rtl.yml`'s `Verilator shard` and `Yosys shard` keys, which had the same defect before #980. `docs` and `elaborate` have `{}`. A scan of every job without a matrix in all four workflows found no other `matrix.` use.

## Control and plant

`ci_fail_fast_selftest.py` now has `watcher_runtime_control()`. It reads each committed workflow, asserts the watcher has no `strategy`, and evaluates the watcher env as a job with no matrix. Only then does it run the real `watch()` over two reads:

- **Read 1:** the raw matrices are completed/skipped and one job is running.
- **Read 2:** that job has failed.

It requires rc 1 after 2 reads, no `observer_error`, the failure named, and cancellation of every sibling. The delivered map must equal the raw names.

- **Plant: round-1 form.** For `rtl` and `rtl-fast` it fails with `watcher stopped observing: observer_error after 1 read(s), rc=0`. That holds in-memory and against the `b7b35193` committed files.
- **Reviewer's probe.** Run unmodified, it now finds the runtime key equal to the raw name, so its own assertion fires ("probe no longer reproduces").

## Validation at 5392adf9

- **Gates:** 28 of 28 CI and docs gates rc 0.
- **`ci_events --check`:** OK, 2369 items.
- **`ci_events --selftest`:** PASS, 2369 items, 5881 arms.
- **Act replica: not run.** It refuses a candidate that is not the exact remote PR head, and pushing was out of scope.

Receipts: `receipts/INDEX.md`.

## For the manager

1. **Push and update the PR.** Push `pf-fbshard-1` to `5392adf9`, then replace PR #982's body with `PR-BODY.md`. That closes R3. Its prefix is `[A827]`, not the review's `[A10]`, because `[A827]` is this lane's executor identity.
2. **Run the act replica** at the pushed head, from a trusted clean worktree at the live `dev` tip (`trusted-dev-20261117-e275d795` matches live `dev` `e275d795`).
3. **Hosted evidence.** Record the per-shard times on the hosted `rtl-fast` run. That is still the open acceptance item. If a docs-only run occurs, check that `ci-fail-fast` reports no observer error with the matrix skipped unexpanded.
4. **Re-review.** Request a re-review of `5392adf9`, since R897-1 does not cover it. All five lenses need fresh coverage at this head: the delta touches workflows, the generator, the consumer, a test and docs.
5. **Unchanged gaps.** The `ci/image/*.json` inventories are not regenerated. The merge candidate against live `dev` is unvalidated.

## Note

The Write tool decoded `\u0024` to `$` in every file I wrote this session. The committed doc line was caught and fixed before the final commit. Source files edited with Edit kept the escape, and the generator emits it correctly. All output files and the posted comment were re-checked byte-wise.

REVIEW READY 5392adf989349b68cfbb54d91fd0413c5b745521
