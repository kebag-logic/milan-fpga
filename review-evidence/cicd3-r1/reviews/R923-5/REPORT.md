[R923] NEGATIVE - exact head 4f0d7a837512064d67f89938c32e4a064c39ed75

# R923-5: composition re-review of PR #1003 (issue #998)

- **Candidate:** `4f0d7a837512064d67f89938c32e4a064c39ed75`, tree `9bc16d519883acd97ddfbfbb31a8b8f3dce73c55`. It merges the validated dev side `b127f378a48adaa404d5a1f74ee352df2c8b532c` (live dev plus the queued predecessors) with the PR source head `b0f2bc1a784d9f006204491c883ac2b1783e970a`.
- **Scope:** composition acceptance only. The source head already has two independent POSITIVE source reviews, R923-3 and R924-3, both at `b0f2bc1a`.
- **What changed since R923-4:** the head and tree are unchanged. The only new input is the manager's option (b) decision on R923-4-C1 (PR comment 7163800342) and its follow-up on #1008 (comment 7163801037).
- **Verdict: NEGATIVE, for one MINOR (D1).** The decision exists, has the delegated authority, names a follow-up and correctly says that no hosted limit is threatened. But the overshoot it names belongs to the re-deal it postpones, not to the stale deal it accepts. Under the accepted condition, the worker carrying `gptp_shadow` projects about 1377 s, which is 101 s over the 1276 s bound on one worker. The decision says "up to 4 s ... on at most four workers". C1's option (b) asks for the expected overshoot to be named, so C1 stays open. The rest of the R923-4 composition verdict still stands.

## 1. Verification of the three manager questions

### 1a. Is this the decision C1 option (b) asks for?

C1 option (b) asks for "a maintainer decision that accepts the stale figure until the composed tree's first hosted windows replace it, naming the expected overshoot."

| Element | Present? | Evidence |
|---|---|---|
| Maintainer authority | Yes | It is made "under the owner's delegation" (7163800342). |
| Accepts the stale figure until the first hosted windows replace it | Yes | "The stale figure is accepted until the composed tree's first hosted windows replace it." |
| Follow-up | Yes | Owned by the CICD lane under #1008: re-key from the merged head's first two complete hosted runs, re-deal with a worker or a split to at most 1276 s, record the derivation. #1008 comment 7163801037 carries the re-key and the re-deal. |
| Names the expected overshoot | **No, it names the wrong one (D1)** | See below. |

**Probe.** `scripts/deal_probe.py` (read-only) imports the candidate's own `suite_shards.py` and deals the candidate's inventory over 26 workers. Its output is in `receipts/deal_probe.txt`:

