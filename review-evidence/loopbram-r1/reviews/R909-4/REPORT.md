[R909] NEGATIVE - exact head c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99

# R909-4: internal independent narrow re-review of PR #987 (issue #979)

- Head `c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99`, tree `8a668511253c4ef88a2a3cefe37ad202ccc5742a` (verified in the clone).
- Delta reviewed: `9acb9b82..c413d33a`, three commits (`42c0d636`, `243516da`, `c413d33a`). Each commit message is one line with no trailers.
- Files changed: `sw/builder/test_input_loopback.py`, `scripts/suite_shards.py`, `scripts/run_all_suites.sh`, `scripts/measure_test_evidence.py` and `docs/testing/TESTING.md`. That is 28 insertions and 15 deletions.
- `git diff --stat 9acb9b82 HEAD -- hdl tb configs .github .gitmodules syn sw/litex` is empty, so the delta changes no RTL, bench, configuration, workflow or submodule byte.
- Author packet: `review-evidence/loopbram-r1/author-r6` at `9305c8e8`.
- Authorities read: AGENTS.md, CONTRIBUTING.md, `docs/README.md`, the issue #979 body and its option-B ruling, the `scripts/suite_shards.py:15-20` new-suite contract, `docs/testing/TESTING.md`, and `docs/testing/CI_WORKFLOWS.md` for the suite budgets.
- Lenses applied: all five, each against the delta.

**Verdict reason.** One MINOR finding is open under Docs (R909-4-N1). The authoritative CI policy page still says every default suite without a named budget gets 1800 s, which is now false for the two loopback suites.

The three focus items are otherwise confirmed at their causes:
- (1) The hosted `--list` failure is fixed.
- (2) R909-3-N1 is resolved by outcome (a).
- (3) Every hosted job that has completed at this head is green, including the two aggregates that failed at `9acb9b82`. The Verilator, Yosys and firmware shards had not finished when this review closed.

## Focus verification

### (1) Hosted failure: cause and fix (RESOLVED at cause)

- **Cause.** `avdecc/gen_aemi_image.py:78-84` raises `SystemExit(2)` at import when `protocol-processor/hdl/aecp/desc` is absent. `sw/builder/test_builder.py:30592` imports `test_input_loopback` in `__main__` before it answers `--list`. At `9acb9b82` that module imported `gen_aemi_image` at module scope.
- **My reproduction.** I made `git archive` exports with no submodules.
  - At `9acb9b82`, `python3 -I sw/builder/test_builder.py --list` gives rc=2 and the generator's own refusal on stderr (`receipts/list-nosub-9acb9b82.{rc,err}`).
  - At `c413d33a` it gives rc=0 (`receipts/list-nosub-c413d33a.rc`).
- **Inventory unchanged.** The 114-gate inventory is byte-identical across three trees: no submodules at `c413d33a`, submodules at `c413d33a`, and submodules at `9acb9b82`. All three have sha256 `acc4d933d03afea09650fdd05df5400900fc1bf09960225b6980e01ef519c7fc`, the digest the author claims (`receipts/list-*.txt`).
- **Fix shape.** The imports now sit inside `image()` (`test_input_loopback.py:20-22`) and `test_input_loopback_contract()` (`:31-33`). Every use of those modules is inside those two functions (`:24-26, 78-101`). This matches the existing pattern at `test_declarations.py:41` and `:437`. Assertions and fixtures are unchanged.
- **The gate still runs.** With submodules, `test_input_loopback_contract()` passes (`receipts/loopback-contract-withsub.*`).
- **Failure stays loud.** Without submodules, the gate still fails with rc=1 (a `ConfigError` for the missing submodule). So moving the imports opened no silent-pass path (`receipts/loopback-contract-nosub.*`).
- **Comment rule.** The added comment at `:17-19` states behaviour and reason. It carries no lane label, review round, reviewer ID or comment ID.

### (2) R909-3-N1: provisional registration (RESOLVED, outcome (a))

