[R947] NEGATIVE - exact head 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4

Round R947-1, internal independent review of PR #1019 (Relates to #1008).
Tree `d0508027199923e8d3464eb9d55ef185af10b6f5`, source base dev-soft-core `c34e7d8b06739a22cc79997a9a1f4cbcd9bd0350`, eight commits.

All five lenses were applied. Three MINOR findings remain open, and one SUGGESTION is made:

- **F1 (MINOR):** no gate holds a mutation campaign's command leg count to its matrix. A fault probe in which they differ silently drops a fifth of each campaign, and every gate stays green.
- **F2 and F3 (MINOR):** two figure claims about the docs workers contradict the new policy table.
- **F4 (SUGGESTION):** the campaign dispatch proof bypasses the driver's argument mapping. This fails safe.

The scheduling change itself is sound at this head:

- the verdicts are identical to the serial reference;
- a failed or cancelled leg fails `rtl-fast`;
- the required contexts, cancellation and fork safety are unchanged;
- no limit is raised;
- every divided leg projects at most 1031 s hosted.

## Reconstruction

The reading order was: AGENTS.md, CONTRIBUTING.md (sections 2, 3, 5 and 6), docs/README.md (the authority order, and the CI policy page as the authority for CI scheduling), REQUIREMENTS.md REQ-VER-01 and REQ-VER-04 (the clauses the new code cites), issue #1008 (body, frozen acceptance 1-3, and the two scope comments that add the `gptp_shadow` re-key), and docs/testing/CI_WORKFLOWS.md (the fast-feedback, census, protected merge bar and projection sections). Then came the full delta `c34e7d8b..5b5b0765` and the per-commit history.

The evidence was the published packet at `6be24f18:review-evidence/cicd4-r1/author`. This review re-derived its figures from that packet's raw hosted job records and raw logs.

The required contexts are unchanged and each is still carried by exactly one job: `rtl-fast`, `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`, `verilator-suites` and `yosys-portability`. Only `docs.yml` and `rtl-fast.yml` changed among the workflows.

## Findings

### F1 - MINOR - Tests, Robustness - campaign leg count in the command is not held to the matrix

**Artifact:**
- `scripts/ci_fast_legs.py:30-31`: the count is appended to the command;
- `scripts/ci_events.py:3915` (`check_fast_legs`): this holds `strategy` only;
- `scripts/ci_fast_legs_selftest.py:102`: this holds strategy and unit commands, not campaign commands.

**Authority/evidence:** Issue #1008 requires identical verdicts, and the PR claims that "a dropped or failing leg fails the run". At runtime, each campaign leg proves the arithmetic of `COUNT` legs (`campaign_cases`), and `COUNT` is read from its own argv. The contract checks the matrix against an independent constant, `FAST_LEG_JOBS`. Nothing compares the command's `COUNT` with the matrix's length. The policy page (`CI_WORKFLOWS.md:206`) says `ci_events.py` compares commands only after shard arguments are removed.

Probe P1 changed the generator to emit `COUNT+1` and regenerated the workflow. The generated commands then read `--campaign-shard "${{ matrix.leg }}" 5` beside a four-leg matrix (`receipts/probes/P1-generated-commands.txt`). Four gates all passed: `ci_gate_workflows.py --check`, `ci_events.py --check`, `ci_gate_workflows_selftest.py` (with the fast-leg self-test) and `test_ctrl_firmware_shards.py` (`receipts/probes/summary`).

**Impact:** A future generator or template edit that desynchronises the two would silently skip one leg's share of a campaign: about 169 control mutants, 133 AECP defects or 221 SRP defects. Every run would stay green and every receipt would still look complete. The census has a runtime union judge against exactly this failure; the campaigns do not.

**Required outcome:** A gate refuses any divided campaign whose command `COUNT` differs from its matrix's leg count. This could be in the generated-file contract or in the generator's self-test, with a planted arm.

**Verification:** Re-run probe P1 (`scripts/probes.py`). It must now be refused, and the unplanted head must still pass.

### F2 - MINOR - Docs - the policy page's docs-workflow total describes the superseded schedule

**Artifact:** `docs/testing/CI_WORKFLOWS.md:3503-3507`.

**Authority/evidence:** REQ-VER-04, and the Docs lens of AGENTS.md section 6: changed contracts must be reflected accurately.

The PR changed the table directly above (lines 3450-3454) to show `docs-gates-0` at 738 s and `docs-gates-1` at 1302 s, plus two new workers at 1237 and 879 s. The following paragraph still reads "Docs now projects at 1395 seconds for its slowest worker, `docs-gates-0`", and it derives 1665 s, about 27.8 minutes, and 135 s of margin from that figure.

**Impact:** The authoritative page gives two contradictory figures for the bottleneck and the workflow total. This changes a figure claim, so it is not residue.