- **Shipped figure (393 s):** `gptp_shadow` is dealt to worker 1/26, which projects 1250 s. No regular worker is over 1276 s. This matches R923-4 and the decision's own "1,250 s".
- **Shipped deal, composed cost (520 s):** the deal is unchanged, because the figure is what drives it. Worker 1 carries 127 s more and projects **1377 s, 101 s over 1276 s**. On the 1.41x runner that is about 1942 s, or 32.4 min, against #998's 30 min. This is the condition the decision accepts.
- **Re-dealt with 520 s:** workers 10, 20, 22 and 23 project 1280, 1278, 1279 and 1280 s, so 2 to 4 s over. This is the condition the decision names. It applies only after the follow-up re-keys the figure, and the follow-up is required to remove it anyway.
- **Hosted corroboration:** in run 45550366428 (the PR's final run, `b0f2bc1a` merged into `e608f8d8`, 13 `gptp_shadow` controls), "Verilator shard 1/26" took 1373 s of job wall. That is already above 1276 s on the ordinary runner (`receipts/hosted_run45550366428_jobs.tsv`).

### 1b. Is any hosted job limit threatened?

No. The decision's claim is true.

- `rtl.yml` gives the Verilator matrix `timeout-minutes: ${{ matrix.shard == 25 && 60 || 45 }}`, so worker 1 has 2700 s.
- The #727 headroom rule caps a worker at 60 % of that, 1620 s. Under the stale deal at 520 s, worker 1 projects 1377 s, below 1620 s. The probe's headroom and hard-limit lists are both empty for every worker.
- On the 1.41x runner, worker 1's 1942 s is still below its 2700 s timeout.
- The other over-1276 s walls in run 45550366428 (2/26 at 1500 s, 9/26 at 1459 s) do not come from the composition. They are #1008's existing scope, as R923-4-O2 recorded.

### 1c. Does the rest of the R923-4 composition verdict stand?

Yes.

- **Same tree.** `git merge-tree --write-tree b127f378 b0f2bc1a` reproduces `9bc16d51`, which equals `4f0d7a83^{tree}`. It is a clean automatic merge (`receipts/composition_overlap.txt`).
- **Overlap set is the same three files.** The merge base is `fcbc31f3`. Computing the files changed on both sides from it gives `sw/firmware/ctrl/README.md`, `tb/verilator/gptp_shadow/mutants.py` and `tb/verilator/gptp_shadow/test_mutant_lifecycle.py`.
- **Both sides' intent is kept.** For each of the three files, the candidate-vs-dev diff carries exactly the PR side's changed lines, and the candidate-vs-PR diff carries exactly the dev side's. The sorted changed-line digests match pairwise in `receipts/composition_overlap.txt`. Nothing is lost or duplicated.
- **Gates re-run at the candidate:**
  - `scripts/suite_shards.py --selftest`: PASS, rc=0. It passes on the stale figure, which is what C1 describes.
  - `scripts/ci_events.py --check`: OK, 2378 contract items across 4 workflow files and `CI_WORKFLOWS.md`, rc=0.
  - `scripts/ci_events.py --selftest`: PASS, 2378 items and 5968 arms, rc=0.
- R923-4's other composition results (gptp_shadow mutants 13/13, lifecycle PASS, the Markdown/TOC/anchor/em-dash gates, `mutant_stage --selftest`, fw boundary leg 0) were taken on this same tree. Nothing in the delta changes what they depend on, so they are carried forward and were not re-run.

## 2. Findings

### D1 - MINOR - Conformance, Docs - PR #1003 comment 7163800342 ("Effect of the stale figure" and "Expected overshoot"), against `scripts/suite_shards.py:57,108` and `docs/testing/CI_WORKFLOWS.md:532-536`

**Authority/evidence:**
- #998 AC2 is "every hosted job within 30 minutes", implemented as "every regular worker must project at most 1276 s" (`CI_WORKFLOWS.md:532-536`).
- R923-4-C1 option (b) requires the decision to name the expected overshoot of accepting the stale figure.
- `receipts/deal_probe.txt`: under the accepted stale deal, worker 1 projects 1377 s (+101 s). The "2-4 s on four workers" figure belongs to the re-deal (option (a) without another lever).
- Hosted job "Verilator shard 1/26" in run 45550366428 measured 1373 s.

**Impact:**
- The decision accepts an AC2 shortfall about 25 times larger than it states: one worker at about 32.4 min on the 1.41x runner, not about 30.1 min.
- The paragraph "On the shipped deal, worker 1 projects 1,250 s" quotes the projection on the stale figure. That is the on-paper result C1 identified as the defect, so a cold reader would conclude the accepted state is within 4 s of the bound.
- This is a figure claim in the record that releases a finding, so it is not RESIDUE.

**Required outcome:** one of the following.
- An amended or superseding maintainer decision that names the accepted condition's expected overshoot. Suggested text: "Until the re-key, `gptp_shadow` stays on worker 1/26, which at the composed window (about 520 s) projects about 1,377 s, about 101 s over the 1,276 s bound on one worker (about 32.4 min on the 1.41x runner). Hosted run 45550366428 measured that worker at 1,373 s. Its 45-minute timeout and the 60 % headroom (1,620 s) are not threatened. The 2-4 s on four workers is the residual of a re-deal alone, which the follow-up's extra worker or split removes."
- Or C1 option (a).

**Verification:** the decision text names about 1377 s, about 101 s, on one worker under the shipped deal. `python3 -I scripts/deal_probe.py <checkout> 520` reproduces it.

### C1 (R923-4) - MINOR - Conformance, Robustness, Tests - `scripts/suite_shards.py:108` - RETAINED

The tree is unchanged. Option (b) is not yet met, because its decision names the wrong overshoot (D1). C1 resolves when D1 is resolved, or when option (a) lands.

### S-a - SUGGESTION - Docs - #1008 comment 7163801037

The PR decision lists three follow-up steps, but the #1008 entry carries only the re-key and the re-deal. Add "record the figure's derivation with the other #998 figures" there, so the owning issue holds all three steps.

## 3. Prior public findings, at this head (read after my own pass)

- **R923-4-C1:** retained (see above).
- **R923-4-O1, O2 (SUGGESTION, out of composition):** retained and unaffected. O2's worker walls are the same hosted run used above.
- **R923-3-R1, R924-3-R1 (RESIDUE):** retained, as R923-4 recorded. Nothing changed.
- **R923-1-F1, R924-1-F1, R923-2-F1, R924-2-F1:** resolved at the source and not reopened. The tree is unchanged since R923-4, which verified that.
- **S1-S7:** retained, optional, and not affected.
- **Comment rule:** the delta adds no source line, so there is no new residue.

## 4. Per-lens lines

```text
[R923] MINOR Conformance - PR #1003 comment 7163800342 vs receipts/deal_probe.txt - accepted stale deal projects worker 1/26 at 1377 s (+101 s); decision names the re-deal's 2-4 s (D1); C1 retained
[R923] PASS RTL - git diff --name-only fcbc31f3..b0f2bc1a (no hdl/ path) and receipts/composition_overlap.txt - composition touches no RTL; gptp-processor gitlink 1213ac5b is dev-side only; covered by source reviews R923-3, R924-3 at b0f2bc1a
[R923] MINOR Robustness - rtl.yml verilator-shards timeout-minutes (45/60) and receipts/deal_probe.txt - hard limits and 60% headroom hold (no hosted limit threatened, confirmed); C1's overstated budget headroom remains open until D1 is resolved
[R923] MINOR Tests - receipts/gate_suite_shards_selftest.log rc=0 on the 393 s figure vs deal_probe 520 s re-deal over bound - C1 retained; ci_events --check/--selftest rc=0 at the candidate
[R923] MINOR Docs - PR #1003 comment 7163800342 - the public decision record misstates the accepted overshoot for a cold reviewer (D1)
```

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (D1, C1) | #998 AC2; `CI_WORKFLOWS.md:532-536`; `suite_shards.py:57,108`; decision 7163800342; #1008 comment 7163801037; deal probe; hosted run 45550366428 jobs | R923-5 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| RTL | CLEAN (not touched by the composition) | PR file list from `fcbc31f3` (no HDL); overlap set; submodule gitlinks (`receipts/restore_check.txt`) | Source: R923-3, R924-3 at `b0f2bc1a`; composition: R923-4, R923-5 | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Robustness | UNCLEAN (C1) | `rtl.yml` Verilator timeouts; #727 headroom; deal probe headroom and hard-limit lists (empty); hosted worker walls | R923-5 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Tests | UNCLEAN (C1) | `suite_shards --selftest` rc=0; `ci_events --check`/`--selftest` rc=0; carried forward from R923-4 on the same tree: gptp_shadow mutants 13/13, lifecycle PASS | R923-5 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Docs | UNCLEAN (D1) | Decision 7163800342; #1008 comment 7163801037; three overlap files (both-sides digests) | R923-5 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |

## 6. Real limits

- **Not re-run:** the Markdown, TOC, anchor and em-dash gates, and the gptp_shadow mutant suite and lifecycle. The tree is byte-identical to the one R923-4 ran them on, and the delta is only a PR comment.
- **What the probe shows:** the deal probe is a projection from the registry figures. Its 520 s comes from hosted windows (R923-4 receipts). The 1.41x factor is the PR's own derived runner ratio, not a measurement on a slow runner.
- **Not done:** no hosted or act acceptance, no manager source bank, no physical calibration and no hardware. Field skips are not hardware proof.
- **Probe hygiene:** the probe edited no file. After it, the head is `4f0d7a83`, the tree is `9bc16d51`, the status is empty, the index digest is recorded and the gitlinks match the tree (`receipts/restore_check.txt`).

## 7. Pending manager duties

- Resolve D1 by amending or superseding the decision with the accepted condition's overshoot, or take C1 option (a). Then a short composition re-check (D1 and C1 only).
- Add the derivation step to #1008 (S-a, optional).
- Carry R923-3-R1 and R924-3-R1 to the residue checklist.
- Build and validate the current-dev merge candidate at the merge turn, and link its receipts. Own hosted and act acceptance. Get explicit maintainer authorization to merge.

R923-5 FINISHED