- **What changed.** `scripts/suite_shards.py:111-112` sets both figures to 300. `:151` adds both suites to `PROVISIONAL_SUITES`. `scripts/run_all_suites.sh:259-260` adds 300 s `suite_timeout` arms, and the header at `:38-43` lists them. `scripts/measure_test_evidence.py:672-673` pins the arms in the runner contract.
- **Planner self-test.** `python3 -I scripts/suite_shards.py --selftest` gives rc=0 with `selftest: PASS`. It prints "head provisional figures {'input_loopback': 300, 'input_loopback_dp': 300, 'reboot_ctrl': 300} are what run_all_suites.sh's suite_timeout gives". The largest regular worker is 1615 s against the 1620 s bound (`receipts/shards-selftest.*`).
- **Shard listings.** All 19 `--ci-pieces --shard i/19` listings exit 0 (`receipts/shards-listing.rc`). `input_loopback_dp` appears once, on shard 12. `input_loopback` appears once, on shard 13 (`receipts/shard-*.txt`).
- **Runner contract.** `measure_test_evidence.py --selftest` passes 105 of 105. `--check` reports "runner evidence contract: OK" and the ratchet PASS (`receipts/mte-*`).
- **The checks can fail.** I ran mutation probes on disposable copies (`scripts/timeout_mutations.sh`, `receipts/timeout-mutations.log`):

  | Plant | Planner self-test | Runner contract |
  |---|---|---|
  | None (control copy) | rc 0 | rc 0 |
  | Figure 300 changed to 299 | rc 1, provisional mismatch named | not its job |
  | `input_loopback_dp` figure set to 1800 | rc 1 | not its job |
  | `input_loopback` arm removed | rc 1 | rc 1 |
  | `input_loopback_dp` arm set to 301 | rc 1 | rc 1 |

  Removing both suites from `PROVISIONAL_SUITES` still passes. That is by design: the 300 s values then become ordinary figures. It is not a defect of this delta.
- **The author's material assumption.** The author added new 300 s arms instead of registering the `*` arm's 1800 s. I confirm that reading as reviewer. An 1800 s figure cannot fit under the 1620 s regular bound. The docstring rule is "register the exact run_all_suites.sh timeout", and the self-test enforces it. `reboot_ctrl` (`a0e555a7`) is the precedent.
- **Margin.** A slow hosted run of either suite would end in a classified TIMEOUT (exit 92), not a pass. My own cold runs leave 8.5x and 3.03x headroom (see S1).
- **Still owed.** The measured hosted windows must replace both provisional figures. Per the brief, that is a later round's work.

### (3) Hosted CI at `c413d33a`

The final snapshot was taken at 2026-11-24T19:14:55Z (`receipts/hosted-c413d33a.txt`, `receipts/hosted-aggregates-c413d33a.txt`).

- **Previously failing aggregates.** `docs-check` (job 138705737874, run 45459575153) and `elaborate` (job 138701767114, run 45459575049) both concluded `success` at head `c413d33a`. In each, step 8 "Require every gate exactly once" succeeded. These two jobs failed at `9acb9b82`.
- **Other jobs.** 16 succeeded:
  - `docs-gates-0/1/2` and `elaborate-gates-0..4`;
  - `docs-check` and `docs-check-no-git`;
  - `wire-accountability`, `bdd-conformance`, `changes` and `full-ci-gate`;
  - `elaborate` and "Prepare pinned Yosys".
- **Skipped.** "Physical gPTP (nightly and manual)" is a scheduled-only context, unrelated to this PR.
- **Not finished.** 39 jobs were queued or in progress:
  - the 19 Verilator shards, including shards 12 and 13, which own the new suites;
  - the 4 Yosys shards;
  - the firmware jobs, `verilator-lint`, `split-cdc` and `publication-census`;
  - the fail-fast watchers.
- No job had failed. I make no claim for the unfinished jobs; hosted and act acceptance stay with the manager.

## Findings

### R909-4-N1 - MINOR - Docs - `docs/testing/CI_WORKFLOWS.md:577-590` - the suite-budget table contradicts the new 300 s arms

- **Authority.**
  - AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs."
  - AGENTS.md section 5 names `docs/testing/CI_WORKFLOWS.md` as the CI workflow policy.
  - Its table at `:577-583` reads: "Each suite runs under a per-suite wall clock from the table in `scripts/run_all_suites.sh`. The measured hosted worst case plus a stated margin sets each named entry", with the row "every other default suite | 1800 s".