**Required outcome:** The paragraph names the table's slowest docs worker and recomputes the total and margin from it. It also keeps `docs-gates-1`'s 1302 s visibly over the 1276 s per-job budget.

**Verification:** Recompute from the final rows, and re-run `docs_check.py` and `ci_events.py --check`.

### F3 - MINOR - Docs - the docs-worker figure in the generator's comment contradicts the policy table

**Artifact:** `scripts/ci_gate_workflows.py:27-30`.

**Authority/evidence:** The comment says that "every docs worker then sums to at most 1046 s of its steps' largest windows and its setup". The policy table, under the same component-maxima rule, puts `docs-gates-3` at 1237 s and `docs-gates-1` at 1302 s.

This review recomputed those rows from the published hosted docs records (`receipts/projection/docs-workers.txt`): `docs-gates-3` comes to about 1244 s. The step maxima are the firmware controls at 479 s, the event contract at 373 s and the act contract at 109 s, which sum to 961 s before setup.

**Impact:** The figure that justifies the worker assignment in source is not the figure the policy states. A future re-deal that relies on the comment would under-budget a worker by about 190 s.

**Required outcome:** The comment states the same projection and rule as the policy table, or cites the table.

**Verification:** Read the comment against the table and the step maxima above.

### F4 - SUGGESTION - Tests - the dispatch proof bypasses `main()`'s campaign-to-mutation-shard mapping

**Artifact:**
- `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:39`: `inventory` sets `mutation_shard` directly;
- `sw/firmware/ctrl/test/test_ctrl_firmware.py:389`.

**Evidence:** Probe P6 removed `args.mutation_shard = args.campaign_shard`, and every gate passed. With that line gone, each control and AECP leg runs its whole table. That is a superset: no verdict is lost, but the time is roughly four times or twice as long.

**Suggestion:** Derive the leg arguments in the proof through the same parse-and-map path that `main()` uses.

## Prior public findings on this PR

When the PR discussion was fetched after this review's independent pass, it held one other reviewer's report, posted at 08:44Z during this round: R948-1, NEGATIVE.

**Disclosure:** that report was read after this review's independent pass and all its probes and receipts were complete (`receipts/timeline.txt`: every receipt predates the 09:56 local fetch). It was read before this verdict and ledger were written. The findings and verdict here are the ones fixed before that read.

- **R948-1-D1** (stale docs-workflow paragraph): independently found here as F2. Retained, open.
- **R948-1-T1** (the census leg JSON receipts are absent from the published packet): not raised by this review. This review's listing of `author/receipts/local/census/`, taken before the read, is consistent with it: there are logs, timings, a summary and `union.log`, and no `census-leg-*.json`. This review verified census identity from the printed logs only. The finding is not resolved at this head and is retained for the manager.

## Lens results (artifact-specific)

```text
[R947] PASS Conformance - receipts/identity/campaigns.txt, receipts/identity/census.txt, receipts/projection/*.txt,
  receipts/inventory/*.txt, .github/workflows/{rtl-fast,docs}.yml - verdict identity, budgets, limits and contexts
  checked against #1008 acceptance 2-3 and the PR's stated partial scope
```

- **Verdict identity** is independently re-derived from the raw serial run 45657606423 and the leg logs:
  - control: 844 lines, verdict and first failing check, identical as a multiset;
  - AECP: 398 lines, identical;
  - SRP: the 662 defect lines are identical, and each leg repeats the two pin controls;
  - census: 221 arm and rule lines in identical order, differing only in one Yosys heap address. The summary lines are "0 of 164 arm(s) failed" and "0 of 57 rule(s)".
- **Control-leg receipts:** they were made at `3fbfa3bc`. The later driver change (`ab11a1d2`) touches only the SRP path and the argument bounds.
- **No limit raised:** the new legs job carries 30 minutes, and every other timeout is unchanged.
- **Required contexts, triggers, concurrency and permissions:** unchanged.
- **Projections:** re-derived: control 739 s, AECP 892 s, SRP 1017 s, census 498 s, and unit legs 1031, 503 and 811 s. The PR states 1027 s for unit leg 0; every other figure matches. All are at most 1276 s.
- **`gptp_shadow`:** 517 s is re-measured from both raw worker logs (478 s and 517 s). Both runs are rtl-full successes at gptp-processor `1213ac5b`. All 27 policy rows equal the deal, and the largest regular worker is 1275 s.
- **Runner-minutes:** the before figures reproduce exactly, at 263.9 for rtl-fast and 91.2 for docs (`receipts/projection/runner-minutes.txt`). The after figures are a model, and their order of magnitude is plausible.
- **Issue acceptance 1** (two hosted runs) is not met by this PR and is not claimed. The PR relates to #1008 and lists the jobs that remain over budget, so #1008 stays open.

