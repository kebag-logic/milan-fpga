[R923] POSITIVE - exact head 4f0d7a837512064d67f89938c32e4a064c39ed75

# R923-6: composition re-review of PR #1003 (issue #998)

- **Candidate:** `4f0d7a837512064d67f89938c32e4a064c39ed75`, tree `9bc16d519883acd97ddfbfbb31a8b8f3dce73c55`. Its first parent is the validated dev side `b127f378a48adaa404d5a1f74ee352df2c8b532c`, which is live dev plus the queued predecessors. Its second parent is the PR source head `b0f2bc1a784d9f006204491c883ac2b1783e970a`.
- **Scope:** composition acceptance only. The source head has two independent POSITIVE source reviews, R923-3 and R924-3, both at `b0f2bc1a`.
- **What changed since R923-5:**
  - The head and tree are unchanged, and the PR head on GitHub is still `b0f2bc1a` (`receipts/pr1003_state.json`).
  - There are two new inputs:
    - the manager's corrected option (b) decision, PR comment 7164094739, which explicitly supersedes 7163800342;
    - the #1008 correction and completion, comment 7164095366.
- **Verdict: POSITIVE.**
  - R923-5-D1 is resolved, so R923-4-C1's option (b) is met.
  - The rest of the R923-5 composition verdict stands, because no input it depends on has changed.
  - No new finding blocks the merge. There is one SUGGESTION and one observation for the manager.

## 1. D1: the decision now names the accepted condition's true overshoot

D1 asked for the decision to name the overshoot of the accepted (stale-deal) condition: about 1377 s, about 101 s over the bound, on one worker. It also asked that `deal_probe.py <checkout> 520` reproduce that figure.

| Claim in 7164094739 | Check | Result |
|---|---|---|
| Supersedes 7163800342, whose "2 to 4 s on four workers" is the re-deal's figure | Comment text (`receipts/comment_7164094739.json`) | Stated explicitly |
| `gptp_shadow` stays on worker 1/26 until the re-key | `receipts/deal_probe.txt`: on the shipped deal `gptp_shadow` goes to worker 1 | True |
| At about 520 s, worker 1 projects about 1,377 s, about 101 s over 1,276 s, on one worker | Probe at 520: "shipped deal worker 1 -> 1377 s", and the only regular worker over budget is `[(1, 1377)]`. 1377 - 1276 = 101 | True, reproduced (rc=0) |
| About 32.4 min on the 1.41x runner | 1377 x 1.41 / 60 = 32.36 | True |
| Hosted run 45550366428 measured "Verilator shard 1/26" at 1,373 s, 22.9 min, on an ordinary runner | Jobs API: started 04:59:59Z, completed 05:22:52Z, which is 1373 s = 22.88 min, success, head `b0f2bc1a` (`receipts/hosted_run45550366428_shard1.tsv`) | True |
| Hosted `timeout-minutes` is 45, so no hosted job is cancelled | `.github/workflows/rtl.yml:216`: `${{ matrix.shard == 25 && 60 || 45 }}`. The probe's 60 % headroom list (cap 1620 s) and hard-limit list are both empty | True |
| The overshoot comes from PR #995's pin, and this PR's own reviewed tree is within the bound | R923-4 composition evidence: 13 controls after #995's `1213ac5b`, against 9 on the PR side. Probe at the shipped 393 s puts worker 1 at 1250 s with no regular worker over | True |
| Three follow-up steps on #1008, owned by the CICD lane | 7164094739 lists re-key, re-deal to at most 1,276 s, and record the derivation. 7164095366 on #1008 repeats all three plus the 1,377 s / 101 s / 1,373 s figures. #1008 is open (`receipts/issue1008_state.json`) | True. This also resolves R923-5 S-a |

The probe script is byte-identical to the R923-5 one (sha256 `afaa0a85...`). Its output for 393 s and 520 s matches R923-5's receipt line for line. The only difference is that R923-5 also probed 530 s.

**Conclusion:** D1 is resolved. R923-4-C1's option (b) asked for "a maintainer decision that accepts the stale figure until the composed tree's first hosted windows replace it, naming the expected overshoot". That decision now exists with the correct overshoot, so C1 is closed by option (b).

Authority: the corrected decision is published by the same manager identity as 7163800342. That earlier decision was made "under the owner's delegation", and the new one presents itself as a correction that supersedes it. I treat the delegation as carried over (see S-b).

## 2. Findings

### S-b - SUGGESTION - Docs - PR #1003 comment 7164094739

The corrected decision does not repeat "under the owner's delegation". It also does not state the 60 % headroom result, which is that 1,377 s is below the 1,620 s cap. Both facts are in the superseded comment or in the review receipts, so nothing is wrong. Repeating them would let the record stand on its own for a cold reader who never opens 7163800342. This is optional.

### Observation O3 - for the manager, not a finding on the composed tree

PR #1003's base ref is `dev-soft-core` (`receipts/pr1003_state.json`).
- That ref's tip `4d188f24` has the same tree (`4ccdecfa`) and the same parents (`e608f8d8`, `2b98e219`) as the candidate's first parent `b127f378`. So the candidate is exactly the merge onto the PR's real base.
- The branch named `dev` (`e275d795`, the "live dev" in the brief) has diverged from `dev-soft-core`: `dev-soft-core` is 1254 commits ahead and 4 behind.