- **Evidence.**
  - At this head, `scripts/run_all_suites.sh:259-260` gives `input_loopback` and `input_loopback_dp` 300 s.
  - `docs/testing/TESTING.md:442-443` and the driver header `:38-43` say so too.
  - The CI policy table has no row for either suite, so its "every other default suite: 1800 s" row now states a wrong budget for both.
  - At `9acb9b82` the row was true for them, because they had no arm. This delta introduces the contradiction.
  - The preamble's "measured hosted worst case plus a stated margin" also does not describe a provisional arm.
  - `reboot_ctrl`'s 300 s arm is missing from the table too. That omission is older than this PR, and the driver header in this delta now lists it.
- **Impact.** The two authoritative testing pages disagree about the wall clock these suites run under. A reader of the CI policy would expect 1800 s, and would not know the 300 s figures are provisional and owed hosted windows. The defect concerns a stated budget figure, so under the owner's rule it is MINOR, not RESIDUE.
- **Required outcome.**
  - `CI_WORKFLOWS.md`'s budget table, or the text right after it, states the 300 s budgets of `input_loopback` and `input_loopback_dp`.
  - It gives their basis: provisional at their own arm under the new-suite steps, cold local runs, and hosted windows owed.
  - The "every other default suite" row stays true at this head.
  - Adding the `reboot_ctrl` row in the same edit is recommended but not required.
- **Verification.** Read the table against `run_all_suites.sh:256-266`: every named arm appears with its figure. The docs gates (contents, inventory and the added-line gates) stay green.

### R909-4-R1 - RESIDUE - Docs - `docs/testing/TESTING.md:442`

- **Text.** "Both are provisional under the selftest's new-suite steps".
- **Problem.** The new-suite steps live in the selector's module docstring (`scripts/suite_shards.py:15-20`). The same page already says this at `:646`: "by the new-suite steps in the selector's docstring". The self-test only checks the figure.
- **Exact fix.** "Both are provisional under the new-suite steps in the selector's docstring: each figure in `scripts/suite_shards.py` is 300 s."
- This is wording only. It changes no figure or check.

### R909-4-S1 - SUGGESTION - Docs, Tests - `docs/testing/TESTING.md:445-446`, PR body line 83 - the cold-run figures have no published receipt

- **The claim.** The doc and the PR body state 34.2 s and 98.0 s, "four pinned CPUs" and "a host load average near 206".
- **What the receipts hold.** The cited receipts, `author-r6/receipts/cold-input_loopback{,_dp}.log.txt`, contain only make and simulator output. None of the 97 packet files records a wall time, a CPU mask or a load average.
- **My reproduction.** `scripts/cold_suite_time.sh` exports the head and runs `taskset -c` on 4 CPUs, with Verilator 5.054 as on PATH and in the author's logs, at a load average of about 156. Results, in `receipts/cold-input_loopback{,_dp}.log`:
  - `input_loopback`: PASS in 35.4 s, with 79587 and 76017 checks;
  - `input_loopback_dp`: PASS in 99.0 s, with 122549 checks.
- **Reading.** This corroborates the claim's magnitude. The doc's "at least three times its slowest run" holds for my run too: 300 / 99.0 = 3.03. So nothing was falsified.
- **Suggestion.** Carry the timing lines (wall clock, CPU list, load average) in the packet's cold receipts, or cite these receipts. Also note how thin the parent suite's local margin is, at about 3x.

### R909-4-S2 - SUGGESTION - Tests - `sw/builder/test_builder.py` `--list` without submodules has no self-check

- This is the author's own open risk. The property "`--list` answers in a checkout with no submodules" is guarded only by the hosted aggregates.
- A future module-scope generator import in any builder test module would fail again only on hosted.
- A small docs-workflow step or self-test that runs `--list` in a submodule-free export would catch it locally. That belongs in a new issue; it is not required by #979's frozen acceptance criteria.

### R909-4-S3 - SUGGESTION - Docs - `author-r6/receipts/manifest-1.jsonl`