```text
[R947] PASS RTL - git diff --stat c34e7d8b..5b5b0765 (14 files: workflows, scripts, campaign driver, census
  driver, policy page; no hdl/, tb/, syn/, configs/ or gitlink change), receipts/tree-integrity.txt - no clock,
  reset, CDC, FSM or width surface changed. The CI interface contracts were checked: aggregate names, needs, and
  the Yosys restore key, which is byte-identical to yosys-elaboration's, with fail-on-cache-miss and a dependency
  on yosys-tool.
```

The census judge's inventory needs no Yosys: `syn/yosys/run.sh` exits in `emit_record` before `require_tools` (`receipts/identity/judge-no-tool.txt`).

```text
[R947] UNCLEAN Robustness - F1 open. Otherwise covered: scripts/probes.py P2-P5, P7 and P8, each caught;
  ci_fast_legs_selftest (failed or cancelled results for every divided job fail the required shell, with the
  census judge skipped); census receipt schema, identity, selection and exit checks (sw/mailbox/census_legs.py:75-115)
```

```text
[R947] UNCLEAN Tests - F1 open, F4 suggested. Otherwise covered: receipts/gates/summary shows 15 gates at the
  head, all rc 0, including 2390 contract items and 6161 arms
```

The fast-leg self-tests at the head bind the campaign and census plants and the required-context shell. The campaign and census identity was re-derived independently (above).

```text
[R947] UNCLEAN Docs - F2, F3 open. Otherwise covered: docs/testing/CI_WORKFLOWS.md:152-207 and 446-454 match
  the generated graph
```

The source comments in the delta carry no lane, round, reviewer or issue-comment labels. `docs_check.py` passes.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #1008 body and comments; serial run 45657606423 logs against the leg logs; generated graphs; projection and runner-minute records; `gptp_shadow` raw logs | R947-1 | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |
| RTL | CLEAN | Diff stat (no HDL, test bench, synthesis, config or gitlink change); Yosys restore keys; `run.sh` emit path; tree integrity | R947-1 | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |
| Robustness | UNCLEAN (F1) | `census_legs.py`; `ci_fast_legs.py`; probes P1-P8; required-context shell controls | R947-1 applied, not banked | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |
| Tests | UNCLEAN (F1; F4 suggested) | 15 gates; fast-leg, census and dispatch self-tests; probes P1-P8 | R947-1 applied, not banked | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |
| Docs | UNCLEAN (F2, F3) | `CI_WORKFLOWS.md` changed sections and projection table; generator comments; PR body | R947-1 applied, not banked | 5b5b0765143593f05f5a85ecd4ab1d089d23a3e4 |

## Execution, limits and pending manager duties

**Gates run:** 15 gates ran concurrently in this clone at the exact head, all with rc 0 (`scripts/run_gates.sh`, `receipts/gates/`).

**Probes:** P1-P8 (`scripts/probes.py`) ran in a disposable probe clone under `scratch/`. The probe clone was restored byte for byte after each probe.

**Independent re-derivations:**
- `scripts/projection.py`, `scripts/identity.py` and `scripts/step_inventory.py` re-derive figures from the published packet's raw records;
- `scripts/judge_no_tool.py` shows the census judge's inventory calls only `run.sh --emit`;
- `scripts/verify_tree.py` re-hashed 1986 tracked files against their index blob and mode, with 0 mismatches. The five initialized gitlinks match and have no tracked changes, and `external` is intentionally uninitialized.

**Clone cleanup:** the gate runs created one untracked `dispatch-build/` directory and Python bytecode caches. Both were removed, and the index hash and gitlinks equal those taken before the review.

**What was not run:**
- no mutation campaign, census leg or firmware-unit leg. Identity rests on the published logs, which were re-compared independently here, so legs 0-2 of `firmware-unit` are equivalent by construction only;
- no full parent, processor, gPTP, Yosys or builder bank;
- no container replica and no host replica orchestrator or its self-test;
- no hardware, no source edit or commit, and no GitHub write.

**Hosted state (informational, not acceptance):** this review read the exact-head runs once, at 08:54Z (`receipts/hosted-exact-head-jobs.tsv`):
- the docs workflow had completed successfully, with `docs-check` and the new `docs-gates-3` and `docs-gates-4`;
- rtl-fast was still in progress. `firmware-unit` legs 1 and 2, the AECP legs, control legs 0, 1 and 3, and SRP leg 0 had succeeded, and the census legs were running.

No skipped context is claimed as executed.

**Manager source bank:** none was run at this head. The author's published gate receipts are the source execution evidence.

**Pending manager duties:**
- exact-head hosted and act acceptance;
- the two-run hosted timing observation for #1008 acceptance 1;
- the R948-1-T1 census receipt evidence;
- the current-dev merge candidate (live dev `e275d7950ef3385753e6a15d2e191ba855b171ed` or later), with its builder and native banks;
- post-merge containment.

Physical calibration is NOT RUN. Field skips are not hardware proof.

R947-1 FINISHED