At the merge turn, the manager should confirm which ref the current-dev candidate is built and validated against.

## 3. Prior public findings at this head

- **R923-5-D1:** resolved (section 1).
- **R923-4-C1:** resolved by option (b), the accepted maintainer decision 7164094739 with the follow-up on #1008. The overshoot is still in the tree: worker 1 projects 1377 s against #998 AC2's 1276 s. It is a recorded, accepted and owned condition, not an open finding.
- **R923-5-S-a:** resolved. #1008 now carries the derivation step.
- **R923-4-O1, O2 (SUGGESTION, outside the composition):** retained and unaffected.
- **R923-3-R1, R924-3-R1 (RESIDUE):** retained. Nothing has changed.
- **R923-1-F1, R924-1-F1, R923-2-F1, R924-2-F1:** resolved at the source and not reopened, because the tree is unchanged.
- **S1-S7:** retained, optional, and not affected.
- **Comment rule:** the delta adds no source line, so there is no new residue.

## 4. Per-lens lines

```text
[R923] PASS Conformance - PR #1003 comment 7164094739 vs receipts/deal_probe.txt (520 s) and rtl.yml:216 - accepted condition named correctly (worker 1/26 ~1377 s, +101 s, ~32.4 min at 1.41x; hosted 1373 s); D1 resolved, C1 option (b) met; #998 AC2 shortfall is a recorded maintainer acceptance owned by #1008
[R923] PASS RTL - git diff --name-only fcbc31f3..b0f2bc1a (no hdl/ path), receipts/restore_check.txt gitlinks - composition touches no RTL; covered by source reviews R923-3, R924-3 at b0f2bc1a
[R923] PASS Robustness - rtl.yml:216 timeout-minutes 45/60 and receipts/deal_probe.txt headroom/hard-limit lists (empty) - accepted stale deal stays under the 1620 s cap and 2700 s limit; C1 closed by option (b)
[R923] PASS Tests - receipts/deal_probe.txt reproduces the decision's figures from the candidate's own suite_shards.py; R923-5 gate receipts (suite_shards --selftest, ci_events --check/--selftest rc=0) on the identical tree - stale-figure self-test pass is now the accepted, documented condition (C1 option (b))
[R923] PASS Docs - PR #1003 comment 7164094739 and #1008 comment 7164095366 - public decision record states the true accepted overshoot and all three follow-up steps; S-b optional
```

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #998 AC2; `CI_WORKFLOWS.md:532-536`; decision 7164094739 (supersedes 7163800342); deal probe at 393 s and 520 s; hosted job "Verilator shard 1/26" of run 45550366428 | R923-6 (composition); source: R923-3, R924-3 at `b0f2bc1a` | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| RTL | CLEAN (the composition does not touch it) | PR file list from `fcbc31f3` (no HDL); submodule gitlinks (`receipts/restore_check.txt`) | Source: R923-3, R924-3 at `b0f2bc1a`; composition: R923-4, R923-5, R923-6 | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Robustness | CLEAN | `rtl.yml:216` timeouts; #727 60 % headroom; probe headroom and hard-limit lists | R923-6 (composition); source: R923-3, R924-3 at `b0f2bc1a` | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Tests | CLEAN | Deal probe against the candidate's `suite_shards.py`; R923-5 gate receipts on the identical tree; R923-4 gptp_shadow mutants 13/13 and lifecycle PASS on the identical tree | R923-6 (composition); source: R923-3, R924-3 at `b0f2bc1a` | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Docs | CLEAN | Decision 7164094739; #1008 comment 7164095366; three overlap files (R923-4/R923-5 both-sides digests on the identical tree) | R923-6 (composition); source: R923-3, R924-3 at `b0f2bc1a` | `4f0d7a837512064d67f89938c32e4a064c39ed75` |

## 6. Real limits

- **C1 is accepted, not fixed.** It is closed by a maintainer decision, not by a code change. The candidate still projects worker 1/26 at about 1377 s, above #998 AC2's 1276 s bound. Removing that is #1008's follow-up, and #1008 is open.
- **Not re-run:** the gates and suites from R923-4 and R923-5. The tree is byte-identical, and the delta is only PR and issue comments.
- **What the probe shows:** the probe projects from registry figures. Its 520 s figure comes from hosted windows (R923-4 receipts). The 1.41x factor is the PR's own derived runner ratio, not a measurement on a slow runner.
- **Not done:** no hosted or act acceptance, no manager source bank, no physical calibration and no hardware. Field skips are not hardware proof.
- **Probe hygiene:** the probe edited no file. After it, the checks in `receipts/restore_check.txt` hold:
  - head `4f0d7a83` and tree `9bc16d51`;
  - empty status;
  - an `ls-files -s` digest of `4165bf0b...`;
  - six gitlinks that match the tree.

## 7. Pending manager duties

- Optionally, repeat the delegation and the headroom result in the decision (S-b).
- Confirm the merge-turn validation ref, `dev-soft-core` or `dev` (O3).
- Carry R923-3-R1 and R924-3-R1 to the residue checklist.
- At the merge turn, build and validate the current-dev merge candidate and link its receipts. Own hosted and act acceptance. Get explicit maintainer authorization to merge. Track the #1008 follow-up to completion.

R923-6 FINISHED