- **Result.** 91 of 95 entries match the published bytes (`scripts/verify_manifest.py`, `receipts/packet-manifest-verify.log`).
- **The other four.** These are the two hosted job excerpts and two `builder-leg-1.json` receipts. They differ by 1 to 6 bytes, because the manifest binds the pre-normalization originals, as `INDEX.md:8` discloses. `INDEX.md` itself is not listed.
- **Effect.** A cold reader can verify those four published receipts only against the index's byte counts, not by hash.
- **Suggestion.** Also list post-normalization sha256 values. The packet commit `9305c8e8` is unsigned, so integrity rests on content hashes alone.

No other RESIDUE. The comment-rule scan of the added source lines finds none of the prohibited labels. The added lines are `test_input_loopback.py:17-19` and the `run_all_suites.sh:38-43` header; the `measure_test_evidence.py` and `suite_shards.py` lines are code.

## Prior public findings at this head

I read these only after my own pass over the diff.

| Finding | Status at `c413d33a` | Evidence |
|---|---|---|
| R909-3-N1 MINOR, Tests/Docs (non-provisional figures) | **RESOLVED** by outcome (a). The hosted-window replacement is owed to a later round, per the brief | Focus (2) above |
| R909-3-S1, S2, S3 SUGGESTION | Retained, optional | `tb/verilator/input_loopback_dp/sim_main.cpp` and `docs/design/INPUT_MAPPED_LOOPBACK.md` are untouched by the delta |
| R910-3-S1 SUGGESTION (test-control parser range checks) | Retained, optional | Parser files are untouched by the delta |
| R909-1-F1..F7, R909-2-N1..N3, R910-1-F1, R910-2-F1/F2 and all earlier RESIDUE/SUGGESTION items | Prior resolutions stand | Each was closed at `9acb9b82` (R909-3, R910-3). Their artifacts (RTL, benches, design and README pages, routes) have no byte in this delta. The only overlapping artifact is the planner, which focus (2) re-verified |

R910-3 POSITIVE at `9acb9b82` stands for that head. It does not cover the `CI_WORKFLOWS.md` contradiction, which this delta created.

## Lens results

```text
[R909] PASS Conformance - test_input_loopback.py:17-33 vs gen_aemi_image.py:78-84 and test_builder.py:30592; scripts/suite_shards.py:15-20 vs :111-112, :151 and run_all_suites.sh:259-260; hosted docs-check/elaborate jobs at c413d33a - the hosted gate-inventory contract holds without submodules (rc 0, inventory acc4d933 unchanged), and the planner's new-suite contract is met (self-test provisional equality)
[R909] PASS RTL - git diff --stat 9acb9b82 HEAD -- hdl tb configs syn sw/litex .github .gitmodules is empty - no RTL or interface byte; the R909-3 RTL verdict's artifacts are unchanged
[R909] PASS Robustness - run_all_suites.sh:256-266 (300 s arms under ${SUITE_TIMEOUT:-}, timeout still classified exit 92); receipts/loopback-contract-nosub.* (missing submodule fails loudly, rc 1); receipts/cold-*.log (3.03x/8.5x local headroom)
[R909] PASS Tests - receipts/shards-selftest.*, shard-*.txt, mte-*, timeout-mutations.log, list-*.txt - the self-test and runner contract reject every planted figure/arm change, all 19 listings exit 0 with one owner per new suite, the moved gate passes with submodules
[R909] MINOR Docs - docs/testing/CI_WORKFLOWS.md:577-590 - R909-4-N1 (the other Docs artifacts were checked: TESTING.md:441-447 (R1 RESIDUE, S1), run_all_suites.sh:38-43 header, PR body lines 36-38 and 65-83, the author-r6 packet (S3))
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `test_input_loopback.py:15-33`. `gen_aemi_image.py:78-84`. `test_builder.py:30590-30723`. `suite_shards.py:15-20, 111-112, 148-151, 384-398`. Hosted `docs-check`/`elaborate` steps at the head. `receipts/list-*` | R909-4 | c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |
| RTL | CLEAN | Delta scope: the empty `git diff --stat` over `hdl tb configs syn sw/litex .github .gitmodules`. The R909-3 RTL artifacts are unchanged | R909-4 | c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |
| Robustness | CLEAN | `run_all_suites.sh:256-266`. `receipts/loopback-contract-nosub.*`. `receipts/cold-*.log`. The `input_loopback_dp/sim_main.cpp` bounds are unchanged (R909-3-S2 retained) | R909-4 | c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |
| Tests | CLEAN | `suite_shards.py --selftest`. 19 listings. `measure_test_evidence.py --selftest/--check`. `measure_test_evidence.py:661-690`. `measure_test_evidence_selftest.py:284-305`. Mutation probes. Loopback contract with and without submodules. My cold runs of both suites | R909-4 | c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |
| Docs | UNCLEAN (R909-4-N1) | `docs/testing/CI_WORKFLOWS.md:520-590`. `docs/testing/TESTING.md:441-447, 640-650`. `run_all_suites.sh:38-43`. PR body. Author-r6 `REVIEW-READY.md`, `INDEX.md`, manifest | R909-4 | c413d33abe016f5c1e44bdaa1e0354cfe4ab6d99 |

## Commands and receipts (listed in MANIFEST.sha256)

- **Inventory:** `python3 -I sw/builder/test_builder.py --list` in exports with and without submodules, at both heads. Receipts: `receipts/list-*`.
- **Loopback gate:** `test_input_loopback_contract()` with and without submodules. Receipts: `receipts/loopback-contract-*`.
- **Planner:** `python3 -I scripts/suite_shards.py --selftest` and `--suite-root tb/verilator --ci-pieces --shard i/19` for i = 0..18. Receipts: `receipts/shards-*`, `receipts/shard-*.txt`.
- **Evidence contract:** `python3 -I scripts/measure_test_evidence.py --selftest` and `--check`. Receipts: `receipts/mte-*`.
- **Mutations:** `bash scripts/timeout_mutations.sh <clone> <scratch>`. Receipt: `receipts/timeout-mutations.log`.
- **Cold runs:** `bash scripts/cold_suite_time.sh <clone> <scratch> <suite> <cpus> <receipts>` on CPUs 64-67 and 68-71, run concurrently. Receipts: `receipts/cold-*.log` and `cold-*.make.log`.
- **Packet:** `python3 -I scripts/verify_manifest.py <author-r6/receipts>`. Receipt: `receipts/packet-manifest-verify.log`.
- **Hosted:** `bash scripts/poll_hosted.sh` (read-only API). Receipts: `receipts/hosted-*.txt`.
- **Clone restoration:** `bash scripts/restore_check.sh`. Receipt: `receipts/restore-check.txt`.
  - HEAD, tree and index tree are as stated, and the worktree and index equal HEAD.
  - There are 0 untracked and 0 ignored entries, after I removed the Python caches this review created.
  - The six gitlinks are unchanged and the initialized submodules are clean. `external` was already uninitialized.

## Real limits

- I ran no complete sweep and no parent, PP, gPTP, Yosys or builder bank (not allowed). I ran no act. The source-head execution evidence is the author's receipts plus my focused probes above. I make no manager source-bank claim.
- Hosted Verilator, Yosys and firmware shards had not finished at review close. I cannot report a hosted window for either new suite.
- My cold runs were at a load average of about 156 on a shared host. They corroborate the order of magnitude only.
- I did not re-execute the author's docs-workflow replay. I rely on the hosted `docs-gates-0/1/2` successes at this head for the docs gates.
- The author packet is unsigned. Integrity is by content hash: 91 of 95 match, and 4 are disclosed as normalized.
- The "manager decision (option a)" the author cites is not on the PR or issue threads. Outcome (a) needed no decision, and I confirm the 300 s arm reading above.
- Physical calibration NOT RUN. Skipped field contexts are not hardware proof.

## Pending manager duties

- R909-4-N1: return the lane for the `CI_WORKFLOWS.md` budget-table edit, then a narrow Docs re-review at the new head.
- Carry R909-4-R1 to the residue checklist.
- Hosted and act acceptance at the final head: `rtl-fast`, `verilator-suites` (shards 12 and 13 own the new suites at 300 s) and `yosys-portability`.
- Replace both provisional 300 s figures with measured hosted windows, owed to a later round.
- Candidate-merge validation at the merge turn: source base `3cda030c17`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`, builder and native banks.
- Carry the optional suggestions: R909-4-S1..S3, R909-3-S1..S3 and R910-3-S1.

R909-4 FINISHED
